import os
from flask import request, current_app
from werkzeug.utils import secure_filename

def init_app(app):
    """Initialize app configuration."""
    upload_folder = os.path.join(app.root_path, 'static/uploads')  
    os.makedirs(upload_folder, exist_ok=True)  # Ensure upload directory exists
    app.config['UPLOAD_FOLDER'] = upload_folder

def upload_files():
    """Handle multiple file uploads and return filenames."""
    if 'images' not in request.files:
        return []
    
    files = request.files.getlist('images')
    filenames = []
    
    upload_folder = current_app.config['UPLOAD_FOLDER']  # Use app config

    for file in files:
        if file.filename:  # Check if file is selected
            filename = secure_filename(file.filename)  # Secure filename
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)
            filenames.append(filename)
    
    return filenames  # You can also return {'filenames': filenames} if using JSON
