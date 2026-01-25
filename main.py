import torch
import torch.nn as nn
import joblib
import numpy as np
import yfinance as yf
import logging
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import List

# Configuração do logging/ Monitoração de erros
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()] # Exibe os erros no terminal do Docker/VSCode
)
logger = logging.getLogger(__name__)

#DEFINIÇÃO DA CLASSE DO MODELO igual à do treino
class ModeloLSTM(nn.Module):
    def __init__(self, input_size=1, hidden_size=60, output_size=1):
        super(ModeloLSTM, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :]) 
        return out

app = FastAPI(title="API de Previsão de Ações - META", description="Tech Challenge Fase 4")
modelo = None
scaler = None

@app.on_event("startup")
def load_artifacts():
    global modelo, scaler
    try:
        # Carregar o Scaler
        scaler = joblib.load('scaler.pkl')
        # Instanciar e Carregar o Modelo
        # Nota: Os parâmetros (1, 60, 1) devem ser os mesmos usados no treino!
        modelo = ModeloLSTM(input_size=1, hidden_size=60, output_size=1)
        modelo.load_state_dict(torch.load('modelo_lstm_meta.pth'))
        modelo.eval() # Modo de avaliação (importante!)
        print("Modelo e Scaler carregados com sucesso!")
        print("\n" + "="*50)
        print("API DE PREVISÃO DA META ESTÁ ONLINE!")
        print("ACESSE O MANUAL AQUI: http://localhost:8000/docs")
        print("TESTE A PREVISÃO: http://localhost:8000/predict_auto/META")
        print("="*50 + "\n")
    except Exception as e:
        print(f"Erro ao carregar arquivos: {e}")


#DEFINIÇÃO DO FORMATO DE ENTRADA (Input Schema)
class StockData(BaseModel):
    prices: List[float] # O usuário deve enviar uma lista de preços (float)

#DEFINIÇÃO DO FORMATO DE SAÍDA (Output Schema)
@app.get("/predict_auto/{ticker}")
def predict_auto(ticker: str):
    global modelo, scaler
    ticker = ticker.upper()

    logger.info(f"Recebida requisição para o ticker: {ticker}")
    
    try:
        data = yf.download(ticker, period="90d", progress=False)
        
        # Verifica se o Yahoo retornou um DataFrame vazio (ex: ticker inexistente)
        if data.empty:
            logger.warning(f"Ticker '{ticker}' não encontrado ou sem dados disponíveis.")
            raise HTTPException(status_code=404, detail=f"Ticker {ticker} não encontrado.")

        # Verifica se há dados suficientes (exigência do modelo: 60 dias)
        if len(data) < 60:
            logger.warning(f"Dados insuficientes para {ticker}: {len(data)} dias encontrados.")
            raise HTTPException(status_code=400, detail="Histórico insuficiente (mínimo 60 dias úteis).")

        # --- PROCESSAMENTO ---
        precos_reais = data['Close'].tail(60).values.reshape(-1, 1)
        input_scaled = scaler.transform(precos_reais)
        input_tensor = torch.tensor(input_scaled, dtype=torch.float32).unsqueeze(0)
        
        with torch.no_grad():
            prediction = modelo(input_tensor)
        
        pred_real = scaler.inverse_transform([[prediction.item()]])[0][0]
        
        logger.info(f"Previsão gerada para {ticker}: ${round(float(pred_real), 2)}")
        
        return {
            "status": "sucesso",
            "ticker": ticker,
            "predicted_next_close": round(float(pred_real), 2)
        }

    except HTTPException as http_e:
        raise http_e # Repassa erros 400 e 404 já tratados
    except Exception as e:
        # Captura erros inesperados (ex: queda de conexão, erro na rede neural)
        logger.error(f"Erro inesperado ao processar {ticker}: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno ao processar a previsão.")

@app.get("/")
def home():
    return {"message": "API de Previsão Automática Online! Use /predict_auto/META"}

# Rota de teste
@app.get("/")
def home():
    return {"message": "API de Previsão de Ações está Online!"}
