FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY data/ data/
COPY pipeline/ pipeline/
COPY backend/api.py .

RUN python pipeline/clean_data.py && python pipeline/score_leads.py

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/')"

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
