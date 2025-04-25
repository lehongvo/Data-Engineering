Tôi sẽ tạo 3 bài tập thực hành Terraform với độ khó tăng dần, tập trung vào data engineering với GCP. Tôi sẽ tạo các thư mục cho từng bài tập:

Tôi sẽ trình bày chi tiết 3 bài tập thực hành Terraform, mỗi bài tập sẽ có một mục tiêu và độ khó khác nhau:

Bài tập 1: Data Lake Cơ bản
Mục tiêu: Xây dựng data lake đơn giản với Cloud Storage và BigQuery

Tạo Cloud Storage bucket cho raw data
Tạo BigQuery dataset và table
Thiết lập quyền truy cập cơ bản
Cấu hình lifecycle management cho data
Chi tiết bài tập 1:

main.tf+51-1
Tôi sẽ tiếp tục với chi tiết bài tập 2 và 3:

Bài tập 2: Data Pipeline Infrastructure
Mục tiêu: Xây dựng infrastructure cho data pipeline hoàn chỉnh

main.tf+73-1
Let me continue with Exercise 3, which will be our most advanced exercise:

Bài tập 3: Data Warehouse Module với Disaster Recovery
Mục tiêu: Xây dựng một module Terraform có thể tái sử dụng cho data warehouse với khả năng disaster recovery

main.tf+82-1
Tôi sẽ tóm tắt chi tiết của 3 bài tập để bạn có thể bắt đầu thực hành:

Bài tập 1: Data Lake Cơ bản
Mục tiêu học tập:

Hiểu cách tạo và quản lý Cloud Storage bucket
Học cách thiết lập BigQuery dataset
Thực hành với lifecycle management cho data
Hiểu cách quản lý quyền truy cập cơ bản
Yêu cầu thực hành:

Tạo một GCP project
Setup Terraform với GCP provider
Tạo infrastructure theo code đã cung cấp
Thử nghiệm upload một file vào bucket
Kiểm tra quyền truy cập trong BigQuery
Bài tập 2: Data Pipeline Infrastructure
Mục tiêu học tập:

Học cách tạo VPC và subnet cho Dataflow
Hiểu cách setup multiple storage buckets cho các mục đích khác nhau
Thực hành với Pub/Sub cho streaming data
Tạo và quản lý service accounts
Yêu cầu thực hành:

Setup VPC network cho Dataflow
Tạo các storage buckets cho data lake và temporary files
Thiết lập Pub/Sub topic
Cấu hình service account với appropriate permissions
Test connectivity giữa các services
Bài tập 3: Data Warehouse Module với DR
Mục tiêu học tập:

Học cách tạo reusable Terraform modules
Hiểu về multi-region deployment
Thực hành với BigQuery data transfer
Học cách implement disaster recovery
Yêu cầu thực hành:

Tạo module structure
Setup primary và DR regions
Implement schema management
Cấu hình data transfer giữa regions
Test disaster recovery scenario
Để bắt đầu với bất kỳ bài tập nào, bạn cần:

Có một GCP project
Đã cài đặt Terraform và Google Cloud SDK
Có service account với đủ quyền
Export credentials:
