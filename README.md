# 🏥 Medical Assistant Chatbot 

The Medical Assistant Chatbot is an AI-powered application that leverages Retrieval Augmented Generation (RAG) to provide accurate medical information. It uses a comprehensive medical knowledge base to answer health-related queries with reliable, sourced information.


## Tech Stack

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Vector Database**: Pinecone
- **Embeddings**: Hugging Face (sentence-transformers)
- **LLM**: OpenAI, Groq (llama-3.1-8b-instant)
- **Infrastructure**: AWS (EC2, ECR)
- **CI/CD**: GitHub Actions

## Project Structure

```
medical_chatbot/
├── app.py              # Streamlit frontend interface
├── main.py            # FastAPI backend server
├── pinecone_index.py  # Vector embedding creation script
├── Dockerfile         # Container configuration
├── src/
│   ├── helper.py      # Utility functions
│   └── prompt.py      # LLM prompt templates
├── data/              # Medical knowledge base
└── requirements.txt   # Project dependencies
```

## Local Development Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd medical_chatbot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**
Create a `.env` file:
```env
GROQ_API_KEY=your_groq_api_key
PINECONE_API_KEY=your_pinecone_api_key
```

4. **Create vector embeddings**
```bash
python pinecone_index.py
```

5. **Run the application**
In separate terminals:
```bash
# Terminal 1: Backend
uvicorn main:app --reload --port 8000

# Terminal 2: Frontend
streamlit run app.py
```

## AWS Deployment Guide

### 1. AWS IAM Setup

1. Login to AWS console
2. Create an IAM user with the following access:
   - AmazonEC2ContainerRegistryFullAccess
   - AmazonEC2FullAccess

### 2. ECR Repository Setup

1. Create a new ECR repository:
```bash
aws ecr create-repository --repository-name medicalbot
```
2. Note the repository URI: 
   `415866595327.dkr.ecr.us-east-1.amazonaws.com/medicalbot`

### 3. EC2 Instance Setup

1. Launch an Ubuntu EC2 instance
2. Configure security groups:
   - Allow SSH (Port 22)
   - Allow HTTP (Port 80)
   - Allow HTTPS (Port 443)
   - Allow application ports (8000, 8501)

3. Install Docker on EC2:
```bash
sudo apt-get update -y
sudo apt-get upgrade -y
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker
```

### 4. GitHub Actions Configuration

1. Configure repository secrets:
   - AWS_ACCESS_KEY_ID
   - AWS_SECRET_ACCESS_KEY
   - AWS_DEFAULT_REGION
   - ECR_REPO
   - PINECONE_API_KEY
   - GROQ_API_KEY

2. Set up EC2 as self-hosted runner:
   - Go to repository Settings > Actions > Runners
   - Click "New self-hosted runner"
   - Choose operating system
   - Follow the provided setup commands on your EC2 instance

### 5. Deployment Process

The deployment process follows these steps:
1. Build Docker image of the source code
2. Push Docker image to ECR
3. Pull image from ECR to EC2
4. Launch Docker container on EC2

The GitHub Actions workflow will automate this process on every push to the main branch.

## API Documentation

### Endpoints

- `POST /ask`: Submit a medical question
  ```json
  {
    "question": "string",
    "context": "string"
  }
  ```
- `GET /health`: Health check endpoint


## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! 

📩 **Need professional support?** [Contact me](mailto:hafizshakeel1997@gmail.com) for assistance.  
