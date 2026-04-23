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
        # Streamlit apps need extra time for JS hydration, especially on free tier cold starts
        pg.wait_for_timeout(15000)
        pg.wait_for_selector("h1", timeout=30000)
        yield pg
        browser.close()


class TestProductionSmokeTest:
    def test_page_loads(self, page):
        heading = page.locator("h1").first
        expect(heading).to_be_visible()

    def test_title_text(self, page):
        heading = page.locator("[data-testid='stMain'] h1").first
        expect(heading).to_contain_text("CRA Payroll Automation Tool")

    def test_has_two_tabs(self, page):
        tabs = page.locator("[data-baseweb='tab']")
        expect(tabs).to_have_count(2)

    def test_manual_entry_tab_is_default(self, page):
        tabs = page.locator("[data-baseweb='tab']")
        expect(tabs.nth(0)).to_contain_text("Manual Entry")

    def test_dev_ui_hidden_no_hamburger_menu(self, page):
        menu = page.locator("#MainMenu")
        expect(menu).to_be_hidden()

    def test_dev_ui_hidden_no_footer(self, page):
        footer = page.locator("footer")
        expect(footer).to_be_hidden()

    def test_dev_ui_hidden_no_toolbar(self, page):
        toolbar = page.locator("[data-testid='stToolbar']")
        expect(toolbar).to_be_hidden()

    def test_sidebar_visible(self, page):
        sidebar = page.locator("[data-testid='stSidebar']")
        expect(sidebar).to_be_visible()

    def test_manual_entry_form_fields(self, page):
        expect(page.locator("text=Employee Name").first).to_be_visible()
        expect(page.locator("text=Gross Pay").first).to_be_visible()
        expect(page.locator("text=Pay Frequency").first).to_be_visible()

    def test_manual_entry_calculate(self, page):
        name_input = page.locator("input[aria-label='Employee Name']")
        name_input.fill("Test Employee")

        gross_input = page.locator("input[aria-label='Gross Pay ($)']")
        gross_input.fill("5000")

        calc_button = page.get_by_role("button", name="Calculate Payroll")
        calc_button.click()
        page.wait_for_timeout(5000)

        expect(page.locator("text=Processed 1 employees successfully")).to_be_visible(timeout=15000)

    def test_results_show_metrics(self, page):
        expect(page.locator("text=Total Gross Pay")).to_be_visible(timeout=5000)
        expect(page.locator("text=Total Net Pay")).to_be_visible(timeout=5000)

    def test_download_button_appears(self, page):
        expect(page.locator("text=Download Complete Excel Report")).to_be_visible(timeout=5000)
