FROM python:3.10-slim-buster

# Set work directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose FastAPI (8000) and Streamlit (8501) ports
EXPOSE 8000 8501

# Default: run FastAPI backend
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
