from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'  # Pasta onde os arquivos serão salvos
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Função para verificar se a extensão do arquivo é permitida
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Endpoint para upload de arquivo PDF
@app.route('/upload', methods=['POST'])
def upload_file():
    # Verifica se o arquivo foi enviado na requisição
    # if 'file' not in request.files:
    #     return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    print(file)

    
    # Verifica se um arquivo foi selecionado
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400
    
    # Verifica se o arquivo é um PDF
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Cria a pasta de upload se não existir
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        # Salva o arquivo
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return jsonify({"message": "File successfully uploaded", "file_path": file_path}), 200
    else:
        return jsonify({"error": "Allowed file type is PDF"}), 400

if __name__ == '__main__':
    app.run(debug=True)
