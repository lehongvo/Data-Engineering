# CẤU TRÚC DỮ LIỆU TRONG PYTHON (DATA STRUCTURES)
# Tài liệu: Data Structures - https://codewithmosh.com/p/python-programming-course-beginners

# ========== 1. DANH SÁCH (LISTS) ==========
"""
List là một cấu trúc dữ liệu được sử dụng để lưu trữ nhiều phần tử.
List có thể chứa các phần tử với các kiểu dữ liệu khác nhau.
List cho phép phần tử trùng lặp và có thứ tự.
List có thể thay đổi (mutable).
"""
print("===== 1. DANH SÁCH (LISTS) =====")

# Tạo list
so_nguyen = [1, 2, 3, 4, 5]
ten_hoa_qua = ["Táo", "Cam", "Chuối", "Dưa hấu"]
danh_sach_hon_hop = [1, "hello", 3.14, True, [1, 2]]

print(f"Danh sách số nguyên: {so_nguyen}")
print(f"Danh sách tên hoa quả: {ten_hoa_qua}")
print(f"Danh sách hỗn hợp: {danh_sach_hon_hop}")

# Tạo list bằng constructor list()
danh_sach_tu_chuoi = list("Python")
print(f"Danh sách từ chuỗi: {danh_sach_tu_chuoi}")

# Tạo list bằng range
danh_sach_tu_range = list(range(5))
print(f"Danh sách từ range: {danh_sach_tu_range}")

# Kiểm tra độ dài list
print(f"Độ dài của danh sách số nguyên: {len(so_nguyen)}")


# ========== 2. TRUY CẬP PHẦN TỬ (ACCESSING ITEMS) ==========
"""
Phần tử trong list được truy cập bằng chỉ số (index).
Chỉ số bắt đầu từ 0 cho phần tử đầu tiên.
Chỉ số âm đếm ngược từ cuối list (-1 là phần tử cuối cùng).
"""
print("\n===== 2. TRUY CẬP PHẦN TỬ (ACCESSING ITEMS) =====")

# Truy cập phần tử bằng chỉ số
print(f"Phần tử đầu tiên: {ten_hoa_qua[0]}")
print(f"Phần tử thứ hai: {ten_hoa_qua[1]}")
print(f"Phần tử cuối cùng: {ten_hoa_qua[-1]}")
print(f"Phần tử gần cuối: {ten_hoa_qua[-2]}")

# Cắt list (slicing)
print(f"Hai phần tử đầu: {ten_hoa_qua[0:2]}")
print(f"Hai phần tử đầu (cách khác): {ten_hoa_qua[:2]}")
print(f"Hai phần tử cuối: {ten_hoa_qua[-2:]}")
print(f"Tất cả trừ phần tử đầu và cuối: {ten_hoa_qua[1:-1]}")

# Cắt với bước nhảy (step)
print(f"Các phần tử ở vị trí chẵn: {so_nguyen[0::2]}")  # Bước nhảy 2
print(f"Các phần tử ở vị trí lẻ: {so_nguyen[1::2]}")  # Bắt đầu từ 1, bước nhảy 2
print(f"Đảo ngược list: {so_nguyen[::-1]}")  # Bước nhảy -1 (đảo ngược)


# ========== 3. GIẢ NÉN DANH SÁCH (LIST UNPACKING) ==========
"""
List unpacking cho phép gán các phần tử của list vào nhiều biến cùng lúc.
"""
print("\n===== 3. GIẢ NÉN DANH SÁCH (LIST UNPACKING) =====")

# Unpacking cơ bản
a, b, c = [1, 2, 3]
print(f"a = {a}, b = {b}, c = {c}")

# Unpacking với toán tử *
first, *rest = ten_hoa_qua
print(f"Phần tử đầu: {first}")
print(f"Phần tử còn lại: {rest}")

*dau, cuoi = ten_hoa_qua
print(f"Phần tử đầu: {dau}")
print(f"Phần tử cuối: {cuoi}")

dau, *giua, cuoi = ten_hoa_qua
print(f"Phần tử đầu: {dau}")
print(f"Phần tử giữa: {giua}")
print(f"Phần tử cuối: {cuoi}")

# Hoán đổi giá trị
x, y = 10, 20
print(f"Trước khi hoán đổi: x = {x}, y = {y}")
x, y = y, x
print(f"Sau khi hoán đổi: x = {x}, y = {y}")


# ========== 4. DUYỆT QUA DANH SÁCH (LOOPING OVER LISTS) ==========
"""
Có nhiều cách để duyệt qua các phần tử trong list.
"""
print("\n===== 4. DUYỆT QUA DANH SÁCH (LOOPING OVER LISTS) =====")

# Duyệt qua phần tử
print("Duyệt qua phần tử:")
for hoa_qua in ten_hoa_qua:
    print(hoa_qua)

# Duyệt qua phần tử với chỉ số (enumerate)
print("\nDuyệt qua phần tử với chỉ số:")
for i, hoa_qua in enumerate(ten_hoa_qua):
    print(f"{i}: {hoa_qua}")

# Duyệt qua phần tử với chỉ số bắt đầu từ 1
print("\nDuyệt qua phần tử với chỉ số bắt đầu từ 1:")
for i, hoa_qua in enumerate(ten_hoa_qua, 1):
    print(f"{i}: {hoa_qua}")


# ========== 5. THÊM HOẶC XÓA PHẦN TỬ (ADDING OR REMOVING ITEMS) ==========
"""
List trong Python là mutable (có thể thay đổi).
Chúng ta có thể thêm, xóa hoặc thay đổi phần tử trong list.
"""
print("\n===== 5. THÊM HOẶC XÓA PHẦN TỬ (ADDING OR REMOVING ITEMS) =====")

# Thêm phần tử vào cuối list
so_nguyen.append(6)
print(f"Sau khi thêm 6: {so_nguyen}")

# Thêm phần tử vào vị trí cụ thể
so_nguyen.insert(0, 0)
print(f"Sau khi thêm 0 vào đầu: {so_nguyen}")

# Nối hai list
so_nguyen.extend([7, 8, 9])
print(f"Sau khi nối thêm [7, 8, 9]: {so_nguyen}")

# Xóa phần tử cuối và trả về giá trị
phan_tu_cuoi = so_nguyen.pop()
print(f"Phần tử đã xóa: {phan_tu_cuoi}")
print(f"Sau khi xóa phần tử cuối: {so_nguyen}")

# Xóa phần tử ở vị trí cụ thể
phan_tu_thu_nhat = so_nguyen.pop(0)
print(f"Phần tử đã xóa ở vị trí 0: {phan_tu_thu_nhat}")
print(f"Sau khi xóa phần tử đầu: {so_nguyen}")

# Xóa phần tử có giá trị cụ thể
so_nguyen.remove(5)  # Xóa phần tử có giá trị 5
print(f"Sau khi xóa giá trị 5: {so_nguyen}")

# Xóa tất cả phần tử
so_nguyen_copy = so_nguyen.copy()  # Tạo bản sao
so_nguyen_copy.clear()  # Xóa tất cả phần tử
print(f"Sau khi xóa tất cả: {so_nguyen_copy}")

# Xóa phần tử bằng từ khóa del
del so_nguyen[0]  # Xóa phần tử đầu tiên
print(f"Sau khi xóa phần tử đầu bằng del: {so_nguyen}")

# Xóa nhiều phần tử bằng slicing
del so_nguyen[1:3]  # Xóa phần tử từ vị trí 1 đến 2
print(f"Sau khi xóa phần tử từ vị trí 1 đến 2: {so_nguyen}")


# ========== 6. TÌM PHẦN TỬ (FINDING ITEMS) ==========
"""
Có nhiều phương thức để tìm kiếm phần tử trong list.
"""
print("\n===== 6. TÌM PHẦN TỬ (FINDING ITEMS) =====")

# Kiểm tra phần tử có trong list không
print(f"'Cam' có trong danh sách hoa quả không? {'Cam' in ten_hoa_qua}")
print(f"'Xoài' có trong danh sách hoa quả không? {'Xoài' in ten_hoa_qua}")

# Tìm vị trí của phần tử
print(f"Vị trí của 'Cam': {ten_hoa_qua.index('Cam')}")

# Đếm số lần xuất hiện
danh_sach_lap = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
print(f"Số lần xuất hiện của 3: {danh_sach_lap.count(3)}")


# Tìm kiếm an toàn (tránh lỗi khi không tìm thấy)
def tim_vi_tri_an_toan(danh_sach, gia_tri):
    try:
        return danh_sach.index(gia_tri)
    except ValueError:
        return -1


print(f"Vị trí của 'Xoài' (an toàn): {tim_vi_tri_an_toan(ten_hoa_qua, 'Xoài')}")


# ========== 7. SẮP XẾP DANH SÁCH (SORTING LISTS) ==========
"""
Có thể sắp xếp list theo thứ tự tăng dần hoặc giảm dần.
"""
print("\n===== 7. SẮP XẾP DANH SÁCH (SORTING LISTS) =====")

# Sắp xếp list số nguyên
numbers = [3, 1, 5, 2, 4]

# Sắp xếp tăng dần
sorted_numbers = sorted(numbers)  # Tạo list mới đã sắp xếp
print(f"List gốc: {numbers}")
print(f"List đã sắp xếp (tăng dần): {sorted_numbers}")

# Sắp xếp giảm dần
sorted_numbers_desc = sorted(numbers, reverse=True)
print(f"List đã sắp xếp (giảm dần): {sorted_numbers_desc}")

# Sắp xếp và thay đổi list gốc
numbers.sort()  # Thay đổi list gốc
print(f"List gốc sau khi sắp xếp: {numbers}")

# Sắp xếp list chuỗi
ten_hoa_qua.sort()
print(f"Danh sách hoa quả sau khi sắp xếp: {ten_hoa_qua}")

# Sắp xếp list tuple theo phần tử thứ 2
san_pham = [("Sản phẩm A", 10), ("Sản phẩm B", 5), ("Sản phẩm C", 15)]


def lay_gia(item):
    return item[1]


san_pham.sort(key=lay_gia)
print(f"Danh sách sản phẩm sau khi sắp xếp theo giá: {san_pham}")


# ========== 8. HÀM LAMBDA (LAMBDA FUNCTIONS) ==========
"""
Hàm lambda là hàm vô danh, được sử dụng để tạo các hàm ngắn gọn.
"""
print("\n===== 8. HÀM LAMBDA (LAMBDA FUNCTIONS) =====")

# Hàm lambda cơ bản
binh_phuong = lambda x: x**2
print(f"Bình phương của 5: {binh_phuong(5)}")

# Sử dụng lambda với sorted
san_pham = [("Sản phẩm A", 10), ("Sản phẩm B", 5), ("Sản phẩm C", 15)]

san_pham.sort(key=lambda item: item[1])
print(f"Sắp xếp sản phẩm theo giá (lambda): {san_pham}")

# Hàm lambda với nhiều tham số
tong = lambda a, b: a + b
print(f"Tổng của 5 và 3: {tong(5, 3)}")


# ========== 9. HÀM MAP (MAP FUNCTION) ==========
"""
map() áp dụng một hàm cho mỗi phần tử trong một iterable.
"""
print("\n===== 9. HÀM MAP (MAP FUNCTION) =====")

# Sử dụng map với hàm có sẵn
numbers = [1, 2, 3, 4, 5]
squares = map(lambda x: x**2, numbers)
print(f"Bình phương của các số: {list(squares)}")

# Sử dụng map với nhiều iterable
numbers1 = [1, 2, 3]
numbers2 = [10, 20, 30]
tong_theo_cap = map(lambda x, y: x + y, numbers1, numbers2)
print(f"Tổng theo cặp: {list(tong_theo_cap)}")


# Sử dụng map với hàm thông thường
def binh_phuong(x):
    return x**2


squares = map(binh_phuong, numbers)
print(f"Bình phương (hàm thông thường): {list(squares)}")


# ========== 10. HÀM FILTER (FILTER FUNCTION) ==========
"""
filter() lọc các phần tử trong iterable dựa trên một hàm kiểm tra.
"""
print("\n===== 10. HÀM FILTER (FILTER FUNCTION) =====")

# Lọc các số chẵn
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
so_chan = filter(lambda x: x % 2 == 0, numbers)
print(f"Các số chẵn: {list(so_chan)}")

# Lọc các chuỗi có độ dài > 3
strings = ["a", "ab", "abc", "abcd", "abcde"]
chuoi_dai = filter(lambda s: len(s) > 3, strings)
print(f"Các chuỗi có độ dài > 3: {list(chuoi_dai)}")

# Kết hợp map và filter
numbers = [1, 2, 3, 4, 5]
binh_phuong_chan = map(lambda x: x**2, filter(lambda x: x % 2 == 0, numbers))
print(f"Bình phương các số chẵn: {list(binh_phuong_chan)}")


# ========== 11. LIST COMPREHENSIONS ==========
"""
List comprehension là cú pháp ngắn gọn để tạo list mới từ iterable.
"""
print("\n===== 11. LIST COMPREHENSIONS =====")

# List comprehension cơ bản
numbers = [1, 2, 3, 4, 5]
squares = [x**2 for x in numbers]
print(f"Bình phương (list comprehension): {squares}")

# List comprehension với điều kiện
so_chan = [x for x in numbers if x % 2 == 0]
print(f"Các số chẵn (list comprehension): {so_chan}")

# List comprehension với biến đổi có điều kiện
ket_qua = [x**2 if x % 2 == 0 else x**3 for x in numbers]
print(f"Kết quả (list comprehension phức tạp): {ket_qua}")

# So sánh với cách viết thông thường
ket_qua_thong_thuong = []
for x in numbers:
    if x % 2 == 0:
        ket_qua_thong_thuong.append(x**2)
    else:
        ket_qua_thong_thuong.append(x**3)
print(f"Kết quả (cách viết thông thường): {ket_qua_thong_thuong}")

# List comprehension lồng nhau (tạo matrix)
matrix = [[i for i in range(3)] for j in range(3)]
print(f"Matrix 3x3: {matrix}")


# ========== 12. HÀM ZIP (ZIP FUNCTION) ==========
"""
zip() kết hợp các phần tử từ nhiều iterable thành các tuple.
"""
print("\n===== 12. HÀM ZIP (ZIP FUNCTION) =====")

# Kết hợp hai list
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
people = list(zip(names, ages))
print(f"Kết hợp tên và tuổi: {people}")

# Kết hợp nhiều list
cities = ["Hanoi", "HCM City", "Da Nang"]
population = [8, 9, 1]
area = [3358, 2095, 1285]
city_info = list(zip(cities, population, area))
print(f"Thông tin thành phố: {city_info}")

# Unzip (giải nén)
names, ages = zip(*people)
print(f"Tên sau khi giải nén: {names}")
print(f"Tuổi sau khi giải nén: {ages}")


# ========== 13. NGĂN XẾP (STACKS) ==========
"""
Stack là cấu trúc dữ liệu LIFO (Last In, First Out).
Trong Python, list có thể được sử dụng làm stack.
"""
print("\n===== 13. NGĂN XẾP (STACKS) =====")

# Tạo stack rỗng
stack = []

# Push: Thêm phần tử vào đỉnh stack
stack.append(1)
stack.append(2)
stack.append(3)
print(f"Stack sau khi push 1, 2, 3: {stack}")

# Pop: Lấy phần tử từ đỉnh stack
top = stack.pop()
print(f"Phần tử vừa pop: {top}")
print(f"Stack sau khi pop: {stack}")

# Peek: Xem phần tử ở đỉnh stack mà không lấy ra
peek = stack[-1] if stack else None
print(f"Phần tử ở đỉnh stack: {peek}")

# Kiểm tra stack rỗng
is_empty = len(stack) == 0
print(f"Stack có rỗng không? {is_empty}")


# Ví dụ: Đảo ngược chuỗi bằng stack
def reverse_string(s):
    stack = []
    for char in s:
        stack.append(char)

    reversed_str = ""
    while stack:
        reversed_str += stack.pop()

    return reversed_str


print(f"'Python' đảo ngược: {reverse_string('Python')}")


# ========== 14. HÀNG ĐỢI (QUEUES) ==========
"""
Queue là cấu trúc dữ liệu FIFO (First In, First Out).
Trong Python, collections.deque được sử dụng để implement queue hiệu quả.
"""
print("\n===== 14. HÀNG ĐỢI (QUEUES) =====")

from collections import deque

# Tạo queue rỗng
queue = deque()

# Enqueue: Thêm phần tử vào cuối queue
queue.append(1)
queue.append(2)
queue.append(3)
print(f"Queue sau khi enqueue 1, 2, 3: {queue}")

# Dequeue: Lấy phần tử từ đầu queue
front = queue.popleft()
print(f"Phần tử vừa dequeue: {front}")
print(f"Queue sau khi dequeue: {queue}")

# Peek: Xem phần tử ở đầu queue mà không lấy ra
peek = queue[0] if queue else None
print(f"Phần tử ở đầu queue: {peek}")

# Kiểm tra queue rỗng
is_empty = len(queue) == 0
print(f"Queue có rỗng không? {is_empty}")


# Ví dụ: Sử dụng queue để xử lý các công việc
def process_tasks(tasks):
    task_queue = deque(tasks)
    completed = []

    while task_queue:
        current_task = task_queue.popleft()
        print(f"Đang xử lý công việc: {current_task}")
        completed.append(current_task)

    return completed


tasks = ["Task 1", "Task 2", "Task 3"]
completed_tasks = process_tasks(tasks)
print(f"Các công việc đã hoàn thành: {completed_tasks}")


# ========== 15. TUPLES ==========
"""
Tuple là một cấu trúc dữ liệu tương tự list nhưng không thể thay đổi (immutable).
"""
print("\n===== 15. TUPLES =====")

# Tạo tuple
point = (1, 2)
rgb = (255, 0, 0)
empty_tuple = ()
single_item_tuple = (1,)  # Lưu ý dấu phẩy

print(f"Tuple tọa độ: {point}")
print(f"Tuple RGB: {rgb}")
print(f"Tuple một phần tử: {single_item_tuple}")

# Truy cập phần tử trong tuple
print(f"Tọa độ x: {point[0]}")
print(f"Tọa độ y: {point[1]}")

# Giải nén tuple
x, y = point
print(f"x = {x}, y = {y}")

# Tuple không thể thay đổi
# point[0] = 10  # TypeError: 'tuple' object does not support item assignment

# Các phương thức của tuple
coordinates = (1, 2, 3, 2, 4, 1, 5)
print(f"Số lần xuất hiện của 1: {coordinates.count(1)}")
print(f"Vị trí đầu tiên của 2: {coordinates.index(2)}")

# Chuyển đổi giữa list và tuple
list_from_tuple = list(coordinates)
print(f"List từ tuple: {list_from_tuple}")

tuple_from_list = tuple(list_from_tuple)
print(f"Tuple từ list: {tuple_from_list}")

# So sánh tuple
point1 = (1, 2)
point2 = (1, 2)
point3 = (3, 4)

print(f"point1 == point2: {point1 == point2}")
print(f"point1 == point3: {point1 == point3}")


# ========== 16. HOÁN ĐỔI BIẾN (SWAPPING VARIABLES) ==========
"""
Python cho phép hoán đổi giá trị biến một cách dễ dàng.
"""
print("\n===== 16. HOÁN ĐỔI BIẾN (SWAPPING VARIABLES) =====")

# Cách thông thường (sử dụng biến tạm)
a = 10
b = 20

print(f"Trước khi hoán đổi: a = {a}, b = {b}")

temp = a
a = b
b = temp

print(f"Sau khi hoán đổi (cách thông thường): a = {a}, b = {b}")

# Cách Python (tuple unpacking)
a, b = 10, 20

print(f"Trước khi hoán đổi: a = {a}, b = {b}")

a, b = b, a

print(f"Sau khi hoán đổi (cách Python): a = {a}, b = {b}")

# Hoán đổi nhiều biến
a, b, c = 1, 2, 3

print(f"Trước khi hoán đổi: a = {a}, b = {b}, c = {c}")

a, b, c = c, a, b

print(f"Sau khi hoán đổi: a = {a}, b = {b}, c = {c}")


# ========== 17. MẢNG (ARRAYS) ==========
"""
Array là cấu trúc dữ liệu giống list nhưng chỉ chứa các phần tử cùng kiểu.
Array trong Python được cung cấp bởi module array.
"""
print("\n===== 17. MẢNG (ARRAYS) =====")

from array import array

# Các kiểu dữ liệu phổ biến trong array:
# 'i': int
# 'f': float
# 'd': double
# 'u': Unicode character

# Tạo mảng số nguyên
int_array = array("i", [1, 2, 3, 4, 5])
print(f"Mảng số nguyên: {int_array}")

# Tạo mảng số thực
float_array = array("f", [1.1, 1.2, 1.3, 1.4, 1.5])
print(f"Mảng số thực: {float_array}")

# Truy cập phần tử
print(f"Phần tử đầu tiên trong mảng số nguyên: {int_array[0]}")

# Thêm phần tử
int_array.append(6)
print(f"Sau khi thêm 6: {int_array}")

# Nối mảng
int_array.extend([7, 8, 9])
print(f"Sau khi nối thêm [7, 8, 9]: {int_array}")

# Xóa phần tử
int_array.pop()
print(f"Sau khi xóa phần tử cuối: {int_array}")

# Xóa phần tử ở vị trí cụ thể
int_array.pop(0)
print(f"Sau khi xóa phần tử đầu tiên: {int_array}")

# Xóa phần tử có giá trị cụ thể
int_array.remove(3)
print(f"Sau khi xóa giá trị 3: {int_array}")

# Đảo ngược mảng
int_array.reverse()
print(f"Sau khi đảo ngược: {int_array}")

# Chuyển đổi về list
list_from_array = list(int_array)
print(f"List từ mảng: {list_from_array}")


# ========== 18. TẬP HỢP (SETS) ==========
"""
Set là một tập hợp không có thứ tự và không chứa các phần tử trùng lặp.
"""
print("\n===== 18. TẬP HỢP (SETS) =====")

# Tạo set
numbers_set = {1, 2, 3, 4, 5}
print(f"Set số: {numbers_set}")

# Set loại bỏ các phần tử trùng lặp
duplicate_numbers = {1, 1, 2, 2, 3, 3, 4, 4, 5, 5}
print(f"Set loại bỏ trùng lặp: {duplicate_numbers}")

# Tạo set từ list
numbers_list = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5]
unique_numbers = set(numbers_list)
print(f"Set từ list có trùng lặp: {unique_numbers}")

# Thêm phần tử
numbers_set.add(6)
print(f"Sau khi thêm 6: {numbers_set}")

# Xóa phần tử
numbers_set.remove(3)  # Báo lỗi nếu không tìm thấy phần tử
print(f"Sau khi xóa 3: {numbers_set}")

numbers_set.discard(10)  # Không báo lỗi nếu không tìm thấy phần tử
print(f"Sau khi discard 10: {numbers_set}")

# Kiểm tra phần tử có trong set
print(f"2 có trong set không? {2 in numbers_set}")
print(f"3 có trong set không? {3 in numbers_set}")

# Các phép toán tập hợp
set1 = {1, 2, 3, 4, 5}
set2 = {4, 5, 6, 7, 8}

# Hợp (Union)
union_set = set1 | set2  # Hoặc set1.union(set2)
print(f"Hợp của hai set: {union_set}")

# Giao (Intersection)
intersection_set = set1 & set2  # Hoặc set1.intersection(set2)
print(f"Giao của hai set: {intersection_set}")

# Hiệu (Difference)
difference_set = set1 - set2  # Hoặc set1.difference(set2)
print(f"Hiệu của set1 và set2: {difference_set}")

# Hiệu đối xứng (Symmetric Difference)
symmetric_difference = set1 ^ set2  # Hoặc set1.symmetric_difference(set2)
print(f"Hiệu đối xứng của hai set: {symmetric_difference}")

# Kiểm tra tập con
set3 = {1, 2}
print(f"set3 là tập con của set1? {set3.issubset(set1)}")
print(f"set1 là tập cha của set3? {set1.issuperset(set3)}")


# ========== 19. TỪ ĐIỂN (DICTIONARIES) ==========
"""
Dictionary là cấu trúc dữ liệu lưu trữ theo cặp key-value.
"""
print("\n===== 19. TỪ ĐIỂN (DICTIONARIES) =====")

# Tạo dictionary
person = {"name": "Nguyễn Văn A", "age": 30, "city": "Hà Nội"}
print(f"Thông tin người: {person}")

# Tạo dictionary bằng dict constructor
person2 = dict(name="Trần Thị B", age=25, city="TP.HCM")
print(f"Thông tin người 2: {person2}")

# Truy cập giá trị bằng key
print(f"Tên: {person['name']}")
print(f"Tuổi: {person['age']}")
print(f"Thành phố: {person['city']}")

# Truy cập an toàn với get() (không gây lỗi nếu key không tồn tại)
print(f"Nghề nghiệp: {person.get('job', 'Không có thông tin')}")

# Thêm hoặc cập nhật phần tử
person["email"] = "nguyenvana@email.com"
print(f"Sau khi thêm email: {person}")

person["age"] = 31  # Cập nhật tuổi
print(f"Sau khi cập nhật tuổi: {person}")

# Xóa phần tử
del person["city"]
print(f"Sau khi xóa thành phố: {person}")

removed_value = person.pop("email")  # Xóa và trả về giá trị
print(f"Giá trị email đã xóa: {removed_value}")
print(f"Sau khi xóa email: {person}")

# Xóa và trả về cặp key-value cuối cùng được thêm vào
last_item = person.popitem()
print(f"Cặp key-value cuối cùng: {last_item}")
print(f"Sau khi xóa cặp cuối: {person}")

# Lấy tất cả keys và values
keys = person.keys()
values = person.values()
items = person.items()

print(f"Keys: {keys}")
print(f"Values: {values}")
print(f"Items: {items}")

# Duyệt qua dictionary
print("\nDuyệt qua dictionary:")
for key in person:
    print(f"{key}: {person[key]}")

print("\nDuyệt qua items:")
for key, value in person.items():
    print(f"{key}: {value}")

# Kiểm tra key có trong dictionary
print(f"'name' có trong dictionary không? {'name' in person}")
print(f"'city' có trong dictionary không? {'city' in person}")

# Gộp hai dictionary
person.update({"city": "Hà Nội", "job": "Engineer"})
print(f"Sau khi gộp: {person}")


# ========== 20. DICTIONARY COMPREHENSIONS ==========
"""
Dictionary comprehension là cú pháp ngắn gọn để tạo dictionary mới.
"""
print("\n===== 20. DICTIONARY COMPREHENSIONS =====")

# Dictionary comprehension cơ bản
squares = {x: x**2 for x in range(6)}
print(f"Bình phương các số từ 0-5: {squares}")

# Dictionary comprehension với điều kiện
even_squares = {x: x**2 for x in range(10) if x % 2 == 0}
print(f"Bình phương các số chẵn từ 0-9: {even_squares}")

# Chuyển đổi từ list sang dictionary
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
people = {name: age for name, age in zip(names, ages)}
print(f"Dictionary người từ lists: {people}")

# Hoán đổi key và value
original = {"a": 1, "b": 2, "c": 3}
swapped = {value: key for key, value in original.items()}
print(f"Dictionary sau khi hoán đổi: {swapped}")

# Dictionary comprehension với nhiều điều kiện
complex_dict = {x: ("chẵn" if x % 2 == 0 else "lẻ") for x in range(10)}
print(f"Dictionary phức tạp: {complex_dict}")


# ========== 21. BIỂU THỨC SINH (GENERATOR EXPRESSIONS) ==========
"""
Generator expression tạo ra các giá trị theo yêu cầu, giúp tiết kiệm bộ nhớ.
"""
print("\n===== 21. BIỂU THỨC SINH (GENERATOR EXPRESSIONS) =====")

# Generator expression cơ bản
numbers = [1, 2, 3, 4, 5]
squares_gen = (x**2 for x in numbers)
print(f"Kiểu của squares_gen: {type(squares_gen)}")

# Sử dụng next() để lấy giá trị tiếp theo
print(f"Giá trị đầu tiên: {next(squares_gen)}")
print(f"Giá trị thứ hai: {next(squares_gen)}")

# Chuyển đổi generator thành list
remainining_squares = list(squares_gen)
print(f"Các giá trị còn lại: {remainining_squares}")

# So sánh với list comprehension về bộ nhớ
import sys

list_comp = [x**2 for x in range(1000)]
gen_exp = (x**2 for x in range(1000))

print(f"Kích thước của list comprehension: {sys.getsizeof(list_comp)} bytes")
print(f"Kích thước của generator expression: {sys.getsizeof(gen_exp)} bytes")

# Sử dụng generator expression trong các hàm tổng hợp
sum_squares = sum(x**2 for x in range(10))
print(f"Tổng bình phương các số từ 0-9: {sum_squares}")

max_square = max(x**2 for x in range(10))
print(f"Bình phương lớn nhất trong các số từ 0-9: {max_square}")

min_square = min(x**2 for x in range(1, 10))
print(f"Bình phương nhỏ nhất trong các số từ 1-9: {min_square}")


# ========== 22. TOÁN TỬ UNPACKING (UNPACKING OPERATOR) ==========
"""
Toán tử unpacking (*) được sử dụng để giải nén các iterable.
"""
print("\n===== 22. TOÁN TỬ UNPACKING (UNPACKING OPERATOR) =====")

# Unpacking list
numbers = [1, 2, 3]
print(*numbers)  # Tương đương với print(1, 2, 3)


# Unpacking trong các hàm
def sum_three(a, b, c):
    return a + b + c


print(f"Tổng của [1, 2, 3]: {sum_three(*numbers)}")

# Gộp các list
list1 = [1, 2, 3]
list2 = [4, 5, 6]
combined = [*list1, *list2]
print(f"Gộp hai list: {combined}")

# Unpacking dictionary
dict1 = {"a": 1, "b": 2}
dict2 = {"c": 3, "d": 4}
combined_dict = {**dict1, **dict2}
print(f"Gộp hai dictionary: {combined_dict}")

# Unpacking với giá trị trực tiếp
combined = [*list1, 10, 20, *list2]
print(f"Gộp list với giá trị trực tiếp: {combined}")

combined_dict = {**dict1, "e": 5, **dict2, "f": 6}
print(f"Gộp dict với giá trị trực tiếp: {combined_dict}")

# Trường hợp key trùng
dict3 = {"a": 10, "e": 50}
combined_dict = {**dict1, **dict3}
print(f"Gộp với key trùng (key sau ghi đè key trước): {combined_dict}")

# Unpacking trong string
string = "abc"
chars = [*string]
print(f"Các ký tự trong chuỗi: {chars}")
