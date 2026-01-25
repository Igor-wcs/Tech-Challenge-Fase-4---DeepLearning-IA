import yfinance as yf
import requests
import json

ticker = "META"
api_url = "http://localhost:8000/predict/"

print(f"Obtendo dados históricos para {ticker}")

# Buscar o histórico de preços usando yfinance
data = yf.download(ticker, period="90d")

# Preparar os dados para a requisição
# Pegamos apenas a coluna 'Close' (Fechamento) e os últimos 60 registros
real_prices = data['Close'].tail(60).values.tolist()

# Garantia de tratamento de valores para float para evitar erro
cleaned_prices = [float(price) for price in real_prices]
print(f" Coletados {len(cleaned_prices)} preços.")

# Criar o payload JSON
payload = {
    "ticker": ticker,
    "prices": cleaned_prices
}

# Enviar para a API rodando no Docker
try:
    print("Enviando requisição para a API")
    response = requests.post(api_url, json=payload)
    
    if response.status_code == 200:
        resultado = response.json()
        print("\nRESPOSTA DA API:")
        print(f"Ticker: {resultado['ticker']}")
        print(f"Preço Previsto para amanhã: ${resultado['predicted_price']}")
        print(f"Último preço real hoje: ${round(cleaned_prices[-1], 2)}")
    else:
        print(f"Erro na API: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"Erro ao conectar na API: {e}")