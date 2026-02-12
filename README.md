# 📈 Previsão de Preços de Ações (META) - Tech Challenge Fase 4

Este projeto implementa uma solução completa de **Deep Learning** para prever o preço de fecho das ações da Meta Platforms (META). O sistema utiliza uma rede neural recorrente **LSTM (Long Short-Term Memory)** desenvolvida em **PyTorch**, servida através de uma API **FastAPI** e containerizada com **Docker** para fácil implantação.

---

## 📋 Visão Geral do Projeto

O objetivo é prever o valor de fecho do dia seguinte com base numa sequência histórica de **60 dias**. O projeto abrange todo o ciclo de vida de ciência de dados:

1.  **Coleta e Processamento:** Extração de dados via `yfinance`, normalização e preparação de sequências.
2.  **Modelagem:** Treino de uma rede LSTM capaz de capturar dependências temporais de longo prazo.
3.  **Avaliação:** Validação rigorosa com métricas de erro (MAE/RMSE).
4.  **Deploy:** Disponibilização do modelo via API RESTful containerizada.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.11
* **Machine Learning:** PyTorch, Scikit-learn, Numpy, Pandas
* **API Web:** FastAPI, Uvicorn, Pydantic
* **Dados Financeiros:** yfinance
* **Infraestrutura:** Docker

---

## 🧠 Arquitetura da Rede Neural

O modelo utiliza uma arquitetura recorrente otimizada para séries temporais:

* **Entrada:** Tensor `(batch_size, 60, 1)` representando os últimos 60 dias de preços normalizados.
* **Camada Oculta (LSTM):** 60 unidades ocultas com mecanismos de *gates* para gerir a memória temporal.
* **Camada de Saída:** Camada linear (Dense) que projeta o resultado num único valor de previsão.
* **Otimizador:** Adam (Learning Rate: 0.001).
* **Função de Perda:** MSELoss (Mean Squared Error).

---

## 📊 Performance e Métricas

O modelo foi avaliado com dados históricos de 2018 até ao presente, demonstrando capacidade de seguir a tendência de mercado.

| Métrica | Valor Obtido | Descrição |
| :--- | :--- | :--- |
| **MAE** (Erro Médio Absoluto) | **$11.81** | Média do erro absoluto em dólares. |
| **RMSE** (Raiz do Erro Quadrático Médio) | **$16.04** | Penaliza desvios maiores (outliers). |

> **Nota:** O modelo utiliza uma janela de *look-back* de 60 dias. É necessário fornecer pelo menos 60 dias de dados históricos para realizar uma previsão.

### Fórmulas de Avaliação:
$$MAE = \frac{1}{n} \sum_{i=1}^{n} |y_i - \hat{y}_i|$$

$$RMSE = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2$$


---

## Como Executar

### Pré-requisitos
* Docker Desktop instalado e em execução.
* Python 3.11+ (se quiser rodar scripts locais).

### Execução Automática (Recomendado)
O projeto inclui um script de automação que constrói a imagem, inicia o container e abre a documentação no navegador automaticamente:

``` bash
python start_project.py
```

---

------------------------------------------------------------------------

### Execução Manual via Docker

Para garantir a escalabilidade e consistência do ambiente, utilize os comandos abaixo (requer **Docker Desktop** ativo):


1.  **Acesse o diretório do projeto:**

    ``` bash
    cd caminho/do/projeto
    ```

2.  **Build da imagem:**

    ``` bash
    docker build -t api-meta-auto .
    ```

3.  **Execute o container:**

    ``` bash
    docker run -p 8000:8000 api-meta-auto
    ```

4.  **Acesse a API no navegador:**

        http://localhost:8000

------------------------------------------------------------------------

## 📂 📂 Estrutura do Projeto

* `lstm.ipynb`: Jupyter Notebook contendo a análise exploratória, pré-processamento, treinamento e avaliação do modelo.
* `main.py`: Aplicação FastAPI que carrega o modelo treinado e expõe o endpoint de previsão.
* `Dockerfile`: Receita para construção da imagem Docker da aplicação.
* `requirements.txt`: Lista de dependências do projeto.
* `start_project.py`: Script utilitário para construir e rodar o container Docker automaticamente.
* `test_api.py`: Script para testar a API enviando dados reais recentes.

    📁 projeto-meta-lstm
    │── lstm.ipynb          → Treinamento e validação do modelo
    │── main.py             → API FastAPI com endpoint de previsão
    │── Dockerfile          → Configuração do container
    │── requirements.txt    → Dependências
    │── start_project.py    → Execução automática do Docker
    │── test_api.py         → Script de teste da API
    │── environment ──
                      │── modelo_lstm.pth
                      │── scaler.pkl

------------------------------------------------------------------------

---

## ⚙️ Parâmetros de Treinamento

| Parâmetro | Detalhe |
| :--- | :--- |
| **Janela Temporal (Lookback)** | 60 dias |
| **Otimizador** | Adam (Learning Rate: 0.001) |
| **Função de Perda** | MSE (Mean Squared Error) |
| **Escalonamento** | MinMaxScaler no intervalo $[0, 1]$ |

---

## 🔌 Utilização da API

### Documentação Interativa (Swagger UI)

A API disponibiliza uma interface visual para explorar e testar os endpoints de forma interativa.

- **URL:** http://localhost:8000/docs

---

### Endpoint de Previsão

- **Endpoint:** `/predict/`
- **Método:** `POST`
- **Descrição:** Realiza a previsão do próximo preço de fechamento com base nos últimos valores informados.

---

### ⚡ Teste Rápido via Script

Para validar a API utilizando dados reais recentes, execute o script abaixo:

python test_api.py

---

## 📊 Monitorização de Performance

O sistema possui um Middleware de Observabilidade integrado. A cada requisição, ele registra no console do Docker:

ROTA: O endpoint acessado.

STATUS: Código HTTP (200, 400, 500).

TEMPO: Latência da resposta em segundos.

RAM: Consumo de memória do processo (MB).

CPU: Utilização do processador (%).