from flask import Flask, request, send_file, jsonify
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

app = Flask(__name__)

OUTPUT_FOLDER = "invoices"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/generate_invoice', methods=['POST'])
def generate_invoice():
    data = request.json
    
    if not data or 'user' not in data or 'cart' not in data:
        return jsonify({"error": "Faltan datos"}), 400

    user = data['user']
    cart = data['cart']
    invoice_filename = f"{OUTPUT_FOLDER}/invoice_{user['id']}.pdf"

    # Generar PDF con ReportLab
    c = canvas.Canvas(invoice_filename, pagesize=letter)
    c.drawString(100, 750, f"Factura para: {user['name']}")
    c.drawString(100, 730, f"Email: {user['email']}")

    y_position = 700
    total = 0

    for item in cart:
        c.drawString(100, y_position, f"{item['name']} - {item['quantity']} x ${item['price']}")
        total += item['quantity'] * item['price']
        y_position -= 20

    c.drawString(100, y_position - 20, f"Total: ${total}")
    c.save()

    return jsonify({"message": "Factura generada", "invoice": invoice_filename})

@app.route('/download_invoice/<user_id>', methods=['GET'])
def download_invoice(user_id):
    invoice_filename = f"{OUTPUT_FOLDER}/invoice_{user_id}.pdf"
    if not os.path.exists(invoice_filename):
        return jsonify({"error": "Factura no encontrada"}), 404
    return send_file(invoice_filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
