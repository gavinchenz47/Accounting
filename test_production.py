"""Quick smoke test against the production Streamlit Cloud deployment."""

import pytest
from playwright.sync_api import sync_playwright, expect

PROD_URL = "https://accounting-3pns7vsk95pikojyhccgv4.streamlit.app/"


@pytest.fixture(scope="module")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        pg = browser.new_page()
        pg.goto(PROD_URL, wait_until="load", timeout=90000)
        # Streamlit Cloud apps need extra time for JS hydration + cold starts
        pg.wait_for_timeout(20000)
        # Streamlit may render inside an iframe on Cloud
        iframe = pg.frame_locator("iframe[title='streamlitApp']")
        try:
            iframe.locator("h1").first.wait_for(timeout=10000)
            # Content is in an iframe — use the iframe context
            pg._streamlit_frame = iframe
        except Exception:
            # No iframe — content is in main page (local dev or newer Streamlit)
            pg.wait_for_selector("h1", timeout=30000)
            pg._streamlit_frame = None
        yield pg
        browser.close()


def _loc(page, selector):
    """Get a locator that works whether content is in an iframe or not."""
    if hasattr(page, '_streamlit_frame') and page._streamlit_frame:
        return page._streamlit_frame.locator(selector)
    return page.locator(selector)


class TestProductionSmokeTest:
    def test_page_loads(self, page):
        expect(_loc(page, "h1").first).to_be_visible()

    def test_title_text(self, page):
        expect(_loc(page, "[data-testid='stMain'] h1").first).to_contain_text("CRA Payroll Deductions Calculator")

    def test_has_two_tabs(self, page):
        expect(_loc(page, "[data-baseweb='tab']")).to_have_count(2)

    def test_manual_entry_tab_is_default(self, page):
        expect(_loc(page, "[data-baseweb='tab']").nth(0)).to_contain_text("Manual Entry")

    def test_sidebar_visible(self, page):
        expect(_loc(page, "[data-testid='stSidebar']")).to_be_visible()

    def test_manual_entry_form_fields(self, page):
        expect(_loc(page, "text=Employee Name").first).to_be_visible()
        expect(_loc(page, "text=Gross Pay").first).to_be_visible()
        expect(_loc(page, "text=Pay Frequency").first).to_be_visible()

    def test_manual_entry_calculate(self, page):
        _loc(page, "input[aria-label='Employee Name']").fill("Test Employee")
        _loc(page, "input[aria-label='Gross Pay ($)']").fill("5000")
        _loc(page, "button:has-text('Calculate Payroll')").click()
        page.wait_for_timeout(5000)
        expect(_loc(page, "text=Processed 1 employees successfully")).to_be_visible(timeout=15000)

    def test_results_show_metrics(self, page):
        expect(_loc(page, "text=Total Gross Pay")).to_be_visible(timeout=5000)
        expect(_loc(page, "text=Total Net Pay")).to_be_visible(timeout=5000)

    def test_download_button_appears(self, page):
        expect(_loc(page, "text=Download Complete Excel Report")).to_be_visible(timeout=5000)
