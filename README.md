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
