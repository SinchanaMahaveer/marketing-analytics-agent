# Marketing Analytics Agent — AI-Powered Campaign Intelligence

> Upload your marketing data. Ask questions in plain English. Get instant insights and recommendations — no SQL, no Excel formulas, no analyst needed.

**🔗 Live Demo:** [Try it here →](https://marketing-analytics-agent-001.streamlit.app/)

---

## What Problem Does This Solve?

Marketing managers waste 5–10 hours every week manually pulling reports, writing pivot tables, and waiting for analysts to answer basic questions like:

- *"Which channel is burning our budget?"*
- *"Which customer segment converts the best?"*
- *"Should we cut Instagram or YouTube spend?"*

This agent answers all of that **instantly**, in plain English, from any CSV or Excel file.

---

##  Key Features

- **Plain English questions** — no SQL, no formulas, just type what you want to know
- **Works with any data** — upload any marketing CSV or Excel file
- **Conversation memory** — ask follow-up questions, it remembers context
- **Instant business recommendations** — not just numbers, but what to do about them
- **Zero technical knowledge needed** — built for marketing managers, not analysts

---

## Live Demo

**[Click here to try the live app](https://marketing-analytics-agent-001.streamlit.app/)**

**Sample questions to try:**
| Question | What it tells you |
|---|---|
| "Which channel has the best ROI?" | Where to increase budget |
| "Which customer segment converts most?" | Who to target |
| "What is our average acquisition cost by channel?" | Where you're overspending |
| "Which campaigns should I cut if budget drops 30%?" | Data-backed budget decisions |
| "Write a CMO-ready performance summary" | Executive report in seconds |

---

##  Tech Stack

| Layer | Technology |
|---|---|
| AI / LLM | Anthropic Claude API (claude-sonnet-4-6) |
| Data Analysis | Python, Pandas, NumPy |
| Frontend | Streamlit |
| Deployment | Streamlit Cloud |
| Data Support | CSV, Excel (.xlsx, .xls) |

---

## How to Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/SinchanaMahaveer/marketing-analytics-agent
cd marketing-analytics-agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

You'll need a free Anthropic API key from [console.anthropic.com](https://console.anthropic.com)

---

## 📁 Project Structure

```
marketing-analytics-agent/
├── app.py              # Full Streamlit web app
├── requirements.txt    # Python dependencies
└── README.md           # You are here
```

---

## Built For Freelance Clients

This project is part of my AI Analytics portfolio. I build custom versions of this for:

- **E-commerce brands** — sales, returns, customer behaviour analysis
- **Marketing agencies** — multi-client campaign reporting automation
- **D2C brands** — ROAS, CAC, conversion rate intelligence
- **SaaS companies** — product analytics and user behaviour agents

**Looking for a custom analytics agent for your business?**

📧 [sinchanamahaveer@gmail.com](mailto:sinchanamahaveer@gmail.com)
🔗 [GitHub →](https://github.com/SinchanaMahaveer)

---

## How It Works

```
User asks a question in plain English
        ↓
Claude reads the question + your data schema
        ↓
Claude writes pandas code to answer it
        ↓
Code runs on your actual data
        ↓
Claude reads the result + writes business insight
        ↓
You get an answer + recommendation in seconds
```

No hardcoded logic. No if/else rules. The agent figures out how to answer any question dynamically.

---

##  Example Output

**Question:** *"Which channel has the best ROI and lowest acquisition cost?"*

**Agent response:**
> Google Ads leads with an average ROI of 7.2x and acquisition cost of $8,400 — significantly better than Meta Ads (5.1x ROI, $12,300 CAC). Recommendation: shift 20-25% of Meta budget to Google Ads, specifically targeting the Health & Wellness segment where conversion rates are 3x the platform average.

---

## Data Privacy

- Your data is never stored on any server
- All analysis runs in-session memory only
- Files are discarded when you close the browser
- API calls go directly to Anthropic — no third-party storage

---

## About the Builder

**Sinchana Mahaveer** — Ex-Amazon | Product Data Analyst |AI Analytics Engineer

4+ years building data systems at Amazon scale. Now helping businesses turn raw data into automated intelligence using Python and AI agents.

- 🏢 Previously: Amazon Payments(4.5years)
- 🛠️ Skills: Python, SQL, Pandas, Anthropic API, Streamlit, Tableau
- 📍 Based in Bangalore, India — available for Remote freelance globally

📧 [sinchanamahaveer@gmail.com](mailto:sinchanamahaveer@gmail.com)

**[View my full portfolio →](https://github.com/SinchanaMahaveer)**

---

## 📄 License

MIT License — free to use and modify with attribution.

---

*If this helped you, consider giving it a ⭐ on GitHub — it helps others find it!*
