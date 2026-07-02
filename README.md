# Ad-Contents-Generator

> An AI-powered advertising content generation service that helps small businesses create high-quality marketing copy and promotional images with minimal effort.

---

## 📌 Project Overview

**Ad-Contents-Generator** is an AI-powered web service designed to simplify the creation of marketing content for small businesses.

Users upload a product image and provide basic product information. The system automatically generates engaging marketing copy and promotional images optimized for online advertising.

Our goal is to reduce the time and cost required to produce professional-quality advertisements by leveraging state-of-the-art generative AI models.

---

## ✨ Key Features

- 🖼️ Product image upload
- ✍️ AI-generated marketing copy
- 🎨 AI-generated promotional images
- 🎯 Multiple advertising styles
- 📱 SNS-ready advertising content
- ⚡ Fast API response
- 🚀 GPU-accelerated inference (NVIDIA L4)

---

## 🏗️ System Architecture

```text
                User
                  │
                  ▼
          Streamlit Frontend
                  │
                  ▼
           FastAPI Backend
                  │
                  ▼
         AI Generation Engine
         ├── Text Generation
         └── Image Generation
                  │
                  ▼
      Generated Advertisement
```

---

## 🛠 Tech Stack

### Frontend

- Streamlit

### Backend

- FastAPI
- Uvicorn

### AI Framework

- PyTorch
- Hugging Face Transformers
- Diffusers
- Stable Diffusion / FLUX (TBD)

### Infrastructure

- Google Cloud Platform (GCP)
- NVIDIA L4 GPU
- Docker

---

## 📁 Project Structure

```text
Ad-Contents-Generator/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── services/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── utils/
│   │   └── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── pages/
│   ├── components/
│   └── app.py
│
├── model/
│
├── outputs/
│
├── docs/
│
├── docker/
│
├── requirements.txt
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone git@github.com:zoyhanee/Ad-Contents-Generator.git

cd Ad-Contents-Generator
```

### 2. Create Virtual Environment

```bash
python3 -m virtualenv .venv

source .venv/bin/activate
```

### 3. Install PyTorch (CUDA)

```bash
pip install torch torchvision torchaudio \
--index-url https://download.pytorch.org/whl/cu128
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Run

### Backend

```bash
uvicorn app.main:app --reload
```

### Frontend

```bash
streamlit run frontend/app.py
```

---

## 📚 Development Workflow

```text
feature/*
      │
      ▼
Develop Branch
      │
      ▼
Main Branch
```

Each feature should be developed in an independent feature branch and merged through Pull Requests.

---

## 👥 Team

| Name | Role |
|------|------|
| Han Seong Taek | Backend · AI Integration |
| TBD | Frontend |
| TBD | AI Model |
| TBD | Project Management |

---

## 🎯 Future Improvements

- Fine-tuned image generation model
- Personalized advertisement styles
- Multi-language support
- One-click SNS publishing
- A/B testing for generated advertisements
- Automatic banner generation

---

## 📄 License

This project was developed for educational purposes as part of the Codeit AI Project.