import os
from playwright.async_api import async_playwright

async def ensure_session(
    site_url: str,
    login_url: str = None,
    session_path: str = "session.json",
):
    """
    Generic Playwright session manager.
    - Reuses existing login session if available.
    - Otherwise opens the login page, waits for manual login, and saves session.

    Args:
        site_url (str): The main URL to navigate after login.
        login_url (str): Optional explicit login page URL (if different from site_url).
        session_path (str): Where to store session cookies/localStorage.

    Returns:
        (browser, context, page): A tuple of Playwright handles ready for use.
    """

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, channel="chrome")

        # If we already have a session, reuse it
        if os.path.exists(session_path):
            print(f"🔁 Reusing existing session from {session_path}")
            context = await browser.new_context(
                storage_state=session_path,
                viewport={"width": 1920, "height": 1080},
                device_scale_factor=1.0
            )
            page = await context.new_page()
            await page.goto(site_url, wait_until="domcontentloaded", timeout=20000)
            print(f"✅ Logged in automatically to {site_url}")
            return browser, page

        # If no session found, go to login page and wait for manual login
        print(f"🔐 No session found. Opening {login_url or site_url} for manual login...")
        context = await browser.new_context(viewport={"width": 1920, "height": 1080}, device_scale_factor=1.0)
        page = await context.new_page()
        
        await page.goto(login_url or site_url, wait_until="domcontentloaded", timeout=20000)

        wait_time = 30000

        print(f"⏳ Please log in manually within {wait_time / 1000} seconds...")
        await page.wait_for_timeout(wait_time)

        await context.storage_state(path=session_path)
        print(f"✅ Session saved to {session_path}")

        await page.goto(site_url, wait_until="domcontentloaded", timeout=20000)
        print(f"✅ Ready at {site_url}")

        return browser, page
