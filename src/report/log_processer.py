import re
import csv
import glob
import os

def analisar_log_gurobi(caminho_arquivo):
    """
    Analisa um único arquivo de log do Gurobi para extrair o valor da solução,
    o gap de otimalidade e o tempo de execução.

    Args:
        caminho_arquivo (str): O caminho para o arquivo de log.

    Returns:
        dict: Um dicionário contendo o nome do arquivo, valor da solução,
              gap e tempo. Retorna 'N/A' para valores não encontrados.
    """
    # Valores padrão caso alguma informação não seja encontrada
    valor_solucao = 'N/A'
    gap = 'N/A'
    tempo_execucao = 'N/A'

    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            conteudo = f.read()

            # --- Extração do Tempo de Execução ---
            # Padrão para encontrar a linha "Explored ... nodes ... in X.XX seconds"
            padrao_tempo = re.compile(r"Explored \d+ nodes .* in ([\d.]+) seconds")
            match_tempo = padrao_tempo.search(conteudo)
            if match_tempo:
                tempo_execucao = float(match_tempo.group(1))

            # --- Extração do Valor da Solução e Gap ---
            # Primeiro, tenta encontrar o resumo final para soluções ótimas
            padrao_otimo = re.compile(r"Best objective ([\d.eE+-]+), best bound [\d.eE+-]+, gap ([\d.]+)%")
            match_otimo = padrao_otimo.search(conteudo)

            if match_otimo:
                valor_solucao = float(match_otimo.group(1))
                gap = float(match_otimo.group(2))
            else:
                # Se não encontrou o resumo final (ex: tempo limite atingido),
                # busca a última linha do log de nós para obter os dados mais recentes.
                # Padrão para linhas do log de nós que contêm incumbent, best bound e gap.
                # Ex: H 123 456 ... 533.00000  602.30000  13.0%   ...
                # Ex: * 123 456 ... 553.00000  553.00000  0.00%  ...
                padrao_log_nos = re.compile(r"^\s*([H*]|\s)\s*\d+\s+\d+.*?([\d.eE+-]+)\s+([\d.eE+-]+)\s+([\d.]+)%.*$", re.MULTILINE)
                matches_log_nos = padrao_log_nos.findall(conteudo)
                
                if matches_log_nos:
                    # Pega a última ocorrência encontrada no arquivo
                    ultimo_match = matches_log_nos[-1]
                    # O valor da solução é o 'Incumbent'
                    valor_solucao = float(ultimo_match[1]) 
                    gap = float(ultimo_match[3])


    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em {caminho_arquivo}")
        return None
    except Exception as e:
        print(f"Ocorreu um erro ao processar o arquivo {caminho_arquivo}: {e}")
        return None

    return {
        'nome_arquivo': os.path.basename(caminho_arquivo),
        'valor_solucao': valor_solucao,
        'gap_otimalidade_%': gap,
        'tempo_execucao_s': tempo_execucao
    }

def processar_pasta(pasta_logs='.', arquivo_saida='resultados_gurobi.csv'):
    """
    Processa todos os arquivos .log em uma pasta e salva os resultados em um CSV.

    Args:
        pasta_logs (str): O caminho para a pasta contendo os arquivos de log.
                          O padrão é o diretório atual.
        arquivo_saida (str): O nome do arquivo CSV de saída.
    """
    # Encontra todos os arquivos com a extensão .log na pasta especificada
    arquivos_log = glob.glob(os.path.join(pasta_logs, '*.log'))
    
    if not arquivos_log:
        print(f"Nenhum arquivo .log encontrado na pasta '{pasta_logs}'.")
        return

    print(f"Encontrados {len(arquivos_log)} arquivos de log. Processando...")

    resultados = []
    for arquivo in arquivos_log:
        resultado = analisar_log_gurobi(arquivo)
        if resultado:
            resultados.append(resultado)

    if not resultados:
        print("Nenhum dado foi extraído dos arquivos de log.")
        return

    # Escreve os resultados em um arquivo CSV
    try:
        with open(arquivo_saida, 'w', newline='', encoding='utf-8') as f:
            # Define os nomes das colunas com base nas chaves do primeiro dicionário
            nomes_colunas = resultados[0].keys()
            writer = csv.DictWriter(f, fieldnames=nomes_colunas)

            writer.writeheader()  # Escreve o cabeçalho
            writer.writerows(resultados) # Escreve todas as linhas de dados

        print(f"\nProcessamento concluído! Os resultados foram salvos em '{arquivo_saida}'.")
    except Exception as e:
        print(f"Ocorreu um erro ao salvar o arquivo CSV: {e}")


# --- Ponto de Entrada do Script ---
if __name__ == "__main__":
    # Você pode alterar a pasta onde os logs estão localizados aqui.
    # Por exemplo: processar_pasta(pasta_logs='./meus_logs')
    caminho_dos_logs = '../solver/logs'
    processar_pasta(pasta_logs=caminho_dos_logs)