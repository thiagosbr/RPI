from flask import Flask, request, jsonify
import fitz  # PyMuPDF para manipular PDFs
import re  # Para usar expressões regulares na busca de padrões no texto

app = Flask(__name__)

# Função para extrair os dados de um processo de uma única página
def extrair_dados_pagina(texto):
    processos = []

    numero_processos = re.findall(r'BR\d{4}\d{7}-\d{1}', texto)
    numero_processo = re.findall(r'BR\d{4}\d{7}-\d{1}', texto)
    
    # Regex para capturar o titular (entre Titular: e Procurador)
    titulares = re.findall(r'Titular:\s*(.*?)\s*Procurador', texto, re.DOTALL)
    
    # Regex para capturar o procurador (entre Procurador: e Detalhes do despacho)
    procuradores = re.findall(r'Procurador:\s*(.*?)\s*Detalhes do despacho', texto, re.DOTALL)
    
    # Regex para capturar os detalhes do despacho (entre Detalhes do despacho: e fim do texto)
    detalhes = re.findall(r'Detalhes do despacho:\s*(.*?)\s*(?=BR\d{4}\d{7}-\d{1}|$)', texto, re.DOTALL)

    
    # # Expressões regulares para identificar as partes do processo
    # # numero_processos = re.findall(r'nBR\d{4}\d{7}-\d{1}', texto)  # Padrão de número de processo: BR302020005019-3
    # numero_processos = re.findall(r'\s*BR\d{4}\d{7}-\d{1}', texto)
    # # Regex corrigida
    # numero_processos = re.findall(r'BR\d{4}\d{7}-\d{1}', texto)

    # titulares = re.findall(r'Titular: (.*?) Procurador', texto, re.DOTALL)  # Captura o texto entre 'Titular:' e 'Procurador'
    # procuradores = re.findall(r'Procurador: (.*?) Detalhes do pedido', texto, re.DOTALL)  # Captura o texto entre 'Procurador:' e 'Detalhes do pedido'
    # detalhes = re.findall(r'Detalhes do pedido: (.*?)\n', texto, re.DOTALL)  # Captura o texto após 'Detalhes do pedido'

    print(f"Numero de processos encontrados: {len(numero_processos)}")
    print(f"Titulares encontrados: {titulares}")
    print(f"Procuradores encontrados: {procuradores}")
    print(f"Detalhes do despacho encontrados: {detalhes}")

    # Criação dos objetos de processo
    for i in range(len(procuradores)):
        processo = {
            # "numero": numero_processos[i],
            "Titular": titulares[i].strip() if i < len(titulares) else "",
            "Procurador": procuradores[i].strip() if i < len(procuradores) else "",
            "detalhes_do_despacho": detalhes[i].strip() if i < len(detalhes) else ""
        }
        processos.append(processo)
    
    return processos

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

        # Pega a 8ª página (index 7, pois começa do 0)
        if len(pdf_document) > 7:
            page = pdf_document.load_page(7)
            texto = page.get_text()

            print(f"Texto extraído da página 8:")
            print(texto)  # Imprime o texto extraído da página 8

            # Extrai os processos da 8ª página
            processos = extrair_dados_pagina(texto)

            # Retorna os dados encontrados na página 8
            return jsonify({"pagina": 8, "processos": processos}), 200
        else:
            return jsonify({"error": "PDF não tem 8 páginas"}), 400
    else:
        return jsonify({"error": "Allowed file type is PDF"}), 400

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
