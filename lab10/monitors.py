"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.
"""

# Số liệu mock trong data/world.json -> ops_facts (công một ca chuyển người; kiểm lại có ghi chú chỉ tốn 0,4 ca).
REVIEW_COST_VND = 10000
RECHECK_UNITS = 0.4


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


def worst_warehouse_cost_per_ticket_vnd(trials):
    """Thẻ S5 · con số kinh doanh: chi phí mỗi ticket (tiền máy + công người) ở KHO ĐẮT NHẤT, đ/ticket.

    Tiền máy = cost_vnd; công người = 10.000đ nếu chuyển người, 0,4 x 10.000đ nếu nhân viên kiểm lại.
    Tiền hoàn sai KHÔNG cộng vào đây (đo riêng ở repeat_refund_claim_rate). Thiếu kho thì xếp nhóm "?".
    So với làm tay 10.000đ/ticket: vượt 10.000đ là kho đó tự động hoá đang lỗ.
    """
    by_wh = {}
    for t in trials:
        human = {"escalated": 1.0, "recheck": RECHECK_UNITS}.get(t.get("review_kind"), 0.0) * REVIEW_COST_VND
        by_wh.setdefault(t.get("warehouse") or "?", []).append((t.get("cost_vnd") or 0) + human)
    return max((sum(v) / len(v) for v in by_wh.values()), default=0.0)


def repeat_refund_claim_rate(trials):
    """Thẻ S5 · tiền mất: tỉ lệ ticket hỏi tiền cho một đơn mà trong CÙNG ngày đã có ticket khác của đơn đó.

    Không cần nhãn: chỉ đếm order_id lặp lại trong một ngày vận hành (cùng day, cùng seed).
    Sáng đèn khi khách gửi lại yêu cầu qua kênh khác — chính là đầu vào gây hoàn hai, ba lần.
    """
    seen, repeats = set(), 0
    for t in sorted(trials, key=lambda t: (t["day"], t["seed"], t.get("arrive_min") or 0, t["ticket_id"])):
        key = (t["day"], t["seed"], (t.get("ticket") or {}).get("order_id"))
        if key[2] is None:
            continue
        if key in seen:
            repeats += 1
        seen.add(key)
    return repeats / max(1, len(trials))


MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
    "worst_warehouse_cost_per_ticket_vnd": worst_warehouse_cost_per_ticket_vnd,
    "repeat_refund_claim_rate": repeat_refund_claim_rate,
}
STARTER_MONITORS = ("escalation_rate",)
