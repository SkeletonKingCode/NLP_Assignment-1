FROM python:3.11-slim

WORKDIR /app

# Copy requirements first (for Docker layer caching)
COPY api/requirements.txt /app/api/requirements.txt
RUN pip install --no-cache-dir -r api/requirements.txt

# Copy application code and data
COPY api/ /app/api/
COPY BSETokenizer/ /app/BSETokenizer/
COPY Trigram_Language_Model/ /app/Trigram_Language_Model/
COPY Tokenized_Dataset/ /app/Tokenized_Dataset/

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
