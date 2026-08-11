import platform
import json
import os
import ctypes

ARQUIVO_SISTEMA = "filesystem.json"

filesystem = {}
diretorio_atual = ["Root"]


def carregar_filesystem():
    global filesystem

    if os.path.exists(ARQUIVO_SISTEMA):
        with open(ARQUIVO_SISTEMA, "r", encoding="utf-8") as arquivo:
            filesystem = json.load(arquivo)
    else:
        filesystem = {
            "Root": {}
        }


def salvar_filesystem():
    with open(ARQUIVO_SISTEMA, "w", encoding="utf-8") as arquivo:
        json.dump(filesystem, arquivo, indent=4, ensure_ascii=False)


carregar_filesystem()

# Padronizar os caralho a 4

def eh_pasta(conteudo):
    return isinstance(conteudo, dict)


def eh_arquivo(conteudo):
    return not eh_pasta(conteudo)


def obter_diretorio_atual():
    atual = filesystem

    for pasta in diretorio_atual:
        atual = atual[pasta]

    return atual


def obter_caminho():
    return "C:\\" + "\\".join(diretorio_atual[1:])


def listar_pastas():
    atual = obter_diretorio_atual()

    pastas = []

    for nome, conteudo in atual.items():
        if eh_pasta(conteudo):
            pastas.append(nome)

    return pastas


def mudar_diretorio(nome):
    atual = obter_diretorio_atual()

    if nome == "..":
        if len(diretorio_atual) > 1:
            diretorio_atual.pop()
            return "Voltando para o diretório anterior."
        else:
            return "Você já está no diretório raiz."

    if nome in atual and eh_pasta(atual[nome]):
        diretorio_atual.append(nome)
        return f"Diretório alterado para '{nome}'."

    return f"A pasta '{nome}' não existe."

def criar_pasta(nome):
    atual = obter_diretorio_atual()

    if nome not in atual:
        atual[nome] = {}
        salvar_filesystem()
        return f"Pasta '{nome}' criada com sucesso."

    return f"A pasta '{nome}' já existe."


def deletar_pasta(nome):
    atual = obter_diretorio_atual()

    if nome in atual and eh_pasta(atual[nome]):
        if atual[nome]:
            return f"A pasta '{nome}' não está vazia. Não é possível deletá-la."

        del atual[nome]
        salvar_filesystem()

        return f"Pasta '{nome}' deletada com sucesso."

    return f"A pasta '{nome}' não existe."


def criar_arquivo(nome):
    atual = obter_diretorio_atual()

    if nome not in atual:
        atual[nome] = None
        salvar_filesystem()
        return f"Arquivo '{nome}' criado com sucesso."

    return f"O arquivo '{nome}' já existe."


def escrever_arquivo(nome, conteudo):
    atual = obter_diretorio_atual()

    if nome not in atual:
        return f"O arquivo '{nome}' não existe."

    if eh_pasta(atual[nome]):
        return f"'{nome}' é uma pasta, não um arquivo."

    atual[nome] = conteudo
    salvar_filesystem()

    return f"Conteúdo escrito no arquivo '{nome}' com sucesso."


def ler_arquivo(nome):
    atual = obter_diretorio_atual()

    if nome not in atual:
        return f"O arquivo '{nome}' não existe."

    if eh_pasta(atual[nome]):
        return f"'{nome}' é uma pasta, não um arquivo."

    if atual[nome] is None:
        return "(arquivo vazio)"

    return atual[nome]


def listar_arquivos():
    atual = obter_diretorio_atual()

    arquivos = []

    for nome, conteudo in atual.items():
        if eh_arquivo(conteudo):
            arquivos.append(nome)

    return arquivos


def deletar_arquivo(nome):
    atual = obter_diretorio_atual()

    if nome in atual and eh_arquivo(atual[nome]):
        del atual[nome]
        salvar_filesystem()

        return f"Arquivo '{nome}' deletado com sucesso."

    return f"O arquivo '{nome}' não existe."


def copiar_arquivo(origem, destino):
    atual = obter_diretorio_atual()

    if destino in atual:
        return f"Erro: o arquivo '{destino}' já existe."

    if origem not in atual:
        return f"Erro: o arquivo '{origem}' não existe."

    if eh_pasta(atual[origem]):
        return f"'{origem}' é uma pasta, não um arquivo."

    atual[destino] = atual[origem]

    salvar_filesystem()

    return f"Arquivo '{origem}' copiado para '{destino}' com sucesso."


def renomear_arquivo(nome_atual, novo_nome):
    atual = obter_diretorio_atual()

    if nome_atual not in atual:
        return f"O arquivo '{nome_atual}' não existe."

    if novo_nome in atual:
        return f"O arquivo '{novo_nome}' já existe."

    if eh_pasta(atual[nome_atual]):
        return f"'{nome_atual}' é uma pasta, não um arquivo."

    atual[novo_nome] = atual[nome_atual]
    del atual[nome_atual]

    salvar_filesystem()

    return f"Arquivo '{nome_atual}' renomeado para '{novo_nome}' com sucesso."


class MEMORYSTATUSEX(ctypes.Structure):
    _fields_ = [
        ("dwLength", ctypes.c_ulong),
        ("dwMemoryLoad", ctypes.c_ulong),
        ("ullTotalPhys", ctypes.c_ulonglong),
        ("ullAvailPhys", ctypes.c_ulonglong),
        ("ullTotalPageFile", ctypes.c_ulonglong),
        ("ullAvailPageFile", ctypes.c_ulonglong),
        ("ullTotalVirtual", ctypes.c_ulonglong),
        ("ullAvailVirtual", ctypes.c_ulonglong),
        ("ullAvailExtendedVirtual", ctypes.c_ulonglong)
    ]


def get_total_ram():
    memoria = MEMORYSTATUSEX()
    memoria.dwLength = ctypes.sizeof(MEMORYSTATUSEX)

    ctypes.windll.kernel32.GlobalMemoryStatusEx(
        ctypes.byref(memoria)
    )

    return memoria.ullTotalPhys


def fetch():
    print("       ██████")
    print("       ██")
    print("       █████")
    print("       ██")
    print("       ██")
    print(" ")

    print("Sistema Operacional: " + platform.system())
    print("Versão: " + platform.release())
    print("Arquitetura: " + platform.machine())
    print("Processador: " + platform.processor())
    print("Versão do Python: " + platform.python_version())
    print("Memória RAM: " + str(round(get_total_ram() / (1024 ** 3), 2)) + " GB")
    print("Diretório atual: " + obter_caminho())

def mover_arquivo(origem, destino):
    atual = obter_diretorio_atual()

    if origem not in atual:
        return f"Erro: o arquivo '{origem}' não existe."

    if eh_pasta(atual[origem]):
        return f"Erro: '{origem}' é uma pasta, não um arquivo."

    if destino in atual:
        return f"Erro: o arquivo '{destino}' já existe."

    atual[destino] = atual[origem]
    del atual[origem]
    salvar_filesystem()
    return f"Arquivo '{origem}' movido para '{destino}' com sucesso."
