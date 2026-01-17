from flask import Flask, render_template, request, jsonify
import os
from tools.resume_checker import analyze_resume
from tools.pdf_tools import merge_pdfs, pdf_to_word, compress_pdf
from tools.study_planner import create_study_plan
from tools.grade_calculator import calculate_grade

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/privacy-policy")
def privacy():
    return render_template("privacy-policy.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/resume-check", methods=["POST"])
def resume_check():
    file = request.files["resume"]
    path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(path)
    result = analyze_resume(path)
    return jsonify(result)

@app.route("/grade-calc", methods=["POST"])
def grade_calc():
    data = request.json
    return jsonify(calculate_grade(data))

@app.route("/study-plan", methods=["POST"])
def study_plan():
    data = request.json
    return jsonify(create_study_plan(data))

if __name__ == "__main__":
    app.run(debug=True)
