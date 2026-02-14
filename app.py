from flask import Flask, render_template, request, redirect, session, jsonify, send_file
from flask_bcrypt import Bcrypt
import sqlite3
import os
from groq import Groq
from dotenv import load_dotenv
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

# ---------------- LOAD ENV ----------------
load_dotenv()

app = Flask(__name__)
app.secret_key = "super_secret_key"
bcrypt = Bcrypt(app)

# ---------------- GROQ CLIENT ----------------
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user[2], password):
            session["user"] = username
            return redirect("/")
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = bcrypt.generate_password_hash(
            request.form["password"]).decode("utf-8")

        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users(username, password) VALUES(?,?)",
                           (username, password))
            conn.commit()
            conn.close()
            return redirect("/login")
        except:
            return render_template("register.html", error="Username already exists")

    return render_template("register.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


# ---------------- HOME (PROTECTED) ----------------
@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")
    return render_template("index.html")


# ---------------- GENERATE AI ----------------
@app.route("/generate", methods=["POST"])
def generate():

    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()

    prompt = f"""
You are an educational curriculum planner.

Generate a COMPLETE semester-wise weekly curriculum.

Inputs:
Educational Level: {data['education_level']}
Skill/Course Name: {data['skill_name']}
Number of Semesters: {data['num_semesters']}
Weekly Hours: {data['weekly_hours']}
Industry Focus: {data['industry_focus']}

STRICT REQUIREMENTS:

1. Generate ALL semesters from 1 to {data['num_semesters']}.
2. Each semester must have exactly 16 weeks.
3. Each week must follow EXACTLY this format:

Semester X:
Week 1 - Focus Area - Activities
Week 2 - Focus Area - Activities
...
Week 16 - Focus Area - Activities

4. Do NOT summarize.
5. Do NOT skip weeks.
6. Do NOT add explanations.
7. Use ONLY normal hyphen (-).
8. Output plain text only.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    output = response.choices[0].message.content
    session["curriculum"] = output

    return jsonify({"curriculum": output})


# ---------------- BRANDING PAGE ----------------
@app.route("/branding")
def branding():
    if "user" not in session:
        return redirect("/login")
    return render_template("branding.html")


# ---------------- GENERATE PDF ----------------
@app.route("/generate-pdf", methods=["POST"])
def generate_pdf():

    if "user" not in session:
        return redirect("/login")

    institution = request.form["institution_name"]
    curriculum = session.get("curriculum")
    logo = request.files.get("logo")

    pdf_path = "generated_curriculum.pdf"
    doc = SimpleDocTemplate(pdf_path)
    elements = []

    styles = getSampleStyleSheet()

    # ---------------- ADD LOGO ----------------
    if logo and logo.filename != "":
        upload_folder = "static"

        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        logo_path = os.path.join(upload_folder, logo.filename)
        logo.save(logo_path)

        try:
            img = Image(logo_path, width=1.5 * inch, height=1.5 * inch)
            elements.append(img)
            elements.append(Spacer(1, 20))
        except:
            print("Error loading image into PDF")

    # ---------------- ADD INSTITUTION TITLE ----------------
    elements.append(Paragraph(institution, styles["Heading1"]))
    elements.append(Spacer(1, 20))

    # ---------------- ADD CURRICULUM ----------------
    if curriculum:
        for line in curriculum.split("\n"):
            elements.append(Paragraph(line, styles["Normal"]))
            elements.append(Spacer(1, 8))

    doc.build(elements)

    return send_file(pdf_path, as_attachment=True)


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)
