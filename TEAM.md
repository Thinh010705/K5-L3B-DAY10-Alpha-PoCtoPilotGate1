# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng):
- Lớp: `L3A` / `L3B`
- Repo của bàn: `K5-<L3A|L3B>-DAY10-<TenNhom>-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8):

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; bàn 3 người thì để trống dòng 4. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Cao Minh Quang | 2A202603906 | Kỹ sư cổng | Thành viên |
|   2 | Nguyễn Năng Thịnh | 2A202604028 | Sản phẩm và kinh doanh | Trưởng nhóm |
|   3 | Hoàng Minh Quyền | 2A202603961 | Vận hành và pháp lý | Thành viên |
|   4 |           |      |     |             |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## CaoMinhQuang-MSSV

### Phần việc phụ trách

Vai: **Kỹ sư cổng**.

- Chạy đánh giá, đọc report và trace; phụ trách câu 2.1–2.2, Phiếu B mục B0–B2.
- Viết và kiểm tra cổng phòng ngừa, bảo vệ dữ liệu và ticket hiểm; phụ trách câu 2.6–2.8, Phiếu B mục B7.1–B7.3.
- Chốt cổng vòng 1; phân tích và sửa lỗi kỹ thuật khi nhận thẻ sự cố; kiểm tra hồi quy và bổ sung chỉ số theo dõi.
- File phụ trách: `lab10/guards.py`, `lab10/monitors.py`; phối hợp điền bằng chứng kỹ thuật trong Phiếu C.

### Đóng góp cụ thể

...

### Bằng chứng

Mã commit, mã lần chạy (`runs/<mã>`), dòng trong phiếu.

### Exit ticket

Một điều học được, một điều còn chưa chắc.

## NguyenNangThinh-MSSV

### Phần việc phụ trách

Vai: **Sản phẩm và kinh doanh**.

- Phối hợp cả nhóm xây dựng tiêu chí và cách đo trong Phiếu A; phụ trách điền `config/acceptance_criteria.json` trước khi ký.
- Lập bản đồ dữ liệu và ví dụ drift; phụ trách câu 2.3, Phiếu B mục B3.
- Xác định và giải thích giới hạn hoàn tiền, chi phí, ROI và phạm vi pilot; phụ trách câu 2.9, Phiếu B mục B7.4 và mục `business` trong `config/operating_gates.json`.
- Đối chiếu bằng chứng với tiêu chí đã ký, phối hợp cả nhóm quyết định v1 tại B8 và v2 tại C12, bao gồm ba dòng bắt buộc.

### Đóng góp cụ thể

- Dùng AI hỗ trợ lập bản đồ dữ liệu (B3), đối chiếu trace và report baseline cho pre-mortem (B6), và ghi lý do cho cấu hình `business` (B7.4).

### Bằng chứng

Bổ sung mã commit, mã lần chạy và mục phiếu liên quan sau khi thực hiện.

### Exit ticket

Tự viết một điều học được và một điều còn chưa chắc.

## HoangMinhQuyen-MSSV

### Phần việc phụ trách

Vai: **Vận hành và pháp lý**.

- Phụ trách HAZOP vòng 1 và checklist có người chịu trách nhiệm; câu 2.4, Phiếu B mục B4–B5.
- Xác định người trực, người duyệt, năng lực xử lý, điều kiện dừng và yêu cầu bảo vệ dữ liệu; phụ trách câu 2.10, Phiếu B mục B7.5–B7.6.
- Điền mục `operations`, `legal` trong `config/operating_gates.json`; viết runbook phần 1–3 và mục Giờ cao điểm.
- Khi có sự cố, phối hợp cập nhật HAZOP, risk register, checklist và runbook phần 4–5 trong Phiếu C.
- Điền `submission/submission.json`, phối hợp chạy kiểm tra và gom đủ thành phần bài nộp.

### Đóng góp cụ thể

Tự bổ sung sau khi thực hiện công việc.

### Bằng chứng

Bổ sung mã commit, mã lần chạy và mục phiếu liên quan sau khi thực hiện.

### Exit ticket

Tự viết một điều học được và một điều còn chưa chắc.
