# Analisador de Dados de Vendas
 
Aplicação desenvolvida em Python para análise exploratória de um ficheiro CSV
com dados de vendas, incluindo validação de dados, calculo de métricas, geração de relatório em HTML
com gráfico incluído.
Esta aplicação tambem inclui um mini CRM para gestão de clientes e leads/oportunidades.

## Funcionalidades

    - Upload do CSV 
    - Cálculo de métricas(Total de vendas, Total Faturado, Média de Vendas
       Totais por Produto e Top 3 Produtos)
    - Geração de um relatório em HTML com gráfico incluído
    - Mini CRM construído em Streamlit(UI) para gestão de: 
      - clientes(criação, atualização, remoção e filtragem de registos)  
      - leads/oportunidades(criação, atualização, remoção e filtragem de registos) 
      - opção de adicionar novos clientes e faturação ao CRM diretamente do ficheiro CSV
    - Incorporação de um ficheiro executável para maior comodidade do utilizador, onde apenas tem de fazer duplo click
       para executar o programa

## Como correr o programa

1 - Instalar dependências:
    
    pip install -r requirements.txt

2 - Correr o streamlit:
    
    streamlit run main.py

3 - Escolher na aplicação entre:

    - Análise de CSV(onde tem a opção de selecionar um ficheiro .csv pretendido)
    - CRM


## Tecnologias utilizadas

    - Python >= +3.10
    - Pandas
    - Matplotlib
    - SQLite3
    - Streamlit
    - PyWebView
    - PyInstaller