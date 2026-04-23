"""End-to-end browser tests for the CRA Payroll Streamlit app using Playwright."""

import pytest
import subprocess
import time
import os
import signal
from playwright.sync_api import sync_playwright, expect

APP_URL = "http://localhost:8501"
CSV_PATH = os.path.join(os.path.dirname(__file__), "templates", "employees.csv")


@pytest.fixture(scope="module")
def streamlit_app():
    """Start Streamlit app if not already running, yield, then clean up."""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    already_running = sock.connect_ex(("localhost", 8501)) == 0
    sock.close()

    if already_running:
        yield
        return

    proc = subprocess.Popen(
        ["streamlit", "run", "app.py", "--server.headless", "true", "--server.port", "8501"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    # Wait for app to be ready
    for _ in range(30):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if sock.connect_ex(("localhost", 8501)) == 0:
            sock.close()
            break
        sock.close()
        time.sleep(1)
    else:
        proc.kill()
        raise RuntimeError("Streamlit app failed to start")

    yield

    os.kill(proc.pid, signal.SIGTERM)
    proc.wait(timeout=10)


@pytest.fixture()
def page(streamlit_app):
    """Provide a fresh browser page for each test."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        pg = browser.new_page()
        pg.goto(APP_URL, wait_until="networkidle")
        # Wait for Streamlit to fully render
        pg.wait_for_selector("h1", timeout=15000)
        yield pg
        browser.close()


# ── Page loads correctly ──

class TestPageLoad:
    def test_title_visible(self, page):
        heading = page.locator("[data-testid='stMain'] h1").first
        expect(heading).to_contain_text("CRA Payroll Automation Tool")

    def test_sidebar_visible(self, page):
        sidebar = page.locator("[data-testid='stSidebar']")
        expect(sidebar).to_be_visible()

    def test_has_two_tabs(self, page):
        tabs = page.locator("[data-baseweb='tab']")
        expect(tabs).to_have_count(2)

    def test_manual_tab_label(self, page):
        tabs = page.locator("[data-baseweb='tab']")
        expect(tabs.nth(0)).to_contain_text("Manual Entry")

    def test_csv_tab_label(self, page):
        tabs = page.locator("[data-baseweb='tab']")
        expect(tabs.nth(1)).to_contain_text("Upload CSV")


# ── CSV upload flow ──

class TestCSVUpload:
    def _switch_to_csv_tab(self, page):
        tabs = page.locator("[data-baseweb='tab']")
        tabs.nth(1).click()
        page.wait_for_timeout(1000)

    def test_upload_and_calculate(self, page):
        """Upload employees.csv and verify results appear."""
        self._switch_to_csv_tab(page)
        # Upload CSV
        file_input = page.locator("input[type='file']")
        file_input.set_input_files(CSV_PATH)
        page.wait_for_timeout(2000)

        # Click Calculate
        calc_button = page.get_by_role("button", name="Calculate Payroll").first
        calc_button.click()
        page.wait_for_timeout(3000)

        # Verify success message
        expect(page.locator("text=Processed 3 employees successfully")).to_be_visible(timeout=10000)

    def test_results_show_metrics(self, page):
        """After calculation, summary metrics should be visible."""
        self._switch_to_csv_tab(page)
        file_input = page.locator("input[type='file']")
        file_input.set_input_files(CSV_PATH)
        page.wait_for_timeout(2000)

        calc_button = page.get_by_role("button", name="Calculate Payroll").first
        calc_button.click()
        page.wait_for_timeout(3000)

        expect(page.locator("text=Total Gross Pay")).to_be_visible(timeout=10000)
        expect(page.locator("text=Total Net Pay")).to_be_visible(timeout=10000)
        expect(page.locator("text=Total to Remit to CRA")).to_be_visible(timeout=10000)

    def test_download_button_appears(self, page):
        """Excel download button should appear after calculation."""
        self._switch_to_csv_tab(page)
        file_input = page.locator("input[type='file']")
        file_input.set_input_files(CSV_PATH)
        page.wait_for_timeout(2000)

        calc_button = page.get_by_role("button", name="Calculate Payroll").first
        calc_button.click()
        page.wait_for_timeout(3000)

        expect(page.locator("text=Download Complete Excel Report")).to_be_visible(timeout=10000)


# ── Manual entry flow ──

class TestManualEntry:
    def test_manual_tab_has_form_fields(self, page):
        """Manual entry tab should show labeled input fields (default tab)."""
        expect(page.locator("text=Employee Name").first).to_be_visible()
        expect(page.locator("text=Gross Pay").first).to_be_visible()
        expect(page.locator("text=Pay Frequency").first).to_be_visible()

    def test_add_employee_button(self, page):
        """Clicking + Add Employee should add another set of fields."""
        # Manual entry is the default tab, no switching needed

        # Should start with Employee 1
        expect(page.locator("text=Employee 1")).to_be_visible()

        # Click add
        page.get_by_role("button", name="+ Add Employee").click()
        page.wait_for_timeout(2000)

        # Should now have Employee 2
        expect(page.locator("text=Employee 2")).to_be_visible()

    def test_manual_entry_calculate(self, page):
        """Fill in one employee manually and calculate."""
        # Manual entry is the default tab, no switching needed

        # Fill in employee name
        name_input = page.locator("input[aria-label='Employee Name']")
        name_input.fill("Test Employee")

        # Fill in gross pay
        gross_input = page.locator("input[aria-label='Gross Pay ($)']")
        gross_input.fill("")
        gross_input.type("5000")

        # Click calculate
        calc_button = page.get_by_role("button", name="Calculate Payroll")
        calc_button.click()
        page.wait_for_timeout(3000)

        # Verify results
        expect(page.locator("text=Processed 1 employees successfully")).to_be_visible(timeout=10000)

    def test_manual_entry_validation_empty_name(self, page):
        """Should show error when name is empty."""
        # Manual entry is the default tab, no switching needed

        # Leave name empty, set gross pay
        gross_input = page.locator("input[aria-label='Gross Pay ($)']")
        gross_input.fill("")
        gross_input.type("5000")

        # Click calculate
        calc_button = page.get_by_role("button", name="Calculate Payroll")
        calc_button.click()
        page.wait_for_timeout(2000)

        # Should show error
        expect(page.locator("text=Name is required")).to_be_visible(timeout=5000)

    def test_manual_entry_validation_zero_gross(self, page):
        """Should show error when gross pay is 0."""
        # Manual entry is the default tab, no switching needed

        # Fill name, leave gross at 0
        name_input = page.locator("input[aria-label='Employee Name']")
        name_input.fill("Test Employee")

        # Click calculate
        calc_button = page.get_by_role("button", name="Calculate Payroll")
        calc_button.click()
        page.wait_for_timeout(2000)

        expect(page.locator("text=Gross Pay must be greater than 0")).to_be_visible(timeout=5000)

    def test_remove_employee_button(self, page):
        """Remove Last button should remove an employee row."""
        # Manual entry is the default tab, no switching needed

        # Add a second employee
        page.get_by_role("button", name="+ Add Employee").click()
        page.wait_for_timeout(2000)
        expect(page.locator("text=Employee 2")).to_be_visible()

        # Remove it
        page.get_by_role("button", name="- Remove Last").click()
        page.wait_for_timeout(2000)
        expect(page.locator("text=Employee 2")).not_to_be_visible()
