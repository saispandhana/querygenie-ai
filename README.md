QueryGenie AI – GenAI-Powered Data Analytics Assistant

Overview

QueryGenie AI is a natural language data analytics system that enables users to query structured datasets using plain English—without writing SQL or manually exploring data.

The system combines Google Gemini (LLM) for query understanding with Python (pandas) for execution, translating user questions into structured query plans and producing accurate, deterministic results.


Why QueryGenie AI?

Traditional GenAI approaches often rely entirely on LLMs, which can lead to incorrect numerical outputs when working with structured data.

QueryGenie AI solves this by using a hybrid architecture:

         1.LLM (Gemini)→ Converts user queries into structured JSON query plans
         2.Execution Engine (pandas)→ Performs accurate computations on real data

This ensures:

✅ Accurate and reliable results (no hallucinated numbers)
✅ Scalable analytics over structured datasets
✅ Flexible handling of real-world user queries

Key Features:

1.Natural Language Querying (No SQL required)
2.LLM-based Query Planning (Gemini → JSON execution plan)
3.Deterministic Execution using pandas
4.Supports:

  * Aggregations (sum, average, count)
  * Filtering and conditional queries
  * Group-by analysis (region, category, product)
  * Top-N queries (e.g., top 5 products)
  * Highest / Lowest value queries
  * Distinct value extraction
5.Fuzzy Matching & Synonym Handling
       (e.g., "softdrinks" → "Soft Drinks", "people" → "Customer_ID")
6.Intelligent Column Mapping (handles schema variations)

System Architecture
![Architecture](architecture.png)

Query Execution Flow
![Sequence](sequence.png)

Explanation
- The architecture diagram shows how natural language queries are processed through the LLM and executed using pandas.
- The sequence diagram illustrates the step-by-step flow from user query to structured query plan to final answer generation.

## 🔄 Step-by-Step Query Lifecycle

### 1️⃣ Input Layer – User Query

A business user asks a question in natural language, such as:
*"How many people bought drinks?"*

The goal is to retrieve accurate insights without writing SQL or code.

---

### 2️⃣ Intelligence Layer – Query Understanding (LLM)

The QueryGenie Orchestrator forwards the query to **Google Gemini (LLM)**.

Gemini interprets the user’s intent and converts the question into a structured JSON query plan**, defining:

* the required operation (e.g., count, sum)
* filters (e.g., Category = "Drinks")
* grouping logic (if applicable)


Execution Layer – Deterministic Processing

The JSON query plan is passed to the **Execution Engine (Python + pandas)**.

This layer performs the actual computation by applying filters, aggregations, and transformations on the dataset.


Data Layer – Source of Truth

The executor retrieves data from the CSV dataset, ensuring all computations are performed on real data rather than inferred responses.

Only the relevant subset of data is processed based on the query plan.


Output Layer – Final Result

The computed result is formatted into a clean, human-readable response, such as:

"42 users bought drinks."

This ensures fast, accurate, and reliable insights for the user.



Key Design Insight

QueryGenie AI separates:

understanding (LLM)→ Converts natural language into structured plans
Execution (pandas)→ Performs accurate computations

This hybrid approach avoids LLM hallucinations and ensures reliable analytics.

User Query
→ Gemini (LLM generates structured query plan)
→ Query Executor (Python + pandas)
→ Final Answer

Example Workflow

User Query:

> How many people bought soft drinks?

System Flow:

1. Gemini converts the query into a structured JSON plan
2. Executor applies filters and aggregation using pandas
3. System returns an accurate numerical result

Example Queries

* How many people got soft drinks?
* Which product has the highest price?
* Show top 5 highest priced products
* Total sales by category
* Average price by region
* Which region has the highest revenue?


Tech Stack

* Python
* Pandas
* Google Gemini API
* Prompt Engineering
* Natural Language Processing (NLP)



Setup

1. Clone the repository
2. Install dependencies:
   `pip install -r requirements.txt`
3. Add API key in `.env`
4. Run the application:
   `python app.py`


Environment Variables

Create a `.env` file:

GEMINI_API_KEY=AIzaSyAstOrzMGUo-DXAV9NO6y9HpzmeNLBENy4

Future Enhancements

* AWS Glue integration
* SQL backend support
* Streamlit-based web UI
* Conversational memory (multi-turn queries)
* Multi-dataset joins


 Key Insight

This project demonstrates how combining Generative AI with deterministic data processing can produce reliable, production-ready analytics systems—overcoming the limitations of LLM-only solutions.



Author

Sai Spandhana Billupati

