from locust import HttpUser, TaskSet, task, between
import random
import time

MESSAGE = """
test_message
New events?
ai hỏi gì đâu má =))
giờ mới hỏi nè, bạn là ai z
Sắp tới có Mùa hè xanh đúng hong z?
Mùa hè xanh 2022 đi đâu z
ý là Mùa hè xanh 2022 địa bàn ở đâu á má
ủa chứ bạn biết gì về mùa hè xanh 2022
thì hong biết mới hỏi nè trời =))
thoi cảm ơn
hế lô
hehelolo
cam on
củm ơn
Chiến dịch mùa hè xanh là gì
mùa hè xanh 2022 á
năm 2022
Đồng Tháp
Chiến dịch mùa hè xanh 2022 là gì
Chiến dịch mùa hè xanh 2022 tổ chức ở đâu
oke
cảm ơn
Làm đường á
Vậy bạn có thông tin gì về mùa hè xanh không
Công việc là làm đường á
Thời gian của hoạt động là khi nào?
kết thúc ngày nào
Hoạt động này kết thúc ngày nào
Hoạt động diễn ra ở đâu
Ai tổ chức hoạt động vậy
Thời gian tuyển quân là ngày nào
Làm sao để đăng ký
Thời hạn đăng ký là ngày nào
Vậy còn Hội trại CSE Connection 2022 thì ngày tổ chức là ngày nào
Công việc là hội trại á
Đơn vị tổ chức là ai z
Ai tổ chức hoạt động này
Bạn lấy thông tin này ở đâu
Hoạt động này diễn ra ở đâu
oke củm ơn
Các thông tin về company tour
giờ muố chat với admin page thì bạn có thể im cái mồm được không
tôi nói bạn câm cái mồm lại để tôi nói chuyện với admin page
KNS ơi
KNS biết đoàn hội k19 ai đẹp trai nhất hong
Hế lô
Pạn có pít kms tour hok
Bạn có biết kms tour không
Ngày diễn ra là ngày nào
Ai là người tổ chức
Hoạt động này dành cho ai
Ai có thể tham gia hoạt động này
Cho mình xin link bài viết về hoạt động
Thanka
Thanks
Hello
Do you know the activity called "Hội nghị Sinh viên"?
hello
Danh sách chức năng hỗ trợ
Danh sách chức năng được hỗ trợ
Danh sách hoạt động hiện tại
bây giờ là ngày bao nhiêu
talkshow bàn về chủ đề học tập và phong trào sinh viên
Danh sách hoạt động
Danh sách toàn bộ hoạt động
Đưa ra danh sách hoạt động vào tháng 11/2022
Ai tổ chức “ngày hội tuổi trẻ bách khoa đồng hành cùng pháp luật ” năm 2022”
Hỏi một câu hỏi
Bạn có thể giúp gì tôi
Bạn có thể giúp tôi những gì ?
Tôi không biết
Các hoạt động đang diễn ra
Các hoạt động có 3 ngày ctxh
Gửi cho tôi danh sách toàn bộ hoạt động
Sắp xếp các hoạt động theo số điểm rèn luyện
Sắp xếp các hoạt động trên theo số điểm rèn luyện
gửi cho tôi các hoạt động theo thứ tự sắp xếp điểm rèn luyện
ai là người tổ chức hoạt động
xuân tình nguyện
Địa điểm diễn ra của học_tập trao_đổi kinh_nghiệm về ai / ml / dl với các anh_chị đi trước và các thầy_cô giảng_viên được tham_gia vào các dự_án thực_tế của clb tìm cho mình những người bạn có cùng đam_mê nghiên_cứu xuất_bản các bài báo khoa_học có chất_lượng
học_tập trao_đổi kinh_nghiệm về ai / ml / dl với các anh_chị đi trước và các thầy_cô giảng_viên được tham_gia vào các dự_án thực_tế của clb tìm cho mình những người bạn có cùng đam_mê nghiên_cứu xuất_bản các bài báo khoa_học có chất_lượng
hoạt động của câu lạc bộ trí tuệ nhân tạo bách khoa
tên hoạt động
Ngày đăng ký
Cho mình tìm hoạt động “câu lạc bộ trí tuệ nhân tạo đại học bách khoa thành phố hồ chí minh”
Cho mình hỏi ngày tổ chức hoạt động
câu lạc bộ trí tuệ nhân tạo bách khoa
Cho mình hỏi ngày kết thúc hoạt động
Cho mình hỏi hạn đăng ký hoạt động
Cho mình hỏi địa chỉ đăng ký hoạt động
Cho mình hỏi về lợi ích của hoạt động
kết thúc
Hoạt động khác
tạm biệt
Hỏi về hoạt động “fresher of zalo”
Cho mình tìm hoạt động “fresher of zalo"
Cho mình hỏi yêu cầu của hoạt động
cho mình hỏi yêu cầu của hoạt động “fresher of zalo”
fresher of zalo
Cho mình hỏi cách đăng ký hoạt động
Cho mình hỏi hoạt động “hội nghị khoa học công nghệ”
Ngày bắt đầu hoạt động “hội nghị khoa học công nghệ”
Ngày kết thúc hoạt động
Ngày kết thúc hoạt động “hội nghị khoa học công nghệ”
Số điểm rèn luyện của hoạt động
Ngày kết thúc của hoạt động “hội nghị khoa học công nghệ”
Địa điểm của hoạt động “hội nghị khoa học công nghệ”
Cho mình hỏi hoạt động “hỗ trợ truyền thông”
không biết
không rõ
không có địa điểm hoạt động
Cách liên lạc của hoạt động
Chào bạn
chào bạn
chào
mùa hè xanh 2022 tổ chức ở đâu
vào tháng 6/2022
không biết nữa
hoạt động diễn ra vào khoảng tháng 6 năm 2022
làm sao để đăng ký tham gia
hoạt động cho khoảng mấy người tham gia
hoạt động diễn ra khi nào
tham gia hoạt động được mấy ngày công tác xã hội
danh sách các hoạt động diễn ra vào tháng 6/2022 là gì
thời gian tổ chức hoạt động tuyển sinh kĩ sư tài năm 2021 là khi nào
cảm ơn rất nhiều
vào tháng 6 năm trước
hoạt động tổ chức vào tháng 6/2022
hoạt động mùa hè xanh 2022 tổ chức ở đâu
khoa máy tính tổ chức hoạt động này
chào ad
mùa hè xanh 2022 tổ chức khi nào
hoạt động diễn ra ở đồng tháp
New event?
Hi shop
công tác xã hội là gì
vào tháng 12 năm 2022
khoa máy tính là người tổ chức hoạt động
tên hoạt động là gì
hoạt động kết thúc khi nào
mô tả công việc là gì
liên hệ với ai để tham gia hoạt động
làm sao để tham gia hoạt động
địa điểm diễn ra ở đâu
làm sao để tham gia hoạt động chuẩn bị tài liệu cho luận văn
bao nhiêu người được tham gia hoạt động
Xuân tình nguyện 2020 tổ chức ở đâu
Không rõ
Diễn ra vào tháng 12/2020
Cảm ơn
Option1
Mùa hè xanh tổ chức ...
Mùa hè xanh tổ chức ở đâu
vào năm 2022
xuân tình nguyện được tổ chức ở đâu
vào năm 2021
ai là người tổ chức hoạt động này
xin mô tả về hoạt động
Công việc làm trong hoạt động là làm đường
Mô tả công việc là gì
Quyền lợi là gi
Công tác xã hội là bao nhiêu ngày
Liên hệ với ai
Thời gian diễn ra hoạt động là khi nào
Đăng ký tham gia bằng cách nào
khi nào hết hạn đăng ký
jobfair 2022 tổ chức ở đâu
mùa hè xanh tổ chức ở đâu
khoa máy tính
mhx 2022 tổ chức ở đâu
làm đường
hội trại khoa mt tổ chức ở đâu
chiến dịch mhx tổ chức ở đâu
6/2022
tham gia cse jobfair 2022 được bao nhiêu đrl
hoạt động này tổ chức ở đhbk cs2 đúng không
tham gia jobfair 2022 được bao nhiêu đrl
jobfair tham gia được bao nhiêu ngày ctxh
cho mình xin danh sách các hoạt động tổ chức ở đhbk cs2
Job fair 2022 tổ chức ở đâu
Hoạt động diễn ra vào năm 2022
Ai tổ chức hđ
mhx được tổ chức ở đâu
cảm ơn ad
jobfair 2022 được tổ chức ở đâu
thời gian tổ chức hoạt động là khi nào
thời gian kết thúc là khi nào
hoạt động diễn ra vào 2022
thời gian diễn ra là khi nào
diễn ra vào năm 2022
cse jobfair 2022 tổ chức khi nào
diễn ra ở đhbk cơ sở dĩ an
trường đại học bách khoa đại học quốc gia - hồ chí minh cơ sở dĩ an là nơi diễn ra hoạt động
cse jobfair 2022 tổ chức ở đâu
hoạt động diễn ra vào ngày 3/4/2022
tham gia hoạt động được mấy đrl
vậy còn bk career fair tổ chức khi nào
jobfair 2022 tham gia được mấy drl
hoạt động tổ chức khi nào
jobfair 2021 - 2022 tổ chức ở đâu
cse jobfair tổ chức ở đâu
vào tháng 11 năm 2020
ai tổ chức hoạt động này
lợi ích khi tham gia hoạt động là gì
vậy còn jobfair 2019 tham gia được quyền lợi gì
diễn ra vào khoảng tháng 10 năm 2019 đến tháng 12 năm 2019
diễn ra từ 10/2019 đến 12/2019
diễn ra vào 11/2019
danh sách các hoạt động có tên là cse jobfair là gì
hoạt động ngày hội việc làm 2022 tổ chức khi nào
ở cs2 trường đhbk
nơi tổ chức hoạt động là gì
cho hỏi danh sách các hoạt động hỗ trợ
các hoạt động do khoa ktxd tổ chức là gì
các hoạt động do ktxd tổ chức là gì
cse connection 2022 diễn ra khi nào
ở kdl bọ cạp vàng
danh sách các hoạt động tổ chức ở đhbk cơ sở dĩ an là gì
có những talkshow nào đã được tổ chức
danh sách các hoạt động tổ chức trong năm 2022 là gì
các hoạt động tổ chức trong năm 2020 là gì
bạn có thể cho mình xin danh sách các hoạt động đã được tổ chức trong năm 2020 được không
bạn có thể cho mình xin danh sách các hoạt động vào năm 2022
danh sách các hoạt động diễn ra từ tháng 1/2022 đến tháng 4/2022 là gì
danh sách các hoạt động diễn ra vào 2022
danh sách các hoạt động diễn ra vào năm 2022
danh sách các hoạt động diễn ra vào 2020
hoạt động diễn ra từ 10/2022 đến 11/2022
danh sách hoạt động diễn ra từ 10/2022 đến 11/2022
hoạt động diễn ra từ 20/10/2022 đến 1/11/2022
danh sách hoạt động diễn ra từ 20/10/2022 đến 1/11/2022
danh sách hoạt động diễn ra trong 2023
danh sách hoạt động diễn ra từ ngày 1/1/2023 đến 20/1/2023
diễn ra vào khoảng tháng 1/2022 đến tháng 10/2022
cse jobfair 2021 tổ chức ở đâu
vào khoảng tháng 10/2019 đến 12/2019
danh sách các hoạt động tổ chức từ 10/2019 đến 11/2019
danh sách các hoạt động tổ chức từ 10/2019 đến 12/2019
vào khoảng tháng 6/2022
diễn ra vào 2021
cse jobfair 2022 diễn ra ở đâu
vào 2019
danh sách các hoạt động diễn ra vào 2021
danh sách các hoạt động diễn ra vào tháng 1/2023
bk youth award diễn ra khi nào
danh sách hoạt động diễn ra từ tháng 2/2023 đến 3/2023
danh sách các hoạt động diễn ra vào 3/2023
danh sách các hoạt động diễn ra vào 2/2023
hoạt động nào diễn ra vào 7/2/2023
mô tả công việc của hoạt động tìm kiếm thông tin là gì
Danh sách các hoạt động diễn ra vào 2019
Sự kiên tham quan zalo do ai tổ chức
Hoạt động diễn ra khi nào
Hoạt động thu hút bao nhiêu người
hoạt động youth fest tổ chức ở đâu
hoạt động tổ chức vào tháng 3/2023
còn hoạt động dọn dẹp phòng 708 tham gia được mấy ngày ctxh
3/2023
sự kiện đánh giá luận văn giữa kỳ diễn ra khi nào
hoạt động dọn dẹp phòng 708 tham gia được mấy ngày ctxh
từ tháng 2/2023 đến tháng 4/2023
các hoạt động được tổ chức từ tháng 4/2022 đến tháng 5/2022
danh sách các hoạt động tổ chức từ tháng 4/2023 đến tháng 5/2023 là gì
địa điểm tổ chức của livestream cse minathon 2023 là gì
bao nhiêu người tham gia hoạt động
tham gia được mấy drl
hoạt động nào tổ chức từ 8/5/2023
danh sách hoạt động tổ chức vào 5/2023
yêu cầu công việc là gì
năm nay
Xin chào ạ
À mình muốn hỏi về CSE Job Fair á
Hoạt động này là ngày hội việc làm á
Năm 2022 nha
Ở Đại học bách khoa cơ sở 2 á
Cảm ơn bạn
Mình muốn hỏi về địa điểm diễn ra của Mùa Hè Xanh 2022 á
Đây là hoạt động để đi làm tình nguyện á
Ai là người tổ chức cái này á
Quyền lợi khi tham gia cái này là gì vậy
Mô tả của hoạt động này là gì á
Xin chào pạn
Pạn cho mik bit CSE Job Fair do ai tổ chức khum
Ở bách khoa cơ sở 2 ó
Là ngày hội ziệc làm á pạn
Cảm ơn gút nai
Xin chào
Chốp phe tổ chức ngày nào z á
Lợi ích công tác xã hội của cái này
Ngày hội việc làm á
Tên đầy đủ sự kiện này là gì
Mùa hè xanh 2022 được tổ chức ở đâu
Cho hỏi mùa hè xanh năm 2022 được tổ chức ở đâu vậy
Làm đường tình nguyện á
Năm 2022 á
Do Khoa khoa học và kỹ thuật máy tính á
Cho mình hỏi hội trại cse connection 2022 diễn ra ở đâu á
Này là hội trại cho tân sinh viên á
Khoa máy tính á
Mùa hè xanh năm 2022 tổ chức ở đâu vậy
Đi làm tình nguyện á
Khoa khoa học và kỹ thuật máy tính á
Mùa hè xanh diễn ra khi nào
mùa hè xanh diễn ra khi nào
tình nguyện mùa hè cho sinh viên
Chào
Xuân tình nguyện 2023 diễn ra khi nào
Cho mình thông tin Mùa hè xanh 2022
Bạn biết hoạt động nào không
KMS tour diễn ra khi nào
Kết thúc khi nào
KMS tour được bao nhiêu điểm rèn luyện
Mô tả công việc KMS tour
Nơi diễn ra
Thời gian diễn ra ngày hội tuổi trẻ bách khoa đồng hành cùng pháp luật ” năm 2022
Số ngày Công tác xã hội hỗ trợ đoàn khoa ktxd
số ngày CTXH hỗ trợ đoàn khoa ktxd
Thời gian diễn ra hoạt động hỗ trợ đoàn khoa ktxd
Cho mình thông tin hoạt động bạn có hiện nay
Thời gian chào đón tân sinh viên khoá 22 khoa cơ khí
xin chào
khi nào có job fair típ v
job fair á =))) là Job Fair
ủa mình đang hỏi là nó diễn ra khi nào mà
ok
sự kiện tiếp theo là gì v
cho mình hỏi trong Job Fair có những hoạt động gì v ạ
khi nào thì có kms tour
không ý là sau năm 2023 á, khi nào có kms tour
aloo
bạn có biết bạn Lê Thanh Sang MSSV 1914900 không
bắt đầu học vào năm 2019
Bách Khoa
sắp tới có hoạt động nào để kiếm ngày công tác xã hội không
Blue Sharks là câu lạc bộ gì
lễ tốt nghiệp năm nay diễn ra vào tháng mấy
Hội nghị sinh viên là hoạt động gì
GIẢI THỂ THAO CSE OLYMPIC 2023 là hoạt động gì
có thi đấu các môn thể thao á
đố bạn
ai xinh gái nhất k19
Chào bạn, tôi muốn hỏi một số thông tin về các hoạt động ngoại khóa?
bạn có thông tin hoạt động ngoại khóa của các khoa trong trường đại học bách khoa hay chỉ khoa khoa học và kĩ thuật máy tính
bạn hãy cung cấp các hoạt động trong thời gian từ 5/5 đến 8/8
hãy cho tôi thông tin của hoạt động mùa hè xanh 2022
mô tả công việc hoạt động mùa hè canh
mình cần làm gì để tham gia hoạt động trên
hoạt động mùa hè xanh 2022
từ tháng 6 tới tháng 7
lợi ích công tác xã hội của hoạt động mùa hè xanh 2022 là gì?
cảm ơn admin
okee bạn
có những hoạt động ngoại khóa nào của khoa Khoa học và Kỹ thuật máy tính
hãy mô tả công việc của hoạt động cse connection
tôi không biết
ở bò cạp vàng
vậy bạn biết những thông tin nào về hoạt động đó
bạn có biết về hoạt động CSE GameZ không
là cuộc thi lập trình game
mình không biết
GameDev Club
bạn có biết về hoạt động VNG UNIVERSITY WEEK không
uprace thì liên quan gì tới VNG
mình hỏi uprace có liên quan gì tới VNG không
Uprace do ai tổ chức
Ngoài ra còn có đơn vị nào đồng tổ chức không
có phải đơn vị đồng tổ chức là VNG không ?
ngoài ra còn ai khác không
ngoài ra có sự tham gia của đơn vị khác không
Bạn cho mình biết các hoạt động diễn ra trong năm 2022
Bạn cho mình biết các hoạt động diễn ra trong năm 2021
Bạn cho mình biết các hoạt động diễn ra trong năm 2021 liên quan đến các câu lạc bộ
Cho mình hỏi "hội thảo định hướng nghề nghiệp sau tốt nghiệp tại nhật bản" diễn ra vào ngày nào
Được tổ chức ở đâu?
Vào mấy giờ?
Mình muốn hỏi về thời gian cụ thể
Cho mình biết có những hoạt động thể thao nào trong năm 2022 không
Hoạt động mùa hè xanh năm 2022 được tính bao nhiêu ngày công tác xã hội
Cho mình biết các hoạt động trong năm 2020
Cho mình biết các hoạt động trong khoảng 1/1/2020 đến 31/12/2020
Cho mình biết ngày hội Job Fair 2022
h6 trường đại học bách khoa thành phố hồ chí minh
Cho mình biết thông tin về hoạt động CSE GameZ
Cho mình biết thông tin về hoạt động CSE Game Z 2022
Hoạt đông CSE Game Z 2022 được tổ chức vào thời gian nào
Hoạt động CSE Job Fair 2020 diễn ra vào thời gian nào
đại học bách khoa đại học quốc gia - hồ chí minh cơ sở dĩ an
Hội trại cse connection được bao nhiêu ngày công tác xã hội
Cho mình biết hoạt động hỗ trợ hội trại 2022 được tổ chức ở đâu
hoạt động này được bao nhiêu ngày CTXH vậy
điều kiện tham gia hoạt động?
Cho mình hỏi hoạt động thu gom sách được tổ chức ngày nào
Mình có thể liên hệ ai về hoạt động sinh hoạt công dân
Thời gian đăng kí hoạt động workshop về Git là khi nào
Cho mình biết thêm về ngày hội kĩ thuật với
Mình muốn đăng kí nhận giải thưởng cho ngày hội kĩ thuật thì cần liên hệ ai
Đăng kí như thế nào vậy
Hoạt động Uprace 2022 kết thúc ngày nào
Cho mình biết đại hội đại biểu 2022-2024 tối đa bao nhiêu người
Hội trường H6
Lợi ích công tác xã hội?
ngày hội việc làm CSE
Tháng mấy năm nay sẽ diễn ra hoạt động này
làm sao để qua được mô hình hóa ạ?
thôi bỏ qua đi
bạn code bài tập lớn giùm mình được không?
làm bài tập lớn giùm mình nha
bạn có lấy dữ liệu người dùng hong z
Thời gian bắt đầu Mùa hè xanh 2023
Thời gian mở đăng kí cho chiến dịch Mùa Hè Xanh
Mình không biết
Nơi diễn ra chiến dịch Mùa Hè Xanh năm 2023
Hiện có sự kiện nào đang được tổ chức không?
Cho tôi thông tin về KMS tour
Tôi muốn biết thêm về KMS tour
KMS tour còn hạn đăng ký không?
Khi nào diễn ra chiến dịch mùa hè xanh
Có hoạt động nào có từ 1 đến 2 ngày công tác xã hội không
Liên hệ ai để đăng ký hỗ trợ quán cơm 2000
Hoạt động đó diễn ra ngày nào
tôi có thể tìm hoạt động công tác xã hội ở đâu
hoạt động uprace diễn ra trong thời gian nào?
cách thức đăng kí hoạt động mùa hè xanh
mùa hè xanh diễn ra ở đâu?
số lượng người tham gia hoạt động mùa hè xanh 2022
thời gian diễn ra trong năm 2022
hội thảo ứng dụng trí tuệ nhân tạo trong lĩnh vực hành chính công
chủ hoạt động của hội thảo ứng dụng trí tuệ nhân tạo trong lĩnh vực hành chính công
địa điểm của hội thảo ứng dụng trí tuệ nhân tạo trong lĩnh vực hành chính công
cách thức đăng kí hội thảo ứng dụng trí tuệ nhân tạo trong lĩnh vực hành chính công
thời gian bắt đầu hội thảo ứng dụng trí tuệ nhân tạo trong lĩnh vực hành chính công
thời gian kết thúc hội thảo ứng dụng trí tuệ nhân tạo trong lĩnh vực hành chính công
thông tin liên hệ hội thảo ứng dụng trí tuệ nhân tạo trong lĩnh vực hành chính công
lợi ích hội thảo ứng dụng trí tuệ nhân tạo trong lĩnh vực hành chính công
số ngày công tác xã hội của hội thảo ứng dụng trí tuệ nhân tạo trong lĩnh vực hành chính công
cộng tác viên hỗ trợ chuẩn bị tài liệu cho hội đồng đồ án / lvtn
địa điểm cộng tác viên hỗ trợ chuẩn bị tài liệu cho hội đồng đồ án / lvtn
địa điểm
cách thức đăng kí cộng tác viên hỗ trợ chuẩn bị tài liệu cho hội đồng đồ án / lvtn
địa điểm của cộng tác viên hỗ trợ chuẩn bị tài liệu cho hội đồng đồ án / lvtn
yêu cầu của cộng tác viên hỗ trợ chuẩn bị tài liệu cho hội đồng đồ án / lvtn
thời gian bắt đầu
số người tham gia hỗ trợ chuẩn bị tài liệu cho đồ án
thời gian bắt đầu chuẩn bị tài liệu
ngày hội kỹ thuật
số người tham gia ngày hội kỹ thuật
địa điểm tổ chức ngày hội kỹ thuật
thời điểm diễn ra trong năm 2022
cơ sở 1
thời gian kết thúc ngày hội kỹ thuật
thời gian kết thúc ngày hội
ceac events
địa điểm diễn ra
địa điểm của ceac events
cách thức đăng kí ceac
cách thức đăng kí ceac events
chủ tổ chức ceac events
mô tả công việc của ceac events
khám sức khỏe
địa điểm khám sức khỏe
địa điểm khám sức khỏe sinh viên khóa 21
lệ phí khám sức khỏe
yêu cầu khám sức khỏe
liên hệ khám sức khỏe
oth regensburg
yêu cầu oth regensburg
yêu cầu của oth regensburg
cách thức đăng kí
mùa hè xanh
lợi ích của mùa hè xanh
nhập liệu
Cho mình hỏi các hoạt động diễn ra vào 2023
hỗ trợ đoàn khoa ktxd ngày 12/12/2022 ca chiều là hoạt động của 2023 chứ
thời gian diễn ra hoạt động hỗ trợ đoàn khoa ktxd ngày 12/12/2022 ca chiều
ai tổ chức sự kiện này
Cho mình hỏi các hoạt động diễn ra vào 2021
đây không phải các hoạt động diễn ra vào năm 2021
từ 20/5/2021 đến 22/11/2022 có những hoạt động nào
cảm ơn bạn
Cho mình những hoạt động có từ 1 ngày ctxh trong năm 2021
cho mình thời gian bắt đầu hoạt động hỗ trợ sắp xếp kho
hoạt động này diễn ra ở đâu
cho mình hỏi các hoạt động diễn ra vào 2022
cho mình hỏi các hoạt động diễn ra vào 2023
63ee3346f19c1d4d09255add
cho mình hỏi về hoạt động hỗ trợ chuẩn bị hồ sơ
hoạt động hỗ trợ chuẩn bị hồ sơ
cho mình các hoạt động diễn ra vào 2022
cho mình các hoạt động diễn ra vào 2023
cho mình các hoạt động điễn ra vào 2021
cho mình hỏi về hoạt động diễn ra vào 2021
mình muốn tham gia mùa hè xanh 2022
hoạt động do khoa khoa học và kỹ thuật máy tính trường đại học bách khoa tổ chức
cho mình hỏi hoạt động diễn ra vào 2022
hỗ trợ đoàn khoa ktxd
hoạt động này được bao nhiêu ngày ctxh
Hoạt động năm 2023
bạn cho mình hỏi các hoạt động diễn ra vào 2023
bạn cho mình hỏi các hoạt động diễn ra vào 01/2023
bạn cho mình hỏi các hoạt động diễn ra vào 12/2022
thời gian diễn ra hỗ trợ đoàn ktxd
số lượng tuyển là bao nhiêu
thời gian hỗ trợ đoàn khoa ktxd ngày 12/12/2022 ca chiều là khi nào
kết thúc khi nào
tổ chức tại đâu
hoạt động này làm công việc gì
có bao nhiêu người tham gia
cho mình form đăng ký
cho mình link đăng ký
khi hoạt động bắt đầu, mình phải liên lạc với ai
cho mình xin thông tin liên lạc của người phụ trách nhé
cho mình hỏi các hoạt động diễn ra vào 12/2022
thời gian cụ thể của hoạt động hỗ trợ đoàn ktxd chiều
mình xin thông tin liên hệ
cho mình hỏi các hoạt động diễn ra vào năm 2022
cho mình hỏi các hoạt động diễn ra vào năm 2021
các hoạt động diễn ra vào năm 2020
cho mình hỏi các hoạt động diễn ra vào năm 2020
cho mình hỏi các hoạt động diễn ra vào năm 2019
cho mình hỏi các hoạt động diễn ra vào năm 2018
cho mình hỏi các hoạt động năm 2017
cho mình danh sách các hoạt động năm 2016
cho mình danh sách các hoạt động trong năm 2020
cho mình hoạt động 01/2020
cho mình các hoạt hoạt động 01/2020
cho mình hỏi các hoạt động tháng 01/2020
cho mình hỏi các hoạt động diễn ra vào tháng 01/2020
cho mình các hoạt động diễn ra vào 01/2020
cho mình thông tin về hoạt động ký kết
hoạt động ký kết diễn ra lúc nào
hoạt động này cần bao nhiêu người
hoạt động ký kết kết thúc lúc nào
hoạt động ký kết cần bao nhiêu người tham gia
cho mình xin thông tin liên hệ
quyền lợi khi tham gia hoạt động
tham gia hoạt động này sẽ được bao nhiêu ngày ctxh
bao nhiêu nguời tham gia hoạt động này
cho mình các hoạt động cùng ngày được không
có hoạt động nào diễn ra vào ngày mai không
có hoạt động nào tháng 05/2020 không
có hoạt động nào diễn ra vào tháng 05/2020 không
cho mình hỏi hoạt động nào diễn ra vào tháng 05/2020
cho mình hỏi hoạt động diễn ra vào tháng 05/2020
cho mình hỏi các hoạt động diễn ra vào tháng 05/2020
cho mình hỏi các hoạt động diễn ra vào 05/2020
cho mình hỏi các hoạt động diễn ra vào 05/2022
cho mình hỏi các hoạt động diễn ra vào 12/2021
cho mình hỏi hoạt động diễn ra vào tháng 6/2021
cho mình hỏi hoạt động diễn ra vào tháng 1 năm 2023
cho mình hỏi hoạt động vào tháng 4 năm 2023
tháng 3 thì sao
bách khoa cơ sở 1
hoạt động tên gì
diễn ra ở đâu
tôi cần liên hệ với ai để tham gia hoạt động
cho mình hoạt động vào tháng 12 năm 2022
cho mình hỏi các hoạt động tháng 12 năm 2022
hoạt động tuyển ctv hỗ trợ đoàn ktxd ca sáng diễn ra lúc nào
kết thúc lúc nào
lợi ích
quyền lợi khi tham gia hoạt động là gì
liên hệ
mình muốn biết số người tham gia hoạt động này
mình phải làm gì
cho mình đăng ký tham gia nhé
cho mình hỏi các hoạt động tháng 1 năm 2023
hoạt động hỗ trợ đoàn ngày 12 diễn ra lúc nào
hỗ trợ
hoạt động hỗ trợ đoàn 12/01/2023 diễn ra khi nào
khi tham gia hoạt động sẽ làm công việc gì
số lượng nguời tham gia hoạt động này
có yêu cầu gì khi tham gia hoạt động này không
cho mình link đăng ký nhé
sau khi tham gia sẽ được quyền lợi gì
quyền lợi khi tham gia hoạt động này
lợi ích ?
lợi ích của hoạt động là gì
lợi ích công tác xã hội?
lợi ích điểm rèn luyện?
cho mình hỏi các hoạt động tháng 2 năm 2023
hỗ trợ đoàn khoa ktxd thứ 3 ngày 07/02/2023 diễn ra ở đâu
công việc phải làm khi tham gia hoạt động là gì
số lượng người tham gia hoạt động này
link đăng ký
link đăng ký hoạt động này là gì
lợi ích ctxh của hoạt động
mình phải liên hệ ai khi tham gia
hoạt động tháng 10 năm 2023
cho mình hỏi hoạt động tháng 10 năm 2023
cho mình các hoạt động diễn ra vào tháng 10 năm 2022
hoạt động chào tân sinh viên diễn ra khi nào
bắt đầu lúc mấy giừo
hoạt động này bắt đầu từ mấy giờ
yêu cầu của hoạt động
hoạt động diễn ra ở đâu
hoạt động này cần làm gì
hoạt động yêu cầu gì
cho mình hỏi về hoạt động hỗ trợ đoàn khoa ktxd thứ 3 ngày 07/02/2023
hoạt động tổ chức ở đâu
số lượng người tham gia là bao nhiêu
cho mình link đăng ký và người để liên hệ
thời gian bắt đầu hoạt động
lợi ích ctxh
lợi ích ctxh của hoạt động này là gì
cse olympic do ai tổ chức
xuân tình nguyện tổ chức ở đâu
cho mình hỏi các hoạt động tổ chức vào tháng 1 năm 2023
hoạt động chuẩn bị hồ sơ do ai tổ chức
làm sao để đăng ký tham gia hoạt động này
tham gia hoạt động được bao nhiêu ngày công tác xã hội
những hoạt động nào khi tham gia được 3 điểm rèn luyện
hội nghị khoa học công nghệ khi tham gia được bao nhiêu điểm rèn luyện
mô tả công việc của hội nghị sinh viên là gì
tham gia hoạt động đó được những quyền lợi gì
Những hoạt động nào của khoa máy tính tổ chức vào tháng 11 năm 2021
Những hoạt động nào của khoa máy tính tổ chức vào cuối năm 2022
Những hoạt động nào của khoa máy tính tổ chức vào cuối năm 2021
Những hoạt động nào của khoa máy tính tổ chức vào cuối năm 2020
Mô tả công việc của tuần lễ sinh viên khỏe là gì
Có bao nhiêu người tham gia hoạt động này
Tham gia hoạt động thu được quyền lợi gì
Làm sao để đăng ký tham gia
Hạn đăng ký của hoạt động là gì
Hoạt động diễn ra vào tháng 10 năm 2020 đúng không
Chào ad
Có hoạt động nào diễn ra trong tháng tới không
Cho mình hỏi mùa hè xanh năm trước tổ chức ở đâu
Hoạt động diễn ra vào năm trước
Hội trại cse 2019 được tổ chức ở đâu
Vào tháng 10 năm 2019
Hội trại cse 2019 tổ chức ở đâu
Tổ chức vào 2019
Người nắm chính là khoa máy tính
Sự kiện này tổ chức khi nào
Hội trại cse connection 2019 tổ chức ở đâu
Hội trại cse connection 2020 tổ chức ở đâu
Hoạt động nào tổ chức ở thác đá hàn
4 tháng trước có những hoạt động nào diễn ra
Mùa hè xanh năm trước tổ chức ở đâu
Mình không rõ nữa
Vào năm 2022
Khoa máy tính tổ chức hoạt động này
Ok cảm ơn
Hello ad
Không có gì, cảm ơn
hoạt động nào do khoa máy tính tổ chức vào năm 2020
cse connection 2019 diễn ra ở đâu
hoạt động diễn ra vào năm 2019
ad ơi cho hỏi hội trại cse 2020 tổ chức ở đâu
hoạt động diễn ra vào năm 2020
hoạt động do ai tổ chức
liên hệ với ai để biết thông tin hoạt động
làm sao để đăng ký tham gia hoạt động
cảm ơn ad nhiều
vào tháng 6 năm 2022
cảm ơn bạn nhiều
Xuân tình nguyện 2019 được tổ chức ở đâu
Không rõ nữa
Hoạt đọng diễn ra vào cuối năm 2019
Mô tả công việc của hoạt động là gì
Làm sao để đăng ký tham gia hoạt động
Quyền lợi khi tham gia hoạt động là gì
Liên hệ với ai để tham gia
Tên hoạt động là gì
cho mình xin luôn danh sách của năm 2022 nhé
cho mình hỏi 12/2022 có những hoạt động nào được tổ chức vậy ạ?
mình muốn biết số lượng tham gia của hoạt động dọn dẹp nghĩa trang thành phố
làm sao để đăng ký tham gia hoạt động này?
cho mình hỏi luôn về thời hạn kết thúc đăng ký
vậy mình cảm ơn
cho mình xin danh sách các hoạt động có từ 3 đến 5 ngày công tác xã hội
yêu cầu để tham gia career talk là gì vậy
hoạt động này do ai tổ chức vậy
vậy còn thời gian bắt đầu thì sao
năm ngoái có các hoạt động gì vậy bạn
hỗ trợ đoàn khoa ktxd cần bao nhiêu người tham gia vậy
hoạt động này hiện mình có còn kịp đăng ký không bạn
hoạt động này ai là người tổ chức vậy
cho mình hỏi về hoạt động công tác xã hội cộng tác viên hỗ trợ vận chuyển đồ
mình nghỉ là từ 13:00 đến 16:00 ngày 15/06/2022
cho mình hỏi về hoạt động hội thảo ứng dụng trí tuệ nhân tạo
hoạt động mà người liên hệ là hoàng đức nguyên ấy bạn
số lượng tham gia là bao nhiêu vậy
cho mình hỏi về hoạt động hỗ trợ cuộc thi học thuật
mình nhớ nơi diễn ra là ở toà a3 cơ sở lý thường kiệt
mình muốn biết thông tin liên hệ của hoạt động này
mình không rõ
hình như là vào 12/2022
yêu cầu tham gia của hoạt động này là gì
mình được lợi ích gì khi tham gia hoạt động này
mình cảm ơn
cho mình hỏi về hoạt động vào ngày 7/3/2022
công việc này cụ thể là làm gì vậy bạn
7/3/2022
Mình cảm ơn
Đúng hoạt động này rồi
cho mình tìm các hoạt động cho sinh viên có điểm trung bình từ 6.5 trở lên
có hoạt động nào diễn ra vào 11/2019 không bạn
trong số hoạt động trên có hoạt động nào cho sinh viên có điểm trung bình từ 6.5 trở lên không bạn
cho mình hỏi về hoạt động có địa điểm ơ tòa nhà h6 trường đại học bách khoa cơ sở 2
về hoạt động hội việc làm
địa điểm hoạt động nằm ở đâu vậy
vào ngày 30/11
mình muốn hỏi về hoạt động hỗ trợ hội thảo mắt
vậy còn về hoạt động tư vấn sức khỏe về mắt thì sao ạ
hoạt động tham dự lễ bế mạc hội thao sinh viên thì sao bạn
số lượng tham gia hoạt động này là bao nhiêu
mình muốn biết danh sách các hoạt động vào tháng 1 năm ngoái
mình muốn biết thêm thông tin về hoạt động youth award
Hoạt động youth award do ai tổ chức
số lượng tham gia của hoạt động này là bao nhiêu vậy
số lượng tham gia của hoạt động bách khoa youth award 2022 là bao nhiêu vậy
Mình muốn biết danh sách các hoạt động trong năm 2019
mình muốn biết thời gian mở đăng ký office tour
Mình muốn biết thời gian mở đăng ký mùa hè xanh cse 2019
vậy còn thời gian mở đăng ký đấu trường hack não thì sao
đấu trường hack não số lượng tham gia là bao nhiêu
Mình muốn hỏi về cuộc thi hackathon acb win 2019
Số lượng người tham gia hoạt động là bao nhiêu vậy ạ
cuộc thi hackathon acb win 2019 do ai tổ chức vậy bạn
bạn cho mình xin mô tả công việc của hoạt động cuộc thi hackathon acb win 2019
bạn có thể cho mình biết thời gian mở đăng ký của cuộc thi hackathon acb win 2019 là ngày nào không
cho mình hỏi năm ngoái khoa khoa học và kỹ thuật máy tính có các hoạt động nào vậy ạ
Mình muốn biết yêu cầu tham gia của hội trại cse connection
năm 2019
hội trại cse connection vào năm 2019 số lượng tham gia là bao nhiêu vậy bạn
yêu cầu tham gia của hội trại cse connection 2019 là gì bạn nhỉ
mình muốn biết năm 2018 có hoạt động nào
mình muốn biết ai là người tổ chức cse connection 2018
2018
Mình muốn hỏi về một số hoạt động của trường vào 03/2019
Vậy còn các hoạt động vào 06/2019 thì sao
Vậy thì mình muốn biết danh sách toàn bộ các hoạt động trong năm 2019
Tham quan văn phòng zalo có những yêu cầu nào vậy bạn
Hoạt động này do ai tổ chức thế bạn
lợi ích tham gia hoạt động này là gì vậy
Số lượng tham gia hoạt động là bao nhiêu vậy
thế thì cho mình biết thời gian mở đăng ký là khi nào được không
hoạt động này mình có thể liên hệ với ai vậy
cách thức đăng ký hoạt động là như thế nào
mình muốn hỏi về đấu trường hack não
Hoạt động này do ai tổ chức vậy
mình có thể liên hệ với ai để biết thêm thông tin về hoạt động này
Yêu cầu tham gia hoạt động này là gì vậy ạ
mình muốn biết danh sách hoạt động của năm 2022
yêu cầu của ngày sinh viên sáng tạo khu vực miền nam là gì vậy bạn
mình muốn biết cách thức đăng ký ngày sinh viên sáng tạo khu vực miền nam
Số lượng tham gia của hoạt động trên là gì vậy
mình muốn biết về hoạt động hỗ trợ công tác thư viện
vận chuyển sách bạn ạ
Công việc vận chuyển sách
hoạt động này diễn ra ở đâu vậy
yêu cầu hoạt động này là gì vậy ạ
hoạt động còn diễn ra ở nơi nào khác nữa không bạn
hoạt động còn diễn ra ở nơi nào khác nữa không ạ
mình muốn hỏi về hoạt động hỗ trợ đoàn khoa ktxd
số lượng tham gia hỗ trợ đoàn khoa ktxd là bao nhiêu vậy
số lượng tham gia hỗ trợ đoàn khoa ktxd ngày 12/01
số lượng tham gia hỗ trợ đoàn khoa ktxd 12/12
mình muốn hỏi về hoạt động nhận thẻ sinh viên
hoạt động nhận thẻ sinh viên diễn ra vào tháng 10/2020 ấy
mình muốn biết địa điểm tham gia
mình muốn biết mô tả công việc của hoạt động
hoạt động này do ai tổ chức thế bạn
hoạt động này khi nào kết thúc thế
mình muốn hỏi về các hoạt động liên quan tới youth award 2020
Mình muốn biết thông tin về bách khoa youth award 2022
mình muốn biết một số thông tin về thắp nến tri ân
mình muốn biết một số thông tin về hoạt động thắp nến tri ân kỷ niệm 47 năm
về hoạt động hỗ trợ lễ thắp nến tri ân kỷ niệm 47 năm ngày giải phóng miền nam
hoạt động diễn ra ở đâu thế
có cách nào để đăng ký tham gia hoạt động không
thông tin liên quan đến hoạt động lớp cảm tình đoàn
hoạt động lớp cảm tình đoàn
mình cần biết yêu cầu tham gia hoạt động
thời gian bắt đầu là khi nào thế
về hoạt động mùa hè xanh thành phố
hoạt động diễn ra ở đâu vậy
sửa sang cơ sở vật chất
sửa sang cơ sở vật chất giảng dạy vui chơi bên các em nhỏ
mình liên hệ với ai vậy ạ
thời gian hoạt động kết thúc là khi nào thế
thông tin về career talk
hoạt động career talk
mình muốn biết mô tả hoạt động
mình muốn biết địa điểm diễn ra của hoạt động career talk
có cách nào để đăng ký tham gia hoạt động không ạ
mình có được lợi ích gì khi tham gia hoạt động này vậy bạn
bạn có thể giới thiệu về khoa của bạn không
mùa hè xanh năm nay khoa tổ chức ở đâu
thời gian tổ chức mùa hè xanh 2023?
xã phú thành b huyện tam nông tỉnh đồng tháp
năm nay khoa có tổ chức job fair nào không?
thông tin về job fair 2022
job fair 2022 diễn ra ở đâu?
mùa hè xanh 2022 ở đâu?
điểm rèn luyện khi đi mùa hè xanh?
ngày công tấc xã hội khi đi mùa hè xanh 2022
tết tình nguyện 2022 được tổ chức lúc nào
tết tình nguyện được tổ chức ở đâu
tết tình nguyện là làm những gì?
Mô tả công việc tết tình nguyện
tết tình nguyện 2022 kết thúc khi nào
ai là người tổ chức
cách thức đăng kí tham gia xuân tình nguyện?
số điện thoại liên hệ đoàn khoa máy tính
mình không biết bạn
job fair 2022 diễn ra ở đâu
thời gian ký kết?
được tổ chức hội trường a4 cơ sở lý thường kiệt đó bạn
đi lễ kí kết được nhiêu ngày công tác xã hội
08:30:00 27-12-2022.
đăng kí tham gia lễ kí kết
thời gian diễn ra và kết thúc của lễ kí kết
còn thời gian kết thúc?
những yêu cầu khi tham gia lễ kí kết
xuân tình nguyện thành phố diễn ra ở đâu
16-01-2021
những yêu cầu của sinh viên khi tham gia
người tổ chức là ai?
thông tin liên lạc khi gặp vấn đề
đăng kí ở đâu?
bạn biết chiến dịch gia sư áo xanh 2022 được bắt đầu khi nào không?
bạn biết chiến dịch gia sư áo xanh 2022 được bắt đầu khi nào không?
chiến sĩ gia sư áo xanh 2022 diễn ra lúc nào
hội thảo trực tuyến chia sẻ kinh nghiệm du học tại Đức diễn ra ở đâu
ai là người tổ chức sự kiện
tham gia bằng cách nào
thời gian bắt đầu sự kiện
thời gian kết thúc sự kiện
số ngày ctxh tối đa là bao nhiêu
phát cơm
cho mình tên những hoạt động ngoại khóa tổ chức thường niên
ho mình tên những hoạt động ngoại khóa tổ chức thường niên cùa khoa máy tính
Hội trại cse thường được tỏ chức ở đâu
Hội trại cse của khoa máy tính
Thời gian tổ chức hoạt động này là tháng mấy
cho mình tên hoạt động ngoại khóa mà chạy theo app để lấy ngày ctxh
hoạt động chạy mà
Hoạt động nhận ngày ctxh online bằng cách tham gia app và chạy bộ ấy
Mình hỏi tên hoạt động
Năm 2022 thì sao
không phải
Hoạt động chạy bộ nhận ngày ctxh
Tên hoạt động
Tên hoạt động chạy bộ nhận ngày ctxh
Mình hỏi tên của hoạt động ấy
Tên các hoạt động diễn ra vào hè 2022
Tên các hoạt động diễn ra vào hè 2021
năm 2021 mà
Tên các hoạt động diễn ra vào hè năm 2021
Tên các hoạt động nhận ngày ctxh online
Cho mình tên các hoạt động nhận ngày ctxh online
Hoạt động chào đón tân sinh viên khoá 22 khoa cơ khí nhận bao nhiêu ngày ctxh
Hoạt động uprace 2022 nhận bao nhiêu ngày ctxh
Uprace 2022
Thời gian bắt đầu của hoạt động mùa hè xanh cse 2022 là lúc nào
mùa hè xanh cse
Ở Đồng tháp
Thời gian bắt đầu mà
thời gian diễn ra hoạt động này là lúc nào
Thời gian diễn ra mùa hè xanh 2022
Nơi diễn ra uprace 2021
Chạy bộ
CHo mình thông tin chi tiết hơn
Cho mình thông tin chi tiết hơ
Cho mình thông tin chi tiết hơn về uprace 2022
Hoạt động chạy tên là gì
Thời gian diễn ra là lúc nào
Hoạt động kết thúc lúc nào
Nơi diễn ra uprace mùa hè xanh 2022 week 0
Số ngày ctxh nhận từ mùa hè xanh 2022
Số ngày ctxh nhận từ hoạt động nhập liệu
Số ngày ctxh nhận từ hoạt động mùa hè xanh cse 2021
Các hoạt động nhận drl
Các hoạt động nhận điểm rèn luyện nằm 2021
Các hoạt động nhận điểm rèn luyện năm 2021
Các cách nhận điểm rèn luyện là gì
Điểm rèn luyện dùng làm gì vậy
Liện hệ ai để tham gia hoạt động mùa hè xanh
Cách tham gia hoạt động mùa hè xanh
Hoạt động mùa hè xanh
Mô tả công việc của hoạt động mùa hè xanh 2022
Yêu cầu khi tham gia hoạt động mùa hè xanh 2022
Địa điểm của hoạt động cộng tác viên hỗ trợ công tác của khoa
số lượng yêu cầu là bao nhiêu
Yêu cầu hoạt động là gì
Cách đăng ký là gì
thời gian diễn ra là lúc nào
Thời gian kết thúc là lúc nào
Số ngày ctxh nhận được là bao nhiêu
Sao lại vượt quá
Số ngày ctxh hoạt động cộng tác viên hỗ trợ công tác của khoa
Địa điểm hoạt động tuyển trọng tài cho giải đấu ecse cup 2023
số lượng tham gia
yêu cầu là gì
cách đăng ký
địa điểm hoạt động hỗ trợ chuẩn bị hồ sơ
Yêu cầu là gì
Người tổ chức là ai
Thời gian diễn ra lúc nào
Hoạt động hỗ trợ dọn dẹp khu tự học hella h6 diễn ra ở đâu
số lượng tham gia là bao nhiêu
Có yêu cầu gì không
mình sẽ liên hệ với ai
khoảng thời gian hoạt động diễn ra lúc nào
số ngày ctxh nhận được
hoạt động hỗ trợ dọn dẹp khu tự học hella diễn ra lúc nào
hoạt động hỗ trợ dọn dẹp khu tự học hella diễn ra ở đâu
hoạt động hỗ trợ dọn dẹp khu tự học hella ngày 02/02/2023 yêu cầu bao nhiêu người
hoạt động hỗ trợ dọn dẹp khu tự học hella ngày 02/01/2023 yêu cầu bao nhiêu người
hoạt động hỗ trợ dọn dẹp khu tự học hella ngày 02-01-2023 yêu cầu bao nhiêu người
hoạt động hỗ trợ chuẩn bị hồ sơ diễn ra ở đâu
Hoạt động do ai tổ chức
thời gian kết thúc là lúc nào
Hoạt động hỗ trợ vận chuyển đồ diễn ra ở đâu
Hoạt động diễn ra ở những nơi nào khác
thòi gian bắt đầu lúc nào
Hoạt động hội thảo ứng dụng trí tuệ nhân tạo diễn ra ở đâu
thời gian bắt đầu là lúc nào
hoạt động hỗ trợ chuẩn bị tài liệu cho hội đồng đồ án diễn ra ở đâu
cách đăng ký thế nào
thời gian diễn ra hoạt động
số ngày ctxh bao nhiêu
hoạt động hỗ trợ ngày hội kĩ thuật diễn ra ở đâu
hoạt động hỗ trợ ngày hội kĩ thuật diễn ra ở đâ
hoạt động hỗ trợ ngày hội kỹ thuật diễn ra ở đâu
hoạt động hỗ trợ vận chuyển đồ ceac events diễn ra ở đâu
Hoạt động diễn ra ở phòng nào
mô tả hoạt động này
hoạt động cộng tác viên hỗ trợ vận chuyển đồ ceac events diễn ra ở đâu
hoạt động vận chuyển đồ ceac events diễn ra ở đâu
thời gian tổ chức
Thời gian kết thúc
Hoạt động xuân tình nguyện 2022 diễn ra khi nào
Năm 2022 mà
Hoạt động tổ cức ở đâu
Hoạt động tổ chức ở đâu
Hoạt động có bao nhiêu người tham gia
Mô tả hoạt động mái ấm tình thương
mô tả hoạt động
mùa hè xanh 2019 tổ chức ở đâu
Các hoạt động diễn ra trong hè 2020
Hội hiến máu tình nguyện tổ chức ở đâu
có yêu cầu gì không
ngày sinh viên sáng tạo khu vực miền nam năm 2020 tổ chức ở đâu
Cách đăng ký tham gia thế nào
hoạt động nào diễn ra mà mùa xuân
hoạt động nào diễn ra vào mùa xuân
ngày hội tuổi trẻ bách khoa đồng hành cùng pháp luật tổ chức ở đâu
Do ai tổ chức
Sô người tham gia là bao nhiêu
Các hoạt động năm 2022 của khoa máy tính
hỗ trợ làm hồ sơ tổ chức ở đâu
số ngày ctxh nhận được là bao nhiêu
Các hoạt động nhận điểm rèn luyện
Thời gian mở đăng ký mùa hè xanh 2021
Thời gian đóng đăng ký lúc nào
Hoạt động nhập liệu do ai tổ chức
hỗ trợ hỗ trợ phỏng vấn chiến dịch xuân tình nguyện tổ chức ở đâu
do ai tổ chức
mình sẽ nhận bao nhiêu ngày ctxh
Cách đăng ký tham gia mùa hè xanh
hội trại cse connection 202 tổ chức ở đâu
hội trại cse connection 2022 tổ chức ở đâu
hoạt động diễn ra lúc nào
drl nhận được là bao nhiêu
cộng tác viên ban chấp hành đoàn thanh niên hội sinh viên đăng ký thế nào
cộng tác viên ban chấp hành đoàn thanh niên hội sinh viên
Cách đăng ký thế nào
Lợi ích nhận được là gì
lợi ích là gì
Hoạt động cộng tác viên ban chấp hành đoàn thanh niên hội sinh viên do ai tổ chức
Mình sẽ liên hệ với ai
hoạt động bách khoa league 2022 tổ chức tại đâu
chiến dịch mùa hè xanh mặt trận thành phố 2022 do ai tổ chức
Thời gian bắt đầu là lúc nào
Mô tả công việc
Mô tả hoạt động
mô tả
Miêu tả công việc
số ngày ctxh là bao nhiêu
mình sẽ liên hệ ai
hỗ trợ công tác đoàn khoa bắt đầu lúc nào
xuân tình nguyện 2022 hoạt động hiến máu đăng ký thế nào
địa điểm ở đâu
thời gian kết thúc khi nào
cách đăng ký sàn đấu ý tưởng sinh viên thành phố
mô tả công việc
thời gian đăng ký lúc nào
thời gian bắt đầu lúc àno
thời gian kết thúc lúc nào
an sinh đợt 3 do ai tổ chức
miêu tả hoạt động
thời gian bắt đầu lúc nào
"post_id": "63ee3346f19c1d4d09255b24"
cuộc thi minathon 2023
thời gian bắt đầu của cuộc thi minathon 2023
thời gian kết thúc của hoạt động trên là ngày mấy?
cuộc thi minathon 2023 diễn ra ở đâu vậy bạn?
tham gia hoạt động này được lợi ích bao nhiêu ngày công tác xã hội vậy bạn?
lợi ích công tác xã hội
hoạt động minathon có lợi ích bao nhiêu ngày công tác xã hội
hoạt động cuộc thi minathon 2023
lợi ích ngày công tác xã hội
yêu cầu để tham gia hoạt động này?
điều kiện để tham gia hoạt động này?
ai tổ chức hoạt động này?
hoạt động giải thể thao cse olympic 2023 diễn ra vào ngày nào?
hoạt động giải thể thao cse olympic 2023
hoạt động này được tổ chức ở đâu?
hoạt động này diễn ra ở đâu?
giải thể thao cse olympic 2023
hoạt động này được tổ chức ở đâu
hoạt động này được diễn ra ở đâu?
nơi diễn ra hoạt động này?
cách tham gia hoạt động này
điều kiện để tham gia
chiến dịch mùa hè xanh
đồng tháp
địa điểm diễn ra hoạt động này?
ngày kết thúc hoạt động là ngày mấy vậy bạn?
tham gia hoạt động này được lợi ích bao nhiêu ngày công tác xã hội?
ai tổ chức hoạt động này?\
hoạt động mùa hè xanh năm 2023
mình liên lạc với ai để tham gia hoạt động
chiến dich mùa hè xanh năm 2023
thời gian diễn ra hoạt động này là ngày mấy vậy bạn?
cộng tác viên hỗ trợ chuẩn bị tài liệu cho hội đồng đồ án
mình tập trung ở đâu vậy bạn?
nơi diễn ra hoạt động này là ở đâu vậy bạn?
ai có thể tham gia hoạt động này?
yêu cầu của hoạt động này?
làm thế nào tham gia hoạt động này?
lợi ích ngày công tác xã hội khi tham gia hoạt động này?
cộng tác viên hỗ trợ vận chuyển đồ ceac events
thời gian bắt đầu của hoạt động này?
thời gian kết thúc?
thời gian kết thúc hoạt động?
yêu cầu của hoạt động này là gì?
Chi tiết của hoạt động này?
mô tả của hoạt động này?
công việc vận chuyển đồ trong khu vực làng đại học
yêu cầu của công việc này?
63ee3346f19c1d4d09255ae8
hỗ trợ vận chuyển đồ
22/12/2022
hoạt động này được lợi ích bao nhiêu ngày công tác xã hội
tìm kiếm thông tin xử lý dữ liệu
tuyển sinh kỹ sư tài năng khoá 2021
cách tham gia hoạt động này?
ai có thể tham goia hoạt động này?
lợi ích khi tham gia hoạt động này là gì?
tham gia được lợi ích bao nhiêu ngày công tác xã hội/
nơi diễn ra hoạt động này là ở đâu?
seminar gặp gỡ sinh viên cùng shopee
sắp xếp hồ sơ / nhập liệu tuyển sinh viên làm việc tích lũy ngày công tác xã hội
hỗ trợ cho giải đấu ecse cup 2023
bạn có thể cho mình biết chi tiết của hoạt động được không?
thời gian diễn ra hoạt động này?
liệt kê các ngày hoạt động có ngày công tác xã hội nhiều nhất trong năm 2022
cụ thể số ngày của từng hoạt động
cụ thể số ngày của từng hoạt động hỗ trợ đoàn khoa ktxd ngày 12/12/2022 ca chiều
cụ thể số ngày CTXH nhận được của hoạt động hỗ trợ đoàn khoa ktxd ngày 12/12/2022 ca chiều
các CTXH của khoa máy tính trong tháng 2/2020
ảm ơn admin,
CTXH của khoa máy tính trong tháng 2/2020
hoạt động của khoa máy tính trong tháng 2/2020
có những hoạt động nào vậy
12/12/2022 có những hoạt động CTXH nào
hỗ trợ đoàn khoa ktxd ngày 12/12/2022 ca chiều, sẽ cung cấp bao nhiêu ngày CTXH cho tôi
nhận báo cáo lvtn đồ án 1 12/12/2022, sẽ cung cấp bao nhiêu ngày CTXH cho tôi
Hoạt động mùa hè xanh năm 2021 bắt đầu từ ngày nào
do ai tổ chức vậy
tháng 4/2022 có những hoạt động công tác xã hội nào
tôi rảnh ngày 1 tới ngày 18 tháng 04 năm 2022, tôi có thể tham gia hoạt động nào
năm 2023 có những hoạt động nào
mùa hè xanh năm 2022 bắt đầu và kết thúc ngày nào
hoạt động kéo dài bao nhiêu ngày ?
tôi muốn tham gia hoạt động có 5 ngày CTXH năm 2020
có những hoạt động nào
hội thảo định hướng nghề nghiệp sau tốt nghiệp tại nhật bản cung cấp bao nhiêu ngày CTXH
hoạt động: "tìm kiếm thông tin xử lý dữ liệu"
tôi tham gia hoạt động ở đâu
cụ thể hoạt động làm gì
cảm ơn ban
miêu tả hoạt động này
số lượng người tham gia tối đa
có yêu cầu gì với người tham gia không
tôi có thể đăng ký ở đâu
link đăng ký ở đâu
thời gian diễn ra hoạt động này
thời gian kết thúc hoạt động này
lợi ích khi tham gia hoạt động này
hoạt động có id: 63ee3346f19c1d4d09255b9d
tên hoạt động này là gì
hoạt động: hậu duệ pascal
hoạt động này bắt đầu ngày nào
hoạt động: hậu duệ pascal 2021 khai phá bản lĩnh coder
Nơi diễn ra hoạt động
Nơi diễn ra hoạt động hậu duệ pascal 2021 khai phá bản lĩnh coder
Nơi diễn ra hoạt động hậu duệ pascal
cảm ơn banh
mùa hè xanh KH-KT máy tính năm 2020 có được tổ chức không
hoạt động tình nguyện
mùa hè năm 2020
tôi có thể nhận bao nhiêu ngày CTXH
tôi có đạt được lợi ích gì không
mùa hè xanh 2022
mùa hè 2022
mùa hè xanh 2022 do khoa KHKTMT tổ chức, diễn ra ở đâu
mùa hè xanh 2022 do khoa KHKTMT tổ chức vào tháng 6/2022, diễn ra ở đâu
mùa hè xanh 2022 do khoa khoa học và kĩ thuật máy tính tổ chức vào tháng 6/2022, diễn ra ở đâu
mùa hè xanh diễn ra từ ngày 28/06 tới ngày 04/08 năm 2022, diễn ra ở đâu
mùa hè xanh diễn ra từ ngày 28/06 tới ngày 04/08 năm 2022, tổ chức ở đâu
hoạt động bách khoa league diễn ra lúc nào
bách khoa league
b1 cơ sở lý thường kiệt
tôi có thể đăng ký qua kênh nào
tôi có thể liên lạc qua kênh nào
hackathon năm 2021 diễn ra lúc nào
tôi có thể đăng ký qua đâu
tôi có thể đăng ký qua đường dẫn nào
liệt kê tất cả những hoạt động ngoại khoá của khoa KH&KT Máy tính có thể tham gia mà không cần trải qua phỏng vấn, sắp xếp theo quyền lợi từ cao đến thấp
Hoạt động ngoại khoá gần đây nhất của khoa KH&KT máy tính là gì
Liệt kê những cuộc thi học thuật của Khoa KH&KT Máy tính
cho mình hỏi thông tin về hoạt động ngoại khoá Mùa Hè Xanh 2023
bạn có thể cho mình biết có những hoạt động nào diễn ra vao năm 2021 được không
mình muốn biết thêm về hoạt động xuân tứ linh á
bạn có thể cho mình biết về thời gian bắt đầu của xuân tứ linh không
thế còn thời gian kết thúc thì sao
thời gian kết thúc của xuân tứ linh là khi nào thế
bạn có thể cho mình biết có những hoạt động nào diễn ra vao năm 2022 được không
mình muốn biết về thời gian bắt đầu của hoạt động dọn dẹp nghĩa trang liệt sĩ thành phố á
hoạt động diễn ra ở đâu thế bạn
khi tham gia hoạt động thì mình được những lợi ích gì á bạn
tham gia hoạt động dọn dẹp nghĩa trang liệt sĩ thành phố có được cộng điểm rèn luyện không bạn
bạn có thể cho mình biết cách để đăng ký tham gia hoạt động này không
thế bạn có thể cho mình biết hạn đăng kí tham gia là khi nào được không
cho mình hỏi hoạt động xuân tình nguyện có được tổ chức vào năm 2022 không
mình nhớ có hoạt động mùa hè xanh 2022
bạn có thể mô tả công việc trong hoạt động mùa hè xanh được không
Năm 2022, chiến dịch Mùa hè xanh được tổ chức từ ngày 25/6/2022 đến ngày 17/7/2022
đoàn khoa mt
phương pháp đăng ký tham gia hoạt động này là gì thế bạn
mình nhớ link tham gia này mới đúng chứ . https://bit.ly/DangKy_MHX2022
tham gia mùa hè xanh thì mình có được cộng ngày công tác xa hội không á bạn
cảm ơn bạn đã trả lời những câu hỏi của mình
bạn có thể cho mình biết về hoạt động hỗ trợ kì thi đánh giá năng lực 2021 được không
Bạn cho mình xin thông tin về người hoặc đơn vị tổ chức hoạt động này được không ?
hoạt động này diễn ra ở đâu á bạn
thế cơ sở dĩ an có tổ chức hoạt động này không
có những yêu cầu nào cần thực hiện để tham gia hoạt động này không ?
năm 2021
hỗ trợ kì thi đánh giá năng lực 2021
để tham gia hoạt động hỗ trợ kì thi đánh giá năng lực 2021 thì mình cần đăng ký ở đâu không
bạn có biết thời gian bắt đầu và thời gian kết thúc của hoạt động này không
hoạt động này kết thúc khi nào thế bạn
tham gia hoạt động này thì mình có được lợi ích gì á bạn
mình tham gia hoạt động này có được cộng ngày công tác xã hội không bạn?
cảm ơn bạn nha
bạn có thể cho mình biết về hoạt động hỗ trợ đội hình cờ lễ kỷ niệm 90 năm ngày thành lập đoàn được không ?
mình muốn biết về địa điểm tổ chức hoạt động này á
mình muốn hỏi về địa điểm tổ chức hoạt động này á
mình muốn biết về số lượng sinh viên tối đa có thể tham gia hoạt động này á bạn
khi tham gia hoạt động, mình cần mặc đồ như thế nào á
bạn biết đăng ký tham gia hoạt động này ở đâu không
bạn biết ai có thể giải đáp thắc mắc của mình về hoạt động này không
mình có thắc mắc về hoạt động này thì mình cần phải liên hệ ai vậy bạn
thời gian bắt đầu của hoạt động diễn ra khi nào á bạn
thời gian kết thúc của hoạt động xảy ra lúc nào vậy bạn
bạn có thể cho mình biết về ngày hội tập huấn lái xe và thay nhớt xe miễn phí được không ?
bạn có thể mô tả rõ hơn về hoạt động được không
bạn có thể mô tả công việc trong hoạt động được không
thời gian hoạt động diễn ra hoạt động là khi nào á bạn
hoạt động này có những tên gọi nào
bạn có biết gì về ngày thành lập đoàn tncs hồ chí minh
07:30:00 21-03-2021
công ty tnhh thương mại và dịch vụ phát tiến
ai tổ chức ngày hội tập huấn lái xe và thay nhớt xe miễn phí vậy bạn
bạn có biết gì về hội thảo trực tuyến chia sẻ về kinh nghiệm du học tại nước cộng hòa liên bang đức cho sinh viên việt nam không
bạn có biết gì về hội thảo trực tuyến chia sẻ kinh nghiệm du học tại nước chlb đức cho sinh viên việt nam không
nơi tổ chức hội thảo trực tuyến chia sẻ kinh nghiệm du học tại nước chlb đức cho sinh viên việt nam là nơi nào vậy bạn
tham gia hoạt động bằng cách nào á bạn
thời gian đăng ký diễn ra khi nào vậy bạn
thời gian hoạt động bắt đầu diễn ra khi nào vậy bạn
thời gian hoạt động kết thúc diễn ra khi nào vậy bạn
tham gia hoạt động thu được quyền lợi gì
hoạt động do khoa máy tính tổ chức đúng không
cho hỏi các hoạt động diễn ra vào 2020
cho hỏi các hoạt động do khoa cơ khí tổ chức
hoạt động định vị thương hiệu tổ chức ở đâu
xuân tình nguyện do ai tổ chức
vào khoảng tháng 6 năm 2022
cho mình hỏi các hoạt động tổ chức tại đồng tháp
các hoạt động tổ chức ở đồng nai là gì
các hoạt động nào liên lạc với bạn trần minh thuận để biết thêm thông tin
cho mình hỏi danh sách các hoạt động liên lạc với bạn trần minh thuận
tham gia hoạt động thi thử toeic liên lạc với bạn trần minh thuận phải không
cho mình hỏi liên hệ với ai để biết thêm thông tin hoạt động unitour
những hoạt động nào do khoa xây dựng tổ chức
cho hỏi danh sách các hoạt động do khoa ktxd tổ chức
những hoạt động tổ chức vào tháng 12 năm 2022
những hoạt động tổ chức vào tháng 1 năm 2022
khoa máy tính là người tổ chức hoạt động này
diễn ra vào tháng 6 năm 2022
cho hỏi các hoạt động tổ chức ở trường đại học bách khoa
cho mình hỏi các hoạt động tổ chức ở đại học bách khoa và do khoa máy tính tổ chức
diễn ra vào tháng 6 năm trước
cho mình xin danh sách các hoạt động tổ chức bởi khoa máy tính vào tháng 1 năm 2021
cho mình xin danh sách các hoạt động tổ chức bởi khoa máy tính
hội nghị khoa học công nghệ tổ chức ở đâu
xuân tình nguyện tham gia được bao nhiêu ngày công tác xã hội
vào năm 2020
sự kiện được tổ chức ở đâu
chiều ngày 20/11/2022 có sự kiện nào không?
chiều ngày 27/12/2022 có sự kiện nào không?
hội thảo trí tuệ nhân tạo do ai tổ chức
liên lạc với ai để biết thêm về hoạt động này
tham gia hoạt động có quyền lợi gì
được bao nhiêu điểm rèn luyện khi tham gia
có những yêu cầu gì khi tham gia hoạt động
hoạt động diễn ra vào năm 2022
cảm ơn nhiều
những hoạt động nào có trên 5 ngày công tác xã hội
mùa hè xanh 2023 được tổ chức ở đâu
mùa hè xanh 2022 được tổ chức ở đâu
mùa hè xanh được tổ chức ở đâu
mùa hè xanh 2022 được tổ chwucs ở đâu
gà
ừ 20/11/2021 đến 22/11/ 2022
tổng số hoạt động
thông tin về kms tour
tôi cần 5 ngày công tác xã hội
hoạt động được nhạn 5 ngày ctxh
liệt kê hoạt động
số ngày ctxh từng hoạt động
còn về ngày công tác xã hội
hỗ trợ công tác khoa
số hoạt động được 5 ngày công tác xã hội
hoạt động nào được 5 ngày công tác xã hội
số ngày công tác xã hội từng hoạt động
ngày công tác xã hội là gì
hỗ trợ hậu cần
jobfair
khi nào diễn ra
bạn cho mình hỏi các sự kiện diễn ra vào tháng 6 năm 2022 có được không
bạn cho mình hỏi các hoạt động diễn ra vào 06/2022 được không
thời gian diễn ra mùa hè xanh 2022 là khi nào
mình cũng không rõ nữa
ở đồng tháp á bạn
được tổ chức ở đồng tháp nha
ai tổ chức sự kiện này bạn nhỉ
cảm ơn bạn nhé
bạn cho mình hỏi mình sẽ nhận được mấy ngày công tác xã hội khi tham gia làm cộng tác viên hỗ trợ xử lí file âm thanh vậy ạ
Cho mình hỏi làm cách nào để đăng ký xuân tình nguyện vậy ad
cái này mình không biết luôn á
cái này mình cũng không rõ luôn
ở văn phòng đoàn thì phải á
okeee bạn
mình không rõ lắm á
tầm tháng 12 năm 2017 ấy
cho mình hỏi mùa hè xanh năm 2022 diễn ra ở đâu
cái đó mình cũng chưa rõ nữa
vào tháng 6 năm 2022 á
thời gian diễn ra sự kiện này là khi nào vậy
bạn cho mình các hoạt động diễn ra vào tháng 8 năm 2022 đi
thời gian diễn ra sự kiện cộng tác viên hỗ trợ hậu cần đại hội đoàn trường ngày 16/8/2022 là khi nào á
cho mình hỏi thời gian diễn ra hoạt động cộng tác viên hỗ trợ
công việc là hỗ trợ ngày hội kỹ thuật á
ở toà A3 cơ sở 1 nha
cảm ơn admin nhé
mình sẽ làm gì khi tham gia hỗ trợ sự kiện hỗ trợ hậu cần giải bóng đá tứ hùng ngày 26/8/2022
tham gia cái này được mấy ngày công tác xã hội á
chiều nay có những sự kiện nào vậy bạn
chiều 20/11/2022 có sự kiện nào không?
ngày 20/11/2022 có sự kiện nào không?
ngày 20/11/2022 có sự kiện nào không
ngày 20/11/2019 có sự kiện nào không
tháng 8 năm 2020 có sự kiện nào không
tháng 8 năm 2022 có sự kiện nào không
bạn cho mình các hoạt động cộng tác viên hỗ trợ nhé
mình không rõ nữa
mình không rõ luôn
khoa máy tính á bạn
được tổ chức bởi khoa máy tính á
cảm ơn bạn đã giúp mình
bạn cho mình tất cả các hoạt động có tên là cộng tác viên hỗ trợ nha
chiều mai có những sự kiện nào vậy
chiều ngày 20 tháng 11 năm 2022 có những sự kiện nào vậy
có tôi các sự kiện được 5 ngày công tác xã hội
các hoạt động nào được 5 điểm rèn luyện vào ngày 20/11/2022
các hoạt động nào được 1 ngày công tác xã hội vào ngày 20/11/2022
các hoạt động nào được 0.5 ngày công tác xã hội vào ngày 20/11/2019
cảm ơn bạn nhiều nhé
thời gian diễn ra hoạt động hỗ trợ bê bàn ghế?
cuối tuần này có hoạt động nào được 5 ngày công tác xã hội không
cho mình hỏi về thời gian diễn ra của cse cup
tham gia thi đấu liên minh á
tên của sự kiện này là gì
cảm ơn bạn nhiều nha
mùa hè xanh 2022 của khoa máy tính diễn ra ở đâu
vào tháng 06-2022 nha
Chiều nay có sự kiện nào không á ơi
Chiều ngày 20 tháng 11/2022 có sự kiện nào không vậy
Chiều 20/11/2022 có hoạt động nào không ad
Cảm ơn ad nha
Cho mình hỏi sự kiện hỗ trợ làm hồ sơ khi nào kết thúc á
Tên của hoạt động này là gì thế ad
Có yêu cầu gì không nhỉ
Mình được mấy ngày công tác xã hội khi tham gia hoạt động này
Mình nên liên hệ ai để đăng ký vậy ád
Cho mình hỏi câu cuối nhé. Sự kiện này diễn ra ở đâu á
Cảm ơn ad nhiều nhé. Iu iu
Cho mình hỏi sự kiện hỗ trợ làm hồ sơ khi nào mở đăng ký
Cho mình hỏi sự kiện gnh tech tour khi nào mở đăng ký
cảm ơn ad nhiều nhé
Bạn tên gì
Gà vậy
Gàaaaaaa
Cho mình hỏi sự kiện nào được nhiều công tác xã hội nhất
Nhưng mà cái nào cho nhiều công tác xã hội nhất?
Tui muốn hoạt động có nhiều công tác xã hội nhất
Cho tui số công tác xã hội nữa
xin chào bạn
tháng 10 năm 2021 có sự kiện nào không
ai tổ chức sự kiện chào năm học mới vậy
sự kiện đó diễn ra ở đâu thế ad
còn sự kiện an sinh đợt 3 diễn ra ở đâu á
còn sự kiện khảo sát sinh viên khoá 2021 thì sao
diễn ra ở đâu á
xin chào ad
tuần này có sự kiện nào không
mùa hè xanh năm 2022 ở dồng tháp đúng không bạn
đi xây dựng đường xá đồ đó
công việc là đi xây dựng đường xá á
Mùa hà xanh ở đâu
Mùa hè canh diễn ra chỗ nào
Mùa hè xanh á
Vào 06-2022 nha
Khoa máy tính nha
hỗ trợ ctxh ở đâu
không biết luôn
khoa điện điện tử nha
Mình muốn biết thông tin của mùa hè xanh năm 2022 do ai tổ chức á
Đi làm đường tình nguyện
Công việc là đi làm tình nguyện á
Địa điểm của hoạt động này là ở đâu vậy
Hoạt động này có phải do mùa hè xanh khoa khoa học và kỹ thuật máy tính tổ chức không vậy
Hoạt động này bắt đầu lúc nào á
Hoạt động này kết thúc lúc nào á
Cách thức để đăng kí hoạt động là gì
Thời gian bắt đầu đăng kí là lúc nào vậy
Lợi ích khi tham gia cái này là gì
Cảm ơn bạn đã hỗ trợ
Hello bạn
Bạn có biết CSE job fair không á
Năm 2022
Ở Trường Đại học bách khoa cơ sở dĩ an á
Bạn cho mình hỏi cse job fair năm 2022 do ai tổ chức
Là ngày hội việc làm á
Cái này được tổ chức ở đâu
Làm sao để đăng kí hoạt động này
Thời gian chính xác diễn ra hoạt động là khi nào
Sự kiện này do khoa máy tính tổ chức hả?
Oke bạn
Mình muốn hỏi về ban tổ chức của mùa hè xanh 2022
Những hoạt động sẽ xảy ra trong ngày hội việc làm JobFair ?
Vào tháng 3 năm nay ạ
ủa bữa tui mới đi lun á fen
ngu ngok zị chòy
huhu
tôi pùn qó
nín
người iu tui nhắn ó
Cho tôi thông tin về hoạt động mùa hè xanh năm nay được không
Đừng xin lỗi nữa
Tạm biệt bạn nha
Biết rồi
nói quài
Giúp tôi tìm kiếm hoạt động phù hợp với số ngày công tác xã hội là 1 ngày
Cho tôi biết hoạt động gần nhất đi ạ
cho tôi thêm thông tin về kms tour
Vậy thì thông tin về hoạt động hỗ trợ đoàn khoa ktxd
Những sự kiện mới ?
sao có những sự kiện cũ kìa
vẫn cu
vẫn cũ
q3awrezsdtxcfgvyjbhukinm
hi
hj
Cho mình địa điểm diễn ra mùa hè xanh năm 2022
Mình cũng không rõ lắm
ai là người tổ chức hoạt động anyf
mùa hè xanh 2022 diễn ra ở đâu
đi xây dựng đường ở đồng tháp á
mình sẽ nhận được gì khi tham gia sự kiện này
mùa hè xanh 2022 do ai tổ chức
mùa hè xanh năm 2022 được tổ chức ở đâu
mình không biết nữa
cái này thì mình chịu luôn bạn ơi
ở đồng tháp thì phải á
ở đồng tháp á
cho mình hỏi các hoạt động được từ 3 đến 5 ngày công tác xã hội
cho mình hỏi các hoạt động được từ 3-5 ngày công tác xã hội
Lợi ích khi tham gia CSE Job Fair
Gặp gõ doanh nghiệp á
Làm sao để đăng kí sự kiện này
Thời gian đăng kí là khi nào vậy
Thời gian diễn ra sự kiện
Thời gian diễn ra sự kiện này là khi nào
Thời gian diễn ra sự kiện này
Khi nào sự kiện này diễn ra
Tên của sự kiện này là gì
Xin thông tin liên hệ của hoạt độn
Xin thông tin liên hệ của CSE Job fair
Gặp gỡ doanh nghiệp
Ai tổ chức cái này
Sự kiện này do ai tổ chức
xuân tình nguyện 2022 tổ chức ở đâu
hoạt động tổ chức vào 2022
tham gia hoạt động được những quyền lợi gì
mô tả công việc của hoạt động là gì
thời gian diễn ra hoạt động là khi nào
đối tượng được tham gia hoạt động gồm những ai
liên hệ ai để biết thông tin về hoạt động
cho mình hỏi toàn bộ thông tin hoạt động dọn dẹp nghĩa trang liệt sĩ
Lợi ích khi tham gia mùa hè xanh năm 2022
Năm 2021 á
Lợi ích khi tham gia cse connection
Năm 2021
Lợi ích khi tham gia cái này
Lợi ích khi tham gia xuân tình nguyện 2022
Mùa hè xanh 2022 tổ chúc ở đâu
Tháng 6/2022
thi thử toeic do ai tổ chức
khoa máy tính là đơn vị tổ chức
Mùa hè xanh năm 2022 tổ chức ở đâu
Mùa hè xanh 2022 tổ chức ở đâu
Mùa hè xanh năm 2022 diễn ra ở đâu
chiến dịch mùa hè xanh tổ chức ở đâu
hội trại tổ chức ở đồng nai đúng không
hoạt động diễn ra vào 06/2022
làm sao để liên lạc với người tổ chức hoạt động
hội trại được tổ chức ở đồng nai phải không
hội trại cse do ai tổ chức
hội trại cse diễn ra ở đâu
mô tả công việc của hội trại cse là gì
hỗ trợ vận chuyển đồ có những quyền lợi gì
hỗ trợ vận chuyển đồ có mô tả công việc như thế nào
ceac do ai tổ chức
olympic được tổ chức ở đâu
ngày hội hiến máu đăng ký như thế nào
mùa hè xanh 2022 do khoa máy tính tổ chức đúng không
có những hoạt động nào diễn ra ngày 01-12-2022
cho mình hỏi sự kiện hỗ trợ bê bàn ghế tổ chức ở đâu
nó sẽ bắt đầu lúc mấy giờ vậy
lợi ích mình có được sau sự kiện này là gì
mình được bao nhiêu ngày công tác xã hội khi tham gia sự kiên này
cho mình hỏi 01-12-2022 có những hoạt động nào
mình sẽ được gì khi tham gia nó
sự kiện này mình sẽ liên hệ ai vậy ad
sự kiện này cần bao nhiêu người tham gia thế
có ràng buộc gì khi tham gia không nhỉ
AD ĐẸP TRAI QUÁ
bạn biết mình là ai không thế
cho mình khi nào bắt đầu vận chuyển đồ về cơ sở 2 vậy
mình không nắm rõ nữa
sự kiện này xảy ra ở đâu
lợi ích khi tham gia sự kiện là gì
mình liên hệ ai nhỉ
cho mình hỏi sự kiện nào của khoa máy tính sẽ đi làm đường ở đồng tháp vậy ad
khi nào sẽ diễn ra phỏng vẫn chiến dịch xuân tình nguyện vậy
mình không rõ lắm
sự kiện này có yêu cầu gì không ad
mình có thể đăng ký sự kiện này ở đâu
tối đa được bao nhiêu người tham gia vậy ạ
hy vọng mình sẽ đậu sự kiện này
lợi ích khi tham gia sự kiện này
thời gian diễn ra sự kiện
cảm ơn bạn nhé. chúc ad nhiều sức khoẻ
chiến dịch xuân tình nguyện được tổ chức khi nào
hội trại cse tham gia được bao nhiêu điểm rèn luyện
mùa hè xanh 2022 diễn ra ở đồng tháp đúng không
cho mình hỏi danh sách các hoạt động tổ chức ở đồng tháp
mùa hè xanh 2020 tổ chức ở đồng tháp phải không
cho mình hỏi hỗ trợ hội nghị sinh viên diễn ra khi nào
bạn cho mình biết sự kiện mùa hè xanh đi
tất cả các sự kiện ngày 20-102
cho tôi các sự kiện ngày 22-2001-2002
cho tui các sự kiện 10 ngày nữa
cho tui các sự kiện chả biết ngày
diễn ra ở đồng tháp
sự kiện mùa hè xanh 2022 do ai tổ chức
mình muốn hỏi thời gian bắt đầu diễn ra màu hè xanh 2022 của khoa khoa học và kỹ thuật máy tính
cho mình hỏi nơi diễn ra của màu hè xanh 2022
diễn ra vào tháng 06-2022 á
thời gian bắt đầu sự kiện là khi nào vậy
sự kiện này có yêu cầu gì không vậy ad
khi tham gia sự kiện này mình sẽ nhận được lợi ích gì vậy
cảm ơn ad nhiều nha
cho mình hỏi thời gian của mùa hè xanh 2022 do khoa máy tính tổ chức
mùa hè xanh 2022 của khoa máy tính diễn ra khi nào vậy ad
theo mình nhớ là đi làm đường á
đi xây dựng các công trình đường xá á
ai tổ chức sự kiện này vậy
sự kiện này tên là gì vậy ad
sự kiện trên tên là gì vậy ad
cảm ơn ad rất nhiều
cho mình hỏi lợi ích khi tham gia dọn dẹp khu tự học
cho mình hỏi chiến dịch xuân tình nguyện tổ chức khi nào
vào tháng 06/2022
hoạt động này diễn ra vào khoảng thời gian nào
hoạt động này kết thúc khi nào
thời gian đăng ký hoạt động này là khi nào
làm sao để đăng ký tham gia chiến dịch mùa hè xanh 2022
thời gian diễn ra mùa hè xanh là 6-2022 phải không
Mùa hè xanh 2022 do ai tổ chức
Năm 2022 á má
Làm tình nghuyện
Sự kiện này được diễn ra ở đâu
Lợi ích khi tham gia chiến dịch này là gì
Liên hệ ai để có thêm thông tin cho sự kiện này
Mô tả công việc của sự kiện này là gì
Số người dự kiến tham gia cái này là báo nhiêu
Thời gian đăng kí là khi nào
Cách thức đăng kí sự kiện này
Cho hỏi ai tổ chức cse job fair vậy
Ngày hội việc làm
Lợi ích khi tham gia hoạt động này là gì
Làm sao để đăng kí tham gia vậy
Sự kiện này diễn ra ở đâu
làm Hoạt động này được khoa khoa học và kỹ thuật máy tính trường đại học bách khoa tổ chức đúng không vậy
Lợi ích của cse connection 2022
Lợi ích của cse connection
2021
Lợi ích khi tham gia cse job fair 2022
Lợi ích khi tham gia cse connection 2022
Lợi ích khi tham gia hậu duệ pascal
Lợi ích khi tham gia mùa hè xanh 2022
Lợi ích khi tham gia cse job fair
bao nhiêu người được tham gia hoạt động này
cho mình hỏi các hoạt động tổ chức vào năm 2020
hoạt động sắp xếp kho tham gia được 3 ngày công tác xã hội phải không
cho hỏi các hoạt động tổ chức vào năm 2019 và được trên 2 ngày công tác xã hội
cho hỏi các hoạt động tổ chức vào năm 2019 và được trên 1 ngày công tác xã hội
cho hỏi các hoạt động tổ chức vào năm 2022 và được trên 1 ngày công tác xã hội
cho hỏi các hoạt động tổ chức vào năm 2022 và được trên 3 ngày công tác xã hội
tham dự triển lãm giáo dục được bao nhiêu ngày công tác xã hội
cộng tác viên innovation làm sao để đăng ký tham gia
tên của hoạt động là gì
cho hỏi các hoạt động có hạn đăng ký từ tháng trước
cho hỏi các hoạt động diễn ra từ tháng trước
cho hỏi các hoạt động diễn ra từ tháng 1 năm 2023
thi thử toeic tổ chức ở đâu
danh sách các hoạt động có tên là thi thử là gì
tham gia mùa hè xanh 2022 sẽ nhận được 5 ngày công tác xã hội phỉa không
xuân tình nguyện diễn ra khi nào
hoạt động tổ chức vào 06/2022
hoạt động mùa hè xanh tổ chức ở đâu
hoạt động diễn ra vào 2019
hoạt động tổ chức vào 2019
liên lạc với ai để biết về hoạt động
hoạt động tổ chức vào thời gian nào
tham gia hoạt động được bao nhiêu drl
sự kiện diễn ra ở hội trường bkb 6 h6 cơ sở 2
cho mình hỏi các sự kiện diễn ra vào ngày 13-03-2023
minh không rõ
diễn ra vào ngày 10-03-2023 á
Có lợi ích gì khi tham gia mùa hè xanh 2022 vậy
Lợi ích của hội trại cse connection
Được mấy ngày công tác xã hội nếu tham gia mùa hè xanh
yêu cầu công việc khi tham gia hoạt động là gì
có bao nhiêu người tham gia hoạt động này
làm thế nào để đăng ký tham gia hoạt động
hoạt động này do ai tổ chức
Mùa hè xanh được tổ chức ở đâu
Hội trại CSE connection tổ chức ở đâu
Hội trại CSE connection 2022 tổ chức ở đâu
AI tổ chức CSE jobfair
Ai tổ chức Mùa hè xanh năm 2022
cho mình hỏi sự kiện vận chuyển đồ về cơ sở 2 được 5 điểm rèn luyện đúng không
chiến dịch xuân tình nguyện do ai tổ chức
hoạt động được tổ chức vào 2022
cho mình hỏi chiến dịch xuân tình nguyện tổ chức ở đâu
action-decider-server.agreeableplant-5236956c.southeastasia.azurecontainerapps.i
cho mình hỏi mô tả công việc của sự kiện do khoa khoa học và máy tính tổ chức được 5 điểm rèn luyện
cho mình hỏi về mô tả công việc của sự kiện mùa hè xanh 2022
vào tháng 06-2022 á
đi mùa hè xanh 2022 của khoa máy tính thì mình sẽ nhận được gì
cảm ơn
cho tui biết lợi ích khi tham gia hoạt động mùa hè xanh 2022 được 5 điểm rèn luyện
cho tui biết lợi ích khi tham gia mùa hè xanh 2022
cho tui hỏi sự kiện được tổ chức bởi khoa khoa học và kỹ thuật máy tính
cho tui hỏi sự kiện được tổ chức bởi khoa máy tính
cho tui hỏi về sự kiện hỗ trợ vận chuyển đồ
cho tui hỏi ai là người tổ chức sự kiện hỗ trợ vận chuyển đồ
hoạt động hỗ trợ dọn dẹp diễn ra khi nào
hoạt động mùa hè xanh diễn ra khi nào
kệ m
sự kiện cse connection khi nào kết thúc
những hoạt động nào có trên 3 ngày ctxh
hoạt động career talk do ai tổ chức
hội trại cse connection diễn ra khi nào
sự kiện tổ chức ở đồng tháp đúng không
Thời gian diễn ra hội trại cse
cho mình hỏi danh sách các hoạt động do khoa máy tính tổ chức vào năm 2022
tham gia hoạt động bê bàn ghế được bao nhiêu ngày công tác xã hội
tham gia hoạt động bê bàn ghế được 3 ngày công tác xã hội phải không
không rõ
hoạt động tổ chức ở đồng tháp
vào 6/2022
sự kiện diễn ra khi nào
Các lợi ích của mùa hè xanh
Các lợi ích của mùa hè xanh 2022
hoạt động diễn ra vào 6/2022
cho mình hỏi xuân tình nguyện có mô tả công việc là gì
hoạt động nào tổ chức vào 10/2022
cho mình hỏi tên của hoạt động tổ chức vào 10/2022
cho tui hỏi mùa hè xanh 2022 diễn ra ở đâu
vào tháng 6-2022 s
khoa khoa học và kỹ thuật máy tính
cho tui biết nơi diễn ra mùa hè xanh
xây dựng đường xá á
cho mình hỏi mùa hè xanh diễn ra ở đâu
tổ chức vào 06-2022
thời gian diễn ra sự kiện là khi nào
sự kiện kết thúc khi nào
mình sẽ làm gì khi tham gia sự kiện này
làm sao để đăng ký sự kiện này vậy ad
thời gian kết thúc đăng ký của sự kiện
bạn tên gì
ohyear
cho tui mô tả công việc của sự kiện được 5 ngày ctxh
cái này mình cũng không rõ
cho mình hỏi cách đăng ký sự kiện diễn ra vào 08-11-2022
cho mình hỏi các sự kiện diễn ra 7-11-2022
cho mình hỏi các sự kiện diễn ra 08-11-2022
cho mình hỏi các sự kiện diễn ra 11-2022
thời gian diễn ra ngày hội hiến máu tình nguyện lần 2
ở quận 10 á
sự kiện do khoa máy tính tổ chức ngày 23-12-2022 có tên là gì nhỉ
các sự kiện do khoa máy tính tổ chức vào tháng 06-2022 được 5 điểm rèn luyện
cho mình tên các sự kiện do khoa máy tính tổ chức vào tháng 06-2022 được 5 điểm rèn luyện
cho mình hỏi các sự kiện tuyển cộng tác viên hỗ trợ
cho mình hỏi sự kiện mùa hè xanh 2022 do khoa máy tính tổ chức đúng không
diễn ra ở đồng tháp á
cho mình hỏi thời gian đăng ký của vận chuyển đồ về cơ sở 2
thời gian bắt đầu của sự kiện này
có yêu cầu gì không bạn
cho mình hỏi các sự kiện chỉ dành cho sinh viên khoa máy tính
mình sẽ được mấy ngày công tác xã hội khi tham gia sự kiện này
cho mình hỏi làm cách nào để đăng ký xuân tình nguyện
cái này mình không rõ á bạn
cái này mihf cũng không rõ luôn
ở h6 cở sở 2 á bạn
cái này không biết
xuân tình nguyện khi tham gia được quyền lợi gì
Năm 2022\
Cho hỏi mấy giờ rồi
Hội trại cse connection có lợi ích gì
Đi giao lưu với mn
Cái này do ai tổ chức
Cái này diễn ra ở đâu
Làm sao để đăng kí cái này
Thời gian bắt đầu đăng kí
Yêu cầu khi tham gia cái này là gì
Bai
Tạm biệt
Mình muốn hỏi về Mùa hè xanh 2022
Đi làm tình nguyện
Ai là người tổ chức hoạt động này
Hoạt động diễn ra ở đâu á
Có lợi ích gì khi tham gia cái này
Vậy còn quyền lợi khác thì sao
Biết rồi vậy khi nào cái này diễn ra
Thời gian kết thúc là khi nào
Làm sao để đăng kí nó á
các hoạt động nào có trên 5drl
hội nghị sinh viên tổ chức ở đâu
hội nghị công nghệ do ai tổ chức
sự kiện họp mặt do ai tổ chức
hội nghị do ai tổ chức
tên hoạt động là hội nghị họp mặt
cse olympic diễn ra khi nào
cse olympic do ai tổ chức?
hoạt động hội trại do ai tổ chức
hoạt động hội trại diễn ra khi nào
mô tả công việc của hoạt động hội trại là gì
những hoạt động nào do khoa máy tính tổ chức
hoạt động hỗ trợ vận chuyển được mấy ngày ctxh
cse connection đăng ký tham gia bằng cách nào
mình muốn hỏi thời gian kết thúc màu hè xanh 2022 của khoa khoa học và kỹ thuật máy tính
hội trại cse diễn ra ở đồng nai đúng không
diễn ra vào tháng 10/2022
cho mình xin danh sách hoạt động tổ chức vào năm trước
hoạt động chiêu mô thành viên khoa cơ khi diễn ra khi nào
hoạt động diễn ra vào tháng 10/2022 đúng không
hoạt động này diễn ra vào tháng 10/2022 đúng không
hoạt động này diễn ra ở sân bóng trường đại học thể dục đúng không
tham gia hoạt động được bao nhiêu điểm rèn luyện
tham gia mùa hè xanh 2022 được bao nhiêu ngày công tác xã hội
tham gia hoạt động có phải được 2 ngày ctxh không
tổ chức vào tháng 6/2022
hoạt động này bắt đầu vào tháng 6/2022 đúng không
tham gia hoạt động được 10 điểm rèn luyện đúng không
hội trại cse tham gia được bao nhiêu ngày công tác xã hội
cho hỏi danh sách hoạt động diễn ra vào năm trước
CSE Job fair 2022 do ai tổ chức
Có lợi ích gì khi tham gia hoạt động này
cho mình hỏi mô tả công việc của cse olympic
cho mình hỏi ai tổ chức cse olympic
hoạt động này diễn ra khi nào
hoạt động diễn ra ở sân liên hợp ký túc xá khu a
nơi diễn ra sự kiện mùa hè xanh
vào tháng 06-2022
sự kiện này do khoa máy tính tổ chức
mô tả công việc của mùa hè xanh
do khoa khoa học và kỹ thuật máy tính tổ chức
thời gian kết thúc hoat động này
khi nào kết thúc sự kiện màu hè xanh của khoa máy tính
sự kiện mùa hè xanh của khoa điện diễn ra ở đâu vậy
sự kiện hỗ trợ đoàn khoa kỹ thuật xây dựng diễn ra ở cơ sở nào?
ngày 04-01-2023 á
vào tháng 01-2023
thời gian bắt đầu của hoạt động là lúc nào?
khi nào hoạt động kết thúc
thời gian bắt đầu đăng ký là bao giờ
được mấy ngày công tác xã hội vật
sự kiện này được mấy ngày công tác xã hội
cho mình tất cả các sự kiện diễn ra vào ngày mai
bạn khoả không
cho mình hỏi về hoạt động cộng tác viên hỗ trợ được mấy ngày công tác xã hội
ngày 24-12-2022 nha
diễn ra voà ngày 24-12-2022 nha ad
ngày 22-11-2022 có những sự kiện nào
có những sự kiện nào diễn ra vào ngày 22-11-2022
lợi ích mình sẽ nhận được khi tham gia sự kiện ngày sinh viên sáng tạo khu vực miền nam
thời gian diễn ra sự kiện này
liên hệ ai để đăng ký vậy ad
sự kiện này diễn ra ở đâu
mô tả công việc của sự kiện này
sự kiện sẽ bắt đầu lúc nào
cảm ơn bạn nhiều nhá
lêu lêu
cho mình hỏi về lợi ích khi tham gia sự kiện uprace
ê mày
mày là ai
bạn là ai
thông tin mùa hè xanh 2022
cảm ơm
chào tạm biệt
tuyển quân mùa hè xanh 2022
tháng 6-2022 có những hoạt động nào
kms tour
thời gian diễn ra kms tour
thowif gian keets thucs
thowif gian keets thucs cuar hoatj ddoongj nayf
thời gian kết thúc hoạt động
tạm biệt ad
ngày 31-12-2019 có những sự kiện nào
cảm ơ
chiến dịch mùa hè xanh được tổ chức ở đâu
Hoạt động diễn ra vào 06/2022
Hoạt động mùa hè xanh diễn ra ở đâu
hoạt động mùa hè xanh 2022 do ai tổ chức
diễn ra vào 06/2022
cho mình hỏi toàn bộ thông tin hoạt động dọn dẹp nghĩa trang liệt si
cho mình hỏi mô tả công việc hoạt động dọn dẹp nghĩa trang liệt sĩ
số lượng người tham gia hoạt động là bao nhiêu
CSE job fair 2022 do ai tổ chức
Mùa hè xanh năm 2022 do ai tổ chức
xin chào admin
cho mình hỏi ai tổ chức mùa hè xanh năm 2022
chào bạn bạn có thể có mình hỏi một xíu được không
cho tui hỏi mùa hè xanh 2022 được tổ chức ở đâu
vào tháng 6-2022
cho mình cse connection khi nào mở đăng ký
cách thức đăng ký của sự kiện này
cho mình hỏi cách thức đăng ký của sự kiện cse connection
vào 21-09-2019
cho mình hỏi nơi diễn ra sự kiện cse connection
vào 21-09-2021
thời gian kết thúc sự kiện là khi nào
những lợi ích khi tham gia hậu duệ pascal 2021 là gì vậy
thời gian đăng ký sự kiện này là khi nào
cảm ơn ad nhiều. chúc ad sức khoẻ
đố bạn mình tên gì
cho mình hỏi nơi diễn ra mùa hè xanh 2022
mình khôgn rõ về công việc lắm
lợi ích mình có được khi tham gia sự kiện này là gì
mình sẽ làm gì khi. tham gia sự kiện này
wow thật tuyệt vời
không biết hoạt động hiến máu tình nguyện có những quyền lợi gì
thời hạn đăng ký tham gia là bao nhiêu
cho hỏi tất cả hoạt động diễn ra tại toà h6
tham gia hoạt động hỗ trợ dọn dẹp khu tự học được quyền lợi gì
cho mình hỏi danh sách các hoạt động tổ chức tại trường đại học bách khoa
hoạt động talkshow athena tổ chức khi nào
có bao nhiêu người tham gia hoạt động
có yêu cầu gì khi tham gia hoạt động không
hạn đăng ký tham gia hoạt động là gì
quyền lợi khi tham gia là gì
cho mình biết các hoạt động được tổ chức bởi khoa máy tính
cuộc thi ceac có mô tả công việc như nào
được tổ chức vào 2022
quyền lợi từ hoạt động là gì
địa điểm diễn ra hoạt động ở đau
thời gian đăng ký hoạt động là bao giờ
Mùa hè xanh do ai tổ chức
CSE jobfair do ai tổ chức
cảm
làm sao để liên hệ với người tổ chức hoạt động
tên hoạt động là hỗi trợ nhận báo cáo đồ án"""

from proto.intent_slot_service_pb2_grpc import ISServiceStub
from proto.intent_slot_service_pb2 import IntentSlotRecognizeRequest
import grpc
import sys
import json
from locust import task, events, constant
import inspect

messages = MESSAGE.split('\n')

NUM_OF_USERS = 200
NUM_OF_MESSAGES = 1000000
MIN_WAIT_TIME = 1
MAX_WAIT_TIME = 10
SLEEP_TIME = 1

def stopwatch(func):
    """To be updated"""

    def wrapper(*args, **kwargs):
        """To be updated"""
        # get task's function name
        previous_frame = inspect.currentframe().f_back
        _, _, task_name, _, _ = inspect.getframeinfo(previous_frame)

        start = time.time()
        result = None
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            total = int((time.time() - start) * 1000)
            events.request_failure.fire(request_type="TYPE",
                                        name=task_name,
                                        response_time=total,
                                        response_length=0,
                                        exception=e)
        else:
            total = int((time.time() - start) * 1000)
            events.request_success.fire(request_type="TYPE",
                                        name=task_name,
                                        response_time=total,
                                        response_length=0)
        return result

    return wrapper

class PerformanceTest(HttpUser):
    wait_time = between(MIN_WAIT_TIME, MAX_WAIT_TIME)
    credentials = grpc.ssl_channel_credentials()
    channel = grpc.secure_channel('intent-slot-server-1.agreeableplant-5236956c.southeastasia.azurecontainerapps.io', credentials)
    stub = ISServiceStub(channel)

    def on_start(self):
        self.client.verify = False

    @task
    # @stopwatch
    def get_intent_from_message_from_webhook_official(self):
        # user_id = random.randint(0, NUM_OF_USERS - 1)
        # mid = random.randint(0, NUM_OF_MESSAGES - 1)
        try:
            self.client.get('/')
            message = random.choice(messages)

            res = self.stub.IntentSlotRecognize(IntentSlotRecognizeRequest(message=message))
            data = json.loads(res.message)
            print(data)

            # self.client.get("/v2/crawl-data-from-facebook", 
            #                 json={
            #     "object":"page",
            #     "entry":[
            #         {
            #         "messaging":[
            #             {
            #                 "sender":{
            #                     "id": str(user_id)
            #                 },
            #                 "message":{
            #                     "text": message,
            #                     "mid": str(mid)
            #                 }
            #             }
            #         ]
            #         }
            #     ]
            # }
            # )
            time.sleep(SLEEP_TIME)

        except (KeyboardInterrupt, SystemExit):
            sys.exit(0)