import os
import time
from typing import Any

import logfire
from fastapi import FastAPI

os.environ.setdefault("OTEL_EXPORTER_OTLP_PROTOCOL", "http/protobuf")
os.environ.setdefault("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4318")
os.environ.setdefault("OTEL_SERVICE_NAME", "fastapi-logfire-app")

# Configure Logfire. `send_to_logfire=False` keeps data local (OTEL export only).
logfire.configure(
    service_name=os.environ.get("OTEL_SERVICE_NAME", "fastapi-logfire-app"),
    send_to_logfire=False,
)

app = FastAPI(title="Logfire + OTEL FastAPI Example")

logfire.instrument_fastapi(app)


@logfire.instrument(record_return=True)
def call_llm(prompt: str) -> str:
    time.sleep(2)
    return f"dummy_response_for: {prompt}"


@logfire.instrument(record_return=True)
def save_to_db(message: str) -> None:
    _ = message
    time.sleep(0.1)


@app.get("/chat")
def chat(
    user_id: str = "user-1",
    session_id: str = "session-1",
    model_name: str = "dummy-model",
    prompt: str = "hello",
) -> dict[str, Any]:
    response = call_llm(prompt)
    save_to_db(response)
    return {"ok": True, "response": response}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
