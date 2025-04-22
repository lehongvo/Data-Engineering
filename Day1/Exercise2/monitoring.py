from google.cloud import monitoring_v3
import time
import logging


def setup_monitoring(project_id):
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    def create_custom_metric(metric_type, description):
        descriptor = monitoring_v3.MetricDescriptor()
        descriptor.type = f"custom.googleapis.com/{metric_type}"
        descriptor.metric_kind = monitoring_v3.MetricDescriptor.MetricKind.GAUGE
        descriptor.value_type = monitoring_v3.MetricDescriptor.ValueType.DOUBLE
        descriptor.description = description

        try:
            descriptor = client.create_metric_descriptor(
                name=project_name, metric_descriptor=descriptor
            )
            logging.info(f"Created {descriptor.name}")
        except Exception as e:
            logging.error(f"Error creating metric descriptor: {e}")

    def write_metric(metric_type, value, resource_labels=None):
        series = monitoring_v3.TimeSeries()
        series.metric.type = f"custom.googleapis.com/{metric_type}"

        if resource_labels:
            for key, value in resource_labels.items():
                series.resource.labels[key] = value

        series.resource.type = "gce_instance"

        point = monitoring_v3.Point()
        point.value.double_value = value
        point.interval.end_time.seconds = int(time.time())
        series.points = [point]

        try:
            client.create_time_series(name=project_name, time_series=[series])
            logging.info(f"Wrote {metric_type} value: {value}")
        except Exception as e:
            logging.error(f"Error writing time series: {e}")

    # Create custom metrics
    create_custom_metric("bigquery/query_latency", "BigQuery query execution latency")
    create_custom_metric("bigquery/query_count", "Number of BigQuery queries executed")
    create_custom_metric("app/request_count", "Number of HTTP requests")
    create_custom_metric("app/error_count", "Number of application errors")

    return write_metric
