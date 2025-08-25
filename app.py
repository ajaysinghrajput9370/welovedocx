from flask import Flask, render_template, request, send_file, send_from_directory
import os
import uuid
import threading
import time
import shutil
from datetime import datetime, timedelta
from highlight_feature import highlight_pdf

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# Set the template folder explicitly
app.template_folder = 'templates'

# ---------------- AUTO CLEANUP FUNCTION ----------------
def cleanup_old_files():
    """Delete files older than 10 minutes from upload and result folders"""
    while True:
        try:
            now = time.time()
            # Clean upload folder
            for filename in os.listdir(UPLOAD_FOLDER):
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                if os.path.isfile(file_path):
                    # Delete files older than 10 minutes
                    if now - os.path.getmtime(file_path) > 600:  # 600 seconds = 10 minutes
                        os.remove(file_path)
                        print(f"Deleted old file: {file_path}")
            
            # Clean result folder
            for filename in os.listdir(RESULT_FOLDER):
                file_path = os.path.join(RESULT_FOLDER, filename)
                if os.path.isfile(file_path):
                    # Delete files older than 10 minutes
                    if now - os.path.getmtime(file_path) > 600:  # 600 seconds = 10 minutes
                        os.remove(file_path)
                        print(f"Deleted old file: {file_path}")
        except Exception as e:
            print(f"Error during cleanup: {e}")
        
        # Run cleanup every 5 minutes
        time.sleep(300)

# Start the cleanup thread
cleanup_thread = threading.Thread(target=cleanup_old_files, daemon=True)
cleanup_thread.start()

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("welovedoc.html")

# ---------------- HIGHLIGHT ----------------
@app.route("/highlight")
def highlight_page():
    return render_template("highlight.html")

@app.route("/process", methods=["POST"])
def process():
    pdf_file = request.files["pdf_file"]
    excel_file = request.files["excel_file"]
    mode = request.form.get("mode", "pf")

    # unique filenames
    pdf_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_{pdf_file.filename}")
    excel_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_{excel_file.filename}")
    pdf_file.save(pdf_path)
    excel_file.save(excel_path)

    # run highlighter
    output_pdf, not_found_excel = highlight_pdf(
        pdf_path, excel_path, highlight_type=mode, output_folder=RESULT_FOLDER
    )

    if output_pdf:
        return send_file(output_pdf, as_attachment=True)
    else:
        return "No matches found in PDF."

# ---------------- ALL TOOL PAGES ----------------
@app.route("/merge-pdf")
def merge_pdf_page():
    return render_template("merge-pdf.html")

@app.route("/split-pdf")
def split_pdf_page():
    return render_template("split-pdf.html")

@app.route("/compress-pdf")
def compress_pdf_page():
    return render_template("compress-pdf.html")

@app.route("/jpg-to-pdf")
def jpg_to_pdf_page():
    return render_template("jpg-to-pdf.html")

@app.route("/word-to-pdf")
def word_to_pdf_page():
    return render_template("word-to-pdf.html")

@app.route("/pdf-to-word")
def pdf_to_word_page():
    return render_template("pdf-to-word.html")

@app.route("/excel-to-pdf")
def excel_to_pdf_page():
    return render_template("excel-to-pdf.html")

@app.route("/pdf-to-excel")
def pdf_to_excel_page():
    return render_template("pdf-to-excel.html")

@app.route("/pdf-to-jpg")
def pdf_to_jpg_page():
    return render_template("pdf-to-jpg.html")

@app.route("/rotate-pdf")
def rotate_pdf_page():
    return render_template("rotate-pdf.html")

@app.route("/extract-pages")
def extract_pages_page():
    return render_template("extract-pages.html")

@app.route("/protect-pdf")
def protect_pdf_page():
    return render_template("protect-pdf.html")

@app.route("/pf-esic-ecr")
def pf_esic_ecr_page():
    return render_template("pf-esic-ecr.html")

@app.route("/stamp")
def stamp_page():
    return render_template("stamp.html")

@app.route("/all-tools")
def all_tools_page():
    return render_template("all-tools.html")

@app.route("/about")
def about_page():
    return render_template("about.html")

@app.route("/pricing")
def pricing_page():
    return render_template("pricing.html")

@app.route("/contact")
def contact_page():
    return render_template("contact.html")

@app.route("/faq")
def faq_page():
    return render_template("faq.html")

@app.route("/privacy-policy")
def privacy_policy_page():
    return render_template("privacy-policy.html")

@app.route("/terms-of-service")
def terms_of_service_page():
    return render_template("terms-of-service.html")

@app.route("/business-solutions")
def business_solutions_page():
    return render_template("business-solutions.html")

# ---------------- SERVE LOGO FROM TEMPLATES FOLDER ----------------
@app.route('/logo.png')
def serve_logo():
    return send_from_directory('templates', 'logo.png')

if __name__ == "__main__":
    app.run(debug=True)