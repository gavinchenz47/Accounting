import streamlit as st
import pandas as pd
from datetime import datetime
import os
import json
import requests
from supabase import create_client

from payroll import PayrollCalculator, CRA2026, create_excel_output
from provinces import PROVINCE_LIST, PROVINCES

# Page config
st.set_page_config(
    page_title="CRA Payroll Deductions Calculator",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide Streamlit branding and dev UI
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stToolbar"] {visibility: hidden;}
[data-testid="manage-app-button"] {visibility: hidden;}
[data-testid="stDecoration"] {visibility: hidden;}
._profileContainer_gzau3_53 {visibility: hidden;}
.viewerBadge_container__r5tak {display: none;}
iframe[title="streamlit_lottie.streamlit_lottie"] {display: none;}
[data-testid="stStatusWidget"] {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Supabase client
@st.cache_resource
def get_supabase():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)


SESSION_FILE = os.path.join(os.path.dirname(__file__), '.session.json')


def _save_session(access_token, refresh_token, email):
    """Save session to server-side file."""
    with open(SESSION_FILE, 'w') as f:
        json.dump({'access_token': access_token, 'refresh_token': refresh_token, 'email': email}, f)


def _load_session():
    """Load session from server-side file. Returns dict or None."""
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    return None


def _clear_session():
    """Delete session file."""
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)


def handle_auth_callback():
    """Handle Supabase OAuth PKCE callback."""
    params = st.query_params
    code = params.get("code")
    if code:
        try:
            supabase = get_supabase()
            response = supabase.auth.exchange_code_for_session({"auth_code": code})
            st.session_state.user = response.user
            st.session_state.access_token = response.session.access_token
            _save_session(response.session.access_token, response.session.refresh_token, response.user.email)
            st.query_params.clear()
            st.rerun()
        except Exception as e:
            st.error(f"Authentication failed: {str(e)}")
        return



def show_login():
    """Show login screen with Google sign-in."""
    handle_auth_callback()

    # Try restoring session from saved file
    if 'user' not in st.session_state or not st.session_state.user:
        saved = _load_session()
        if saved and saved.get('refresh_token'):
            try:
                supabase = get_supabase()
                response = supabase.auth.refresh_session(saved['refresh_token'])
                st.session_state.user = response.user
                st.session_state.access_token = response.session.access_token
                _save_session(response.session.access_token, response.session.refresh_token, response.user.email)
                st.rerun()
            except Exception:
                _clear_session()

    # If user was restored, don't show login
    if 'user' in st.session_state and st.session_state.user:
        return

    st.title("🇨🇦 CRA Payroll Deductions Calculator")
    st.markdown("---")

    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        st.markdown("### Sign in to continue")
        st.markdown("")

        if st.button("Sign in with Google", type="primary", use_container_width=True):
            try:
                supabase = get_supabase()
                response = supabase.auth.sign_in_with_oauth({
                    "provider": "google",
                    "options": {
                        "redirect_to": st.secrets["supabase"].get("redirect_url", "http://localhost:8502")
                    }
                })
                if response.url:
                    st.markdown(f'<meta http-equiv="refresh" content="0;url={response.url}">', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Sign in failed: {str(e)}")

        st.markdown("")
        st.caption("Your data is kept private and secure.")


# Main App
def main():
    # Sidebar
    with st.sidebar:
        st.title("💼 CRA Payroll")

        # User info and logout
        user = st.session_state.get('user')
        if user:
            st.caption(f"Signed in as **{user.email}**")
            if st.button("Sign Out", use_container_width=True):
                try:
                    get_supabase().auth.sign_out()
                except Exception:
                    pass
                _clear_session()
                st.session_state.pop('user', None)
                st.session_state.pop('access_token', None)
                st.rerun()

        st.markdown("---")
        st.markdown("### About")
        st.info("Automates CRA payroll calculations. Upload a CSV or enter employee data manually to get T4-ready Excel reports.")

        st.markdown("### 2026 CRA Rates")
        st.text(f"CPP: 5.95%")
        st.text(f"EI: 1.63%")
        st.text(f"Federal Tax: 14% (base)")

        st.markdown("---")
        st.markdown("### Need Help?")
        st.markdown("📄 Upload a CSV with columns:")
        st.markdown("`Employee Name, Gross Pay, YTD CPP, YTD EI, Pay Periods`")
    
    # Header
    st.title("🇨🇦 CRA Payroll Deductions Calculator")
    st.markdown("**Automated payroll calculations matching the CRA website - Get T4-ready Excel in seconds**")
    st.markdown("---")
    
    # Province and pay period
    col_prov, col_period = st.columns(2)

    # Auto-detect province from IP on first load
    if 'detected_province' not in st.session_state:
        st.session_state.detected_province = 'ON'  # default
        try:
            resp = requests.get('https://ipapi.co/json/', timeout=3)
            if resp.status_code == 200:
                region = resp.json().get('region_code', '')
                if region in PROVINCES:
                    st.session_state.detected_province = region
        except Exception:
            pass

    province_options = [f"{name}" for code, name in PROVINCE_LIST]
    province_codes = [code for code, name in PROVINCE_LIST]
    default_idx = province_codes.index(st.session_state.detected_province) if st.session_state.detected_province in province_codes else province_codes.index('ON')

    with col_prov:
        selected_province_name = st.selectbox("Province / Territory", options=province_options, index=default_idx)
        selected_province = province_codes[province_options.index(selected_province_name)]

    with col_period:
        months = ["January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November", "December"]
        current_month = datetime.now().month - 1
        current_year = datetime.now().year
        col_month, col_year = st.columns(2)
        with col_month:
            selected_month = st.selectbox("Month", options=months, index=current_month)
        with col_year:
            selected_year = st.selectbox("Year", options=list(range(current_year - 1, current_year + 2)), index=1)
        pay_period = f"{selected_month} {selected_year}"

    # Input tabs
    tab_manual, tab_csv = st.tabs(["✏️ Manual Entry", "📤 Upload CSV"])

    employees = None

    with tab_csv:
        with st.expander("📋 CSV Format", expanded=False):
            st.markdown("""
            CSV must have columns: `Employee Name, Gross Pay, YTD CPP, YTD EI, Pay Periods`

            **YTD (Year-to-Date) Tips:**
            - First month of year: YTD CPP = 0, YTD EI = 0
            - Subsequent months: Use YTD values from previous month's output
            """)

        uploaded_file = st.file_uploader(
            "Choose CSV file",
            type=['csv'],
            help="CSV must have columns: Employee Name, Gross Pay, YTD CPP, YTD EI, Pay Periods"
        )

        if uploaded_file and st.button("Calculate Payroll", type="primary", use_container_width=True, key="csv_calc"):
            try:
                df = pd.read_csv(uploaded_file)
                required_cols = ['Employee Name', 'Gross Pay', 'YTD CPP', 'YTD EI', 'Pay Periods']
                missing = [col for col in required_cols if col not in df.columns]
                if missing:
                    st.error(f"❌ Missing columns: {', '.join(missing)}")
                else:
                    employees = []
                    has_errors = False
                    for idx, row in df.iterrows():
                        ytd_cpp = float(row['YTD CPP'])
                        ytd_ei = float(row['YTD EI'])
                        gross = float(str(row['Gross Pay']).replace(',', '').replace('$', ''))
                        name = str(row['Employee Name']).strip()
                        if ytd_cpp > 4230.45:
                            st.error(f"❌ {name}: YTD CPP (${ytd_cpp:,.2f}) exceeds 2026 maximum of $4,230.45")
                            has_errors = True
                        if ytd_ei > 1123.07:
                            st.error(f"❌ {name}: YTD EI (${ytd_ei:,.2f}) exceeds 2026 maximum of $1,123.07")
                            has_errors = True
                        if gross <= 0:
                            st.error(f"❌ {name}: Gross Pay must be greater than 0.")
                            has_errors = True
                        employees.append({
                            'name': name,
                            'gross_pay': gross,
                            'ytd_cpp': ytd_cpp,
                            'ytd_ei': ytd_ei,
                            'pay_periods': int(row['Pay Periods'])
                        })
                    if has_errors:
                        employees = None
            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")
                st.info("Please check your CSV format matches the template.")

    with tab_manual:
        st.markdown("Enter employee data directly. Use **+ Add Employee** to add more rows (up to 10).")
        st.caption("YTD = Year-to-Date. First pay period of the year? Leave YTD fields at 0.")

        CPP_MAX = 4230.45
        EI_MAX = 1123.07

        if 'num_employees' not in st.session_state:
            st.session_state.num_employees = 1

        col_add, col_remove = st.columns(2)
        with col_add:
            if st.button("+ Add Employee", use_container_width=True):
                st.session_state.num_employees = min(st.session_state.num_employees + 1, 10)
                st.rerun()
        with col_remove:
            if st.session_state.num_employees > 1:
                if st.button("- Remove Last", use_container_width=True):
                    st.session_state.num_employees -= 1
                    st.rerun()

        pay_period_options = {"Monthly (12)": 12, "Semi-Monthly (24)": 24, "Bi-Weekly (26)": 26, "Weekly (52)": 52}

        manual_data = []
        for i in range(st.session_state.num_employees):
            st.markdown(f"---")
            st.markdown(f"**Employee {i + 1}**")
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("Employee Name", key=f"name_{i}", placeholder="e.g. John Smith")
            with c2:
                pp = st.selectbox("Pay Frequency", options=list(pay_period_options.keys()), key=f"pp_{i}")
            c3, c4, c5 = st.columns(3)
            with c3:
                gross_str = st.text_input("Gross Pay ($)", key=f"gross_{i}", placeholder="e.g. 5000.00",
                                          help="This period's gross salary before deductions")
            with c4:
                ytd_cpp_str = st.text_input(f"YTD CPP (max ${CPP_MAX:,.2f})", key=f"ytd_cpp_{i}", placeholder="0.00",
                                            help="Total CPP already deducted this year from prior pay periods")
            with c5:
                ytd_ei_str = st.text_input(f"YTD EI (max ${EI_MAX:,.2f})", key=f"ytd_ei_{i}", placeholder="0.00",
                                           help="Total EI already deducted this year from prior pay periods")
            manual_data.append({'name': name, 'gross_str': gross_str, 'ytd_cpp_str': ytd_cpp_str, 'ytd_ei_str': ytd_ei_str, 'pp_label': pp})

        st.markdown("---")
        if st.button("Calculate Payroll", type="primary", use_container_width=True, key="manual_calc"):
            valid = True
            parsed = []
            for i, d in enumerate(manual_data):
                if not d['name'].strip():
                    st.error(f"❌ Employee {i + 1}: Name is required.")
                    valid = False

                # Parse gross pay
                gross_raw = d['gross_str'].strip().replace(',', '').replace('$', '')
                if not gross_raw:
                    st.error(f"❌ Employee {i + 1}: Gross Pay is required.")
                    valid = False
                    gross = 0.0
                else:
                    try:
                        gross = float(gross_raw)
                        if gross <= 0:
                            st.error(f"❌ Employee {i + 1}: Gross Pay must be greater than 0.")
                            valid = False
                    except ValueError:
                        st.error(f"❌ Employee {i + 1}: Gross Pay must be a number.")
                        valid = False
                        gross = 0.0

                # Parse YTD CPP
                cpp_raw = d['ytd_cpp_str'].strip().replace(',', '').replace('$', '')
                if not cpp_raw:
                    ytd_cpp = 0.0
                else:
                    try:
                        ytd_cpp = float(cpp_raw)
                        if ytd_cpp < 0:
                            st.error(f"❌ Employee {i + 1}: YTD CPP cannot be negative.")
                            valid = False
                        elif ytd_cpp > CPP_MAX:
                            st.error(f"❌ Employee {i + 1}: YTD CPP (${ytd_cpp:,.2f}) exceeds maximum of ${CPP_MAX:,.2f}.")
                            valid = False
                    except ValueError:
                        st.error(f"❌ Employee {i + 1}: YTD CPP must be a number.")
                        valid = False
                        ytd_cpp = 0.0

                # Parse YTD EI
                ei_raw = d['ytd_ei_str'].strip().replace(',', '').replace('$', '')
                if not ei_raw:
                    ytd_ei = 0.0
                else:
                    try:
                        ytd_ei = float(ei_raw)
                        if ytd_ei < 0:
                            st.error(f"❌ Employee {i + 1}: YTD EI cannot be negative.")
                            valid = False
                        elif ytd_ei > EI_MAX:
                            st.error(f"❌ Employee {i + 1}: YTD EI (${ytd_ei:,.2f}) exceeds maximum of ${EI_MAX:,.2f}.")
                            valid = False
                    except ValueError:
                        st.error(f"❌ Employee {i + 1}: YTD EI must be a number.")
                        valid = False
                        ytd_ei = 0.0

                parsed.append({'name': d['name'].strip(), 'gross': gross, 'ytd_cpp': ytd_cpp, 'ytd_ei': ytd_ei, 'pp_label': d['pp_label']})

            if valid:
                employees = []
                for d in parsed:
                    employees.append({
                        'name': d['name'],
                        'gross_pay': d['gross'],
                        'ytd_cpp': d['ytd_cpp'],
                        'ytd_ei': d['ytd_ei'],
                        'pay_periods': pay_period_options[d['pp_label']]
                    })

    # Process employees (from either tab)
    if employees:
        try:
            with st.spinner("🔄 Processing payroll calculations..."):
                results = []
                for emp in employees:
                    calculator = PayrollCalculator(pay_periods=emp['pay_periods'], province=selected_province)
                    results.append(calculator.calculate_payroll(emp))

            st.success(f"✅ Processed {len(results)} employees successfully!")

            st.markdown("---")
            st.subheader("📊 Payroll Summary")

            total_gross = sum(float(r['gross_pay']) for r in results)
            total_net = sum(float(r['net_amount']) for r in results)
            total_remit = sum(float(r['remittance_total']) for r in results)

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Gross Pay", f"${total_gross:,.2f}")
            col2.metric("Total Net Pay", f"${total_net:,.2f}")
            col3.metric("Total to Remit to CRA", f"${total_remit:,.2f}",
                       help="Includes all deductions + employer CPP + employer EI")

            st.markdown("### Employee Details")
            results_df = pd.DataFrame([
                {
                    'Employee': r['name'],
                    'Gross Pay': f"${float(r['gross_pay']):,.2f}",
                    'CPP': f"${float(r['cpp']):,.2f}",
                    'EI': f"${float(r['ei']):,.2f}",
                    'Federal Tax': f"${float(r['federal_tax']):,.2f}",
                    'Provincial Tax': f"${float(r['provincial_tax']):,.2f}",
                    'Net Amount': f"${float(r['net_amount']):,.2f}",
                    'CRA Remittance': f"${float(r['remittance_total']):,.2f}"
                }
                for r in results
            ])

            st.dataframe(results_df, use_container_width=True, hide_index=True)

            st.markdown("---")
            excel_data = create_excel_output(results, pay_period)
            filename = f"payroll_{pay_period.replace(' ', '_').lower()}.xlsx"

            st.download_button(
                label="📥 Download Complete Excel Report",
                data=excel_data,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                type="primary",
                use_container_width=True
            )

            st.info("💡 Excel file contains: **Payroll Summary** + **T4 Preparation** sheets")

        except Exception as e:
            st.error(f"❌ Error processing payroll: {str(e)}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9em;'>
    <p>CRA-Compliant Calculations | Based on T4127 Payroll Deductions Formulas (122nd Edition - January 2026)</p>
    <p>⚠️ This tool is for estimation purposes. Always verify with a tax professional.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    if 'user' in st.session_state and st.session_state.user:
        main()
    else:
        show_login()
        # show_login may have restored session — check again
        if 'user' in st.session_state and st.session_state.user:
            main()
