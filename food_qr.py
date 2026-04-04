import os
import pandas as pd
import qrcode

if not os.path.exists("qr_codes"):
    os.makedirs("qr_codes")
# Load Excel
df = pd.read_excel("foods.xlsx")

for index, row in df.iterrows():
    food_id = row['food_id']
    
    # Data inside QR (can also be JSON)
    qr_data = f"http://localhost:5000/food/{food_id}"
    
    img = qrcode.make(qr_data)
    img.save(f"qr_codes/food_{food_id}.png")
    