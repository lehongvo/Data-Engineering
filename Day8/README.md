# Apache Spark - Step by Step Learning Guide for Data Engineers

## 1. Giới thiệu về Apache Spark
- Tìm hiểu Spark là gì, tại sao lại dùng Spark trong xử lý dữ liệu lớn.
- So sánh Spark với Hadoop MapReduce.
- Cài đặt Spark (local hoặc trên cloud, khuyến khích dùng local mode để học cơ bản).

**Câu hỏi tự kiểm tra:**
- Apache Spark là gì? Ưu điểm của Spark so với Hadoop MapReduce?
- Spark có thể chạy ở những chế độ nào?

**Đáp án gợi ý:**
- Apache Spark là một framework mã nguồn mở dùng để xử lý dữ liệu lớn (big data) theo mô hình phân tán, hỗ trợ xử lý batch và streaming, có tốc độ nhanh nhờ sử dụng in-memory computing.
- Ưu điểm: Nhanh hơn MapReduce (do xử lý trên RAM), dễ lập trình hơn, hỗ trợ nhiều ngôn ngữ (Python, Scala, Java, R), có nhiều thư viện tích hợp (SQL, MLlib, GraphX, Streaming).
- Spark có thể chạy ở các chế độ: Local, Standalone, YARN, Mesos, Kubernetes.

## 2. Làm quen với SparkSession
- Hiểu SparkSession là gì, vai trò của nó trong Spark.
- Tạo một SparkSession đầu tiên bằng Python (PySpark).

**Câu hỏi tự kiểm tra:**
- SparkSession là gì? Tại sao cần SparkSession?
- Cách tạo một SparkSession trong PySpark?

**Đáp án gợi ý:**
- SparkSession là entry point (điểm khởi đầu) để làm việc với Spark, cho phép tạo DataFrame, thực thi SQL, đọc/ghi dữ liệu.
- Từ Spark 2.0 trở đi, SparkSession thay thế cho SQLContext và HiveContext.
- Tạo SparkSession trong PySpark:
  ```python
  from pyspark.sql import SparkSession
  spark = SparkSession.builder.appName("MyApp").getOrCreate()
  ```

## 3. DataFrames trong Spark
- DataFrame là gì? So sánh với Pandas DataFrame.
- Cách tạo DataFrame từ các nguồn dữ liệu khác nhau (CSV, JSON, Parquet, v.v.).
- Xem schema và preview dữ liệu.

**Câu hỏi tự kiểm tra:**
- DataFrame trong Spark khác gì với Pandas DataFrame?
- Làm thế nào để đọc file CSV thành DataFrame trong Spark?
- Làm sao để xem schema của một DataFrame?

**Đáp án gợi ý:**
- DataFrame trong Spark là tập hợp dữ liệu có cấu trúc (giống bảng SQL), được phân tán trên nhiều node trong cluster, hỗ trợ xử lý song song trên dữ liệu lớn. Pandas DataFrame chỉ chạy trên 1 máy, không tối ưu cho dữ liệu lớn.
- Spark DataFrame có thể xử lý dữ liệu lớn hơn bộ nhớ máy tính nhờ phân tán, còn Pandas bị giới hạn bởi RAM của máy.
- Spark DataFrame hỗ trợ lazy evaluation (chỉ thực thi khi cần lấy kết quả), Pandas thì thực thi ngay.

- Làm thế nào để đọc file CSV thành DataFrame trong Spark?
  
  **Đáp án:**
  - Sử dụng hàm `spark.read.csv()`:
    ```python
    df = spark.read.csv("duongdan/file.csv", header=True, inferSchema=True)
    ```
  - Tham số `header=True` để lấy dòng đầu làm tên cột, `inferSchema=True` để tự động nhận diện kiểu dữ liệu.

- Làm sao để xem schema của một DataFrame?
  
  **Đáp án:**
  - Dùng lệnh:
    ```python
    df.printSchema()
    ```
  - Để xem trước một vài dòng dữ liệu:
    ```python
    df.show(5)  # Xem 5 dòng đầu
    ```

## 4. Các thao tác cơ bản với DataFrame
- **Filtering**: Lọc dữ liệu với `.filter()` hoặc `.where()`.
- **Selecting Columns**: Chọn các cột với `.select()`.
- **Adding Columns**: Thêm cột mới với `.withColumn()`.
- **Dropping Columns**: Xoá cột với `.drop()`.
- **Renaming Columns**: Đổi tên cột với `.withColumnRenamed()`.

**Câu hỏi tự kiểm tra:**
- Cách lọc dữ liệu trong DataFrame?
- Làm sao để chọn nhiều cột trong DataFrame?
- Làm thế nào để thêm/xoá/đổi tên cột?

**Đáp án gợi ý:**
- Lọc dữ liệu:
  ```python
  df_filtered = df.filter(df["age"] > 18)
  # hoặc
  df_filtered = df.where(df["age"] > 18)
  ```
- Chọn nhiều cột:
  ```python
  df_selected = df.select("name", "age")
  ```
- Thêm cột:
  ```python
  from pyspark.sql.functions import col
  df_new = df.withColumn("age_plus_1", col("age") + 1)
  ```
- Xoá cột:
  ```python
  df_drop = df.drop("age")
  ```
- Đổi tên cột:
  ```python
  df_renamed = df.withColumnRenamed("old_name", "new_name")
  ```

## 5. Aggregation (Tổng hợp dữ liệu)
- Sử dụng `.groupBy()` và các hàm tổng hợp như `.count()`, `.sum()`, `.avg()`, `.min()`, `.max()`.
- Thực hành: Đếm số lượng, tính tổng, trung bình theo nhóm.

**Câu hỏi tự kiểm tra:**
- Cách sử dụng groupBy và các hàm tổng hợp?
- Làm sao để tính tổng, trung bình, đếm số lượng theo nhóm?

**Đáp án gợi ý:**
- Sử dụng groupBy và hàm tổng hợp:
  ```python
  df_grouped = df.groupBy("department").agg({"salary": "avg", "id": "count"})
  # Hoặc dùng hàm cụ thể
  from pyspark.sql.functions import avg, count
  df_grouped = df.groupBy("department").agg(avg("salary"), count("id"))
  ```

## 6. Join DataFrames
- Hiểu các loại join: inner, left, right, outer.
- Thực hành join hai DataFrame với `.join()`.

**Câu hỏi tự kiểm tra:**
- Có những loại join nào trong Spark?
- Cách thực hiện join hai DataFrame?

**Đáp án gợi ý:**
- Các loại join: inner, left (left_outer), right (right_outer), outer (full_outer), cross.
- Join hai DataFrame:
  ```python
  df_joined = df1.join(df2, df1["id"] == df2["user_id"], how="inner")
  # Thay how="inner" bằng "left", "right", "outer" tuỳ nhu cầu
  ```

## 7. SparkSQL
- Đăng ký DataFrame thành bảng tạm (temporary view).
- Viết truy vấn SQL trên Spark với `.sql()`.
- So sánh thao tác DataFrame API và SparkSQL.

**Câu hỏi tự kiểm tra:**
- Làm sao để đăng ký DataFrame thành bảng tạm?
- Cách viết truy vấn SQL trên Spark?
- Khi nào nên dùng DataFrame API, khi nào nên dùng SparkSQL?

**Đáp án gợi ý:**
- Đăng ký bảng tạm:
  ```python
  df.createOrReplaceTempView("my_table")
  ```
- Viết truy vấn SQL:
  ```python
  result = spark.sql("SELECT department, AVG(salary) FROM my_table GROUP BY department")
  result.show()
  ```
- DataFrame API phù hợp khi thao tác phức tạp, cần kiểm soát logic bằng code; SparkSQL phù hợp khi quen với SQL hoặc cần truy vấn nhanh.

## 8. Thực hành tổng hợp
- Làm một bài tập nhỏ: Đọc dữ liệu, filter, group, join, và truy vấn SQL.

**Câu hỏi tự kiểm tra:**
- Bạn có thể thực hiện đầy đủ các thao tác filter, group, join, SQL trên một bộ dữ liệu mẫu chưa?
- Bạn gặp khó khăn ở bước nào? Hãy ghi chú lại để hỏi mentor hoặc tra cứu thêm.

**Đáp án gợi ý:**
- Nếu bạn làm được các thao tác trên một bộ dữ liệu mẫu (ví dụ: file CSV về nhân viên, phòng ban), bạn đã nắm vững kiến thức cơ bản về Spark DataFrame và SparkSQL.
- Nếu gặp khó khăn, hãy xem lại ví dụ, đọc lại tài liệu hoặc hỏi mentor.

## 9. Tài liệu tham khảo
- [Official PySpark Documentation](https://spark.apache.org/docs/latest/api/python/)
- [Databricks Spark Guide](https://docs.databricks.com/getting-started/index.html)
- [Spark SQL, DataFrames and Datasets Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)

## 10. Bài tập thực hành

1. **Đọc dữ liệu CSV**
   - Đọc file CSV chứa thông tin nhân viên (ví dụ: id, name, age, department, salary) thành DataFrame.

2. **Xem thông tin dữ liệu**
   - In schema và hiển thị 5 dòng đầu tiên của DataFrame.

3. **Lọc dữ liệu**
   - Lọc ra các nhân viên có tuổi lớn hơn 30.

4. **Chọn cột**
   - Chỉ lấy các cột: name, age, department.

5. **Thêm cột mới**
   - Thêm cột mới 'age_plus_5' = age + 5.

6. **Tổng hợp dữ liệu**
   - Tính số lượng nhân viên và lương trung bình theo từng phòng ban.

7. **Join DataFrame**
   - Đọc thêm file CSV về phòng ban (department_id, department_name). Join với DataFrame nhân viên để lấy tên phòng ban.

8. **Đổi tên và xoá cột**
   - Đổi tên cột 'name' thành 'employee_name', xoá cột 'age_plus_5'.

9. **SparkSQL**
   - Đăng ký DataFrame thành bảng tạm và viết truy vấn SQL để lấy ra 3 phòng ban có lương trung bình cao nhất.

10. **Bài tập tổng hợp**
    - Thực hiện toàn bộ các thao tác trên với một bộ dữ liệu mới (tự tạo hoặc lấy từ Kaggle), ghi chú lại các lỗi gặp phải và cách khắc phục.

---

**Tips:**
- Luôn thực hành song song với lý thuyết.
- Ghi chú lại các lỗi thường gặp và cách khắc phục.
- Thử thay đổi dữ liệu đầu vào để hiểu rõ hơn về các thao tác. 