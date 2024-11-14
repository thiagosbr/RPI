import sys
import web

# Adicione o caminho para a aplicação

# Agora você pode importar sua aplicação
from APIPython import app  # Substitua pelo nome correto da sua aplicação

# Definindo a URL e o controlador para o upload
urls = ('/upload', 'Upload')

class Upload:
    def GET(self):
        return 'Envie um arquivo PDF para o upload.'

# Criação da aplicação web
app_web = web.application(urls, globals())

if __name__ == "__main__":
    app_web.run()
