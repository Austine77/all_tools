from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from tools.resume_checker import analyze_resume
from tools.pdf_tools import merge_pdfs, pdf_to_word, compress_pdf
from tools.study_planner import create_study_plan
from tools.grade_calculator import calculate_grade
from werkzeug.utils import secure_filename

# ----------------------
# App Setup
# ----------------------
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20MB upload limit
ALLOWED_EXTENSIONS = {'pdf'}

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ----------------------
# Helper Functions
# ----------------------
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ----------------------
# Frontend Routes
# ----------------------
@app.route("/index")
def index():
    return render_template("index")

@app.route("/about")
def about():
    return render_template("about")

@app.route("/contact")
def contact():
    return render_template("contact")

@app.route("/privacy-policy")
def privacy():
    return render_template("privacy-policy")

@app.route("/terms")
def terms():
    return render_template("terms")

# ----------------------
# Resume Checker API
# ----------------------
@app.route("/resume-check", methods=["POST"])
def resume_check():
    if "resume" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["resume"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        result = analyze_resume(path)
        return jsonify(result)
    else:
        return jsonify({"error": "Invalid file type"}), 400

# ----------------------
# PDF Tools APIs
# ----------------------
@app.route("/pdf/merge", methods=["POST"])
def pdf_merge_api():
    files = request.files.getlist("pdfs")
    if not files or len(files) < 2:
        return jsonify({"error": "Upload at least 2 PDFs"}), 400
    paths = []
    for f in files:
        if allowed_file(f.filename):
            filename = secure_filename(f.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            f.save(path)
            paths.append(path)
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], "merged.pdf")
    merge_pdfs(paths, output_path)
    return jsonify({"message": "PDFs merged", "output_file": "merged.pdf"})

@app.route("/pdf/to-word", methods=["POST"])
def pdf_to_word_api():
    file = request.files.get("pdf")
    if not file or not allowed_file(file.filename):
        return jsonify({"error": "Invalid PDF"}), 400
    filename = secure_filename(file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)
    output_path = pdf_to_word(path)
    return jsonify({"message": "PDF converted to Word", "output_file": os.path.basename(output_path)})

@app.route("/pdf/compress", methods=["POST"])
def pdf_compress_api():
    file = request.files.get("pdf")
    if not file or not allowed_file(file.filename):
        return jsonify({"error": "Invalid PDF"}), 400
    filename = secure_filename(file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)
    output_path = compress_pdf(path)
    return jsonify({"message": "PDF compressed", "output_file": os.path.basename(output_path)})

# ----------------------
# Grade Calculator API
# ----------------------
@app.route("/grade-calc", methods=["POST"])
def grade_calc():
    data = request.json
    if not data:
        return jsonify({"error": "No input data"}), 400
    return jsonify(calculate_grade(data))

# ----------------------
# Study Planner API
# ----------------------
@app.route("/study-plan", methods=["POST"])
def study_plan():
    data = request.json
    if not data:
        return jsonify({"error": "No input data"}), 400
    return jsonify(create_study_plan(data))

# ----------------------
# Serve uploaded files (optional)
# ----------------------
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ----------------------
# Run App
# ----------------------
if __name__ == "__main__":
    # Use host='0.0.0.0' for Render deployment
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)
