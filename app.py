from flask import Flask, render_template, request, redirect
import hashlib
import os
from blockchain import store_evidence, get_evidence, get_count

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"

@app.route("/")
def index():
    return render_template("index.html")



@app.route("/dashboard")
def dashboard():
    count = get_count()
    evidences = []

    for i in range(count):
        evidences.append(get_evidence(i))

    return render_template("dashboard.html", evidences=evidences)

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    with open(filepath, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()

    store_evidence(file_hash, file.filename)

    return redirect("/dashboard")

@app.route("/verify", methods=["POST"])
def verify():
    index = int(request.form["index"])
    file = request.files["file"]

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    with open(filepath, "rb") as f:
        new_hash = hashlib.sha256(f.read()).hexdigest()

    stored_hash, name, timestamp = get_evidence(index)

    if stored_hash == new_hash:
        result = "Integrity Verified"
    else:
        result = "Tampering Detected"

    return render_template("verify.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)