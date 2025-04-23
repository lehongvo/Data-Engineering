# ========== 1 (VARIABLES) ==========
print("===== 1. BIẾN (VARIABLES) =====")
name = "Nguyễn Văn A"  # Python tự hiểu đây là chuỗi (string)
age = 25  # Python tự hiểu đây là số nguyên (int)
print(f"Tên: {name}, Tuổi: {age}")
print("Đây là chuỗi nhiều dòng")

# Gan nhiều biến cùng lúc
x, y, z = 1, 2, 3
print(f"x = {x}, y = {y}, z = {z}")

# Hoán đổi giá trị hai biến
x, y = y, x
print(f"Sau khi hoán đổi: x = {x}, y = {y}")

# =========== 2. QUY TẮC ĐẶT TÊN BIẾN (VARIABLE NAMES) ==========
# Tên biến có thể chứa chữ cái, số và dấu gạch dưới (_)
# Tên biến phải bắt đầu bằng chữ cái hoặc dấu gạch dưới, không được bắt đầu bằng số
# Tên biến phân biệt chữ hoa và chữ thường (case-sensitive)
# Không được sử dụng từ khóa của Python làm tên biến
# Quy ước đặt tên:
# - snake_case cho biến và hàm: my_variable, calculate_total
# - PascalCase cho lớp: MyClass, PersonInfo
# - SCREAMING_SNAKE_CASE cho hằng số: MAX_VALUE, PI
print("\n===== 2. QUY TẮC ĐẶT TÊN BIẾN =====")
# Đúng
ten_sinh_vien = "Nguyễn Văn A"  # snake_case (khuyến nghị cho biến)
_ten = "Nguyễn Văn B"  # Bắt đầu bằng dấu gạch dưới (OK)
tenSinhVien = "Nguyễn Văn C"  # camelCase (thường dùng trong JavaScript)
MAX_SIZE = 100  # SCREAMING_SNAKE_CASE (cho hằng số)
# Không nên
# 1ten = "Tên không hợp lệ"  # Bắt đầu bằng số -> lỗi cú pháp
# ten-sinh-vien = "Tên không hợp lệ"  # Chứa dấu gạch ngang -> lỗi cú pháp
# class = "Lớp"  # Sử dụng từ khóa 'class' -> lỗi cú pháp
print("Quy ước đặt tên biến:")
print(f"snake_case (cho biến): {ten_sinh_vien}")
print(f"Hằng số (SCREAMING_SNAKE_CASE): {MAX_SIZE}")
#
# ========== 3. CHUỖI (STRINGS) ==========
# Chuỗi trong Python là một dãy các ký tự, được đặt trong dấu nháy đơn ('') hoặc nháy kép ("").
print("\n===== 3. CHUỖI (STRINGS) =====")
# Khai báo chuỗi
chuoi_don = "Xin chào"
chuoi_kep = "Python"
print(f"Chuỗi nháy đơn: {chuoi_don}")
print(f"Chuỗi nháy kép: {chuoi_kep}")
# Chuỗi nhiều dòng
chuoi_nhieu_dong = """
Đây là chuỗi
nhiều dòng
"""
print(f"Chuỗi nhiều dòng: {chuoi_nhieu_dong}")

# Các phép toán với chuỗi
chuoi1 = "Xin chào"
chuoi2 = "Python"
chuoi3 = chuoi1 + " " + chuoi2  # Nối chuỗi
print(f"Nối chuỗi: {chuoi3}")
print(f"Nhân chuỗi: {chuoi1 * 3}")  # Nhân chuỗi
print(f"Độ dài chuỗi: {len(chuoi1)}")  # Độ dài chuỗi
print(f"Chữ hoa: {chuoi1.upper()}")  # Chuyển thành chữ hoa
print(f"Chữ thường: {chuoi1.lower()}")  # Chuyển thành chữ thường
print(f"Thay thế: {chuoi1.replace('chào', 'mừng')}")  # Thay thế chuỗi
print(f"Cắt chuỗi: {chuoi1[0:3]}")  # Cắt chuỗi (từ vị trí 0 đến 2)
print(f"Kiểm tra chuỗi: {'chào' in chuoi1}")  # Kiểm tra chuỗi
print(f"Kiểm tra bắt đầu bằng: {chuoi1.startswith('Xin')}")  # Kiểm tra bắt đầu bằng
print(f"Kiểm tra kết thúc bằng: {chuoi1.endswith('chào')}")  # Kiểm tra kết thúc bằng
print(f"Vị trí chuỗi: {chuoi1.find('chào')}")  # Vị trí chuỗi
print(f"Đếm số lần xuất hiện: {chuoi1.count('o')}")  # Đếm số lần xuất hiện
print(f"Chia chuỗi: {chuoi1.split(' ')}")  # Chia chuỗi
print(f"Đảo ngược chuỗi: {chuoi1[::-1]}")  # Đảo ngược chuỗi

# ========== 4. DANH SÁCH (LISTS) ==========
# Danh sách là một tập hợp các phần tử, có thể chứa nhiều kiểu dữ liệu khác nhau.
print("\n===== 4. DANH SÁCH (LISTS) =====")
# Khai báo danh sách
danh_sach = [1, 2, 3, 4, 5]
print(f"Danh sách: {danh_sach}")
# Danh sách rỗng
danh_sach_rong = []
print(f"Danh sách rỗng: {danh_sach_rong}")
# Danh sách chứa nhiều kiểu dữ liệu
danh_sach_kieu_khac = [1, "Python", 3.14, True]
print(f"Danh sách chứa nhiều kiểu dữ liệu: {danh_sach_kieu_khac}")
# Truy cập phần tử trong danh sách
print(f"Phần tử đầu tiên: {danh_sach[0]}")
print(f"Phần tử cuối cùng: {danh_sach[-1]}")
print(f"Phần tử từ vị trí 1 đến 3: {danh_sach[1:4]}")  # Lấy từ 1 đến 3
print(f"Phần tử từ đầu đến vị trí 3: {danh_sach[:4]}")
print(f"Phần tử từ vị trí 2 đến hết: {danh_sach[2:]}")
print(f"Phần tử từ vị trí 1 đến 4 với bước nhảy 2: {danh_sach[1:5:2]}")  # Bước nhảy 2
print(f"Phần tử từ vị trí 0 đến 4 với bước nhảy 2: {danh_sach[0:5:2]}")  # Bước nhảy 2
# Thay đổi giá trị phần tử trong danh sách
danh_sach[0] = 10
print(f"Danh sách sau khi thay đổi phần tử đầu tiên: {danh_sach}")
# Thêm phần tử vào danh sách
danh_sach.append(6)  # Thêm phần tử vào cuối danh sách
print(f"Danh sách sau khi thêm phần tử 6: {danh_sach}")
danh_sach.insert(0, 0)  # Thêm phần tử vào vị trí đầu tiên
print(f"Danh sách sau khi thêm phần tử 0 vào đầu: {danh_sach}")
# Xóa phần tử trong danh sách
danh_sach.remove(3)  # Xóa phần tử đầu tiên có giá trị 3
print(f"Danh sách sau khi xóa phần tử 3: {danh_sach}")
danh_sach.pop()  # Xóa phần tử cuối cùng
print(f"Danh sách sau khi xóa phần tử cuối cùng: {danh_sach}")
danh_sach.pop(0)  # Xóa phần tử đầu tiên
print(f"Danh sách sau khi xóa phần tử đầu tiên: {danh_sach}")
# Sắp xếp danh sách
danh_sach.sort()  # Sắp xếp danh sách
print(f"Danh sách sau khi sắp xếp: {danh_sach}")
# Đảo ngược danh sách
danh_sach.reverse()  # Đảo ngược danh sách
print(f"Danh sách sau khi đảo ngược: {danh_sach}")
# Sao chép danh sách
danh_sach_sao_chep = danh_sach.copy()  # Sao chép danh sách
print(f"Danh sách sao chép: {danh_sach_sao_chep}")
# Xóa danh sách
del danh_sach  # Xóa danh sách
print("Danh sách đã bị xóa.")
# Kiểm tra danh sách rỗng
if not danh_sach_rong:
    print("Danh sách rỗng.")
else:
    print("Danh sách không rỗng.")
# Kiểm tra phần tử trong danh sách
if 1 in danh_sach_kieu_khac:
    print("Phần tử 1 có trong danh sách.")
else:
    print("Phần tử 1 không có trong danh sách.")
# Kiểm tra độ dài danh sách
print(f"Độ dài danh sách: {len(danh_sach_kieu_khac)}")  # Độ dài danh sách
# Lặp qua danh sách
print("Lặp qua danh sách:")
for phan_tu in danh_sach_kieu_khac:
    print(phan_tu, end=" ")
print()
# Lặp qua danh sách với chỉ số
print("Lặp qua danh sách với chỉ số:")
for i, phan_tu in enumerate(danh_sach_kieu_khac):
    print(f"Phần tử {i}: {phan_tu}")
# Lặp qua danh sách với chỉ số và bắt đầu từ 1
print("Lặp qua danh sách với chỉ số bắt đầu từ 1:")
for i, phan_tu in enumerate(danh_sach_kieu_khac, start=1):
    print(f"Phần tử {i}: {phan_tu}")
# Lặp qua danh sách với chỉ số và bắt đầu từ 1, bước nhảy 2
print("Lặp qua danh sách với chỉ số bắt đầu từ 1, bước nhảy 2:")
for i, phan_tu in enumerate(danh_sach_kieu_khac[::2], start=1):
    print(f"Phần tử {i}: {phan_tu}")

# ========== 7. SỐ (NUMBERS) ==========
# Số trong Python có thể là số nguyên (int), số thực (float) hoặc số phức (complex).
print("\n===== 7. SỐ (NUMBERS) =====")
# Số nguyên
so_nguyen = 123
print(f"Số nguyên: {so_nguyen}, Kiểu: {type(so_nguyen)}")
# Số thực
so_thuc = 3.14  # Số thực
print(f"Số thực: {so_thuc}, Kiểu: {type(so_thuc)}")
# Số phức
so_phuc = 1 + 2j  # Số phức
print(f"Số phức: {so_phuc}, Kiểu: {type(so_phuc)}")
# Phần thực và phần ảo của số phức
print(f"Phần thực: {so_phuc.real}, Phần ảo: {so_phuc.imag}")
# Các phép toán với số
x, y = 10, 3
print(f"{x} + {y} = {x + y}")  # Cộng
print(f"{x} - {y} = {x - y}")  # Trừ

print(f"{x} * {y} = {x * y}")  # Nhân
print(f"{x} / {y} = {x / y}")  # Chia (kết quả là float)
print(f"{x} // {y} = {x // y}")  # Chia lấy phần nguyên
print(f"{x} % {y} = {x % y}")  # Chia lấy phần dư
print(f"{x} ** {y} = {x ** y}")  # Lũy thừa
# Các phép toán với số thực
print(f"3.14 + 2.5 = {3.14 + 2.5}")  # Cộng
print(f"3.14 - 2.5 = {3.14 - 2.5}")  # Trừ
print(f"3.14 * 2.5 = {3.14 * 2.5}")  # Nhân

print(f"3.14 / 2.5 = {3.14 / 2.5}")  # Chia (kết quả là float)
print(f"3.14 // 2.5 = {3.14 // 2.5}")  # Chia lấy phần nguyên
print(f"3.14 % 2.5 = {3.14 % 2.5}")  # Chia lấy phần dư
print(f"3.14 ** 2.5 = {3.14 ** 2.5}")  # Lũy thừa
# Các phép toán với số phức
print(f"1 + 2j + 3 + 4j = {1 + 2j + 3 + 4j}")  # Cộng
print(f"1 + 2j - 3 - 4j = {1 + 2j - 3 - 4j}")  # Trừ
print(f"(1 + 2j) * (3 + 4j) = {(1 + 2j) * (3 + 4j)}")  # Nhân
print(f"(1 + 2j) / (3 + 4j) = {(1 + 2j) / (3 + 4j)}")  # Chia

# Hàm toán học từ module math
import math

print(f"Giá trị tuyệt đối của -10: {abs(-10)}")  # Giá trị tuyệt đối
print(f"Căn bậc hai của 16: {math.sqrt(16)}")  # Căn bậc hai
print(f"3 mũ 2: {pow(3, 2)}")  # Lũy thừa
print(f"3.14 làm tròn lên: {math.ceil(3.14)}")  # Làm tròn lên
print(f"3.14 làm tròn xuống: {math.floor(3.14)}")  # Làm tròn xuống
print(f"3.14 làm tròn: {round(3.14)}")  # Làm tròn
print(
    f"3.14 làm tròn đến 1 chữ số thập phân: {round(3.14, 1)}"
)  # Làm tròn đến 1 chữ số thập phân

# ========== 9. CHUYỂN ĐỔI KIỂU (TYPE CONVERSION) ==========

# Chuyển đổi giữa các kiểu dữ liệu
print("\n===== 9. CHUYỂN ĐỔI KIỂU (TYPE CONVERSION) =====")
# Chuyển đổi sang số nguyên
print(f"int('10') = {int('10')}")
print(f"int(3.14) = {int(3.14)}")  # Cắt phần thập phân
print(f"int(True) = {int(True)}")  # True -> 1
print(f"int(False) = {int(False)}")  # False -> 0
# Chuyển đổi sang số thực
print(f"float('3.14') = {float('3.14')}")
print(f"float(10) = {float(10)}")  # Chuyển đổi số nguyên sang số thực
print(f"float(True) = {float(True)}")  # True -> 1.0
print(f"float(False) = {float(False)}")  # False -> 0.0
# Chuyển đổi sang chuỗi
print(f"str(10) = '{str(10)}'")  # Chuyển đổi số nguyên sang chuỗi
print(f"str(3.14) = '{str(3.14)}'")  # Chuyển đổi số thực sang chuỗi
print(f"str(True) = '{str(True)}'")  # Chuyển đổi True sang chuỗi
print(f"str(False) = '{str(False)}'")  # Chuyển đổi False sang chuỗi
# Chuyển đổi sang danh sách
print(f"list('Python') = {list('Python')}")  # Chuyển đổi chuỗi sang danh sách
print(f"list((1, 2, 3)) = {list((1, 2, 3))}")  # Chuyển đổi tuple sang danh sách
print(f"list(range(5)) = {list(range(5))}")  # Chuyển đổi range sang danh sách

# Chuyển đổi sang tuple
print(f"tuple('Python') = {tuple('Python')}")  # Chuyển đổi chuỗi sang tuple
print(f"tuple([1, 2, 3]) = {tuple([1, 2, 3])}")  # Chuyển đổi danh sách sang tuple
print(f"tuple(range(5)) = {tuple(range(5))}")  # Chuyển đổi range sang tuple
# Chuyển đổi sang tập hợp
print(f"set('Python') = {set('Python')}")  # Chuyển đổi chuỗi sang tập hợp
print(f"set([1, 2, 3]) = {set([1, 2, 3])}")  # Chuyển đổi danh sách sang tập hợp
print(f"set((1, 2, 3)) = {set((1, 2, 3))}")  # Chuyển đổi tuple sang tập hợp


# Kiểm tra trước khi chuyển đổi
# Kiểm tra xem chuỗi có thể chuyển đổi sang số nguyên hay không
def is_convertible_to_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


# Kiểm tra xem chuỗi có thể chuyển đổi sang số thực hay không
def is_convertible_to_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
