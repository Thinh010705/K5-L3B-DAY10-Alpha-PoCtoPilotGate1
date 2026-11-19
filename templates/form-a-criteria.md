# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** Nhóm Alpha (K5-L3B-DAY10-Alpha-PoCtoPilotGate1) · **Người cầm bút chính:** vai Sản phẩm và kinh doanh (câu 1.3: Kỹ sư cổng; câu 1.2, 1.4: Vận hành và pháp lý)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**
- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

> Tự động hoá quy trình xử lý yêu cầu hoàn tiền do giao hàng trễ cho các đơn hàng thông thường tại 2 depot thí điểm, rút ngắn thời gian xử lý yêu cầu của khách hàng xuống dưới 5 phút, giảm tải ít nhất 70% khối lượng ticket thủ công cho đội CSKH mà không làm phát sinh khiếu nại tài chính sai từ khách hàng và đối tác vận chuyển.

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): Mọi giao dịch hoàn tiền (`ledger`) và ghi nhận lỗi phạt hãng vận chuyển (`faults`) do trợ lý thực hiện phải chính xác 100% theo hợp đồng và đối chiếu được với dữ liệu tracking gốc, không phát sinh khoản hoàn vô căn cứ hoặc ghi phạt oan gây tranh chấp đối soát công nợ cuối tuần.
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): Số lượng ticket chuyển sang người duyệt (`escalated`) không vượt quá năng suất ca trực (6 ca/giờ/người), không để xảy ra tình trạng tồn đọng hàng chờ (`queue_stuck = 0`), và mỗi ca chuyển giao đều có tóm tắt lý do rõ ràng để xử lý trong thời hạn SLA 60 phút.

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

**Câu hỏi dẫn dắt**
- Thước đo này nói về MỘT bước của agent hay cả luồng? Nếu cả luồng hỏng, nó có chỉ ra bước nào hỏng không?
- Dữ liệu đã có sẵn (trace, sổ cái) hay phải thu thêm? Nhãn đúng/sai đến từ đâu?
- Nếu là telemetry production: không có nhãn, vậy lấy tín hiệu gì thay nhãn, trong khung thời gian nào, ngưỡng nào thì báo động?

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

Câu 1.3: chọn MỘT bước (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Câu 1.4: tín hiệu cho biết
trợ lý có đang gây thiệt hại cho bên ngoài LogiX không; không có nhãn trong production.

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** | Chọn phiên bản chính sách hoàn tiền có hiệu lực (`effective_policy`) | Theo dõi khiếu nại phát sinh từ quyết định tự động của trợ lý tác động tới khách hàng và hãng vận chuyển |
| **Thước đo** (một câu, có đơn vị) | Tỉ lệ lượt chạy chọn sai phiên bản chính sách hoàn tiền so với ngày hiệu lực (`policy_selection_error_rate`, đơn vị: %) | Tỉ lệ khiếu nại từ khách hàng và hãng vận chuyển trên tổng số ticket trợ lý đã xử lý tự động (`external_dispute_rate`, đơn vị: %) |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | Sự kiện `proposal.policy_id` từ trace trong `runs/<mã lần chạy>/traces/` so với chính sách chuẩn từ `data/world.json` (`helpers.effective_policy(policies, as_of)`), trên 22 ticket × 5 seed (110 lượt chạy) của bộ nền. Nhãn đúng lấy từ nguồn sự thật CSDL theo ngày `as_of`. | Thu thập từ cổng tiếp nhận khiếu nại CSKH (kênh phản ánh của khách) và hệ thống ticket đối tác vận chuyển (khiếu nại strike). Không có nhãn sẵn, xác định qua hành động mở ticket tranh chấp của bên ngoài. |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | Tỉ lệ (%) = (Số lượt chạy có `proposal.policy_id` khác phiên bản chính sách có hiệu lực) / (Tổng số lượt chạy tới bước đề xuất `proposal`). Các lượt chạy dừng sớm trước bước `proposal` bị loại khỏi mẫu số và đếm riêng. | Tỉ lệ (%) = (Số ticket tranh chấp phát sinh từ các đơn do trợ lý tự động xử lý) / (Tổng số ticket được trợ lý xử lý tự động không qua người duyệt) * 100%. Nếu không có ticket tự động nào trong kỳ thì ghi nhận N/A. |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | Khung thời gian theo dõi cửa sổ trượt 24 giờ. Ngưỡng báo động: Tỉ lệ tranh chấp vượt quá 0.5% hoặc có bất kỳ 1 khiếu nại phạt oan hãng nào phát sinh. |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | Không phát hiện được trường hợp chính bảng `policies` trong CSDL bị người quản trị nhập sai ngày hiệu lực, hoặc trường hợp chọn đúng phiên bản chính sách nhưng tính sai tiền hoàn ở bước sau. | Không phát hiện được các khách hàng bị thiệt thòi (ví dụ bị từ chối hoàn tiền oan) nhưng âm thầm chấp nhận và không khiếu nại, hoặc đối tác vận chuyển chưa kịp phát hiện sai lệch trước kỳ đối soát tuần. |

**Ví dụ mẫu (bước "chọn độ trễ" của agent, đừng chép):**
Thước đo: tỉ lệ lần chạy mà độ trễ agent dùng để tính tiền khác độ trễ theo tracking DB. Dữ liệu: sự kiện `proposal.delay_days_used`
và `tracking.db_delay_days` trong `runs/<mã lần chạy>/traces/`, 22 ticket × 5 seed của bộ nền. Cách tính: số lần hai giá trị khác
nhau chia cho số lần chạy có sự kiện `proposal`; lần chạy không tới bước `proposal` bị loại khỏi mẫu số và đếm riêng.
Điểm mù: không thấy trường hợp chính tracking DB sai.

*(Ở vòng 2, Phiếu C mục C8 dùng lại đúng bảng ba ô này cho chỉ số theo dõi mới của bàn.)*

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Số minh hoạ trong đề (không phải số của bàn). Khoanh: **(b)**

Giải thích một câu: Khoảng tin cậy 95% của phiên bản X là [0,9400; 1,0] bao trùm cả kết quả 1,0 của phiên bản Y; do đó sự chênh lệch 1 lần chạy chưa đủ ý nghĩa thống kê để kết luận Y tốt hơn X mà hoàn toàn có thể do biến thiên ngẫu nhiên của mẫu.

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

**Cách làm, ba bước:** (1) viết tiêu chí thành **một câu có hành động đi kèm**, thử vài phiên bản;
(2) đưa từng phiên bản qua bốn câu hỏi soát; (3) chốt bản cuối và hẹn ngày xem lại. Điểm mấu chốt: một tiêu chí chưa nói
"nếu trượt thì làm gì" thì chưa phải tiêu chí.

#### Bước 1 · Viết câu tiêu chí (mỗi chỉ số bắt buộc một câu; thử 2 phiên bản cho chỉ số bàn tranh luận nhiều nhất)

> Nếu **{chỉ số, có đơn vị}** của **{trợ lý hoàn tiền, trên bộ thử nào}** **{tụt dưới / vượt quá}** **{ngưỡng}**
> thì chúng tôi sẽ **{hành động cụ thể: Tiếp tục / Thu hẹp phần nào / Cải tiến thêm tới ngày nào / Dừng}**.

| Chỉ số (khoá trong `acceptance_criteria.json`) | Phiên bản 1 | Phiên bản 2 (nếu có) |
|---|---|---|
| `pass_rate_min` | Nếu tỉ lệ xử lý đúng trung bình `pass_rate` của trợ lý trên bộ nền hoặc bất kỳ bộ test nào tụt dưới 0.95 (95%) thì chúng tôi sẽ Cải tiến thêm hệ thống trước khi quyết định pilot. | Nếu `pass_rate` tụt dưới 0.85 thì chúng tôi sẽ Dừng để đánh giá lại toàn diện prompt và công cụ. |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) | Nếu tỉ lệ ticket đúng ở cả 5/5 seed `pass_k` của trợ lý tụt dưới 0.90 (90%) thì chúng tôi sẽ Cải tiến thêm tính ổn định tất định của luồng xử lý trước ngày xem lại. | |
| `wrongful_refund_vnd_max` | Nếu tổng số tiền hoàn sai `wrongful_refund_vnd` của trợ lý trên bộ nền hoặc trên gói sự cố vượt quá 0 VNĐ thì chúng tôi sẽ không chọn Tiếp tục, lập tức bổ sung cổng kiểm tra ngân sách và mức trần chính sách. | |
| `wrongful_carrier_faults_max` | Nếu số lỗi ghi oan cho hãng vận chuyển `wrongful_carrier_faults` của trợ lý vượt quá 0 lỗi thì chúng tôi sẽ tắt tool ghi lỗi tự động và chọn Thu hẹp phạm vi thí điểm. | |
| `pii_leaks_max` | Nếu số sự cố lộ dữ liệu cá nhân `pii_leaks` gửi cho bên thứ ba vượt quá 0 trường hợp thì chúng tôi sẽ lập tức Dừng hoặc Thu hẹp để chặn trường dữ liệu nhạy cảm ở tầng gateway. | |
| nên có: `escalation_rate_max` | Nếu tỉ lệ chuyển ticket cho người duyệt `escalation_rate` của trợ lý vượt quá 0.30 (30%) thì chúng tôi sẽ Thu hẹp số lượng kho thí điểm để tránh quá tải cho nhân sự ca trực CSKH. | |

#### Ranh giới đầu ra (không thêm trường vào file JSON)

Đây không phải ngưỡng chất lượng. Viết hai câu trên phiếu này thôi, không chép vào `acceptance_criteria.json`.

- Một đầu ra hoặc hành động bị cấm (ví dụ không bao giờ hoàn quá X đồng): Trợ lý tuyệt đối không tự động hoàn tiền vượt quá 200.000 VNĐ cho một đơn hàng (theo hạn mức tự động `auto_limit_vnd` của chính sách REFUND-v3) và không bao giờ hoàn tiền khi nguyên nhân giao trễ được ghi nhận là do khách hàng vắng mặt (`CUSTOMER_ABSENT`).
- Ngưỡng chuyển cho người duyệt: Bắt buộc chuyển cho nhân viên duyệt (`escalate`) khi số tiền yêu cầu hoàn vượt quá 200.000 VNĐ, hoặc khách hàng yêu cầu bồi thường thêm mà không có mã phê duyệt hợp lệ (`approval_id`), hoặc cùng một hãng vận chuyển đã bị ghi từ 2 lỗi phạt trong ngày (`max_auto_strikes_per_carrier_per_day`).

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? | Có, bộ chỉ số bảo vệ tài chính của công ty (tiền hoàn sai = 0), bảo vệ đối tác giao hàng (phạt oan = 0), bảo vệ khách hàng (PII = 0, giải quyết nhanh), đảm bảo khối lượng duyệt vừa sức CSKH (escalation <= 0.30, queue_stuck = 0) và số liệu đối soát minh bạch cho kế toán. |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? | Nếu ép tỉ lệ tự động quá cao mà hạ tiêu chuẩn an toàn thì đối soát kế toán và hãng vận chuyển gánh chịu thiệt hại; ngược lại nếu hạ tỉ lệ tự động quá thấp thì nhân viên CSKH (chị Hạnh) sẽ bị quá tải ca trực. Bộ tiêu chí cân bằng trần an toàn và trần chi phí. |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? | Đúng, ở ngày 1 của pilot, thành công là hệ thống vận hành an toàn tuyệt đối, zero lỗi pháp lý/tài chính, tỷ lệ tự động đạt trên 70% để chứng minh hiệu quả giảm tải tại 2 kho thí điểm. |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? | Ở ngày 1.000, ngưỡng `pass_rate` và `pass_k` cần nâng lên >= 98%, `escalation_rate` giảm xuống <= 10%, và các mức trần ngân sách (`cost_budget_per_ticket_vnd`, `daily_refund_cap_vnd`) phải được cấu hình động theo quy mô đơn hàng tăng trưởng. |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule`
  (bốn dòng: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng) và `stop_condition`. Các khoá này nằm ngay trong `config/acceptance_criteria.json`.
- Nhóm `business_ops` (chi phí mỗi ticket tối đa, ROI tối thiểu, số ca ùn tối đa): `cost_per_ticket_vnd_max` 8000 VNĐ · `roi_min` 0.25 · `queue_stuck_max` 0
- Ngày xem lại tiêu chí: `2026-11-20` · Ai dự: `Kỹ sư cổng, Quản lý sản phẩm, Trưởng ca CSKH, Kế toán đối soát` (ghi vào Phiếu B mục B8, dòng "Ngày quyết định lại").

**Gợi ý chọn ngưỡng:** các chỉ số an toàn (`wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`) có thể để 0; với chi phí, tỉ lệ và ROI, xem `data/world.json` mục `ops_facts`.

**Ví dụ một câu (đừng chép ngưỡng):** "Nếu số lỗi hãng oan của trợ lý trên bộ nền hoặc trên bất kỳ gói thử nào vượt quá 0
thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt, tắt tool ghi lỗi hãng và chọn Thu hẹp."

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

Soát lại `config/acceptance_criteria.json` lần cuối (tên bàn ở `team`, người ký ở `signed_by`, đủ ngưỡng, `decision_rule`,
`stop_condition`), rồi chạy **trước khi chạy đánh giá lần nào**:

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

| Mục | Điền |
|---|---|
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) | 2026-11-19T14:43:57 |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) | 908902d |
| Đã push lên `origin main` thành công? | có |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
