import subprocess
import webbrowser
import time
import os

# Configurações
IMAGE_NAME = "api-meta-auto"
URL = "http://localhost:8000/docs"

def start_api():
    try:
        print(f"Iniciando o container Docker: {IMAGE_NAME}.")
        
        # Comando para rodar o container em segundo plano (-d)
        # O mapeamento -p 8000:8000 garante que o localhost funcione
        subprocess.Popen(["docker", "run", "-p", "8000:8000", "--rm", IMAGE_NAME])
        
        # Espera 5 segundos para o FastAPI e a rede neural LSTM carregarem
        print("Aguardando o carregamento dos artefatos (.pth e .pkl).")
        time.sleep(5)
        
        # Abre o navegador automaticamente
        print(f"Abrindo a documentação em: {URL}")
        webbrowser.open(URL)
        
    except Exception as e:
        print(f"Erro ao iniciar: {e}")

if __name__ == "__main__":
    start_api()