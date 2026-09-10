# modulo python usados para preparar argumentos/comandos
# que serao enviados ao streamlit como se fossem escritos no terminal
import sys
# biblioteca usada para abrir o streamlit numa janela propria do windows
import webview
# permite fazer uma pequena pausa enquanto o servidor streamlit arranca
import time
# permite executar o servidor streamlit num processo separado
from multiprocessing import Process, freeze_support
# importa a linha de comandos do Streamlit(CLI)
from streamlit.web import cli as stcli


def executar_streamlit():
    # simula o comando 'streamlit run main.py'
    sys.argv = [
        "streamlit",
        "run",
        "main.py",
        "--global.developmentMode=false",
        "--server.port=8501",
        # impede o streamlit de abrir automaticamente o browser, assim a aplicação so sera mostrada na janela criada pelo webview
        "--server.headless=true"
    ]

    # executa o comando e arranca a aplicação
    stcli.main()


if __name__ == "__main__":

    # evita problemas ao criar novos processos no executavel do windows
    freeze_support()

    # cria um processo separado que vai executar o servidor streamlit
    streamlit_process = Process(target=executar_streamlit)

    # inicia o processo que vai executar o streamlit
    streamlit_process.start()

    time.sleep(2)

    # prepara a janela da aplicação streamlit; ela corre localmente(localhost), na porta 8501(por defeito o streamlit corre nesta porta)
    janela_streamlit = webview.create_window("TSS Analisador de Dados de Vendas", "http://localhost:8501")

    # inicia o pyview e mostra a janela da aplicação do streamlit
    webview.start()

    # termina o processo da aplicação do streamlit quando a janela é fechada
    streamlit_process.terminate()

    # espera ate o processo do streamlit terminar completamente
    streamlit_process.join()

