"""
Perception - Analyzes the current UI state
Extracts semantic UI snapshot from DOM: visible text, roles, URLs
"""

from typing import Dict, List
from playwright.async_api import Page


class Perception:
    """
    Perception that analyzes the current UI state
    Responsibilities:
    - Extract visible text and interactive elements
    - Identify buttons, forms, links, modals
    - Capture accessibility information
    - Summarize current page context
    """
    
    async def extract_ui_snapshot(self, page: Page) -> Dict:
        """
        Extract a semantic snapshot of the current UI state
        """
        snapshot = {
            "url": page.url,
            "title": await page.title(),
            "visible_elements": await self._get_visible_elements(page),
        }
        return snapshot
    
    async def _get_visible_elements(self, page: Page, limit: int = 500) -> List[Dict]:
        """Extract visible text and interactive elements from the page, including checkboxes, radios, switches, sliders."""
        try:
            results = await page.evaluate("""
            () => {
            const isVisibleEl = (el) => {
                if (!el) return false;
                if (el.nodeType !== 1) return false;
                const style = window.getComputedStyle(el);
                const r = el.getBoundingClientRect();
                if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') return false;
                if (r.width <= 0 || r.height <= 0) return false;
                if (r.bottom < 0 || r.top > window.innerHeight * 1.5) return false;
                let parent = el.parentElement;
                while (parent && parent !== document.body) {
                const ps = window.getComputedStyle(parent);
                if (ps.display === 'none' || ps.visibility === 'hidden' || ps.opacity === '0') return false;
                parent = parent.parentElement;
                }
                return true;
            };

            const meaningfulAncestor = (node) => {
                let el = node.parentElement;

                const interactiveRoles = new Set([
                    'button', 'link', 'menuitem', 'treeitem', 'tab', 'switch', 'checkbox',
                    'radio', 'option', 'textbox', 'combobox', 'slider', 'spinbutton'
                ]);

                while (el && el !== document.body) {
                    const role = el.getAttribute('role');
                    const tag = el.tagName.toLowerCase();

                    const isInteractive =
                    tag === 'a' ||
                    tag === 'button' ||
                    tag === 'input' ||
                    tag === 'textarea' ||
                    el.hasAttribute('tabindex') ||
                    el.hasAttribute('onclick') ||
                    (role && interactiveRoles.has(role)) ||
                    el.getAttribute('contenteditable') === 'true' ||
                    el.hasAttribute('aria-label');

                    if (isInteractive) {
                    return el;
                    }
                    el = el.parentElement;
                }

                // fallback: find the nearest visible parent
                el = node.parentElement;
                while (el && el !== document.body) {
                    if (isVisibleEl(el)) return el;
                    el = el.parentElement;
                }

                return node.parentElement || document.body;
                };

            const items = [];

            // --- Text nodes ---
            const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
                acceptNode: (t) => {
                const raw = t.nodeValue || '';
                const txt = raw.replace(/\\s+/g, ' ').trim();
                if (txt.length < 2) return NodeFilter.FILTER_REJECT;
                if (/^skip to content$/i.test(txt)) return NodeFilter.FILTER_REJECT;
                return NodeFilter.FILTER_ACCEPT;
                }
            });

            let node;
            while ((node = walker.nextNode())) {
                const parent = meaningfulAncestor(node);
                if (!parent || !isVisibleEl(parent)) continue;
                const range = document.createRange();
                range.selectNodeContents(node);
                const rects = Array.from(range.getClientRects()).filter(r => r.width > 0 && r.height > 0);
                if (rects.length === 0) continue;
                const text = node.nodeValue.trim();
                if (text.length > 200) continue;
                const r = parent.getBoundingClientRect();
                items.push({
                tag: parent.tagName.toLowerCase(),
                role: parent.getAttribute('role') || '',
                ariaLabel: parent.getAttribute('aria-label') || '',
                className: parent.className || '',
                hasText: text,
                bbox: { x: r.left, y: r.top, w: r.width, h: r.height }
                });
            }

            // --- Buttons, links, generic clickable ---
            document.querySelectorAll('button, [role="button"], a').forEach(el => {
                if (!isVisibleEl(el)) return;
                const label = el.innerText.trim() || el.getAttribute('aria-label') || '';
                if (!label) return;
                const r = el.getBoundingClientRect();
                items.push({
                tag: el.tagName.toLowerCase(),
                role: el.getAttribute('role') || (el.tagName.toLowerCase() === 'a' ? 'link' : 'button'),
                ariaLabel: el.getAttribute('aria-label') || '',
                className: el.className || '',
                hasText: label.substring(0, 100),
                bbox: { x: r.left, y: r.top, w: r.width, h: r.height }
                });
            });

            // --- Inputs and form fields (text, checkbox, radio, etc.) ---
            document.querySelectorAll('input, textarea, select').forEach(el => {
                if (!isVisibleEl(el)) return;
                const type = el.type || 'text';
                const r = el.getBoundingClientRect();
                const label =
                el.placeholder ||
                el.getAttribute('aria-label') ||
                el.name ||
                el.id ||
                (type === 'checkbox' ? 'checkbox' : type === 'radio' ? 'radio' : '');
                items.push({
                tag: el.tagName.toLowerCase(),
                role: el.getAttribute('role') || (type === 'checkbox' || type === 'radio' ? type : 'textbox'),
                ariaLabel: el.getAttribute('aria-label') || '',
                hasText: label.trim(),
                className: el.className || '',
                inputType: type,
                bbox: { x: r.left, y: r.top, w: r.width, h: r.height }
                });
            });

            // --- Extra ARIA roles: checkbox, radio, switch, slider ---
            document.querySelectorAll('[role="checkbox"], [role="radio"], [role="switch"], [role="slider"]').forEach(el => {
                if (!isVisibleEl(el)) return;
                const r = el.getBoundingClientRect();
                const label = el.getAttribute('aria-label') || el.innerText.trim() || '';
                if (!label) return;
                items.push({
                tag: el.tagName.toLowerCase(),
                role: el.getAttribute('role'),
                ariaLabel: el.getAttribute('aria-label') || '',
                className: el.className || '',
                hasText: label.substring(0, 100),
                bbox: { x: r.left, y: r.top, w: r.width, h: r.height }
                });
            });

            // Deduplicate
            const seen = new Set();
            const out = [];
            for (const it of items) {
                const key = (it.tag + '|' + it.role + '|' + it.hasText.toLowerCase()).slice(0, 160);
                if (!seen.has(key)) {
                seen.add(key);
                out.push(it);
                }
            }

            return out.slice(0, 500);
            }
            """)
            return results
        except Exception as e:
            print(f"Error extracting UI snapshot: {e}")
            return []
