
import os
import requests
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="NexaBank | Digital Banking",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

API = os.getenv("API_BASE_URL", "http://localhost:8000")

st.markdown("""
<style>
.stApp {
    background: #080b0a;
    color: #f4f7f4;
}
[data-testid="stHeader"] {
    background: #080b0a;
}
.block-container {
    padding-top: 2rem;
    max-width: 1250px;
}
h1, h2, h3, p, label {
    color: #f4f7f4 !important;
}
.hero {
    background: linear-gradient(120deg, #14231b, #0c110e);
    border: 1px solid #263c2d;
    border-radius: 24px;
    padding: 48px;
    margin-top: 25px;
}
.hero h1 {
    font-size: 48px;
    line-height: 1.15;
}
.hero p {
    color: #aab7ad !important;
    font-size: 17px;
}
.green {
    color: #b7ff4a;
}
.panel {
    background: #111714;
    border: 1px solid #26342b;
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 15px;
}
.metric {
    color: #b7ff4a;
    font-size: 28px;
    font-weight: 700;
}
div.stButton > button {
    background: #b7ff4a;
    color: #101710;
    border: 0;
    border-radius: 10px;
    font-weight: 700;
    min-height: 42px;
}
div.stButton > button:hover {
    background: #d0ff87;
    color: #101710;
}
input, textarea {
    background: #111714 !important;
    color: white !important;
}
[data-testid="stSidebar"] {
    background: #101713;
}
hr {
    border-color: #26342b;
}
</style>
""", unsafe_allow_html=True)


def get_data(endpoint):
    try:
        response = requests.get(f"{API}/{endpoint}", timeout=20)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def show_home():
    st.markdown("## 🟢 NEXABANK")
    st.caption("SMARTER BANKING. BETTER TOMORROW.")

    st.markdown("""
    <div class="hero">
        <p class="green">THE FUTURE OF DIGITAL BANKING</p>
        <h1>Banking that moves<br>at your <span class="green">speed.</span></h1>
        <p>Experience a smarter way to manage transactions,
        understand your financial data and simplify banking operations.</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    left, right = st.columns([1, 1])

    with left:
        if st.button("Get Started", use_container_width=True):
            st.session_state.page = "Login"
            st.rerun()

    with right:
        if st.button("Login", use_container_width=True):
            st.session_state.page = "Login"
            st.rerun()

    st.divider()
    st.subheader("Banking made simple")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown('<div class="panel"><h3>⚡ Fast</h3><p>Streamlined banking operations.</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="panel"><h3>🔒 Secure</h3><p>Demo portal for banking workflows.</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="panel"><h3>📊 Smart</h3><p>Clear transaction insights.</p></div>', unsafe_allow_html=True)


def show_login():
    st.markdown("## 🟢 NEXABANK")
    st.write("")
    _, center, _ = st.columns([1, 1.2, 1])

    with center:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("Welcome back")
        st.caption("Sign in to your demo banking dashboard.")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Sign In", use_container_width=True):
            expected_user = os.getenv("DEMO_USERNAME", "demo")
            expected_password = os.getenv("DEMO_PASSWORD", "demo123")

            if username == expected_user and password == expected_password:
                st.session_state.logged_in = True
                st.session_state.page = "Overview"
                st.rerun()
            else:
                st.error("Invalid username or password.")

        st.caption("Demo login: demo / demo123")
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("← Back to Home"):
            st.session_state.page = "Home"
            st.rerun()


def show_overview():
    st.title("Overview")
    st.caption("Your banking operations at a glance.")

    summary = get_data("summary")
    records = summary.get("records", []) if summary else []

    total_transactions = sum(
        int(row.get("transaction_count", 0)) for row in records
    )
    total_amount = sum(
        float(row.get("total_amount", 0)) for row in records
    )

    a, b, c = st.columns(3)

    with a:
        st.markdown(
            f'<div class="panel"><p>Total Transactions</p><div class="metric">{total_transactions}</div></div>',
            unsafe_allow_html=True
        )
    with b:
        st.markdown(
            f'<div class="panel"><p>Processed Amount</p><div class="metric">₹{total_amount:,.2f}</div></div>',
            unsafe_allow_html=True
        )
    with c:
        st.markdown(
            f'<div class="panel"><p>ETL Status</p><div class="metric">Ready</div></div>',
            unsafe_allow_html=True
        )

    st.subheader("Daily Transaction Summary")
    if records:
        st.dataframe(pd.DataFrame(records), use_container_width=True)
    else:
        st.info("No summary available. Run ETL first.")


def show_transactions():
    st.title("Transactions")
    st.caption("View successfully processed transactions.")

    if st.button("Refresh Transactions"):
        st.rerun()

    data = get_data("transactions")

    if data and data.get("records"):
        df = pd.DataFrame(data["records"])
        search = st.text_input("Search transaction or customer")

        if search:
            mask = df.astype(str).apply(
                lambda col: col.str.contains(search, case=False, na=False)
            ).any(axis=1)
            df = df[mask]

        st.dataframe(df, use_container_width=True, hide_index=True)

        st.download_button(
            "Download CSV",
            df.to_csv(index=False),
            file_name="banking_transactions.csv",
            mime="text/csv"
        )
    elif data:
        st.info(data.get("message", "No transactions available."))
    else:
        st.error("Could not connect to the banking API.")


def show_reports():
    st.title("Reports")
    st.caption("Daily transaction reports.")

    data = get_data("summary")
    records = data.get("records", []) if data else []

    if records:
        df = pd.DataFrame(records)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.bar_chart(df.set_index("transaction_date")["total_amount"])
    else:
        st.info("No reports available. Run ETL first.")


def show_etl():
    st.title("ETL Operations")
    st.caption("Run the banking transaction processing workflow.")

    if st.button("▶ Run Legacy ETL", use_container_width=True):
        try:
            response = requests.post(f"{API}/etl/run", timeout=120)
            response.raise_for_status()
            result = response.json()

            st.success("ETL completed successfully!")
            a, b, c = st.columns(3)

            a.metric("Input Records", result.get("input_count", 0))
            b.metric("Processed", result.get("processed_count", 0))
            c.metric("Excluded", result.get("excluded_count", 0))

        except requests.RequestException as exc:
            st.error(f"ETL request failed: {exc}")

    st.divider()
    st.subheader("ETL Workflow")
    st.write("1. Read raw transaction data")
    st.write("2. Validate transaction records")
    st.write("3. Separate valid and excluded records")
    st.write("4. Generate daily summary")


def show_ai():
    st.title("AI Migration Assistant")
    st.caption("Ask questions about legacy ETL and PySpark migration.")

    question = st.text_area(
        "Your question",
        "Explain how legacy ETL filtering can be migrated to PySpark."
    )

    if st.button("Generate Explanation"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            try:
                response = requests.post(
                    f"{API}/ai/explain",
                    json={"question": question},
                    timeout=60
                )
                response.raise_for_status()
                st.write(response.json().get("explanation", "No explanation returned."))
            except requests.RequestException as exc:
                st.error(f"AI request failed: {exc}")


if "page" not in st.session_state:
    st.session_state.page = "Home"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    if st.session_state.page == "Login":
        show_login()
    else:
        show_home()
else:
    with st.sidebar:
        st.markdown("## 🟢 NEXABANK")
        st.caption("DIGITAL BANKING PORTAL")
        page = st.radio(
            "Navigation",
            ["Overview", "Transactions", "Reports", "ETL Operations", "AI Assistant"]
        )
        st.session_state.page = page

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.page = "Home"
            st.rerun()

    if st.session_state.page == "Overview":
        show_overview()
    elif st.session_state.page == "Transactions":
        show_transactions()
    elif st.session_state.page == "Reports":
        show_reports()
    elif st.session_state.page == "ETL Operations":
        show_etl()
    elif st.session_state.page == "AI Assistant":
        show_ai()


