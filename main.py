import os
import time

import logfire

os.environ["OTEL_METRIC_EXPORT_INTERVAL"] = "5000"
os.environ["OTEL_EXPORTER_OTLP_PROTOCOL"] = "http/protobuf"
os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "http://localhost:4318"
os.environ["LOGFIRE_HTTPX_CAPTURE_ALL"] = "true"

logfire.configure(
    service_name="service_name",
    send_to_logfire=False,
)

logfire.info("User logged in")


@logfire.instrument
def make_llm_call():
    time.sleep(1)  # Simulate a delay for the LLM call


def my_logger():
    with logfire.span("Processing request {request_id}", request_id=123):
        make_llm_call()
        logfire.info("some state", state={"key": "value"})
        make_llm_call()


if __name__ == "__main__":
    while True:
        my_logger()
        time.sleep(20)
