import os
import datetime


def convert_from_text(input_text: str) -> str:
    """
    Converte um texto contendo blocos de perguntas e respostas no formato:

        Q: Qual é a capital da França?
        A: Paris

    para um formato de linha única com separação por tabulação (\t), ideal para
    importação em aplicativos como o Anki, resultando em:

        Qual é a capital da França? <TAB> Paris

    O texto pode conter múltiplos blocos Q:/A:. A função ignora linhas em branco
    e continua a adicionar conteúdo ao buffer correto (pergunta ou resposta) até
    que um novo bloco comece.

    Parâmetros:
        input_text (str): O texto bruto contendo blocos de Q:/A:.

    Retorna:
        str: Texto com cada pergunta e resposta em uma única linha separadas por tabulação.
    """
    lines = input_text.splitlines()
    q_buff = []
    a_buff = []
    mode = None  # 'Q' ou 'A'
    output_lines = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith('Q:'):
            # Se existe par anterior completo, salva
            if q_buff and a_buff:
                q = ' '.join(q_buff).strip()
                a = ' '.join(a_buff).strip()
                output_lines.append(f"{q}\t{a}")
                q_buff, a_buff = [], []

            mode = 'Q'
            q_buff.append(stripped[2:].strip())

        elif stripped.startswith('A:'):
            mode = 'A'
            a_buff.append(stripped[2:].strip())

        else:
            if mode == 'Q':
                q_buff.append(stripped)
            elif mode == 'A':
                a_buff.append(stripped)

    # Salva o último bloco, se existir
    if q_buff and a_buff:
        q = ' '.join(q_buff).strip()
        a = ' '.join(a_buff).strip()
        output_lines.append(f"{q}\t{a}")

    return "\n".join(output_lines)


def manage_output_files(output_dir: str, max_files: int = 5):
    """
    Gerencia os arquivos existentes no diretório de saída. Caso o número
    de arquivos exceda o limite especificado (max_files), o arquivo mais
    antigo (com base na data de criação) será deletado automaticamente.

    Parâmetros:
        output_dir (str): Caminho absoluto para a pasta de saída.
        max_files (int): Número máximo de arquivos permitidos no diretório. Padrão: 5.
    """
    files = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, f))]
    if len(files) > max_files:
        oldest_file = min(files, key=os.path.getctime)
        os.remove(oldest_file)
        print(f"O arquivo mais antigo foi deletado: {oldest_file}")


if __name__ == '__main__':
    # # Executa o script principal
    # 1) Obtém o diretório onde o script está localizado
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 2) Define o caminho do arquivo de entrada (deve estar no mesmo diretório do script)
    input_file_path = os.path.join(script_dir, 'perguntas_respostas')
    if not os.path.exists(input_file_path):
        raise FileNotFoundError(f"Não encontrei: {input_file_path}")

    # 3) Lê o conteúdo do arquivo de entrada
    with open(input_file_path, 'r', encoding='utf-8') as f:
        input_text = f.read()

    # 4) Converte o texto em formato tabulado para importação
    result = convert_from_text(input_text)

    # 5) Garante que o diretório de saída exista
    output_dir = os.path.join(script_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)

    # 6) Gerencia o número de arquivos de saída, deletando os mais antigos se necessário
    manage_output_files(output_dir)

    # 7) Define o nome do arquivo de saída com base no timestamp atual
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
    output_file = f"import_anki_{timestamp}.txt"
    output_path = os.path.join(output_dir, output_file)

    # 8) Escreve (ou apenda) o conteúdo no arquivo de saída
    with open(output_path, 'a', encoding='utf-8') as f:
        f.write(result)
        f.write('\n')  # garante quebra de linha ao final

    print(f"Q/A importadas para: {output_path}")
