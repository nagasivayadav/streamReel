FROM python:3.11-slim

WORKDIR /code

# Install CA certificates so outbound HTTPS requests (e.g. to TMDB's API)
# can verify SSL certificates correctly — python:3.11-slim doesn't include
# these by default, which silently breaks libraries like `requests`.
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && \
    update-ca-certificates && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]