import os
import re
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory {directory} created.")
    else:
        print(f"Directory {directory} already exists.")

PDF_DIRECTORY = "invoices"
class CustomerDetail:
    def __init__(self, customer_id, first_name, last_name, email, phone, address=None):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.address = address

    def __str__(self):
        return (f"Customer[{self.customer_id}]: {self.first_name}, {self.last_name}, {self.email}, {self.phone},"
                f"{self.address}")

class Address:
    def __init__(self, address_line_1, address_line_2, city, state, country, pin_code):
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.city = city
        self.state = state
        self.country = country
        self.pin_code = pin_code

    def __str__(self):
        return f"{self.address_line_1},{self.address_line_2}, {self.city}, {self.state}, {self.country},{self.pin_code}"

class Product:
    def __init__(self, product_id, name, quantity, unit_price, applicable_discount):
        self.product_id = product_id
        self.name = name
        self.quantity = quantity
        self.unit_price = unit_price
        self.applicable_discount = applicable_discount

    def calculate_total_price(self):
        subtotal = self.quantity * self.unit_price
        if self.applicable_discount > 0:
            subtotal -= subtotal * (self.applicable_discount / 100)
        return subtotal

    def __str__(self):
        return (f"Product[{self.product_id}]: {self.name}, quantity: {self.quantity},Unit Price: Rs{self.unit_price:.2f},Applicable Discount: {self.applicable_discount}% off, Total Price: Rs{self.calculate_total_price():.2f}")

class Invoice:
    def __init__(self, invoice_id, invoice_date, customer_detail, billing_address, total_amount, payment_mode=None):
        self.invoice_id = invoice_id
        self.invoice_date = invoice_date
        self.customer_detail = customer_detail
        self.billing_address = billing_address
        self.items = []
        self.total_amount = total_amount
        self.payment_mode = payment_mode

    def add_item(self, product, quantity):
        self.items.append({"product": product, "quantity": quantity})
        self.total_amount += product.calculate_total_price() * quantity



def __str__(self):
    item_str = "\n".join(
            [f"{item['quantity']}x {item['product'].name} @ Rs{item['product'].unit_price:.2f} each" for item in
             self.items])
    return (f"Invoice[{self.invoice_id}]: {self.invoice_date}\n"
            f"Customer: {self.customer_detail}\n"
            f"Billing Address: {self.billing_address}\n"
            f"Items:\n{item_str}\n"
            f"Total Amount: Rs{self.total_amount:.2f}\n"
            f"Payment Mode: {self.payment_mode}")

def validate_input(prompt, pattern, error_msg):
        while True:
            value = input(prompt)
            if re.match(pattern, value):
                return value
            else:
                print(error_msg)

def validate_email(prompt):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return validate_input(prompt, pattern, "Invalid email address. Please enter a valid email.")
def create_customer_detail():
    customer_id = int(validate_input("Enter customer ID: ", r"^\d+$", "Invalid input. Please enter a numeric value."))
    first_name = validate_input("Enter customer first name: ", r"^[A-Za-z]+$", "Invalid input. Please enter alphabets only.")
    last_name = validate_input("Enter customer last name: ", r"^[A-Za-z]+$", "Invalid input. Please enter alphabets only.")
    email = input("Enter customer email: ")
    phone = validate_input("Enter customer phone number: ", r"^\d+$", "Invalid input. Please enter a numeric value.")


    address_line_1 = input("Enter address line 1: ")
    address_line_2 = input("Enter address line 2: ")
    city = validate_input("Enter city: ", r"^[A-Za-z]+$", "Invalid input. Please enter alphabets only.")
    state = validate_input("Enter state: ", r"^[A-Za-z]+$", "Invalid input. Please enter alphabets only.")
    country = validate_input("Enter country: ", r"^[A-Za-z]+$", "Invalid input. Please enter alphabets only.")
    pin_code =  validate_input("Enter PIN code: ", r"^\d+$", "Invalid input. Please enter a numeric value.")

    address = Address(address_line_1, address_line_2, city, state, country, pin_code)
    customer_detail = CustomerDetail(customer_id, first_name, last_name, email, phone, address,)

    return customer_detail, address

def create_invoice(customer_detail, billing_address):
    invoice_id = int(input("Enter Invoice ID: "))
    invoice_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payment_mode = input("Enter Payment Mode: ")

    invoice = Invoice(invoice_id, invoice_date, customer_detail, billing_address, total_amount=0.0, payment_mode=payment_mode)

    while True:
        try:
            product_id = int(input("Enter Product ID (0 to finish adding products): "))
            if product_id == 0:
                break
            name = input("Enter Product Name: ")
            quantity = int(input("Enter Quantity: "))
            unit_price = float(input("Enter Unit Price: "))
            applicable_discount = float(input("Enter Applicable Discount (%): "))

            product = Product(product_id, name, quantity, unit_price,applicable_discount)
            invoice.add_item(product, quantity)
        except ValueError:
            print("Invalid input. Please enter numeric values where required.")

    return invoice

class InvoicePDF:
    def __init__(self, invoice, pdf_file_name=None):
        self.invoice = invoice

        ensure_dir(PDF_DIRECTORY)
        self.pdf_file_name = pdf_file_name or f"{PDF_DIRECTORY}/invoice_{self.invoice.invoice_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"

    def generate_pdf(self):
        c = canvas.Canvas(self.pdf_file_name, pagesize=letter)
        width, height = letter

        styles = getSampleStyleSheet()
        header_style = styles['Heading1']
        normal_style = styles['Normal']

        # Invoice Header

        c.setFont("Times-Bold", 24)
        c.setFillColor(colors.darkblue)
        c.drawCentredString(100, 705, "INVOICE")
        c.setFillColor(colors.black)

        logo = "C:\\Users\\gupta\\Pictures\\Saved Pictures\\logo.jpeg"
        c.drawImage(logo, 50, 730, width=80, height=50)


        # Company Info
        c.setFont("Times-Bold", 12)
        c.drawString(400, 770, "KIDA STUDIOS PVT LTD.")
        c.setFont("Helvetica", 10)
        c.drawString(400, 755, "DHOLE PATIL ROAD")
        c.drawString(400, 740, "SANGAMWADI")
        c.drawString(400, 725, "PUNE,MAHARASHTRA,490006")
        c.drawString(400, 710, "INDIA")

        c.setStrokeColorRGB(0.5, 0.5, 0.5)
        c.line(50, 680, 550, 680)

        c.setFont("Times-Bold", 12)
        c.drawString(50, 660, "BILL TO:   ")
        c.setFont("Helvetica", 12)
        c.drawString(50, 640, f"{self.invoice.customer_detail.first_name} {self.invoice.customer_detail.last_name}")
        c.drawString(50, 620, f"Email: {self.invoice.customer_detail.email}")
        c.drawString(50, 600, f"Phone: {self.invoice.customer_detail.phone}")

        c.setFont("Times-Bold", 12)
        c.drawString(250, 660, "SHIP TO:   ")
        c.setFont("Helvetica", 12)
        c.drawString(250, 640, f"{self.invoice.billing_address.address_line_1}")
        c.drawString(250, 620, f"{self.invoice.billing_address.address_line_2}")
        c.drawString(250, 600, f"{self.invoice.billing_address.city}, {self.invoice.billing_address.state},")
        c.drawString(250, 580, f"{self.invoice.billing_address.country}, {self.invoice.billing_address.pin_code}")

        c.setFont("Times-Bold", 12)
        c.drawString(400, 660, f"Invoice ID: {self.invoice.invoice_id}")
        c.drawString(400, 640, f"Invoice Date: {self.invoice.invoice_date}")
        # Invoice Details

        c.setStrokeColorRGB(0.5, 0.5, 0.5)
        c.line(50, 570, 550, 570)
        # Invoice Items


        item_data = [[ "Product","Quantity" ,"Unit Price","Applicable Discount", "Total Price"]]
        subtotal = 0.0
        for item in self.invoice.items:
            product = item["product"]
            quantity = item["quantity"]
            unit_price = product.unit_price
            applicable_discount = product.applicable_discount
            total_price = product.calculate_total_price()

            item_data.append(
                [product.name,
                 str(quantity) ,
                 f"Rs{unit_price:.2f}",
                 f"{applicable_discount}%",
                 f"Rs{total_price:.2f}"])
            subtotal +=total_price

        table = Table(item_data, colWidths=[150, 50, 100, 100, 100])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        table.wrapOn(c, width, height)
        table.drawOn(c, 50, 400)

        c.setFont("Times-Bold", 12)
        c.drawString(400, 350, f"Subtotal:  Rs {subtotal:.2f}")

        gst_rate = 18.0  # Adjust as per your GST rate
        gst_amount = subtotal * (gst_rate / 100)
        c.drawString(400, 330, f"GST ({gst_rate}%):  Rs {gst_amount:.2f}")

        total_amount = subtotal + gst_amount
        c.drawString(400, 310, f"Total Amount:  Rs {total_amount:.2f}")

        c.drawString(50, 350, f"Payment Mode: {self.invoice.payment_mode}")



        c.setStrokeColorRGB(0.5, 0.5, 0.5)
        c.line(50, 70, 550, 70)
        # Footer
        c.setFont("Helvetica", 10)
        c.setFillColor(colors.grey)
        c.drawCentredString(300, 50, "Thank you for your business!")
        c.drawCentredString(300, 35, "Please make checks payable to :KIDA STUDIOS PVT LTD.")
        c.drawCentredString(300, 20, "Email: kida.studios@gmail.com | Website: https://www.kidastudios.com/")
        c.showPage()
        c.save()

if __name__ == "__main__":
    # Create customer and address
    customer_detail, billing_address = create_customer_detail()

    print("Customer Detail:")
    print(customer_detail)

    print("\nBilling Address:")
    print(billing_address)

    # Create invoice
    invoice = create_invoice(customer_detail, billing_address)

    print("\nGenerated Invoice:")
    print(invoice)

    # Generate PDF
    pdf_generator = InvoicePDF(invoice)
    pdf_generator.generate_pdf()
    print(f"Invoice PDF generated successfully as {pdf_generator.pdf_file_name}.")
