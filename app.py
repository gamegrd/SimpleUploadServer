import os
from flask import Flask, request, send_from_directory, render_template, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files[]' not in request.files:
        return jsonify({'error': 'No files selected'}), 400
    
    files = request.files.getlist('files[]')
    results = []
    
    for file in files:
        if file.filename == '':
            continue
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            results.append({
                'name': filename,
                'url': f'/download/{filename}',
                'size': os.path.getsize(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            })
        else:
            results.append({
                'name': file.filename,
                'error': 'File type not allowed'
            })
    
    return jsonify({'files': results})

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/list')
def list_files():
    files = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.isfile(path):
            files.append({
                'name': filename,
                'url': f'/download/{filename}',
                'size': os.path.getsize(path)
            })
    return jsonify({'files': files})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=60000, debug=True)