# HÀM TRONG PYTHON (FUNCTIONS)
# Tài liệu: Functions - https://codewithmosh.com/p/python-programming-course-beginners

# ========== 1. ĐỊNH NGHĨA HÀM (DEFINING FUNCTIONS) ==========
"""
Hàm là một khối lệnh thực hiện một tác vụ cụ thể và có thể được tái sử dụng.
Cú pháp:
def tên_hàm(tham_số1, tham_số2, ...):
    # Thân hàm
    return giá_trị_trả_về  # Không bắt buộc
"""
print("===== 1. ĐỊNH NGHĨA HÀM (DEFINING FUNCTIONS) =====")


# Hàm đơn giản không có tham số và không trả về giá trị
def chao_hoi():
    print("Xin chào!")


# Gọi hàm
chao_hoi()  # Kết quả: Xin chào!


# Hàm có trả về giá trị
def cong(a, b):
    return a + b


ket_qua = cong(5, 3)
print(f"5 + 3 = {ket_qua}")  # Kết quả: 5 + 3 = 8


# Hàm có nhiều lệnh return
def kiem_tra_so_am(x):
    if x < 0:
        return "Số âm"
    elif x == 0:
        return "Số không"
    else:
        return "Số dương"


print(f"kiem_tra_so_am(-5): {kiem_tra_so_am(-5)}")  # Kết quả: Số âm
print(f"kiem_tra_so_am(0): {kiem_tra_so_am(0)}")  # Kết quả: Số không
print(f"kiem_tra_so_am(5): {kiem_tra_so_am(5)}")  # Kết quả: Số dương


# Hàm trả về nhiều giá trị
def tinh_toan(a, b):
    tong = a + b
    hieu = a - b
    tich = a * b
    thuong = a / b if b != 0 else "Không thể chia cho 0"
    return tong, hieu, tich, thuong


# Nhận các giá trị trả về
t, h, tich, th = tinh_toan(10, 5)
print(f"10 + 5 = {t}")  # Kết quả: 10 + 5 = 15
print(f"10 - 5 = {h}")  # Kết quả: 10 - 5 = 5
print(f"10 * 5 = {tich}")  # Kết quả: 10 * 5 = 50
print(f"10 / 5 = {th}")  # Kết quả: 10 / 5 = 2.0


# ========== 2. THAM SỐ (ARGUMENTS) ==========
"""
Tham số (parameter): biến được định nghĩa trong khai báo hàm
Đối số (argument): giá trị được truyền vào khi gọi hàm
"""
print("\n===== 2. THAM SỐ (ARGUMENTS) =====")


# Tham số bắt buộc (required parameters)
def chao_hoi_ten(ten):
    print(f"Xin chào {ten}!")


chao_hoi_ten("Nguyễn Văn A")  # Kết quả: Xin chào Nguyễn Văn A!


# Tham số mặc định (default parameters)
def chao_hoi_ten_tuoi(ten, tuoi=18):
    print(f"Xin chào {ten}! Bạn {tuoi} tuổi.")


chao_hoi_ten_tuoi("Nguyễn Văn A")  # Kết quả: Xin chào Nguyễn Văn A! Bạn 18 tuổi.
chao_hoi_ten_tuoi("Nguyễn Văn B", 25)  # Kết quả: Xin chào Nguyễn Văn B! Bạn 25 tuổi.


# Truyền tham số theo thứ tự (positional arguments)
def hien_thi_thong_tin(ten, tuoi, dia_chi):
    print(f"Tên: {ten}, Tuổi: {tuoi}, Địa chỉ: {dia_chi}")


hien_thi_thong_tin("Nguyễn Văn A", 25, "Hà Nội")  # Truyền theo thứ tự

# Truyền tham số theo tên (keyword arguments)
hien_thi_thong_tin(tuoi=30, ten="Trần Thị B", dia_chi="TP.HCM")  # Truyền theo tên


# ========== 3. CÁC LOẠI HÀM (TYPES OF FUNCTIONS) ==========
"""
Python có nhiều loại hàm khác nhau:
1. Hàm có tham số và có giá trị trả về
2. Hàm có tham số và không có giá trị trả về
3. Hàm không có tham số và có giá trị trả về
4. Hàm không có tham số và không có giá trị trả về
5. Hàm lambda (hàm ẩn danh)
6. Hàm đệ quy
7. Hàm nội trang (built-in functions)
"""
print("\n===== 3. CÁC LOẠI HÀM (TYPES OF FUNCTIONS) =====")


# 1. Hàm có tham số và có giá trị trả về
def tinh_dien_tich_hinh_chu_nhat(dai, rong):
    return dai * rong


dt = tinh_dien_tich_hinh_chu_nhat(5, 3)
print(f"Diện tích hình chữ nhật 5x3 = {dt}")  # Kết quả: 15


# 2. Hàm có tham số và không có giá trị trả về
def in_thong_tin_sinh_vien(ten, tuoi):
    print(f"Sinh viên: {ten}, {tuoi} tuổi")


in_thong_tin_sinh_vien("Lê Văn C", 22)  # Kết quả: Sinh viên: Lê Văn C, 22 tuổi


# 3. Hàm không có tham số và có giá trị trả về
def lay_ngay_hien_tai():
    import datetime

    return datetime.datetime.now().strftime("%d/%m/%Y")


ngay_hien_tai = lay_ngay_hien_tai()
print(f"Hôm nay là ngày: {ngay_hien_tai}")


# 4. Hàm không có tham số và không có giá trị trả về
def chao_mung():
    print("Chào mừng bạn đến với Python!")


chao_mung()  # Kết quả: Chào mừng bạn đến với Python!

# 5. Hàm lambda (hàm ẩn danh)
binh_phuong = lambda x: x**2
print(f"Bình phương của 5 = {binh_phuong(5)}")  # Kết quả: 25

# Sử dụng lambda với hàm sorted
danh_sach_sinh_vien = [
    {"ten": "A", "diem": 8.5},
    {"ten": "B", "diem": 7.0},
    {"ten": "C", "diem": 9.0},
]
danh_sach_sinh_vien_sap_xep = sorted(
    danh_sach_sinh_vien, key=lambda sv: sv["diem"], reverse=True
)
print("Danh sách sinh viên sau khi sắp xếp:")
for sv in danh_sach_sinh_vien_sap_xep:
    print(f"Tên: {sv['ten']}, Điểm: {sv['diem']}")


# 6. Hàm đệ quy
def giai_thua(n):
    if n == 0 or n == 1:
        return 1
    return n * giai_thua(n - 1)


print(f"5! = {giai_thua(5)}")  # Kết quả: 120

# 7. Hàm nội trang (built-in functions)
print("Một số hàm nội trang trong Python:")
print(f"abs(-5) = {abs(-5)}")  # Giá trị tuyệt đối
print(f"max(1, 5, 3) = {max(1, 5, 3)}")  # Giá trị lớn nhất
print(f"min(1, 5, 3) = {min(1, 5, 3)}")  # Giá trị nhỏ nhất
print(
    f"sum([1, 2, 3, 4, 5]) = {sum([1, 2, 3, 4, 5])}"
)  # Tổng các phần tử trong danh sách


# ========== 4. THAM SỐ TỪ KHÓA (KEYWORD ARGUMENTS) ==========
"""
Tham số từ khóa là tham số được truyền vào hàm bằng cách sử dụng tên tham số.
"""
print("\n===== 4. THAM SỐ TỪ KHÓA (KEYWORD ARGUMENTS) =====")


def mo_ta_nguoi(ten, tuoi, nghe_nghiep="Sinh viên"):
    return f"{ten} là {nghe_nghiep}, {tuoi} tuổi."


# Sử dụng positional arguments
print(mo_ta_nguoi("Hà", 20))  # Kết quả: Hà là Sinh viên, 20 tuổi.

# Sử dụng keyword arguments
print(
    mo_ta_nguoi(tuoi=25, ten="Nam", nghe_nghiep="Giáo viên")
)  # Kết quả: Nam là Giáo viên, 25 tuổi.

# Kết hợp positional và keyword arguments
print(
    mo_ta_nguoi("Lan", nghe_nghiep="Bác sĩ", tuoi=30)
)  # Kết quả: Lan là Bác sĩ, 30 tuổi.

# Lưu ý: positional arguments phải đứng trước keyword arguments
# print(mo_ta_nguoi(ten="Mai", 22))  # Lỗi: SyntaxError: positional argument follows keyword argument


# ========== 5. THAM SỐ MẶC ĐỊNH (DEFAULT ARGUMENTS) ==========
"""
Tham số mặc định là tham số được gán giá trị mặc định trong khai báo hàm.
Nếu không có đối số được truyền vào, giá trị mặc định sẽ được sử dụng.
"""
print("\n===== 5. THAM SỐ MẶC ĐỊNH (DEFAULT ARGUMENTS) =====")


def tao_profile(ten, tuoi=18, quoc_tich="Việt Nam"):
    return f"Tên: {ten}, Tuổi: {tuoi}, Quốc tịch: {quoc_tich}"


# Sử dụng tất cả giá trị mặc định
print(tao_profile("An"))  # Kết quả: Tên: An, Tuổi: 18, Quốc tịch: Việt Nam

# Ghi đè một số giá trị mặc định
print(tao_profile("Bình", 25))  # Kết quả: Tên: Bình, Tuổi: 25, Quốc tịch: Việt Nam
print(
    tao_profile("Cường", quoc_tich="Mỹ")
)  # Kết quả: Tên: Cường, Tuổi: 18, Quốc tịch: Mỹ

# Ghi đè tất cả giá trị mặc định
print(
    tao_profile("Dũng", 30, "Canada")
)  # Kết quả: Tên: Dũng, Tuổi: 30, Quốc tịch: Canada

# Lưu ý: Tham số mặc định phải đứng sau tham số không mặc định
# def sai(a=1, b):  # Lỗi: SyntaxError: non-default argument follows default argument
#     return a + b


# ========== 6. THAM SỐ BIẾN ĐỔI (*ARGS) ==========
"""
*args cho phép truyền một số lượng đối số không xác định vào hàm.
Python sẽ đóng gói (pack) các đối số thành một tuple.
"""
print("\n===== 6. THAM SỐ BIẾN ĐỔI (*ARGS) =====")


def tinh_tong(*so):
    print(f"Kiểu của so: {type(so)}")
    print(f"Các giá trị: {so}")
    tong = 0
    for x in so:
        tong += x
    return tong


# Gọi hàm với số lượng đối số khác nhau
print(f"Tổng của 1, 2 = {tinh_tong(1, 2)}")  # 3
print(f"Tổng của 1, 2, 3, 4, 5 = {tinh_tong(1, 2, 3, 4, 5)}")  # 15
print(f"Không có đối số: {tinh_tong()}")  # 0


# Kết hợp với tham số bình thường
def tinh_tong_co_trong_so(trong_so, *so):
    tong = 0
    for x in so:
        tong += x
    return tong * trong_so


print(
    f"Tổng có trọng số 2 của 1, 2, 3 = {tinh_tong_co_trong_so(2, 1, 2, 3)}"
)  # (1+2+3)*2 = 12

# Mở rộng (unpack) danh sách hoặc tuple thành các đối số riêng biệt
danh_sach = [1, 2, 3, 4, 5]
print(f"Tổng của danh sách = {tinh_tong(*danh_sach)}")  # 15


# ========== 7. THAM SỐ TỪ KHÓA BIẾN ĐỔI (**KWARGS) ==========
"""
**kwargs cho phép truyền một số lượng tham số từ khóa không xác định vào hàm.
Python sẽ đóng gói các đối số thành một dictionary.
"""
print("\n===== 7. THAM SỐ TỪ KHÓA BIẾN ĐỔI (**KWARGS) =====")


def hien_thi_thong_tin_sinh_vien(**thong_tin):
    print(f"Kiểu của thong_tin: {type(thong_tin)}")
    print(f"Thông tin: {thong_tin}")
    for key, value in thong_tin.items():
        print(f"{key}: {value}")


# Gọi hàm với các đối số từ khóa khác nhau
hien_thi_thong_tin_sinh_vien(ten="Nguyễn Văn A", tuoi=20, lop="12A1")
print()
hien_thi_thong_tin_sinh_vien(ten="Trần Thị B", tuoi=21, lop="12A2", dia_chi="Hà Nội")


# Kết hợp *args và **kwargs
def hien_thi_tat_ca(*args, **kwargs):
    print("Arguments:")
    for arg in args:
        print(arg)

    print("\nKeyword Arguments:")
    for key, value in kwargs.items():
        print(f"{key}: {value}")


hien_thi_tat_ca(1, 2, 3, ten="Nguyễn Văn A", tuoi=20)

# Mở rộng (unpack) dictionary thành các đối số từ khóa riêng biệt
thong_tin = {"ten": "Lê Văn C", "tuoi": 22, "dia_chi": "TP.HCM"}
print("\nMở rộng dictionary:")
hien_thi_thong_tin_sinh_vien(**thong_tin)


# ========== 8. PHẠM VI (SCOPE) ==========
"""
Phạm vi của biến là khu vực trong chương trình mà biến đó có thể được truy cập.
Trong Python, có 4 phạm vi:
1. Local scope (phạm vi cục bộ): bên trong một hàm
2. Enclosing scope (phạm vi bao đóng): bên trong một hàm lồng nhau
3. Global scope (phạm vi toàn cục): trong toàn bộ tệp Python
4. Built-in scope (phạm vi nội trang): các tên được xây dựng sẵn trong Python
"""
print("\n===== 8. PHẠM VI (SCOPE) =====")

# Biến toàn cục (global)
bien_toan_cuc = "Đây là biến toàn cục"


def ham_pham_vi():
    # Biến cục bộ (local)
    bien_cuc_bo = "Đây là biến cục bộ"
    print(f"Bên trong hàm: {bien_toan_cuc}")  # Có thể truy cập biến toàn cục
    print(f"Bên trong hàm: {bien_cuc_bo}")  # Có thể truy cập biến cục bộ


ham_pham_vi()
print(f"Bên ngoài hàm: {bien_toan_cuc}")  # Có thể truy cập biến toàn cục
# print(f"Bên ngoài hàm: {bien_cuc_bo}")  # Lỗi: NameError: name 'bien_cuc_bo' is not defined


# Sử dụng từ khóa global
def thay_doi_bien_toan_cuc():
    global bien_toan_cuc  # Khai báo biến là global
    bien_toan_cuc = "Đã thay đổi biến toàn cục"


print(f"Trước khi gọi hàm: {bien_toan_cuc}")
thay_doi_bien_toan_cuc()
print(f"Sau khi gọi hàm: {bien_toan_cuc}")


# Phạm vi bao đóng (enclosing)
def ham_ngoai():
    bien_bao_dong = "Biến enclosing"

    def ham_trong():
        bien_cuc_bo = "Biến local"
        print(f"Từ hàm trong: {bien_cuc_bo}")  # Truy cập biến cục bộ
        print(f"Từ hàm trong: {bien_bao_dong}")  # Truy cập biến bao đóng
        print(f"Từ hàm trong: {bien_toan_cuc}")  # Truy cập biến toàn cục

    ham_trong()


ham_ngoai()


# Sử dụng từ khóa nonlocal
def ham_ngoai_2():
    bien_bao_dong = "Biến enclosing ban đầu"

    def ham_trong():
        nonlocal bien_bao_dong  # Khai báo biến là nonlocal
        bien_bao_dong = "Biến enclosing đã thay đổi"

    print(f"Trước khi gọi hàm trong: {bien_bao_dong}")
    ham_trong()
    print(f"Sau khi gọi hàm trong: {bien_bao_dong}")


ham_ngoai_2()


# ========== 9. GỠ LỖI (DEBUGGING) ==========
"""
Debugging là quá trình tìm và sửa lỗi trong chương trình.
Python cung cấp nhiều công cụ để debug như:
1. print(): in giá trị của biến
2. assert: kiểm tra điều kiện và báo lỗi nếu điều kiện sai
3. try-except: bắt và xử lý ngoại lệ
4. pdb: trình gỡ lỗi tích hợp của Python
5. IDE: các IDE như PyCharm, VS Code có công cụ gỡ lỗi trực quan
"""
print("\n===== 9. GỠ LỖI (DEBUGGING) =====")


# 1. Sử dụng print() để theo dõi giá trị
def tinh_binh_phuong_tong(a, b):
    print(f"Tham số đầu vào: a = {a}, b = {b}")  # Hiển thị giá trị đầu vào
    tong = a + b
    print(f"Tổng: {tong}")  # Hiển thị giá trị trung gian
    ket_qua = tong**2
    print(f"Kết quả: {ket_qua}")  # Hiển thị kết quả
    return ket_qua


tinh_binh_phuong_tong(3, 4)


# 2. Sử dụng assert để kiểm tra điều kiện
def chia(a, b):
    assert b != 0, "Không thể chia cho 0!"
    return a / b


try:
    print(f"5 ÷ 2 = {chia(5, 2)}")
    # print(f"5 ÷ 0 = {chia(5, 0)}")  # Sẽ gây ra AssertionError
except AssertionError as e:
    print(f"Lỗi: {e}")


# 3. Sử dụng try-except để bắt ngoại lệ
def tinh_nghich_dao(x):
    try:
        return 1 / x
    except ZeroDivisionError:
        print("Lỗi: Không thể tính nghịch đảo của 0!")
        return None
    except TypeError:
        print("Lỗi: Kiểu dữ liệu không hợp lệ!")
        return None
    finally:
        print("Khối finally luôn được thực thi")


print(f"Nghịch đảo của 5: {tinh_nghich_dao(5)}")
print(f"Nghịch đảo của 0: {tinh_nghich_dao(0)}")
print(f"Nghịch đảo của 'abc': {tinh_nghich_dao('abc')}")

# 4. Sử dụng pdb (Python Debugger) - Thường sử dụng trong console
# import pdb
# def ham_phuc_tap(a, b):
#     result = a + b
#     pdb.set_trace()  # Dừng chương trình và bắt đầu debug
#     result = result * 2
#     return result
# ham_phuc_tap(3, 4)

# 5. Sử dụng logging để ghi lại thông tin debug
import logging

# Cấu hình logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


def ham_voi_logging(a, b):
    logging.debug(f"Tham số đầu vào: a = {a}, b = {b}")
    try:
        result = a / b
        logging.info(f"Kết quả: {result}")
        return result
    except Exception as e:
        logging.error(f"Lỗi: {e}")
        return None


# Thử nghiệm với các giá trị khác nhau
ham_voi_logging(10, 2)
ham_voi_logging(10, 0)

# VSCode Coding Tricks: Xem hướng dẫn trong file


# ========== 10. BÀI TẬP VÀ LỜI GIẢI ==========
"""
Bài tập: Viết một hàm tính điểm trung bình của nhiều môn học,
với trọng số khác nhau cho từng môn.
"""
print("\n===== 10. BÀI TẬP VÀ LỜI GIẢI =====")


# Bài tập: Viết hàm tính điểm trung bình
def tinh_diem_trung_binh(*diem_so, trong_so=None):
    """
    Tính điểm trung bình của nhiều môn học.

    Parameters:
    diem_so (float): Điểm số của các môn học
    trong_so (list, optional): Trọng số cho từng môn học. Phải có cùng độ dài với diem_so.

    Returns:
    float: Điểm trung bình
    """
    # Kiểm tra đầu vào
    if len(diem_so) == 0:
        return 0

    # Nếu không có trọng số, sử dụng trọng số đều
    if trong_so is None:
        trong_so = [1] * len(diem_so)

    # Kiểm tra độ dài của trọng số
    if len(diem_so) != len(trong_so):
        raise ValueError("Số lượng điểm và trọng số không khớp nhau!")

    # Kiểm tra tất cả trọng số > 0
    if any(w <= 0 for w in trong_so):
        raise ValueError("Trọng số phải lớn hơn 0!")

    # Tính tổng có trọng số
    tong_diem_co_trong_so = sum(diem * trong_so[i] for i, diem in enumerate(diem_so))
    tong_trong_so = sum(trong_so)

    # Tính điểm trung bình
    diem_trung_binh = tong_diem_co_trong_so / tong_trong_so

    return diem_trung_binh


# Kiểm tra hàm
try:
    # Trường hợp không có trọng số
    print("Không có trọng số:")
    print(f"Điểm trung bình của 8, 7, 9: {tinh_diem_trung_binh(8, 7, 9):.2f}")

    # Trường hợp có trọng số
    print("\nCó trọng số:")
    print(
        f"Điểm trung bình của 8, 7, 9 với trọng số 2, 1, 3: {tinh_diem_trung_binh(8, 7, 9, trong_so=[2, 1, 3]):.2f}"
    )

    # Trường hợp lỗi: số lượng điểm và trọng số không khớp
    # print(f"Điểm trung bình lỗi: {tinh_diem_trung_binh(8, 7, 9, trong_so=[2, 1])}")

except ValueError as e:
    print(f"Lỗi: {e}")

print("\nKết thúc bài học về hàm trong Python!")
