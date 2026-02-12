import requests
import time

ticker = "META"
api_url = f"http://localhost:8000/predict_auto/{ticker}"

print(f"--- TESTANDO API PARA O TICKER: {ticker} ---")

try:
    start = time.time()
    
    # Faz a requisição GET (igual ao navegador)
    print(f"Enviando requisição para: {api_url}")
    response = requests.get(api_url)
    
    duration = time.time() - start

    if response.status_code == 200:
        resultado = response.json()
        print("\nSUCESSO! RESPOSTA DA API:")
        print(f"Ticker: {resultado['ticker']}")
        print(f"Previsão Fechamento: ${resultado['predicted_next_close']}")
        print(f"Tempo total do request: {duration:.4f} segundos")
        
        if "X-Process-Time" in response.headers:
            print(f"Tempo interno do servidor (Header): {response.headers['X-Process-Time']}s")
    else:
        print(f"\nERRO NA API: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"\nERRO DE CONEXÃO: {e}")
    print("Certifique-se que o Docker está rodando: 'docker run -p 8000:8000 api-meta-auto'")