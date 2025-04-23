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
print("Hàm là một khối lệnh thực hiện một tác vụ cụ thể và có thể được tái sử dụng.")
print("Cú pháp:")
print("def tên_hàm(tham_số1, tham_số2, ...):")
print("    # Thân hàm")
print("    return giá_trị_trả_về  # Không bắt buộc")
print("Ví dụ:")


def greet(name):
    print(f"Hello, {name}!")


greet("Alice")  # Hello, Alice!
greet("Bob")  # Hello, Bob!
# ========== 2. THAM SỐ VÀ ĐỐI SỐ (PARAMETERS AND ARGUMENTS) ==========
"""
Tham số là các biến được định nghĩa trong hàm, còn đối số là các giá trị được truyền vào hàm khi gọi hàm.
Cú pháp:
def tên_hàm(tham_số1, tham_số2, ...):
    # Thân hàm
    return giá_trị_trả_về  # Không bắt buộc
"""


def add(a, b):
    return a + b


print(add(5, 10))  # 15
print(add(20, 30))  # 50
# ========== 3. HÀM VÔ DANH (ANONYMOUS FUNCTIONS) ==========
"""
Hàm vô danh là hàm không có tên, thường được sử dụng khi cần một hàm tạm thời.
Cú pháp:
lambda tham_số1, tham_số2, ...: biểu_thức
"""
add = lambda x, y: x + y
print(add(10, 20))  # 30
# ========== 4. HÀM TRONG HÀM (FUNCTIONS WITHIN FUNCTIONS) ==========
"""
Hàm có thể được định nghĩa bên trong một hàm khác.
Cú pháp:    
def tên_hàm1(tham_số1, tham_số2, ...):
    def tên_hàm2(tham_số3, tham_số4, ...):
        # Thân hàm 2
        return giá_trị_trả_về  # Không bắt buộc
    # Thân hàm 1
    return giá_trị_trả_về  # Không bắt buộc
"""


def outer_function(x):
    def inner_function(y):
        return x + y

    return inner_function


add_5 = outer_function(5)
print(add_5(10))  # 15
