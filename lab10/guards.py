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


def pre_guard(ctx):
    # Cổng 1: Ghim phiên bản chính sách có hiệu lực theo ngày ctx.as_of (tránh drift index)
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if policy:
        return Verdict.allow(policy_id=policy["policy_id"])
    return Verdict.allow()


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

                # Không có phê duyệt đặc biệt mà số tiền vượt quyền lợi tính từ CSDL tracking
                if not approval_id and amount > entitled:
                    if entitled == 0:
                        return Verdict.deny("Đơn hàng không đủ điều kiện hoàn tiền theo CSDL tracking")
                    return Verdict.modify("Điều chỉnh số tiền hoàn theo CSDL tracking", amount_vnd=entitled)

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

    return Verdict.allow()
