"""Aasaan Tools site builder.
1) Neeche 3 settings apni values se badlo.  2) `python build.py` chalao.  3) `docs/` folder GitHub Pages pe publish karo.
"""
import os, shutil, json, datetime

SITE_URL = "https://toushif-ansari22.github.io/aasaan-tools"      # <- apna domain (bina last slash). GitHub Pages: https://toushif-ansari22.github.io/aasaan-tools
EMAIL = "tashiuddinkhan306@gmail.com"             # <- apni email
ADSENSE_ID = ""                       # <- approval ke baad: "ca-pub-XXXXXXXXXXXXXXXX"

NAME = "Aasaan Tools"
OUT = "docs"
TODAY = datetime.date.today().isoformat()

# id, slug, name, meta description, intro, how it works, faq question, faq answer
M = [
("emi","emi-calculator","EMI Calculator","Free EMI calculator for home, car and personal loans. See monthly EMI, total interest and total payment instantly.",
 "Enter your loan amount, interest rate and tenure to see your monthly EMI, total interest and total payment.",
 "EMI is calculated with the reducing-balance formula EMI = P × r × (1+r)ⁿ / ((1+r)ⁿ − 1), where P is the loan amount, r the monthly interest rate and n the number of months. Processing fees and insurance charged by banks are not included.",
 "Does a longer tenure reduce my EMI?","Yes. A longer tenure lowers the monthly EMI but increases the total interest you pay over the life of the loan."),
("gst","gst-calculator","GST Calculator","Free GST calculator for India. Add or remove GST at 5%, 12%, 18% or 28% and see CGST and SGST split.",
 "Add GST to a base price or remove it from a GST-inclusive price, at any standard GST rate.",
 "Use Add GST when your price is before tax. Use Remove GST when the price already includes GST. The tool shows the base price, total GST, the CGST and SGST halves, and the final price.",
 "What is the difference between CGST and SGST?","For sales inside a state, GST is split equally between the central government (CGST) and the state (SGST). For sales between states, IGST applies instead."),
("sip","sip-calculator","SIP Calculator","Free SIP calculator. Estimate the future value of your monthly mutual fund SIP investment.",
 "Enter a monthly amount, expected return and time period to estimate how much your SIP can grow.",
 "Future value = P × [((1+i)ⁿ − 1) / i] × (1+i), where P is the monthly investment, i the monthly return and n the number of months. This is an estimate for planning and not financial advice.",
 "Are SIP returns guaranteed?","No. Mutual fund returns depend on the market. The calculator only shows an estimate based on the return rate you enter."),
("age","age-calculator","Age Calculator","Free age calculator. Find your exact age in years, months and days from your date of birth.",
 "Pick a date of birth to see the exact age in years, months and days, plus total days and weeks lived.",
 "Age is counted in completed years, months and days up to today's date on your device.",
 "Does it include today?","Yes. The age is calculated up to the current date in your device's calendar."),
("percent","percentage-calculator","Percentage Calculator","Free percentage calculator. Find X% of Y, what percent one number is of another, and increase or decrease by a percentage.",
 "Enter X and Y to get four common percentage answers at once.",
 "The tool shows X% of Y, X as a percentage of Y, Y increased by X% and Y decreased by X%. Useful for marks, discounts, price hikes and growth.",
 "How do I calculate a discount?","Enter the discount percentage as X and the original price as Y, then read the 'decreased by' result."),
("words","word-counter","Word Counter","Free online word counter. Count words, characters, sentences and estimated reading time.",
 "Paste or type your text to count words, characters, sentences and reading time.",
 "Words are counted by splitting on whitespace. Sentences are counted by full stops, question marks, exclamation marks and the Hindi danda.",
 "How is reading time calculated?","We assume an average adult reading speed of about 200 words per minute."),
("image","image-resizer","Image Resizer","Free online image resizer. Change image size, format and quality in your browser. No upload needed.",
 "Choose an image, set the new width and height, pick a format and download the result.",
 "Resizing happens inside your browser using the canvas API. Lower the quality value for JPG or WebP to get a smaller file size.",
 "Is my image uploaded to a server?","No. Everything happens on your device, so your photo never leaves your browser."),
("password","password-generator","Password Generator","Free strong password generator. Create random passwords with letters, numbers and symbols.",
 "Choose a length and character types, then generate a strong random password.",
 "Passwords are created with your browser's cryptographic random number generator. Use at least 12 characters and a different password for every account.",
 "Are generated passwords stored?","No. They are generated on your device and never sent or saved anywhere."),
]
SLUG = {m[0]: m[1] for m in M}

ADS = (f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_ID}" crossorigin="anonymous"></script>'
       if ADSENSE_ID else "")

HEAD = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>@TITLE@</title><meta name="description" content="@DESC@"><link rel="canonical" href="@URL@">
<meta property="og:title" content="@TITLE@"><meta property="og:description" content="@DESC@"><meta property="og:type" content="website"><meta property="og:url" content="@URL@">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@500;700;800&family=Figtree:wght@400;500;600&display=swap">
<link rel="stylesheet" href="style.css">@ADS@</head><body data-tool="@CUR@">
<header><div class="wrap"><a class="logo" href="index.html">aasaan<b>tools</b></a><p>Free calculators and utilities. No signup, and your data stays in your browser.</p></div></header>
"""
FOOT = """<footer>© @YEAR@ @NAME@ · <a href="about.html">About</a> · <a href="privacy.html">Privacy Policy</a> · <a href="terms.html">Terms</a> · <a href="contact.html">Contact</a></footer>
@SCRIPT@</body></html>"""


def page(fname, title, desc, main, cur="", script=False, wide=False):
    h = (HEAD.replace("@TITLE@", title).replace("@DESC@", desc)
         .replace("@URL@", f"{SITE_URL}/{'' if fname == 'index.html' else fname}")
         .replace("@ADS@", ADS).replace("@CUR@", cur))
    f = FOOT.replace("@YEAR@", str(datetime.date.today().year)).replace("@NAME@", NAME).replace(
        "@SCRIPT@", '<script src="app.js"></script>' if script else "")
    open(f"{OUT}/{fname}", "w", encoding="utf-8").write(h + main + f)


shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT)
shutil.copy("src/style.css", f"{OUT}/style.css")
open(f"{OUT}/app.js", "w").write(open("src/tools.js").read() + """
const cur=document.body.dataset.tool;const t=tools.find(x=>x.id===cur);
if(t){document.getElementById('tool').innerHTML=t.html();t.init();}
""")

def nav(cur):
    return '<nav aria-label="Tools">' + "".join(
        f'<a href="{m[1]}.html"{" class=on" if m[0]==cur else ""}>{m[2]}</a>' for m in M) + "</nav>"

# tool pages
for id_, slug, name, desc, intro, how, fq, fa in M:
    main = f"""<main class="wrap">{nav(id_)}<section><div class="panel"><h1>{name}</h1><p class="sub">{intro}</p>
<div id="tool"></div>
<div class="about"><h2>How it works</h2><p>{how}</p><h2>Frequently asked</h2><h3>{fq}</h3><p>{fa}</p>
<h2>More tools</h2><p>{" · ".join(f'<a href="{x[1]}.html">{x[2]}</a>' for x in M if x[0]!=id_)}</p></div></div></section></main>"""
    page(f"{slug}.html", f"{name} – Free Online | {NAME}", desc, main, cur=id_, script=True)

# home
cards = "".join(f'<a class="card" href="{m[1]}.html"><h2>{m[2]}</h2><p>{m[4]}</p></a>' for m in M)
page("index.html", f"{NAME} – Free EMI, GST, SIP, Age Calculator & Image Resizer",
     "Free online tools for India: EMI calculator, GST calculator, SIP calculator, age calculator, image resizer, word counter and password generator.",
     f'<main class="wrap one"><h1>Free online tools for everyday work</h1><p class="sub">Calculators and utilities that load fast and work on any phone. Pick a tool to start.</p><div class="cards">{cards}</div></main>')

# legal pages
page("about.html", f"About | {NAME}", f"About {NAME}.",
     f'<main class="wrap one"><h1>About {NAME}</h1><p>{NAME} is a set of simple, free tools for everyday money, text and image tasks. We build each tool to be fast, accurate and easy to use on a phone.</p><p>Most tools run entirely in your browser, so the numbers, text and images you enter stay on your device.</p><p>Found a mistake or want a new tool? Write to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></main>')
page("contact.html", f"Contact | {NAME}", f"Contact {NAME}.",
     f'<main class="wrap one"><h1>Contact</h1><p>For feedback, bug reports or tool requests, email us at <a href="mailto:{EMAIL}">{EMAIL}</a>. We usually reply within a few days.</p></main>')
page("terms.html", f"Terms and Disclaimer | {NAME}", f"Terms of use and disclaimer for {NAME}.",
     f'<main class="wrap one"><h1>Terms and Disclaimer</h1><p>Last updated: {TODAY}</p><h2>Use of tools</h2><p>The tools on this site are provided free of charge for general information. Results are estimates and may differ from the figures your bank, tax advisor or financial institution gives you.</p><h2>No financial advice</h2><p>The EMI, GST and SIP calculators are not financial, tax or investment advice. Please consult a qualified professional before making financial decisions.</p><h2>No warranty</h2><p>We try to keep the tools accurate but provide them as they are, without any warranty. We are not liable for any loss arising from their use.</p></main>')
page("privacy.html", f"Privacy Policy | {NAME}", f"Privacy policy of {NAME}.",
     f'<main class="wrap one"><h1>Privacy Policy</h1><p>Last updated: {TODAY}</p><h2>Data you enter</h2><p>Text, numbers and images you enter in our tools are processed in your browser. We do not upload or store them on our servers.</p><h2>Cookies and advertising</h2><p>We use Google AdSense to show ads. Google and its partners may use cookies to show ads based on your previous visits to this and other websites. You can opt out of personalised ads at <a href="https://www.google.com/settings/ads">Google Ads Settings</a> or <a href="https://www.aboutads.info">aboutads.info</a>.</p><h2>Analytics</h2><p>We may use privacy-friendly analytics to count visits and understand which tools are used. This data is aggregated and does not identify you.</p><h2>Contact</h2><p>Questions about this policy: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></main>')

# SEO files
urls = ["index.html"] + [f"{m[1]}.html" for m in M] + ["about.html", "contact.html", "privacy.html", "terms.html"]
open(f"{OUT}/sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' +
    "".join(f"<url><loc>{SITE_URL}/{'' if u=='index.html' else u}</loc><lastmod>{TODAY}</lastmod></url>" for u in urls) + "</urlset>")
open(f"{OUT}/robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
if ADSENSE_ID:
    open(f"{OUT}/ads.txt", "w").write(f"google.com, {ADSENSE_ID.replace('ca-','')}, DIRECT, f08c47fec0942fa0\n")
print("Done:", len(urls), "pages in", OUT + "/")
