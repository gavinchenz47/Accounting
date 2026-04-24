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
    """Provide a fresh browser page for each test. Clears session file to ensure logged-out state."""
    session_file = os.path.join(os.path.dirname(__file__), '.session.json')
    if os.path.exists(session_file):
        os.remove(session_file)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        pg = browser.new_page()
        pg.goto(APP_URL, wait_until="networkidle")
        pg.wait_for_selector("h1", timeout=15000)
        yield pg
        browser.close()


# ── Login screen tests ──

class TestLoginScreen:
    def test_login_page_loads(self, page):
        heading = page.locator("h1").first
        expect(heading).to_contain_text("CRA Payroll Deductions Calculator")

    def test_sign_in_button_visible(self, page):
        btn = page.get_by_role("button", name="Sign in with Google")
        expect(btn).to_be_visible()

    def test_privacy_caption_visible(self, page):
        expect(page.locator("text=Your data is kept private and secure")).to_be_visible()

    def test_calculator_not_visible_when_logged_out(self, page):
        """Calculator should be gated behind auth."""
        expect(page.locator("text=Manual Entry")).not_to_be_visible()
        expect(page.locator("text=Upload CSV")).not_to_be_visible()
