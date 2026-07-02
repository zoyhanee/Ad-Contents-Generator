# Ad-Contents-Generator

> An AI-powered advertising content generation service that helps small businesses create high-quality marketing copy and promotional images with minimal effort.

---

# 📌 Project Overview

**Ad-Contents-Generator** is an AI-powered web service designed to simplify the creation of marketing content for small businesses.

Users upload a product image and provide basic product information. The system automatically generates engaging marketing copy and promotional images optimized for online advertising.

Our goal is to reduce the time and cost required to produce professional-quality advertisements by leveraging state-of-the-art generative AI models.

---

# ✨ Key Features

- 🖼️ Product image upload
- ✍️ AI-generated marketing copy
- 🎨 AI-generated promotional images
- 🎯 Multiple advertising styles
- 📱 SNS-ready advertising content
- ⚡ FastAPI-based backend service
- 🚀 GPU-accelerated inference (NVIDIA L4)

---

# 🏗️ System Architecture

```text
                User
                  │
                  ▼
          Streamlit Frontend
                  │
             HTTP Request
                  │
                  ▼
           FastAPI Backend
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
 Text Generation      Image Generation
      Model                Model
        │                   │
        └─────────┬─────────┘
                  ▼
      Generated Advertisement
```

---

# 🛠 Tech Stack

## Frontend

- Streamlit

## Backend

- FastAPI
- Uvicorn

## AI Framework

- PyTorch
- Hugging Face Transformers
- Diffusers

## Infrastructure

- Google Cloud Platform (GCP)
- NVIDIA L4 GPU
- Docker

---

# 📁 Project Structure

```text
Ad-Contents-Generator/
│
├── backend/
│   ├── app/
│   │   ├── api/            # API Routers
│   │   ├── core/           # Configuration
│   │   ├── ml/             # AI Models & Inference
│   │   ├── schemas/        # Pydantic Schemas
│   │   ├── services/       # Business Logic
│   │   ├── utils/          # Utility Functions
│   │   └── main.py
│   │
│   └── tests/
│
├── frontend/
│   ├── app.py
│   ├── pages/
│   ├── components/
│   └── assets/
│
├── weights/
│   ├── text/
│   └── image/
│
├── outputs/
├── docs/
├── scripts/
│
├── requirements.txt
├── docker-compose.yml
├── README.md
└── .gitignore
```

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone git@github.com:zoyhanee/Ad-Contents-Generator.git

cd Ad-Contents-Generator
```

## 2. Create Virtual Environment

```bash
python3 -m virtualenv .venv

source .venv/bin/activate
```

## 3. Install PyTorch (CUDA)

```bash
pip install torch torchvision torchaudio \
--index-url https://download.pytorch.org/whl/cu128
```

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🚀 Run

## Backend

```bash
cd backend

uvicorn app.main:app --reload
```

The backend server will be available at:

```
http://localhost:8000
```

---

## Frontend

```bash
streamlit run frontend/app.py
```

---

# 📚 Development Workflow

```text
feature/*
      │
      ▼
develop
      │
      ▼
main
```

### Branch Strategy

- **main** : Production-ready branch
- **develop** : Integration branch
- **feature/*** : Individual feature development

All new features should be developed in feature branches and merged into `develop` through Pull Requests.

---

# 👥 Team

| Name | Role |
|------|------|
| TBD | Project Manageer |
| TBD | Frontend |
| TBD | AI Model |
| TBD | Backend · AI Integration |

---

# 📌 Roadmap

### Sprint 1

- Development environment setup
- FastAPI backend
- Streamlit frontend
- Backend-Frontend integration

### Sprint 2

- Text generation model integration
- Image generation model integration
- API implementation

### Sprint 3

- UI/UX improvement
- Docker deployment
- Final presentation

---

# 🎯 Future Improvements

- Fine-tuned image generation model
- Personalized advertisement styles
- Multi-language support
- One-click SNS publishing
- A/B testing for generated advertisements
- Automatic banner generation

---

# 📄 License

This project was developed for educational purposes as part of the Codeit AI Project.