FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
COPY templates/ templates/
COPY static/ static/
RUN mkdir -p /app/data && chown -R 10001:10001 /app
USER 10001
EXPOSE 5000
CMD ["gunicorn", "--workers", "1", "--bind", "0.0.0.0:5000", "app:app"]
