# CẤU TRÚC ĐIỀU KHIỂN TRONG PYTHON (CONTROL FLOW)
# Tài liệu: Control Flow - https://codewithmosh.com/p/python-programming-course-beginners

# ========== 1. TOÁN TỬ SO SÁNH (COMPARISON OPERATORS) ==========
# Toán tử so sánh được sử dụng để so sánh hai giá trị với nhau.
# Kết quả của phép so sánh sẽ là True hoặc False.
# Các toán tử so sánh trong Python:
# - == (bằng)
# - != (không bằng)
# - > (lớn hơn)
# - < (nhỏ hơn)
# - >= (lớn hơn hoặc bằng)
# - <= (nhỏ hơn hoặc bằng)
# Ví dụ:
a = 10
b = 20
print(a == b)  # False
print(a != b)  # True
print(a > b)  # False
print(a < b)  # True
print(a >= b)  # False
print(a <= b)  # True
# ========== 2. CÁC CẤU TRÚC ĐIỀU KHIỂN (CONTROL FLOW STATEMENTS) ==========
# Cấu trúc điều khiển là các câu lệnh cho phép chúng ta điều khiển luồng thực thi của chương trình.
# Các cấu trúc điều khiển trong Python:
# - Câu lệnh if
# - Câu lệnh if-else
# - Câu lệnh if-elif-else
# - Câu lệnh switch-case
# - Câu lệnh for
# - Câu lệnh while
# - Câu lệnh break
# - Câu lệnh continue
# - Câu lệnh pass
# - Câu lệnh try-except
# - Câu lệnh with
# - Câu lệnh lambda
# - Câu lệnh list comprehension
# - Câu lệnh dictionary comprehension
# - Câu lệnh async
# - Câu lệnh await
# - Câu lệnh async for
# - Câu lệnh async with
# - Câu lệnh async def
# - Câu lệnh async lambda
# Vd
# Câu lệnh if
x = 10
if x > 0:
    print("x là số dương")
elif x < 0:
    print("x là số âm")
else:
    print("x là số 0")
# Câu lệnh if-else
x = 10
if x > 0:
    print("x là số dương")
else:
    print("x là số âm")
# Câu lệnh if-elif-else
x = 10
if x > 0:
    print("x là số dương")
elif x < 0:
    print("x là số âm")
else:
    print("x là số 0")
# Câu lệnh switch-case
# Python không hỗ trợ câu lệnh switch-case, nhưng chúng ta có thể sử dụng câu lệnh if-elif-else để thay thế.
# Câu lệnh for
# Câu lệnh for được sử dụng để lặp qua một dãy số hoặc một danh sách.
# Cú pháp:
# for <biến> in <dãy số hoặc danh sách>:
#     <câu lệnh>
# Ví dụ:
numbers = [1, 2, 3, 4, 5]
for number in numbers:
    print(number)
# Câu lệnh while
# Câu lệnh while được sử dụng để lặp lại một khối mã cho đến khi điều kiện là False.
# Cú pháp:
# while <điều kiện>:
#     <câu lệnh>
# Ví dụ:
count = 0
while count < 5:
    print(count)
    count += 1
# Câu lệnh break
# Câu lệnh break được sử dụng để thoát khỏi vòng lặp.
# Cú pháp:
# break
# Ví dụ:
numbers = [1, 2, 3, 4, 5]
for number in numbers:
    if number == 3:
        break
    print(number)
# Câu lệnh continue
# Câu lệnh continue được sử dụng để bỏ qua một lần lặp trong vòng lặp.
# Cú pháp:
# continue
# Ví dụ:
numbers = [1, 2, 3, 4, 5]
for number in numbers:
    if number == 3:
        continue
    print(number)


# Câu lệnh pass
# Câu lệnh pass được sử dụng để bỏ qua một khối mã.
# Cú pháp:
# pass
# Ví dụ:
def my_function():
    pass


# Câu lệnh try-except
# Câu lệnh try-except được sử dụng để xử lý ngoại lệ.
# Cú pháp:
# try:
#     <câu lệnh>
# except <ngoại lệ>:
#     <câu lệnh>
# Ví dụ:
try:
    x = 10 / 0
except ZeroDivisionError:

    print("Không thể chia cho 0")

# Câu lệnh with
# Câu lệnh with được sử dụng để quản lý tài nguyên.
# Cú pháp:
# with <tài nguyên> as <biến>:
#     <câu lệnh>
# Ví dụ:
# with open("file.txt", "r") as file:
#     content = file.read()
#     print(content)
# Câu lệnh lambda
# Câu lệnh lambda được sử dụng để tạo hàm ẩn danh.
# Cú pháp:
# lambda <tham số>: <biểu thức>
# Ví dụ:
add = lambda x, y: x + y
print(add(10, 20))  # 30
# Câu lệnh list comprehension
# Câu lệnh list comprehension được sử dụng để tạo danh sách từ một dãy số hoặc một danh sách.
# Cú pháp:
# [<biểu thức> for <biến> in <dãy số hoặc danh sách>]
# Ví dụ:
numbers = [1, 2, 3, 4, 5]
squared_numbers = [number**2 for number in numbers]
print(squared_numbers)  # [1, 4, 9, 16, 25]
# Câu lệnh dictionary comprehension
# Câu lệnh dictionary comprehension được sử dụng để tạo từ điển từ một dãy số hoặc một danh sách.
# Cú pháp:
# {<khóa>: <giá trị> for <biến> in <dãy số hoặc danh sách>}
# Ví dụ:
numbers = [1, 2, 3, 4, 5]
squared_numbers = {number: number**2 for number in numbers}
print(squared_numbers)  # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
# Câu lệnh async
# Câu lệnh async được sử dụng để tạo hàm bất đồng bộ.
# Cú pháp:
# async def <tên hàm>(<tham số>):
#     <câu lệnh>
# Ví dụ:
import asyncio


async def my_function():
    await asyncio.sleep(1)
    print("Hàm bất đồng bộ đã hoàn thành")


asyncio.run(my_function())


# Câu lệnh await
# Câu lệnh await được sử dụng để chờ một hàm bất đồng bộ hoàn thành.
# Cú pháp:
# await <hàm bất đồng bộ>
# Ví dụ:
async def my_function():
    await asyncio.sleep(1)
    print("Hàm bất đồng bộ đã hoàn thành")


asyncio.run(my_function())


# Câu lệnh async for
# Câu lệnh async for được sử dụng để lặp qua một dãy số hoặc một danh sách bất đồng bộ.
# Cú pháp:
# async for <biến> in <đối tượng lặp bất đồng bộ>:
#     <câu lệnh>
# Ví dụ:
async def my_function():
    # Sửa lỗi: async for không thể sử dụng với range thông thường
    # Thay vào đó, sử dụng for thông thường trong hàm async
    for number in range(5):
        print(number)
        await asyncio.sleep(1)


asyncio.run(my_function())


# Câu lệnh async with
# Câu lệnh async with được sử dụng để quản lý tài nguyên bất đồng bộ.
# Cú pháp:
# async with <tài nguyên> as <biến>:
#     <câu lệnh>
# Ví dụ:
# Đây là ví dụ minh họa cách sử dụng async with, nhưng đang bị comment vì file.txt không tồn tại
# Trong thực tế, chúng ta cần sử dụng một tài nguyên hỗ trợ async context manager
async def my_function():
    # Thay vì cố gắng mở file không tồn tại, chúng ta sẽ in một thông báo
    print("Đây là ví dụ về async with (đã bỏ qua mở file để tránh lỗi)")
    # Để minh họa cách hoạt động của async with, chúng ta sẽ sử dụng asyncio.sleep()
    await asyncio.sleep(1)
    print("Hàm bất đồng bộ đã hoàn thành")

    # Cách sử dụng async with với một context manager thực sự sẽ như sau:
    # async with aiofiles.open("tên_file.txt", "r") as file:
    #     content = await file.read()
    #     print(content)
    # (Lưu ý: aiofiles cần được cài đặt bằng: pip install aiofiles)


asyncio.run(my_function())


# Câu lệnh async def
# Câu lệnh async def được sử dụng để tạo hàm bất đồng bộ.
# Cú pháp:
# async def <tên hàm>(<tham số>):
#     <câu lệnh>
# Ví dụ:
async def my_function():
    await asyncio.sleep(1)
    print("Hàm bất đồng bộ đã hoàn thành")


asyncio.run(my_function())
# Câu lệnh async lambda
# Câu lệnh async lambda được sử dụng để tạo hàm ẩn danh bất đồng bộ.
# Cú pháp:
# async lambda <tham số>: <biểu thức>
# Ví dụ:
async_add = lambda x, y: x + y


async def main():
    print(await async_add(10, 20))  # 30


asyncio.run(main())

# Câu lệnh async lambda không được hỗ trợ trong Python, nhưng chúng ta có thể sử dụng hàm async để thay thế.
# Câu lệnh async lambda không được hỗ trợ trong Python, nhưng chúng ta có thể sử dụng hàm async để thay thế.

# ========== 10. ĐỐI TƯỢNG LẶP (ITERABLES) ==========
# Đối tượng lặp là các đối tượng có thể lặp qua được, chẳng hạn như danh sách, tuple, set, dictionary, chuỗi.
# Các đối tượng lặp trong Python:
# - Danh sách (list)
# - Tuple
# - Set
# - Dictionary
# - Chuỗi (string)
# - Tập hợp (frozenset)
# - Mảng (array)
# - Tập hợp không thay đổi (immutable set)
# - Tập hợp không thay đổi (immutable frozenset)
# - Tập hợp không thay đổi (immutable array)
# - Tập hợp không thay đổi (immutable list)
# - Tập hợp không thay đổi (immutable tuple)
# - Tập hợp không thay đổi (immutable set)
# - Tập hợp không thay đổi (immutable dictionary)
# - Tập hợp không thay đổi (immutable string)
# - Tập hợp không thay đổi (immutable frozenset)
# - Tập hợp không thay đổi (immutable array)
# - Tập hợp không thay đổi (immutable list)
# vd
numbers = [1, 2, 3, 4, 5]
for number in numbers:
    print(number)
# Tạo một đối tượng lặp từ một danh sách
numbers = [1, 2, 3, 4, 5]
iterator = iter(numbers)
print(f"==> {next(iterator)}")
