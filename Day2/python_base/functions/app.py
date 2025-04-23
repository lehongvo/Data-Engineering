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
print(add_5(101))  # 15

# ========== 5. HÀM VỚI THAM SỐ MẶC ĐỊNH (FUNCTIONS WITH DEFAULT PARAMETERS) ==========
"""
Tham số mặc định là các tham số có giá trị mặc định nếu không được truyền vào khi gọi hàm.
Cú pháp:        
def tên_hàm(tham_số1=giá_trị_mặc_định, tham_số2=giá_trị_mặc_định, ...):
    # Thân hàm
    return giá_trị_trả_về  # Không bắt buộc
"""


def greet(name="World"):
    print(f"Hello, {name}!")


greet()  # Hello, World!
greet("Alice")  # Hello, Alice!
greet("Bob")  # Hello, Bob!
# ========== 6. HÀM VỚI THAM SỐ TÙY CHỌN (FUNCTIONS WITH VARIABLE NUMBER OF PARAMETERS) ==========
"""
Tham số tùy chọn cho phép truyền vào một số lượng tham số không xác định.
Cú pháp:
def tên_hàm(*tham_số):
    # Thân hàm
    return giá_trị_trả_về  # Không bắt buộc
"""


def add(*args):
    return sum(args)


print(add(1, 2, 3))  # 6
print(add(1, 2, 3, 4, 5))  # 15

# ========== 7. HÀM VỚI THAM SỐ TỪ KHÓA (FUNCTIONS WITH KEYWORD ARGUMENTS) ==========
"""
Tham số từ khóa cho phép truyền vào các tham số bằng tên của chúng.
Cú pháp:
def tên_hàm(**tham_số):
    # Thân hàm
    return giá_trị_trả_về  # Không bắt buộc
"""


def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")


print_info(name="Alice", age=30, city="New York")
# name: Alice
# age: 30
# city: New York

# ========== 8. HÀM VỚI THAM SỐ VÀ THAM SỐ TỪ KHÓA (FUNCTIONS WITH PARAMETERS AND KEYWORD ARGUMENTS) ==========
"""
Tham số và tham số từ khóa cho phép truyền vào các tham số và tham số từ khóa cùng một lúc.
Cú pháp:    
def tên_hàm(tham_số1, tham_số2, **tham_số_từ_khóa):
    # Thân hàm
    return giá_trị_trả_về  # Không bắt buộc
"""


def print_info(name, age, **kwargs):
    print(f"Name: {name}")
    print(f"Age: {age}")
    for key, value in kwargs.items():
        print(f"{key}: {value}")


print_info("Alice", 30, city="New York", country="USA")

# ========== 9. PHẠM VI (SCOPE) ==========
"""
Phạm vi là khu vực mà một biến có thể được truy cập.
Có 4 loại phạm vi trong Python:
1. Phạm vi toàn cục (Global Scope): Biến được định nghĩa bên ngoài tất cả các hàm.
2. Phạm vi cục bộ (Local Scope): Biến được định nghĩa bên trong một hàm.
3. Phạm vi không gian tên (Namespace Scope): Biến được định nghĩa bên trong một không gian tên.
4. Phạm vi bao quanh (Enclosing Scope): Biến được định nghĩa bên trong một hàm khác.
"""
x = 10  # Biến toàn cục
y = 20  # Biến toàn cục


def my_function():
    z = 30  # Biến cục bộ
    print(f"Biến cục bộ: {z}")  # 30
    print(f"Biến toàn cục: {x}")  # 10
    print(f"Biến toàn cục: {y}")  # 20


my_function()


bien_toan_cuc = "Đây là biến toàn cục"


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
def ham_ngoai():
    bien_bao_dong = "Biến enclosing"

    def ham_trong():
        nonlocal bien_bao_dong  # Khai báo biến là nonlocal
        bien_bao_dong = "Đã thay đổi biến enclosing"
        print(f"Từ hàm trong: {bien_bao_dong}")  # Truy cập biến bao đóng

    ham_trong()
    print(f"Từ hàm ngoài: {bien_bao_dong}")  # Truy cập biến bao đóng


# ========== 9. GỠ LỖI (DEBUGGING) ==========
"""
Gỡ lỗi là quá trình tìm và sửa lỗi trong mã nguồn.
Có nhiều công cụ và phương pháp để gỡ lỗi, bao gồm:
1. Sử dụng print() để in giá trị biến và trạng thái chương trình.
2. Sử dụng trình gỡ lỗi (debugger) để theo dõi từng bước thực thi của chương trình.
3. Sử dụng các công cụ gỡ lỗi tích hợp trong IDE (như PyCharm, Visual Studio Code).
4. Sử dụng các thư viện gỡ lỗi như pdb (Python Debugger).
"""
# ========== 10. TÀI LIỆU THAM KHẢO ==========
