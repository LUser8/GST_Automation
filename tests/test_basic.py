import requests
from bs4 import BeautifulSoup as bs

url_invoice_retrieve = "https://book.goindigo.in/Booking/GSTInvoiceDetails"

booking_reference_number = ""
payload1 = {"indigoGSTDetails.PNR": booking_reference_number}
page1 = requests.post(url_invoice_retrieve, data=payload1, timeout=60)

if "Sorry we are unable to process your request at this time" in page1.text:
    print("Status: wait")
else:
    print("status: success")
# with open("result2.html", "w") as f:
#     f.write(page1.text)
