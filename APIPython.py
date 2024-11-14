from flask import Flask, request, jsonify
import fitz  # PyMuPDF para manipular PDFs

app = Flask(__name__)

# Endpoint para upload e processamento do PDF
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    if file and file.filename.lower().endswith('.pdf'):
        # Processa o PDF em memória
        pdf_document = fitz.open("pdf", file.read())
        pages_content = []
        
        # Extrai o texto de cada página e armazena no JSON
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            pages_content.append(page.get_text())

        pdf_document.close()
        
        # Retorna o conteúdo das páginas em JSON
        return jsonify({"pages": pages_content}), 200
    else:
        return jsonify({"error": "Allowed file type is PDF"}), 400

if __name__ == '__main__':
    app.run(debug=True)
