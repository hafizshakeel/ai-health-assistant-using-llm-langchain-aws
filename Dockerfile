FROM python:3.10-slim-buster

# Set work directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose FastAPI (8000) and Streamlit (8501) ports
EXPOSE 8000 8501

# Run FastAPI backend
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# OR Run both FastAPI and Streamlit
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 & streamlit run app.py --server.port=8501 --server.address=0.0.0.0"]


