from playwright.async_api import Page
from datetime import datetime
import os
from PIL import Image, ImageDraw


async def take_screenshot(page: Page, id_number: str, tag: str = "step", bbox_x: float = None, bbox_y: float = None,
                            bbox_width: float = None, bbox_height: float = None):
        """Capture a screenshot and optionally highlight a bounding box."""
        

        # Store the screenshot in the screenshots directory
        os.makedirs(f"screenshots/{id_number}", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        raw_path = f"screenshots/{id_number}/{tag}_{timestamp}_raw.png"
        final_path = f"screenshots/{id_number}/{tag}_{timestamp}.png"

        # Wait for the page to load
        await page.wait_for_load_state("domcontentloaded")
        # Additional wait for dynamic content to settle
        await page.wait_for_timeout(600)

        # Capture screenshot
        await page.screenshot(
            path=raw_path, full_page=False, timeout=5000,
            animations="disabled", caret="hide"
        )

        # Draw bbox if provided
        if all(v is not None for v in [bbox_x, bbox_y, bbox_width, bbox_height]):
            try:
                img = Image.open(raw_path)
                draw = ImageDraw.Draw(img)
                x1, y1 = bbox_x, bbox_y
                x2, y2 = bbox_x + bbox_width, bbox_y + bbox_height
                draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
                img.save(final_path)
                os.remove(raw_path)
                print(f"Screenshot with bbox: {final_path}")
                return final_path
            except Exception as e:
                print(f"Screenshot saved but bbox draw failed: {type(e).__name__} - {e}")
                return raw_path

        # No bbox → rename and return
        os.rename(raw_path, final_path)
        print(f"Screenshot saved: {final_path}")
        return final_path

        