print("🔥 APP.PY IS RUNNING")

from flask import Flask, render_template, request, send_file
from quote_engine import calculate_quote
from weasyprint import HTML
import pandas as pd
import os
import json
from datetime import datetime





app = Flask(__name__)

#Global variable to store current quote in memory.
CURRENT_QUOTE = {}

#helper functions for loading and saving quotes
def load_quotes():
    if not os.path.exists("quotes.json"):
        return []
    with open("quotes.json", "r") as f:
        return json.load(f)


def save_quotes(quotes):
    with open("quotes.json", "w") as f:
        json.dump(quotes, f, indent=2)


# ---- ROUTES ----
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/quote", methods=["POST"])
def quote():

    data = request.form

    customer_name = data.get("customer_name")
    cart_type = data.get("cart_type")

    selected_parts = []
    for part in ["lift_kit", "wheels", "leds"]:
        if data.get(part):
            selected_parts.append(part)

    quote = calculate_quote(cart_type, selected_parts)

    #STORE THE QUOTE
    quote_data = {
        "id": len(load_quotes()) + 1,
        "customer_name": customer_name,
        "cart_type": cart_type,
        "selected_parts": selected_parts,
        "quote": quote,
        "timestamp": datetime.now().isoformat()
    }

    quotes = load_quotes()
    quotes.append(quote_data)
    save_quotes(quotes)

    CURRENT_QUOTE = quote_data

    return render_template(
        "quote.html",
        customer_name=customer_name,
        quote=quote
    )

@app.route("/export/pdf")
def export_pdf():

    global CURRENT_QUOTE

    if not CURRENT_QUOTE:
        return "No quote found. Create a quote first."

    html = render_template(
        "quote.html",
        customer_name=CURRENT_QUOTE["customer_name"],
        quote=CURRENT_QUOTE["quote"]
    )

    pdf_file = "quote.pdf"
    HTML(string=html).write_pdf(pdf_file)

    return send_file(pdf_file, as_attachment=True)

@app.route("/export/excel")
def export_excel():

    global CURRENT_QUOTE

    if not CURRENT_QUOTE:
        return "No quote found. Create a quote first."

    q = CURRENT_QUOTE["quote"]

    data = {
        "Item": ["Base", "Parts", "Labor", "Total"],
        "Amount": [
            q["base"],
            q["parts_total"],
            q["labor_cost"],
            q["total"]
        ]
    }

    df = pd.DataFrame(data)

    file = "quote.xlsx"
    df.to_excel(file, index=False)

    return send_file(file, as_attachment=True)


@app.route("/quotes")
def quotes_list():
    quotes = load_quotes()
    return render_template("quotes.html", quotes=quotes)


    

# ---- START SERVER (MUST BE LAST) ----
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)