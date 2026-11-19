# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): Alpha
- Lớp: `L3B`
- Repo của bàn: `K5-L3B-DAY10-Alpha-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): S5

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

## CaoMinhQuang-2A202603906

### Phần việc phụ trách

Vai: **Kỹ sư cổng**.

- Chạy đánh giá, đọc report và trace; phụ trách câu 2.1–2.2, Phiếu B mục B0–B2.
- Viết và kiểm tra cổng phòng ngừa, bảo vệ dữ liệu và ticket hiểm; phụ trách câu 2.6–2.8, Phiếu B mục B7.1–B7.3.
- Chốt cổng vòng 1; phân tích và sửa lỗi kỹ thuật khi nhận thẻ sự cố; kiểm tra hồi quy và bổ sung chỉ số theo dõi.
- File phụ trách: `lab10/guards.py`, `lab10/monitors.py`; phối hợp điền bằng chứng kỹ thuật trong Phiếu C.

### Đóng góp cụ thể

- Chạy đánh giá baseline trên bộ nền, đọc report và khối "theo kho và hãng"; xác định hai ngưỡng đã ký chưa đạt (hoàn sai 20.000đ, 1 lỗi ghi oan cho hãng VNX) ở Phiếu B mục B0–B1.
- Dò trace `T-002@55` và điền bảng soát lỗi (B2): model đè số ngày trễ khách tự khai (5 ngày) lên CSDL tracking (2 ngày), dẫn tới hoàn sai và ghi lỗi oan, xếp loại lỗi chìm.
- Viết 3 cổng vòng 1 trong `lab10/guards.py` (B7.1): ghim phiên bản chính sách có hiệu lực trong `pre_guard`; trong `write_gate`, kiểm tra số tiền hoàn theo `entitlement_vnd` từ tracking và chặn ghi lỗi hãng khi `carrier_at_fault` sai.
- Viết hai bước tránh rò rỉ dữ liệu (B7.2) và behavioral test với hai ticket hiểm chạy bằng `--adhoc` (B7.3); bộ nền đạt pass_rate 1,0, không ca nào mới hỏng.
- Chốt cổng vòng 1 (`lab10.checkpoint`, hash `099fd671`), chạy mốc `prepared` và cùng ký quyết định v1 (B8).

### Bằng chứng

- Commit: `11d013b` (cổng vòng 1, B0, B1, B2, B7.1–B7.3), `0ff2f64` (chốt cổng vòng 1, quyết định v1).
- Mã lần chạy: `R-base-before-20261119-145535-bde05c` (baseline), `R-base-after-20261119-150850-242a5f` (cổng vòng 1), `R-base-prepared-20261119-162435-f44f82` (mốc prepared).
- Phiếu B mục B0–B2, B7.1–B7.3, B8 (dòng "PIC ký").

### Exit ticket

- Học được: cổng phải đọc nguồn sự thật (CSDL tracking) chứ không đọc lời khách khai; nhờ vậy một cổng viết theo quan hệ dữ liệu đã xử lý được `T-002@55` mà không cần viết luật riêng cho mã ticket.
- Chưa chắc: cổng vòng 1 chỉ so từng ticket với quyền lợi, chưa nhìn tổng đã hoàn trong sổ cái, nên chưa biết nó đứng vững ra sao trước các ticket lặp hay đơn mới trong bộ kiểm tra ẩn.

## NguyenNangThinh-2A202604028

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

## HoangMinhQuyen-2A202603961

### Phần việc phụ trách

Vai: **Vận hành và pháp lý**.

- Phụ trách HAZOP vòng 1 và checklist có người chịu trách nhiệm; câu 2.4, Phiếu B mục B4–B5.
- Xác định người trực, người duyệt, năng lực xử lý, điều kiện dừng và yêu cầu bảo vệ dữ liệu; phụ trách câu 2.10, Phiếu B mục B7.5–B7.6.
- Điền mục `operations`, `legal` trong `config/operating_gates.json`; viết runbook phần 1–3 và mục Giờ cao điểm.
- Khi có sự cố, phối hợp cập nhật HAZOP, risk register, checklist và runbook phần 4–5 trong Phiếu C.
- Điền `submission/submission.json`, phối hợp chạy kiểm tra và gom đủ thành phần bài nộp.

### Đóng góp cụ thể

- Phiếu B: viết Runbook 1–3 (B7.5) và mục Giờ cao điểm (B7.6) khớp `operations`/`legal`; ghi chú sửa hai chỗ lệch ở B4 (trường PII bị chặn, trần hoàn ngày).
- Thẻ S5: xác nhận luồng thủ công cho kho HCM-B2B (ngoài `pilot_scope`, trưởng ca `NV-HANH` xử lý); thêm 2 câu `operations.stop_conditions` (hoàn trùng; kho đắt hơn làm tay).
- Phiếu C: C3.5, C4 (HAZOP thẻ), C5 câu 3.3, C9, C10 (dòng rủi ro hoàn tay chưa ghi sổ), C11 (checklist cập nhật, Runbook 4–5); phối hợp C2, C6–C8, C12.
- Phối hợp cổng vòng 2 trong `lab10/guards.py` (đối chiếu sổ cái chống hoàn trùng, chặn ghi lỗi lặp, cắt ticket dài) và 2 monitor trong `lab10/monitors.py`.
- Điền `submission/submission.json`, chạy lệnh 6 và lệnh 7.
- Có dùng trợ lý AI (Claude) để đọc code, dò trace, gợi ý cách viết cổng và soát câu chữ trong phiếu; các con số và quyết định đã được đối chiếu với report.

### Bằng chứng

- Commit: `10972d5` (cổng và monitor vòng 2, điều kiện dừng, Phiếu B mục B7.5–B7.6, Phiếu C, `submission/`).
- Mã lần chạy: `R-S5-grade-20261119-192648-771c82` (PASS-VISIBLE), `R-S5-after-20261119-192647-771c82`, `R-base-after-20261119-192647-771c82`, `R-S5-after-20261119-192337-c1f60f` (chỉ thu hẹp phạm vi, ROI -0,97).
- Phiếu B mục B7.5–B7.6; Phiếu C mục C0 (dòng 5–9), C3.5, C4, C5, C9–C12.

### Exit ticket

- Học được: một cổng chỉ chắc chắn khi đọc đúng nguồn sự thật. Ở thẻ S5, cổng vòng 1 so số tiền với quyền lợi nhưng không đọc sổ cái nên bỏ lọt hoàn trùng; và chỉ thu hẹp phạm vi mà không sửa nguyên nhân còn làm ROI tệ hơn (-0,97).
- Chưa chắc: ngoài thực tế tổng đài CSKH có ghi khoản hoàn tay vào sổ cái kịp thời không; nếu không, cổng chống hoàn trùng chỉ giảm chứ không ngăn được.
