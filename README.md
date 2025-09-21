# ShopUNow-Agent
Agent for nternal employees and external customers of a  fictional ecomm company.
Got it ✅
Here’s a polished **README.md** draft for your project — written so that anyone (dev, reviewer, or evaluator) can quickly understand **what the agent does, how it works, how to run it, and what makes it special**.

---


# ShopUNow Agentic FAQ & Support Assistant

An **agentic AI assistant** for **ShopUNow** that handles customer queries across multiple departments:
- 🛒 **Orders & Returns**
- 💳 **Payments & Billing**
- ☎️ **Customer Support**
- 👩‍💼 **HR & IT Helpdesk**

It combines:
- **Intent routing** (order status, return, ticket creation, HR policies, etc.)
- **Sentiment detection** (automatic escalation if user is upset)
- **Department classification with confidence**
- **Vector-based FAQ retrieval (RAG)** with fuzzy fallback
- **Escalation to human support** when confidence is low or the query is ambiguous  

---

## 🚀 Features

- **Multi-intent Routing**
  - `order_status` – tracks orders (asks for Order ID if missing).
  - `return_create` – initiates product returns.
  - `ticket` – files support tickets for complaints.
  - `rag` – answers FAQs from JSONL dataset using embeddings + FAISS.
  - `human_escalation` – auto-escalates for angry users or ambiguous queries.

- **Sentiment Awareness**
  - Negative sentiment → bypasses automation and sends directly to human.

- **Confidence-based Escalation**
  - If department classification is **low confidence** or FAQ similarity is below a **dept-specific threshold**, the query is **escalated** instead of returning the wrong answer.

- **Clean FAQ Answers**
  - Extracts only the `A:` part from “Q:/A:” style FAQs for clean, user-friendly responses.

- **Safe Defaults**
  - When the system isn’t confident, it explicitly says so and routes to human support instead of hallucinating.

---

## 📂 Project Structure

```

.
├── shopunow\_faqs.jsonl     # FAQ dataset (questions, answers, departments)
├── notebook.ipynb          # Jupyter/Colab notebook with full workflow
├── README.md               # This file

````

---

## ⚙️ How It Works

1. **FAQ Loader & Vector Store (Cell A.1)**  
   - Loads FAQs from JSONL → builds FAISS vector store with OpenAI embeddings.

2. **Agent Definition (Cell B)**  
   - Defines `AgentState`, routing logic, sentiment detection, and tool nodes.  
   - Handles escalation and confidence thresholds.  
   - Graph execution via `langgraph`.

3. **Testing (Cell B.1)**  
   - Runs test queries end-to-end.  
   - Prints intent, department, sentiment, tools used, and retrieved context.

---

## 🛠️ Setup & Installation

1. **Clone & Install** 
   ```bash
   git clone https://github.com/<your-repo>/shopunow-agent.git
   cd shopunow-agent
   pip install -r requirements.txt


2. **Environment Variables**

   * Create `.env` and set your OpenAI key:

     ```bash
     OPENAI_API_KEY=sk-xxxx
     



3. **Run Notebook**

   * Open `notebook.ipynb` in Jupyter or Colab.
   * Execute **Cell A.1** to build the vector store.
   * Execute **Cell B** to define the agent.
   * Execute **Cell B.1** to run the test cases.

---

## 📊 Example Queries

### ✅ Correct Answers

* **User:** `How do I pay with UPI?`
  **Agent:** `At checkout, select UPI, click 'Add New ID', and complete verification.`

* **User:** `What are your support hours?`
  **Agent:** `Live chat is available from 9 AM to 9 PM IST on our website and mobile app.`

* **User:** `How many leaves can I take?`
  **Agent:** `Employees can take up to 20 days of annual leave per year. Carryover is subject to approval.`

### ⚠️ Escalation Cases

* **User:** `When will I get my salary?`
  → Ambiguous → Escalates to **HR support**.

* **User:** `My order is delayed` (no Order ID provided)
  → Agent asks: `To check a specific order, please share your Order ID (e.g., ORD-1234).`

* **User (angry):** `This is frustrating, my refund still hasn’t come!`
  → Negative sentiment → **Escalated to human support**.

---

## 🧪 Customization

* **Add new FAQs** → update `shopunow_faqs.jsonl`.
* **Tune thresholds** → edit `DEPT_SIM_THRESHOLDS`.
* **Modify intents** → adjust `route_intent()` rules.
* **Expose confidence & reasons** → extend the `ask()` wrapper to return full payload.

---

## 🏗️ Tech Stack

* **LangChain / LangGraph** – workflow orchestration
* **FAISS** – vector similarity search
* **OpenAI Embeddings (Ada-002)** – semantic embeddings
* **VADER** – sentiment analysis
* **RapidFuzz** – fuzzy fallback for misspellings




