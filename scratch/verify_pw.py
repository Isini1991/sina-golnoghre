
import json, time
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8137/color-reveal-sample.html"
OUT = r"C:/Users/Esi/sina-bass/scratch/verify"

results = {"console": [], "shots": []}
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    pg = b.new_page(viewport={"width":1440,"height":900})
    pg.on("console", lambda m: results["console"].append(f"{m.type}: {m.text}") if m.type in ("error","warning") else None)
    pg.on("pageerror", lambda e: results["console"].append(f"pageerror: {e}"))
    pg.goto(URL, wait_until="networkidle")
    pg.wait_for_timeout(1200)
    total = pg.evaluate("document.body.scrollHeight - innerHeight")
    results["totalScroll"] = total
    fracs = [0, 0.2, 0.4, 0.55, 0.7, 0.85, 1.0]
    for i, f in enumerate(fracs):
        pg.evaluate(f"window.scrollTo(0, {{f * total}})".replace("{f * total}", str(int(f*total))))
        pg.wait_for_timeout(900)
        path = f"{OUT}\\phase-{i}.png"
        pg.screenshot(path=path)
        # shader progress if exposed
        prog = pg.evaluate("window.__reveal ? JSON.stringify(window.__reveal()) : null")
        results["shots"].append({"frac": f, "png": path, "state": prog})
    b.close()
print(json.dumps(results, ensure_ascii=False, indent=1))
