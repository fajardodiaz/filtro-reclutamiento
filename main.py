from flask import Flask, request, render_template, send_file
from utils.filter import filter_candidate
from utils.accountability import compare_codes
import csv, shutil, os, glob

app = Flask(__name__, static_url_path='/static')

# Folder to save the files
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
    

@app.route("/accountability", methods=["GET", "POST"])
def accountability():
    if request.method == "GET":
        return render_template("accountability.html")
    elif request.method == "POST":
        # Create the folders to upload files
        path_to_create = "accountability"
        path_for_colaborators = "colaborators"
        path_for_support_files = "support"
        path_for_results = "results"
        
        # Create the root path
        complete_path = os.path.join(UPLOAD_FOLDER, path_to_create)
        
        # Path for necessary files
        colaborators_path = os.path.join(complete_path, path_for_colaborators)
        support_path = os.path.join(complete_path, path_for_support_files)
        results_path = os.path.join(complete_path, path_for_results)

        # Create the folders
        os.mkdir(complete_path)
        os.mkdir(colaborators_path)
        os.mkdir(support_path)
        os.mkdir(results_path)

        # Save the support files
        for f in request.files.getlist('support-files'):
            f.save(os.path.join(support_path, f.filename))
        
        # Save employee list
        employee_file = ""
        for f in request.files.getlist('employee-list'):
            employee_file = os.path.join(colaborators_path, f.filename) 
            f.save(employee_file)
        
        # Get the support filanems
        support_files_array = os.listdir(support_path)
        other_files_paths = [os.path.join(support_path, file) for file in support_files_array]

        # Execute function
        results = compare_codes(employee_file, *other_files_paths)
        results.to_csv(os.path.join(results_path, "results.csv"), sep=";")
        return render_template("accountability.html", results_ready = True)
    
@app.route("/csvaccountability", methods=["GET"])
def get_csv_accountability():
    try:
        return send_file(
            os.path.join(f"{os.path.join(app.config['UPLOAD_FOLDER'])}/accountability/results/results.csv"),
            mimetype='text/csv',
            download_name='results.csv',
            as_attachment=True
        )
    finally:
        # Delete folder
        path = os.path.join(UPLOAD_FOLDER, "accountability")
        try:
            shutil.rmtree(path)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))

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