"""Playwright-based Medium publisher.

Medium discontinued new API integration tokens. This module provides browser
automation via Playwright as a replacement, navigating Medium's web interface
to create and publish stories directly.

Requires optional dependency:
    pip install "playwright>=1.40.0" && playwright install chromium
"""

import logging
from typing import Any, Dict

try:
    from playwright.sync_api import sync_playwright

    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    sync_playwright = None  # type: ignore[assignment]
    PLAYWRIGHT_AVAILABLE = False

_INSTALL_HINT = (
    "playwright is not installed. "
    "Install it with: pip install 'playwright>=1.40.0' && playwright install chromium"
)


class MediumPlaywrightPublisher:
    """Publishes articles to Medium using Playwright browser automation.

    Medium discontinued new API integration tokens, so this class automates
    the Medium web interface instead.

    Args:
        email: Medium account email address.
        password: Medium account password.
        headless: Run browser in headless mode (default True).
    """

    def __init__(self, email: str, password: str, headless: bool = True):
        self.email = email
        self.password = password
        self.headless = headless
        self.logger = logging.getLogger(__name__)

    def publish(self, article_data: Dict[str, Any]) -> Dict[str, Any]:
        """Publish an article to Medium via browser automation.

        Args:
            article_data: Dict with keys title, content, tags, meta_description.

        Returns:
            Dict with keys: success (bool), platform ("medium"), and either
            url (str) on success or error (str) on failure.
        """
        if not PLAYWRIGHT_AVAILABLE:
            return {
                "success": False,
                "platform": "medium",
                "error": _INSTALL_HINT,
            }

        title = article_data.get("title", "Untitled")
        content = article_data.get("content", "")
        tags: list = article_data.get("tags", [])

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=self.headless)
                context = browser.new_context()
                page = context.new_page()

                self._login(page)
                published_url = self._create_story(page, title, content, tags)

                browser.close()

            self.logger.info(f"Published to Medium: {published_url}")
            return {
                "success": True,
                "platform": "medium",
                "url": published_url,
            }

        except Exception as e:
            self.logger.error(f"Medium Playwright publication failed: {str(e)}")
            return {
                "success": False,
                "platform": "medium",
                "error": str(e),
            }

    def _login(self, page: Any) -> None:
        """Log in to Medium using email and password.

        Args:
            page: Playwright Page object.

        Raises:
            Exception: If login fails or times out.
        """
        self.logger.info("Logging in to Medium...")
        page.goto("https://medium.com/m/signin")
        page.wait_for_load_state("networkidle")

        # Click "Sign in with email"
        page.click("text=Sign in with email")
        page.wait_for_selector("input[name='email']", timeout=10_000)
        page.fill("input[name='email']", self.email)
        page.click("button[type='submit']")

        # Medium may show a password field or a magic-link prompt
        page.wait_for_selector(
            "input[name='password'], text=Check your email", timeout=15_000
        )

        if page.locator("input[name='password']").count() > 0:
            page.fill("input[name='password']", self.password)
            page.click("button[type='submit']")
        else:
            raise RuntimeError(
                "Medium sent a magic link instead of a password prompt. "
                "Set a password on your Medium account or use session cookies."
            )

        # Wait until we land on the Medium home page
        page.wait_for_url("https://medium.com/**", timeout=20_000)
        self.logger.info("Logged in to Medium successfully")

    def _create_story(self, page: Any, title: str, content: str, tags: list) -> str:
        """Create and publish a new story on Medium.

        Args:
            page: Playwright Page object (must already be logged in).
            title: Story title.
            content: Story body (Markdown or plain text).
            tags: List of tag strings (up to 5 used by Medium).

        Returns:
            Published story URL.

        Raises:
            Exception: If story creation or publishing fails.
        """
        self.logger.info("Navigating to new story editor...")
        page.goto("https://medium.com/new-story")
        page.wait_for_load_state("networkidle")

        # Title field is the first h1 / contenteditable
        title_locator = page.locator(
            "h1[data-testid='editor-title'], h1.graf--title"
        ).first
        title_locator.click()
        title_locator.fill(title)

        # Move to body; press Enter to create first paragraph
        page.keyboard.press("Enter")

        # Type the article content
        page.keyboard.type(content)

        # Open the publish flow
        page.click("button:has-text('Publish')")
        page.wait_for_selector(
            "text=Publish now, text=Ready to publish?", timeout=10_000
        )

        # Fill tags (Medium accepts up to 5 comma-separated tags)
        if tags:
            tag_input = page.locator(
                "input[placeholder*='tag'], input[aria-label*='tag']"
            )
            if tag_input.count() > 0:
                tag_input.fill(", ".join(tags[:5]))

        # Confirm publish
        page.click("button:has-text('Publish now')")
        page.wait_for_load_state("networkidle", timeout=30_000)

        return page.url
