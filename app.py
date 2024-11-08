import os
import pytesseract
import cv2
from flask import Flask, request, render_template

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

LANGUAGES = {
    'english': 'eng',
    'arabic': 'ara',
    'french': 'fra'
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            return "No file part"
        
        file = request.files['image']
        language = request.form.get('language')

        if file.filename == '':
            return "No selected file"
        
        if file and language in LANGUAGES:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            
            img = cv2.imread(filepath)
            text = pytesseract.image_to_string(img, lang=LANGUAGES[language])
            
            return render_template('index.html', text=text, img_path=filepath, language=language)
    
    return render_template('index.html', text=None, img_path=None, language=None)

if __name__ == '__main__':
    app.run(debug=True)
