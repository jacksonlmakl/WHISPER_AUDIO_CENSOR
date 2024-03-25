from flask import Flask, request,send_file, render_template_string
import os
from werkzeug.utils import secure_filename
from main_bulk import main

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_PATH'] = 1024 * 1024 * 1024  # Max upload size, adjust as needed

HTML_FORM = '''
<!DOCTYPE html>
<html>
<style>
body {
    font-family: 'Arial', sans-serif;
    background-color: #f5f5f5;
    margin: 0;
    padding: 20px;
    color: #333;
}

h2 {
    color: #444;
}

form {
    background-color: #fff;
    max-width: 600px;
    margin: 40px auto;
    padding: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
}

input[type="file"],
input[type="text"] {
    width: 100%;
    padding: 10px;
    margin: 8px 0 20px;
    display: inline-block;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
    font-size: 16px;
}

input[type="submit"] {
    width: 100%;
    background-color: #4CAF50;
    color: white;
    padding: 14px 20px;
    margin: 8px 0;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 18px;
}

input[type="submit"]:hover {
    background-color: #45a049;
}

label {
    font-size: 16px;
    color: #666;
}

</style>
<head>
    <title>Upload Audio for Censoring</title>
</head>
<body>
    <h2>Upload Audio File</h2>
    <form method="post" action="/upload" enctype="multipart/form-data">
        <label for="audioFile">Choose an audio file:</label>
        <input type="file" id="audioFile" name="audioFile" accept="audio/*" required><br><br>
        <label for="badWords">Bad words (comma-separated):</label>
        <input type="text" id="badWords" name="badWords" required><br><br>
        <input type="submit" value="Upload and Censor">
    </form>
</body>
</html>
'''


@app.route('/')
def index():
    return render_template_string(HTML_FORM)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'audioFile' not in request.files:
        return "No file part", 400
    file = request.files['audioFile']
    if file.filename == '':
        return "No selected file", 400

    bad_words = request.form.get('badWords')
    if not bad_words:
        return "Bad words not specified", 400

    bad_words_list = [word.strip() for word in bad_words.split(',')]

    if file and all(bad_words_list):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Call the censoring function
        output_path = main(file_path, bad_words_list)
        # Serve the censored audio file
        return send_file(path_or_file=output_path,as_attachment=True)

    return "Invalid request", 400


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
