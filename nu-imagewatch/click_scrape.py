import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_interactive_elements(base_url):
    response = requests.get(base_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    interactive = []

    # 1) True hyperlinks
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if not href or href == "#" or href.lower().startswith("javascript:"):
            continue

        full_url = urljoin(base_url, href)
        text = a.get_text(strip=True) or "[no text]"

        interactive.append({
            "type": "link",
            "tag": "a",
            "text": text,
            "url": full_url
        })

    # 2) Buttons
    for btn in soup.find_all("button"):
        text = btn.get_text(strip=True) or "[no text]"
        onclick = btn.get("onclick", "").strip() or None

        interactive.append({
            "type": "button",
            "tag": "button",
            "text": text,
            "onclick": onclick
        })

    # 3) Input buttons (submit/button)
    for inp in soup.find_all("input"):
        input_type = inp.get("type", "").lower()
        if input_type in ("submit", "button", "reset", "image"):
            value = inp.get("value", "").strip() or "[no value]"
            onclick = inp.get("onclick", "").strip() or None

            interactive.append({
                "type": "input_button",
                "tag": "input",
                "input_type": input_type,
                "value": value,
                "onclick": onclick
            })

    # 4) Any element with onclick attribute (divs, spans, etc.)
    for el in soup.find_all(onclick=True):
        # Avoid duplicates for button/input already captured
        if el.name in ("a", "button", "input"):
            continue

        text = el.get_text(strip=True) or "[no text]"
        onclick = el.get("onclick", "").strip() or None

        interactive.append({
            "type": "onclick_element",
            "tag": el.name,
            "text": text,
            "onclick": onclick
        })

    return interactive

if __name__ == "__main__":
    base_url = "https://imagewatch.dell.com/#/home"
    items = get_interactive_elements(base_url)

    for item in items:
        print(item)