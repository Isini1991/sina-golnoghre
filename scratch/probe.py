"""Probe window.__sina state + take real screenshots for the sina-bass page."""
import base64, json, time, urllib.request, urllib.parse, sys
import websocket

CDP = "http://127.0.0.1:9222"
URL = "file:///C:/Users/Esi/sina-bass/index.html"
OUT = r"C:\Users\Esi\sina-bass\scratch\shots"

def new_tab(url):
    req = urllib.request.Request(CDP + "/json/new?" + urllib.parse.quote(url, safe=""), method="PUT")
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.load(r)["webSocketDebuggerUrl"]

ws = websocket.create_connection(new_tab(URL), timeout=60)
mid = 0
def send(method, params=None, cap=40):
    global mid
    mid += 1
    ws.send(json.dumps({"id": mid, "method": method, "params": params or {}}))
    t0 = time.time()
    while time.time() - t0 < cap:
        try:
            m = json.loads(ws.recv())
        except Exception:
            continue
        if m.get("id") == mid:
            return m
    raise RuntimeError("timeout " + method)

errs = []
ws.settimeout(5)
send("Page.enable"); send("Runtime.enable")
# desktop viewport
send("Emulation.setDeviceMetricsOverride", {"width": 1440, "height": 900, "deviceScaleFactor": 1, "mobile": False})
deadline = time.time() + 45
while time.time() < deadline:
    try:
        m = json.loads(ws.recv())
    except Exception:
        break
    if m.get("method") == "Page.loadEventFired":
        break
    if m.get("method") == "Runtime.exceptionThrown":
        errs.append(json.dumps(m["params"]["exceptionDetails"].get("exception", {}).get("description", m["params"]["exceptionDetails"].get("text", ""))[:300]))
    if m.get("method") == "Runtime.consoleAPICalled" and m["params"].get("type") == "error":
        errs.append(str(m["params"]["args"][:1])[:300])
time.sleep(2)

fracs = [0.02, 0.12, 0.22, 0.32, 0.42, 0.55, 0.68, 0.80, 0.90, 0.99]
for f in fracs:
    send("Runtime.evaluate", {"expression": "window.scrollTo(0, document.body.scrollHeight*%f); true" % f})
    time.sleep(1.6)
    st = send("Runtime.evaluate", {"expression": "JSON.stringify(window.__sina ? window.__sina.getState() : 'HOOK-MISSING')", "returnByValue": True})
    print("FRAC %.2f  STATE: %s" % (f, st["result"]["result"].get("value")))
    shot = send("Page.captureScreenshot", {"format": "png"})
    open(OUT + r"\probe_%03d.png" % (f * 100), "wb").write(base64.b64decode(shot["result"]["data"]))

# also test lang toggle at a bio position
send("Runtime.evaluate", {"expression": "window.scrollTo(0, document.body.scrollHeight*0.55); true"})
time.sleep(1.2)
send("Runtime.evaluate", {"expression": "document.getElementById('lang').click(); true"})
time.sleep(1.5)
st = send("Runtime.evaluate", {"expression": "JSON.stringify({lang: window.__sina.getState().lang, dir: document.documentElement.dir, h1: (document.querySelector('h1')||{}).textContent})", "returnByValue": True})
print("AFTER LANG TOGGLE:", st["result"]["result"].get("value"))
shot = send("Page.captureScreenshot", {"format": "png"})
open(OUT + r"\probe_en.png", "wb").write(base64.b64decode(shot["result"]["data"]))

print("JS ERRORS:", errs if errs else "none")
ws.close()
