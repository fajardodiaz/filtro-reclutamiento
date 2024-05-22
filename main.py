from flask import Flask, request, render_template, send_file
from utils.filter import filter_candidate
import os, glob
import csv

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join('static', 'uploads')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/filter", methods=["GET", "POST"])
def filter():
    if request.method == "POST":            
        # Save files into folder
        for f in request.files.getlist('cvfiles'):
            f.save(os.path.join(app.config["UPLOAD_FOLDER"], f.filename))
        
        # Get Keywords
        keywords_form = request.form["keywords"]
        keywords = keywords_form.lower()

        # Execute filter function
        all_results = filter_candidate(app.config['UPLOAD_FOLDER'], os.path.join(app.config["UPLOAD_FOLDER"], "results.csv"), keywords)

        # Delete files
        files = glob.glob(f"{app.config['UPLOAD_FOLDER']}/**")
        for f in files:
            os.remove(f)

        # Get only the positive results
        results = []

        for res in all_results:
            if res[2] == 1:
                results.append(res)

        # Write the results to a file
        with open(f"{os.path.join(app.config['UPLOAD_FOLDER'])}/results.csv" , 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['Candidato', 'Habilidad', 'Resultado'])

            for file in results:
                writer.writerow(file)

        return render_template("filter.html", results=results)
    
    elif request.method == "GET":
        return render_template("filter.html")
    

@app.route("/csv", methods=["GET"])
def get_csv():
    try:
        return send_file(
            os.path.join(f"{os.path.join(app.config['UPLOAD_FOLDER'])}/results.csv"),
            mimetype='text/csv',
            download_name='results.csv',
            as_attachment=True
        )
    finally:
        # Delete files
        files = glob.glob(f"{app.config['UPLOAD_FOLDER']}/*.csv")
        for f in files:
            os.remove(f)