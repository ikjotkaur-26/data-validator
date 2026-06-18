from flask import Flask, render_template, request, send_file
import pandas as pd
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
import os

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)
# HOME PAGE
@app.route('/')
def home():
    return render_template("index.html")


# UPLOAD + VALIDATION
@app.route('/upload', methods=['POST'])
def upload_file():

    file = request.files['file']
    country = request.form['country']

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    df = pd.read_csv(filepath, encoding='ISO-8859-1')

    # STEP 1: Remove empty rows
    df = df.dropna()

    # STEP 2: Phone validation
    if country == "india":
        df = df[df['phone'].astype(str).str.len() == 10]

    elif country == "singapore":
        df = df[df['phone'].astype(str).str.len() == 8]

    # STEP 3: Date validation
    df = df[df['date'].notna()]

    # STEP 4: Save cleaned file
    clean_path = os.path.join(OUTPUT_FOLDER, "cleaned.csv")
    df.to_csv(clean_path, index=False)

    # STEP 5: File splitting (chunks)
    chunk_size = 3  # demo size
    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i:i+chunk_size]
        chunk.to_csv(f"{OUTPUT_FOLDER}/chunk_{i}.csv", index=False)

    return send_file(clean_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)