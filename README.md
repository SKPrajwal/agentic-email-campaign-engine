# Autonomous Email Campaign Engine – Agentic GenAI

An agentic AI system that autonomously plans, generates, reviews, and sends personalized marketing campaign emails using coordinated LLM-driven agents and a retrieval-augmented workflow.

---

## 🚀 Overview

Modern campaign creation often requires multiple manual steps — product research, marketing strategy, content writing, review, and delivery. This project introduces an **agentic AI workflow** that automates the entire lifecycle of campaign email generation.

Given a campaign topic (e.g., *Halloween Sale* or *Valentine’s Offers*), the system orchestrates multiple specialized agents to retrieve relevant products, curate selections, define strategy, generate high-quality email content, validate messaging, and finally send the campaign email.

This solution is designed for experimentation with **autonomous marketing workflows**, rapid prototyping, and enterprise-style GenAI orchestration patterns.

---

## 🧠 Key Features

* Multi-Agent Orchestration (Planner → Retriever → Curator → Strategist → Writer → Critic)
* Retrieval-Augmented Generation using Vector Search
* Automated Campaign Strategy Creation
* LLM-Generated Marketing Email Content
* Built-in Quality Review via Critic Agent
* Dynamic Email Rendering and SMTP Delivery
* Modular, Extensible Agent Architecture

---

## 🏗️ High-Level Architecture

The system follows a **planner-driven agentic execution model** where each agent performs a specialized responsibility within the campaign pipeline.

```
User Input (Campaign Topic)
        ↓
----------------------------------------
Planner Agent
        ↓
----------------------------------------
Retriever Agent (Agents Cluster)
        ↓
Curator Agent
        ↓
Strategy Agent
        ↓
Writer Agent
        ↓
----------------------------------------
Critic Agent (Quality Review)
        ↓
----------------------------------------
Email Renderer / Sender
```

### Core Components

* **Planner Agent** – Defines execution steps for the workflow
* **Retriever Agent** – Fetches relevant products using vector search
* **Curator Agent** – Filters and selects campaign-ready items
* **Strategy Agent** – Creates marketing messaging direction
* **Writer Agent** – Generates structured campaign email content
* **Critic Agent** – Reviews and refines the generated email
* **Email Renderer** – Sends finalized campaign via SMTP

---

## ⚙️ Tech Stack

* Python
* Bedrock LLM models
* Custom Agentic Workflow Pattern
* FAISS Vector Database (RAG)
* Pandas
* SMTP Email Integration
* CLI Interface

---

## 📂 Project Structure

```
project/
│
├── agents/            # Planner, Retriever, Curator, Strategy, Writer, Critic agents
├── rag/               # Vector store and indexing logic
├── app/               # Email renderer and sender
├── data/              # Sample product datasets
├── main.py            # Workflow entry point
└── README.md
```

---

## ▶️ How to Run (Quick Start)
------------------------------------------------------------------
✅ Prerequisites
------------------------------------------------------------------

Make sure the following tools are installed before setup:
Python 3.10+
Git
VS Code (recommended for development)
AWS CLI (required as we are using AWS Bedrock models)

------------------------------------------------------------------
⚙️ Environment Setup
------------------------------------------------------------------

1. Clone Repository
git clone https://github.com/SKPrajwal/agentic-email-campaign-engine.git
cd agentic-email-campaign-engine

2. Create Virtual Environment
python -m venv .venv

Activate environment:
Windows
.venv\Scripts\activate
Mac/Linux
source .venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Configure AWS Profile in user/.aws file

5. Login to AWS Profile to authenticate and use Bedrock models
- IAM user has Bedrock access
- Region supports Bedrock models


------------------------------------------------------------------
▶️ Run the Agentic Workflow
------------------------------------------------------------------
python main.py

When prompted:

Topic for Campaign:
- Enter a campaign theme such as:

Halloween Sale
Valentine Offers
Summer Clearance

Enter TO EMAIL for campaign:
- Enter receivers email id


---


## 🧪 Example Usage

**Input**

```
Topic for Campaign:
Valentine Week
```

**Output**

```
Subject: Celebrate Love with Exclusive Valentine Deals ❤️
Body:
Discover hand-picked gifts curated just for you...
```

---

## 📌 Future Enhancements

* Multi-channel campaigns (SMS, Push Notifications)
* Campaign Performance Analytics Agent
* Feedback-Driven Learning Loop
* A/B Testing Strategy Agent
* UI Dashboard for Campaign Management

---

## 🤝 Notes

This repository is a prototype demonstrating enterprise-style **Agentic GenAI orchestration** for autonomous marketing workflows. The focus is on modular design, experimentation, and extensibility.
