import os
import datetime

def convert_from_text(input_text: str) -> str:
    """
    Recebe o texto com blocos Q:/A: e retorna uma string
    com cada par Pergunta<TAB>Resposta em uma única linha.
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


if __name__ == '__main__':
    # 1) Diretório onde está este script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 2) Arquivo de entrada, na mesma pasta do script
    input_file_path = os.path.join(script_dir, 'perguntas_respostas')
    if not os.path.exists(input_file_path):
        raise FileNotFoundError(f"Não encontrei: {input_file_path}")

    # 3) Lê o conteúdo
    with open(input_file_path, 'r', encoding='utf-8') as f:
        input_text = f.read()

    # 4) Converte
    result = convert_from_text(input_text)

    # 5) Prepara pasta de saída
    output_dir = os.path.join(script_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)

    # 6) Nomeia o arquivo por data, hora e minuto
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
    output_file = f"import_anki_{timestamp}.txt"
    output_path = os.path.join(output_dir, output_file)

    # 7) Se o arquivo já existe (ou seja, rodando no mesmo minuto), ele vai apendar.
    #    Caso contrário, será criado um novo arquivo.
    with open(output_path, 'a', encoding='utf-8') as f:
        f.write(result)
        f.write('\n')  # garante quebra de linha ao final

    print(f"Q/A importadas para: {output_path}")