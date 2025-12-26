# [Data Product Name]

> **Owner:** [Team Name] | **Contact:** [Email/Slack] | **Version:** [x.x.x]

## 📋 Overview

[Mô tả ngắn gọn data product này là gì, phục vụ mục đích gì]


## 🎯 Use Cases

Ai nên sử dụng data product này và để làm gì:

- **[Team/Use case 1]:** [Mô tả]
- **[Team/Use case 2]:** [Mô tả]


## 📊 Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `field_name` | string | ✅ | Mô tả field |


## 🔌 How to Access

### Kafka Topic

- **Topic name:** `[topic.name]`
- **Format:** Avro
- **Schema Registry:** `http://schema-registry:8081`

**Ví dụ consume message:**

    kafka-console-consumer --bootstrap-server localhost:9092 --topic [topic.name]

### S3 (Data Lake)

- **Path:** `s3://bucket/path/`
- **Format:** Parquet
- **Partitioned by:** `[date/hour]`


## ⏱️ SLA

| Metric | Commitment |
|--------|------------|
| Freshness | Data không cũ quá [X phút/giờ] |
| Availability | [99.x%] |
| Update Frequency | [Realtime/Hourly/Daily] |


## 📈 Data Quality

Các quality checks được áp dụng:

- ✅ `field_name`: not null, unique
- ✅ `amount`: > 0

Chi tiết: xem file `quality/expectations.yaml`


## ⚠️ Known Limitations

- [Limitation 1]
- [Limitation 2]


## 📝 Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | YYYY-MM-DD | Initial release |
