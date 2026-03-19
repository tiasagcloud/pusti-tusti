import pandas as pd
import qrcode
import os

# Create folder to store QR images
os.makedirs("qr_codes", exist_ok=True)

# Read Excel file
df = pd.read_excel("students.xlsx")

# If columns do not exist, create them
if "qr_data" not in df.columns:
    df["qr_data"] = ""

if "qr_path" not in df.columns:
    df["qr_path"] = ""

# Generate QR for each student
for i, row in df.iterrows():
    stu_id = row["stu_id"]

    qr_data = f"PUSTI_{stu_id}"

    qr_img = qrcode.make(qr_data)

    qr_path = f"qr_codes/{stu_id}.png"
    qr_img.save(qr_path)

    # Store back into Excel
    df.at[i, "qr_data"] = qr_data
    df.at[i, "qr_path"] = qr_path

# Save updated Excel file
df.to_excel("students.xlsx", index=False)

print("✅ QR codes generated and stored successfully")
input("Press ENTER to exit...")
