# HANDOFF — سینا گل‌نقره / Sina Golnoghreh Bass Portfolio (نسخه B — وضعیت جاری)

تاریخ: ۳۱ آگوست ۲۰۲۶ · این سند برای تحویل پروژه به هر هارنس/AI دیگری است.
خواندن این فایل = داشتن کل دانش پروژه. بقیه‌ی پروژه را از روی خود فایل‌ها بخوان.

---

## ۰) پروژه کجاست

```
C:\Users\Esi\sina-bass\
```

- **فایل اصلی:** `index.html` (~57KB, تک‌فایل، آفلاین کامل — بدون CDN، بدون build)
- **سرور محلی:** `cd C:/Users/Esi/sina-bass && python -m http.server 8137` (بین سشن‌ها می‌میرد؛ هر بار ری‌استارت شود)
- **آدرس نمایش:** `http://127.0.0.1:8137/index.html`
- **نکته‌ی Windows/MSYS:** با bash آزاد. Pathها با `C:/Users/Esi/...` (اسلش رو به جلو) به برنامه‌های native بده.

---

## ۱) پروژه چیست

پورتفولیوی **سینا گل‌نقره** — نوازنده‌ی بیس، آهنگساز، مهندس صدای زنده (فارسی/ایرانی، سایت RTL).
تجربه: **Color-Reveal ورودی (WebGL2 خام)** → بعد از «ورود»، یک **سایت اسکرول‌مجازی با صحنه‌های ثابت** (صفحه هرگز حرکت نمی‌کند؛ اسکرول فقط ورودی فرمان است — الگوی aboutluca.com).

## ۲) معماری فعلی (نقشه‌ی index.html)

**ورودی — Color-Reveal (صحنه ۰):**
- WebGL2 خام بدون کتابخانه؛ دو تکسچر `assets/dual/background.webp` + `foreground.webp` (سوژه با آلفا)
- سفر ۰→۱۰۰ با **دکمه‌ی «ورود»** (`#enterbtn`)، ۳.۵ ثانیه، تایم‌لاین با پمپ `setInterval` (در تب بک‌گراند هم کار می‌کند)
- فازها: ۱) محو B&W (بلر ۱۵→۲، کنتراست .۷۵) ۰→.۳۸ · ۲) فوکوس (بلر→۰، کنتراست→۱.۱) .۳۸→.۵۵ · ۳) رنگ از شش‌ضلعی (reveal با smootherstep) .۵۵→۱
- سوژه: `cuvF = (base-.5)*1.06 + .5 + oFg + vec2(0., -.055)` (کوچک‌سازی و پایین‌آوردن قفلشده)
- ذرات غبار کهربایی: گرید `luv * vec2(sc*slotW*aspect, sc)` — **ضرب نه تقسیم** (باگِ تاریخی)
- فونت **لاله‌زار** برای تیتر/دکمه؛ **وزیرمتن** برای UI
- هوک تست: `window.__reveal.getState()`, `window.__reveal.force(pv)` (رندر sync در p دلخواه)

**بعد از ورود — اسکرول مجازی (بخش اصلی):**
- `body{height:100vh;overflow:hidden}` → **صفحه اصلاً اسکرول نمی‌شود** (تست‌شده: `scrollY` همیشه ۰)
- دکمه‌ی ورود → `journey.complete` → `body.site-ready`
- موتور: `vScroll = {v, target}` روی محور ۰..۱؛ `RANGE_TOTAL = 0.80`
  - صحنه‌ها: `SCENE_RANGE = {instrument:.26, sound:.14, live:.16, bio:.16, contact:.08}`
  - `sceneStart`/`sceneCenter` از روی رنج‌ها؛ `sceneP(id)` = پیشرفت داخل صحنه
  - **حلقه‌ی vLoop (rAF):** `v += (target-v)*.11`؛ هر فریم `applyScroll()` → `placeScene()` برای هر صحنه
- **ترنزیشن سینمایی:**
  - هر صحنه پنجره‌ی `[start-دم، end+دم]`، `دم = FX.tail = .055`، smoothstep
  - **صحنه‌ی اول (instrument) آفست `+tail*.6` دارد** تا در v=0 کاملاً نامرئی بماند (دکمه‌ی ورود مالک صفحه است — باگ قدیمی)
  - اسلاید عمودی `translate3d(0, -d*46, 0)` + `scale(1-|d|*.016)` + `blur(|d|*7px)` — حرکت دوربین Luca-مانند
  - استیج: `sa = smoothstep(1 - v/(tail*1.8))` — هماهنگ با ورود ساز محو می‌شود
- **ورودی‌ها:** wheel (hijack با `preventDefault`، ضریب `.00042`) · کیبورد (arrows/PageUp/Down/Home/End) · touch swipe (ضریب `.0011`) · لینک‌های ناوبری (`vScroll.target = center + range*.45`)
- **اسکرول داخلی:** `shellAfford(target, dy)` — shell های بلند (گالری/بیو، `overflow-y:auto`) **تا لبه** اسکرول بومی می‌گیرند، از لبه به اسکرول مجازی تحویل می‌شود (تله‌ی گیرکردن حل شد)
- **ساز:** سکانس ۲۴۰ فریمی `assets/headstock-frames/f001..f240.webp` روی `#pegCanvas` (2D canvas، DPR-aware)؛ `updatePeg()` از `sceneP('instrument')` → `pegFrameIndex`؛ نوار پیشرفت `#pegProgress`
- **گالری = سینمای پروجکشن:** `.projector` (پرده با گرین SVG + `kenburns` + `flicker` + لرزش نور)، لنز پروژکتور با درخشش، پرتو نور `conic-gradient` با `mix-blend-mode:screen`، `#liveRail` = نوار فیلم ۱۶ فریم با سوراخ‌های اسپراکت (`::before/::after`)، فریم فعال درخشش کهربایی، نوار حلقه «۰۱ / LIVE FRAME» با Lalezar
- **حالت‌های تست:** `window.__sina.getState()` → `{journey, scene, v, vTarget, pegIndex, pegCount, liveIndex, liveFrames}` · `window.__sina.goto(v)` (پریدن روی محور مجازی)

**محرک‌های ورود:** wheel-down قبل از ورود → `startJourney()` (دلتا پایی‌نشده)؛ دکمه‌ی ورود → کلیک.

## ۳) بخش‌های سایت (محتوا — از content/)

| صحنه | محتوا |
|---|---|
| ۰۱ ساز | Dingwall NG2 — سردسته ۲۴۰ فریم، کپی «امضای دست‌ساز»، نمایه ۰۱ |
| ۰۲ صدا | «پایین‌ترین نت، باقیِ فضا را می‌سازد» + **Bandcamp**: https://carnivalesqueband.bandcamp.com + میدان صدا (orbit rings) |
| ۰۳ صحنه | «روی صحنه» — سینمای پروجکشن، ۱۶ عکس `assets/live/live-01..16.webp` + ویدئوی `content/Bass_guitar_tuning_pegs_rotating_202608271408.mp4` |
| ۰۴ بیو | تایم‌لاین: ۱۳۸۳ شروع+مسترکلاس بابک ریاحی‌پور · ۲۰۱۵ مهندسی صدا (روزبه اسماعیلی، سپهر حقیقی) · ۲۰۱۳–امروز گروه‌ها (مونهد، ماخولا، کارنیوالسک، مگو، جلیل) · ۲۰۲۳ دبی (سیاوش شمس، فتانه، کوروس) |
| ۰۵ تماس | IG سینا `sina.golnoghreh` · Bandcamp · IG ماخولا `makhoola.official` · IG کارنیوالسک `carnivalesqueband` |

## ۴) نسخه‌بندی (برای بازگشت)

- **`versions/A/`** = نسخه‌ی تاییدشده‌ی قبلی (فقط Color-Reveal، بدون اسکرول‌مجازی). بازگشت = کپی `versions/A/index.html` روی `index.html`. README فارسی داخلش هست.
- **`versions/legacy-index-before-B.html`** = index سه‌جی‌اس قدیمی.
- **`color-reveal-sample.html`** = نمونه‌ی اولیه‌ی تایید شده (مرجع شیدر).
- `versions/sina-color-reveal-A.zip` — آرشیو A.

## ۵) قواعد و ترجیحات (مهم!)

- **فارسیِ تمیز و طبیعی** در رابط؛ عنوان با لاله‌زار، بقیه وزیرمتن.
- تک‌فایل آفلاین؛ **صفر خطای کنسول** در هر تغییر؛ وریفای CDP بعد از هر دور تغییر.
- سبک: مشکی `#000`–`#050505`، کهربایی `#ff6a2a`/`#ff5a1f`، گرین فیلمی + vignette — **نه گلو نئونی، نه گرادیان‌های بچه‌گانه**.
- تکرارهای وریفای: `node --check` از اسکریپت استخراج‌شده (به `%TEMP%` بنویس، نه `/dev/fd` — MSYS باز است)، headless Chrome `C:\Program Files\Google\Chrome\Application\chrome.exe` با `--headless=new --virtual-time-budget`، و CDP (websocket-client نصب است) برای کلیک/چرخ واقعی؛ `--user-data-dir` تازه.
- کاربر: **سرعت مهم است** — چند قدم کوتاه، نه سفرهای طولانی. «الو» یعنی سکوت نکرده‌ام؛ پیام فارسی کوتاه بین دسته‌ها.
- **هیچ صدایی در سایت نیست** — فایل‌های صوتی واقعی سینا هنوز نیامده؛ تا رسیدنشان بخش صدا فقط بصری است (تعمدی).

## ۶) وضعیت وریفای (آخرین دور، پاس)

- `node --check` OK · کلیک واقعی (Input.dispatchMouseEvent) روی دکمه → سفر complete
- `elementFromPoint` مرکز → `#enterbtn .ring` (هیچ چیزی روی دکمه نیست)
- چرخ ماوس ۹× پایین → صحنه تماس (v=0.80) · ۱۲× بالا → برگشت کامل به صحنه‌ی ورودی (scene=null، استیج op=1)
- هر ۵ صحنه: opacity=1/visible، متن کامل، `scrollY=0`، صفر خطای JS
- گالری: کلیک فریم ۸ → `liveIndex=8`؛ آمبر کلی (لنز/پرتو/نوار) ۴۴+ پیکسل‌هیت

## ۷) خطاهای تاریخی (دوباره‌ساز نکن!)

- **sceneStart اولین صحنه = 0** → هر جایی که از آن به عنوان «نقطه‌ی شروع» استفاده شود (استیج fade، شرط v=0) کرش منطقی می‌دهد. همیشه `sceneCenter` یا آفست صریح بگیر.
- `offsetTop` نسبت به والد. از `getBoundingClientRect().top + scrollY` یا محور مجازی استفاده کن — اسکرول واقعی دیگر وجود ندارد!
- ذرات غبار: گرید x باید **ضرب** شود در slotW*aspect، نه تقسیم (زیرپیکسل شد).
- فورگراند هرگز محو نمی‌شد؛ `blurF()` با premultiplied alpha لازم است (هاله‌ی تیره نزند).
- IIFE: انتساب `window.__reveal.start` قبل از تعریف آبجکت → کل اسکریپت می‌میرد.
- `--virtual-time-budget` rAF را خواب می‌کند؛ تست رفتاری را با CDP واقعی بزن، نه فقط dump-dom.

## ۸) کارهای باز

- [ ] فایل صوتی واقعی سینا → `assets/audio/` و اتصال به بخش صدا/پلیر (در انتظار دریافت از کاربر)
- [ ] پلیر نمونه در صحنه‌ی «صدا» (فعلاً لینک Bandcamp + میدان بصری)
- [ ] آپلود نهایی (Railway/هاست دلخواه) پس از تأیید کاربر
