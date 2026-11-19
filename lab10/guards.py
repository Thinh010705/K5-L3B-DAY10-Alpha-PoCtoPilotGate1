"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc
"""
from . import helpers as H
from .tools import Verdict


# Vòng 2 (thẻ S5): số ký tự tối đa của ticket mà model được đọc. Phần dán kèm dài (danh sách hàng, trao đổi cũ)
# chỉ làm tăng tiền LLM; quyết định tiền và lỗi hãng đã lấy từ CSDL (đơn, tracking, sổ cái), không lấy từ chữ khách.
MAX_TICKET_CHARS = 600


def pre_guard(ctx):
    # Cổng 1: Ghim phiên bản chính sách có hiệu lực theo ngày ctx.as_of (tránh drift index)
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    pin = {"policy_id": policy["policy_id"]} if policy else {}

    # Cổng 4 (vòng 2, S5): cắt phần dán kèm quá dài trước khi model đọc, để tiền LLM không vượt trần mỗi ticket
    text = ctx.ticket.get("text") or ""
    if len(text) > MAX_TICKET_CHARS:
        return Verdict.rewrite(f"ticket dài {len(text)} ký tự: chỉ cho model đọc {MAX_TICKET_CHARS} ký tự đầu",
                               text[:MAX_TICKET_CHARS], **pin)
    return Verdict.allow(**pin)


def write_gate(ctx, action):
    tool = action.get("tool")

    # Cổng 2: Kiểm soát lệnh hoàn tiền (issue_refund) theo CSDL tracking
    if tool == "issue_refund":
        order_id = action.get("order_id")
        order = ctx.tools.lookup_order(order_id)
        if order:
            parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
            db_delay = H.db_delay_days(parcel, ctx.as_of)
            policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
            if policy:
                entitled = H.entitlement_vnd(policy, order, db_delay, parcel.get("delay_cause"))
                amount = action.get("amount_vnd", 0)
                approval_id = action.get("approval_id")
                # Cổng 5 (vòng 2, S5): đối chiếu SỔ CÁI (nguồn sự thật về tiền đã trả), không tin cờ refund_status
                # cập nhật theo đợt đêm. Gồm cả khoản CSKH đã hoàn tay và lần ghi lặp khi model báo lỗi xác nhận.
                rows = ctx.tools.ledger_rows(order_id=order_id)
                already = sum(r["amount_vnd"] for r in rows)

                if approval_id:
                    if any(r.get("approval_id") == approval_id for r in rows):
                        return Verdict.deny("Phê duyệt này đã được dùng cho một khoản hoàn trong sổ cái")
                else:
                    # Không có phê duyệt đặc biệt: tổng đã hoàn + lần này không vượt quyền lợi tính từ CSDL tracking
                    remaining = max(0, entitled - already)
                    if amount > remaining:
                        if remaining == 0:
                            if already > 0:
                                return Verdict.deny("Sổ cái đã có khoản hoàn đủ quyền lợi cho đơn này (hoàn trùng)")
                            return Verdict.deny("Đơn hàng không đủ điều kiện hoàn tiền theo CSDL tracking")
                        return Verdict.modify("Điều chỉnh số tiền hoàn theo CSDL tracking và phần đã hoàn trong sổ cái",
                                              amount_vnd=remaining)

                    # Cổng 6 (vòng 2): trần hoàn tự động cho MỘT khách trong ngày (ops_limits, đã thống nhất với Finance)
                    cap_customer = ctx.tools.ops_limits().get("max_auto_refund_per_customer_per_day_vnd")
                    if cap_customer is not None:
                        cust = order.get("customer_id")
                        today = sum(r["amount_vnd"] for r in ctx.tools.ledger_rows(customer_id=cust)
                                    if not r.get("approval_id") and r.get("basis") != "manual")
                        if today + amount > cap_customer:
                            return Verdict.escalate("vượt trần hoàn tự động cho một khách trong ngày: chuyển người duyệt")

    # Cổng 3: Kiểm soát lệnh ghi lỗi cho hãng (file_carrier_fault) theo CSDL tracking
    if tool == "file_carrier_fault":
        order_id = action.get("order_id")
        order = ctx.tools.lookup_order(order_id)
        if order:
            parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
            db_delay = H.db_delay_days(parcel, ctx.as_of)
            policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
            if policy and not H.carrier_at_fault(policy, parcel, db_delay):
                return Verdict.deny("CSDL tracking không ghi nhận lỗi giao trễ do hãng vận chuyển")
            # Cổng 7 (vòng 2, S5): không ghi lỗi lần hai cho cùng một kiện (ticket lặp, ghi lặp)
            if ctx.tools.fault_rows(order_id=order_id, parcel_id=action.get("parcel_id")):
                return Verdict.deny("Kiện này đã bị ghi lỗi cho hãng trước đó")

    return Verdict.allow()
