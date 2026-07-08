# Ad-Contents-Generator

> AI-powered platform-specific advertising content generation service for small businesses.

Ad-Contents-Generator is an AI marketing assistant that analyzes products, recommends marketing strategies, and automatically generates advertising content optimized for different marketing platforms.

---

# 📌 Project Overview

Creating advertisements for multiple platforms is a time-consuming task for small business owners.

Even for the same product, advertising strategies differ depending on the platform.

For example,

- **Instagram** focuses on branding and storytelling.
- **Baemin** focuses on promotions and increasing customer orders.

This project leverages Generative AI to recommend marketing strategies and generate platform-specific advertisements automatically.

---

# 🎯 Problem Statement

Conventional AI advertisement generators simply generate text or images.

However, effective marketing requires much more than generation.

It requires:

- Product analysis
- Platform selection
- Marketing strategy
- Advertisement style
- Platform-specific optimization

Our goal is to automate this entire planning process.

---

# 💡 Solution

Instead of

```text
Product

↓

Advertisement
```

Ad-Contents-Generator provides

```text
Product

↓

AI Product Analysis

↓

Platform Recommendation

↓

Marketing Strategy Recommendation

↓

Advertisement Style Selection

↓

Platform-specific Advertisement Generation
```

---

# 🎯 Supported Platforms

## 📸 Instagram

Purpose

- Brand Awareness
- Social Media Marketing

Generated Contents

- Feed Advertisement Image
- Caption
- Hashtags

Advertising Characteristics

- Emotional
- Storytelling
- Lifestyle Branding

---

## 🍽️ Baemin

Purpose

- Increase Orders
- Promotion

Generated Contents

- Promotional Advertisement Image
- Event Copy
- Call-To-Action (CTA)

Advertising Characteristics

- Discount Promotion
- Order Conversion
- Event Marketing

---

# ✨ Core Features

## 📦 AI Product Analysis

Analyze uploaded products using AI.

Input

- Product Image
- Product Name
- Product Description
- Price

Output

- Product Category
- Product Characteristics
- Target Customers
- Marketing Highlights

---

## 📱 Platform Recommendation

Recommend the most suitable advertising platform.

Example

Instagram ⭐⭐⭐⭐⭐ (95)

Reason

This product has strong visual appeal and is suitable for SNS marketing.

---

## 📈 Marketing Strategy Recommendation

Recommend multiple advertising strategies.

Examples

- Emotional Marketing
- Promotion Event
- New Product Launch
- Brand Marketing

Each strategy includes

- Recommendation Score
- Expected Effect
- Recommendation Reason

---

## 🎨 Advertisement Style Selection

Users can customize advertisements by selecting different styles.

Supported Styles

- Emotional
- Premium
- Friendly
- Humorous
- Event Promotion

---

## 🖼 Platform-specific Advertisement Generation

### Instagram

Generate

- Feed Image
- Caption
- Hashtags

### Baemin

Generate

- Promotional Image
- Event Copy
- Call-To-Action

---

# 🚀 Service Flow

```text
Product Information
(Image, Name, Description, Price)

            │

            ▼

     AI Product Analysis

            │

            ▼

 Platform Recommendation

 Instagram / Baemin

            │

            ▼

Marketing Strategy Recommendation

            │

            ▼

Advertisement Style Selection

            │

            ▼

Advertisement Generation

            │

            ▼

Download
```

---

# 🤖 AI Pipeline

```text
             Product

                │

                ▼

      Vision-based Analysis

                │

                ▼

       Product Understanding

                │

                ▼

               LLM

      ┌─────────┼──────────┐

      ▼         ▼          ▼

 Platform   Strategy   Copy Generation

Recommend  Recommend

                │

                ▼

      Prompt Builder

                │

                ▼

   Diffusers / FLUX Model

                │

                ▼

 Advertisement Image
```

---

# ⚙️ Development Environment Setup

## 1. Clone Repository

```bash
git clone git@github.com:zoyhanee/Ad-Contents-Generator.git

cd Ad-Contents-Generator
```

---

## 2. Create Virtual Environment

### macOS / Linux

```bash
python3 -m venv .venv

source .venv/bin/activate
```

### Windows

```powershell
python -m venv .venv

.venv\Scripts\activate
```

---

## 3. Install PyTorch (Required)

PyTorch is **not included** in `requirements.txt` because the installation method depends on the user's environment (CPU or CUDA version).

### CUDA 12.8 (Recommended)

```bash
pip install torch torchvision torchaudio \
--index-url https://download.pytorch.org/whl/cu128
```

### CPU Only

```bash
pip install torch torchvision torchaudio
```

---

## 4. Install Project Dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Initialize Database

Before running the backend for the first time, initialize the SQLite database.

Move to the backend directory:

```bash
cd backend
```

Create all required database tables:

```bash
python -m app.db.init_db
```

Expected output:

Database tables created successfully.

This command creates the SQLite database and all required tables, including:

users
products
ad_projects
ad_strategies
ad_drafts
final_results

Run this command once after cloning the repository and installing the project dependencies.

---

## 6. Verify Installation

```bash
python -c "import torch; print(torch.__version__)"
```

If using an NVIDIA GPU:

```bash
python -c "import torch; print(torch.cuda.is_available())"
```

Expected output:

```text
True
```

---

# 🚀 Development Workflow

```text
Clone Repository
        │
        ▼
Create Virtual Environment
        │
        ▼
Install PyTorch
        │
        ▼
Install Project Dependencies
        │
        ▼
Initialize Database
        │
        ▼
Run Backend / Frontend
```

---