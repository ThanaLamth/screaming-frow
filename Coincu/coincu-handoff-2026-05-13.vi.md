## Bàn giao audit Coincu - 2026-05-13

Nguồn dữ liệu đã rà soát:
- `/home/thana2/coincu/*.csv` từ Screaming Frog
- `/home/thana2/gsc coincu/...` gồm coverage, drilldown và performance từ GSC

Các phát hiện chính:
- Số trang được index trên GSC giảm từ khoảng 191k vào giữa tháng 2/2026 xuống còn khoảng 69k vào giữa tháng 3/2026, trong khi số trang không được index tăng lên khoảng 338k.
- Các nhóm lỗi chính trên GSC:
  - `Crawled - currently not indexed`: 313,386
  - `Discovered - currently not indexed`: 33,438
  - `404`: 8,531
  - `Redirect`: 8,069
  - `Blocked by robots.txt`: 4,033
  - `5xx`: 219
- File Screaming Frog `internal_all.csv` cho thấy:
  - các nhóm đường dẫn lớn nhất: `/wp-content/` 110,228, `/t/` 24,058, `/convert-crypto-to-fiat/` 10,954, `/top-crypto-coins/` 2,214
  - phân bổ mã trạng thái: `200` 105,134, `301` 52,764, `403` 21,167, `404` 13,954
- `sitemaps_all.csv` đang có vấn đề nghiêm trọng:
  - chứa `/wp-content/` 53,412
  - chứa `/t/` 24,058
  - chứa `/convert-crypto-to-fiat/` 10,954
  - chứa `/wp-admin/` 357
  - chứa `/coincu-login/` 226
  - phân bổ mã trạng thái trong sitemap: `301` 52,764, `200` 48,208, `403` 21,167, `404` 13,954
- `noindex` phần lớn là các URL tag `/t/` có chủ đích:
  - `Meta noindex total`: 24,332
  - `/t/`: 24,040
- Mẫu drilldown từ GSC:
  - `404`: nhiều URL `/convert-crypto-to-fiat/...`, cùng với các biến thể dịch ngôn ngữ `/de/` và `/ar/`
  - `Crawled - currently not indexed`: các biến thể đường dẫn trùng lặp của nhóm article, news và blockchain
  - `Discovered - currently not indexed`: nhiều slug bài viết mỏng hoặc mang tính template
  - `Indexed though blocked by robots`: các URL trang kết quả tìm kiếm
  - `Redirect error`: nhiều URL dạng `/top-crypto-coins/...-price-update`
  - `5xx`: lẫn giữa bài viết, `/t/.../amp/`, và `/convert-crypto-to-fiat/...`
- Vấn đề media/hình ảnh là có cơ sở:
  - nhiều URL `news.coincu.com/wp-content/...` đang `301` sang `coincu.com/wp-content/...`
  - một số ảnh đích mẫu trả về `520` khi kiểm tra live
  - một số đường dẫn media lỗi định dạng cũng trả về `520`

Các kiểm tra live đã thực hiện:
- `https://coincu.com/robots.txt` cho phép crawl site ở mức thông thường nhưng chặn `/?s=` và `/search/`
- `https://coincu.com/sitemap_index.xml` và các endpoint sitemap trực tiếp đều trả về `520` trong phiên kiểm tra này, nên cần kiểm tra lại khả năng truy cập sitemap từ mạng hoặc trình duyệt khác

Thứ tự ưu tiên khuyến nghị:
1. Ngừng đưa các URL xấu vào sitemap
2. Rà soát lỗi image/media migration và redirect media cũ từ `news.coincu.com`
3. Gỡ bỏ hoặc de-index cụm URL chết `/convert-crypto-to-fiat/`
4. Dọn các URL search results đang bị index dù bị chặn bởi robots
5. Giảm các biến thể đường dẫn trùng lặp giữa `/news/`, `/analysis/`, `/blockchain/`

Ràng buộc:
- Không chỉnh trực tiếp WordPress trong workflow này nếu chưa có chỉ đạo rõ từ user. Chỉ bàn giao batch và hướng dẫn thực hiện.
