import streamlit as st
import pandas as pd
import anthropic
import plotly.express as px
import io

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Marketing Analytics Agent",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS for professional look ──────────────────────────
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    .built-by {
        font-size: 0.8rem;
        color: #888;
        text-align: center;
        margin-top: 2rem;
    }
    .sample-question {
        background: #f0f2f6;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        margin: 0.3rem 0;
        font-size: 0.85rem;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>📊 Marketing Analytics Agent</h1>
    <p>Upload your data. Ask anything. Get instant insights.</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Setup")
    
    api_key = st.text_input(
        "Anthropic API Key",
        type="password",
        help="Get your key at console.anthropic.com"
    )
    
    st.markdown("---")
    st.markdown("### 📁 Upload Your Data")
    
    uploaded_file = st.file_uploader(
        "CSV or Excel file",
        type=["csv", "xlsx", "xls"],
        help="Any marketing campaign data file"
    )

    st.markdown("---")
    st.markdown("### 💡 Sample Questions")
    
    sample_questions = [
        "Which channel has the best ROI?",
        "Which customer segment converts most?",
        "What is our average acquisition cost by channel?",
        "Which campaign type has highest engagement?",
        "If I cut 30% budget, which campaigns should go?",
        "Write a CMO-ready performance summary"
    ]
    
    for q in sample_questions:
        st.markdown(f"""<div class="sample-question">💬 {q}</div>""",
                   unsafe_allow_html=True)

    st.markdown("---")
    
    if st.button("🔄 Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.history = []
        st.rerun()

    st.markdown("""
    <div class="built-by">
        Built by [Your Name]<br>
        Ex-Amazon Data Analyst<br>
        AI Analytics Engineer
    </div>
    """, unsafe_allow_html=True)

# ── Load Data ─────────────────────────────────────────────────
df = None
if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Clean common issues
        for col in df.columns:
            if df[col].dtype == object:
                try:
                    cleaned = df[col].str.replace("$", "").str.replace(",", "").str.strip()
                    df[col] = pd.to_numeric(cleaned)
                except:
                    pass

        st.success(f"✅ Loaded **{df.shape[0]:,} rows** × **{df.shape[1]} columns**")

        # Show data overview
        with st.expander("📋 Data Preview", expanded=False):
            st.dataframe(df.head(10), use_container_width=True)

        # Show quick metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Rows", f"{df.shape[0]:,}")
        with col2:
            st.metric("Columns", df.shape[1])
        with col3:
            numeric_cols = df.select_dtypes(include="number").columns
            st.metric("Numeric Columns", len(numeric_cols))
        with col4:
            st.metric("Date Range", 
                     f"{df.shape[0]} records" if "Date" not in df.columns 
                     else f"{df['Date'].nunique()} dates")

    except Exception as e:
        st.error(f"Error loading file: {e}")

# ── Agent Setup ───────────────────────────────────────────────
tools = [
    {
        "name": "analyse_data",
        "description": "Write and execute Python pandas code to analyse the dataframe 'df'.",
        "input_schema": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Valid pandas code. Always store final answer in a variable called 'result' as a string."
                }
            },
            "required": ["code"]
        }
    }
]

def analyse_data(code: str, df: pd.DataFrame) -> str:
    try:
        import numpy as np
        local_vars = {"df": df, "pd": pd, "np": np}
        exec(code, {}, local_vars)
        result = local_vars.get("result", "No result variable found.")
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

def get_system_prompt(df: pd.DataFrame) -> str:
    columns = ", ".join(df.columns.tolist())
    dtypes = df.dtypes.to_string()
    sample = df.head(3).to_string()

    return f"""You are a senior marketing data analyst assistant.

You have ONE tool: 'analyse_data'. Use ONLY this tool.

The dataframe 'df' has these columns:
{columns}

Data types:
{dtypes}

Sample rows:
{sample}

STRICT CODING RULES:
1. 'df' is already loaded — never reload it
2. Only use pandas (pd) and numpy (np)
3. ALWAYS store answer in variable called 'result' as a string
4. NEVER use print() or any other function
5. Handle errors gracefully with try/except in your code

After results:
- Explain in plain English what the numbers mean
- Give a specific, actionable business recommendation
- Keep it concise — marketing managers are busy people
"""

def run_agent(question: str, df: pd.DataFrame, api_key: str, history: list) -> str:
    client = anthropic.Anthropic(api_key=api_key)
    history.append({"role": "user", "content": question})

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system=get_system_prompt(df),
        tools=tools,
        messages=history
    )

    while response.stop_reason == "tool_use":
        tool_use_block = next(b for b in response.content if b.type == "tool_use")
        code = tool_use_block.input["code"]
        tool_result = analyse_data(code, df)

        history.append({"role": "assistant", "content": response.content})
        history.append({
            "role": "user",
            "content": [{
                "type": "tool_result",
                "tool_use_id": tool_use_block.id,
                "content": tool_result
            }]
        })

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            system=get_system_prompt(df),
            tools=tools,
            messages=history
        )

    final = next(b.text for b in response.content if hasattr(b, "text"))
    history.append({"role": "assistant", "content": final})
    return final

# ── Chat Interface ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []

# Show welcome message if no conversation yet
if not st.session_state.messages:
    st.markdown("""
    ### 👋 Welcome! Here's how to get started:
    1. **Enter your Anthropic API key** in the sidebar
    2. **Upload your marketing data** (CSV or Excel)
    3. **Ask any question** about your data in plain English
    
    > Try: *"Which channel gives the best ROI?"* or *"Give me a performance summary"*
    """)

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask anything about your marketing data..."):
    if not api_key:
        st.error("⚠️ Please enter your Anthropic API key in the sidebar")
        st.stop()
    if df is None:
        st.error("⚠️ Please upload a data file first")
        st.stop()

    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Agent response
    with st.chat_message("assistant"):
        with st.spinner("🔍 Analysing your data..."):
            try:
                response = run_agent(
                    prompt,
                    df,
                    api_key,
                    st.session_state.history
                )
                st.markdown(response)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })
            except Exception as e:
                st.error(f"Error: {str(e)}")
