# Orders Completed

> **Owner:** Orders Team | **Contact:** orders-team@company.com | #orders-data | **Version:** 1.0.0

## 📋 Overview

Data product chứa thông tin các đơn hàng đã hoàn thành thành công. Bao gồm thông tin về giá trị đơn hàng, phương thức thanh toán, và thời điểm hoàn thành.

**Lưu ý:** Chỉ bao gồm đơn hàng có status = "completed". Đơn hàng bị hủy hoặc đang pending không nằm trong data product này.


## 🎯 Use Cases

- **Analytics Team:** Tính daily/monthly revenue, phân tích trend
- **Marketing Team:** Segment khách hàng theo giá trị đơn hàng
- **Finance Team:** Báo cáo doanh thu, reconciliation
- **Customers Domain:** Enrich customer profile với purchase history


## 📊 Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `order_id` | string | ✅ | ID duy nhất của đơn hàng (UUID) |
| `customer_id` | string | ✅ | ID của khách hàng |
| `total_amount` | double | ✅ | Tổng giá trị đơn hàng |
| `currency` | string | ✅ | Loại tiền tệ (default: VND) |
| `items_count` | int | ✅ | Số lượng sản phẩm |
| `payment_method` | string | ✅ | Phương thức thanh toán |
| `completed_at` | long | ✅ | Timestamp hoàn thành (ms) |
| `completed_date` | string | ✅ | Ngày hoàn thành (YYYY-MM-DD) |
| `shipping_address` | string | ❌ | Địa chỉ giao hàng |
| `notes` | string | ❌ | Ghi chú khách hàng |


## 🔌 How to Access

### Kafka Topic (Realtime)

- **Topic name:** `orders.completed.v1`
- **Format:** Avro
- **Schema Registry:** `http://schema-registry:8081`

**Consume messages:**

    # Với kafka-console-consumer
    kafka-console-consumer \
      --bootstrap-server localhost:9092 \
      --topic orders.completed.v1 \
      --from-beginning

    # Với kafkacat
    kafkacat -b localhost:9092 -t orders.completed.v1 -C

### S3 Data Lake (Batch)

- **Path:** `s3://datalake/orders/completed/`
- **Format:** Parquet
- **Partitioned by:** `completed_date`

**Query với AWS CLI:**

    aws s3 ls s3://datalake/orders/completed/

**Query với Spark/Presto:**

    SELECT * FROM orders_completed 
    WHERE completed_date = '2025-12-26'


## ⏱️ SLA

| Metric | Commitment |
|--------|------------|
| Freshness | Data không cũ quá 5 phút |
| Availability | 99.9% uptime |
| Update Frequency | Realtime (event-driven) |

**Monitoring Dashboard:** [Link to Grafana]


## 📈 Data Quality

Các quality checks được áp dụng:

- ✅ `order_id`: not null, unique
- ✅ `customer_id`: not null
- ✅ `total_amount`: not null, > 0
- ✅ `currency`: in ["VND", "USD", "EUR"]
- ✅ `completed_at`: not null, not in future
- ✅ No duplicate rows

Chi tiết: xem file `quality/expectations.yaml`


## ⚠️ Known Limitations

1. **Không bao gồm đơn hủy:** Đơn hàng bị cancel không có trong data product này. Xem `orders-cancelled` nếu cần.

2. **Historical data:** Data trước 2024-01-01 không có field `payment_method` (sẽ là null).

3. **Timezone:** Tất cả timestamp đều là UTC.


## 📝 Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-26 | Initial release |
