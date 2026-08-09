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

def listar_pastas():
    atual = obter_diretorio_atual()

    pastas = []

    for nome, conteudo in atual.items():
        if isinstance(conteudo, dict):
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

    if nome in atual and isinstance(atual[nome], dict):
        diretorio_atual.append(nome)
        return f"Diretório alterado para '{nome}'."

    return f"A pasta '{nome}' não existe."


def obter_diretorio_atual():
    atual = filesystem

    for pasta in diretorio_atual:
        atual = atual[pasta]

    return atual


def criar_pasta(nome):
    atual = obter_diretorio_atual()

    if nome not in atual:
        atual[nome] = {}
        salvar_filesystem()
        return f"Pasta '{nome}' criada com sucesso."

    return f"A pasta '{nome}' já existe."

def deletar_pasta(nome):
    atual = obter_diretorio_atual()

    if nome in atual and isinstance(atual[nome], dict):
        if atual[nome]:
            return f"A pasta '{nome}' não está vazia. Não é possível deletá-la."
        else:
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

    if isinstance(atual[nome], dict):
        return f"'{nome}' é uma pasta, não um arquivo."

    atual[nome] = conteudo
    salvar_filesystem()

    return f"Conteúdo escrito no arquivo '{nome}' com sucesso."

def ler_arquivo(nome):
    atual = obter_diretorio_atual()

    if nome not in atual:
        return f"O arquivo '{nome}' não existe."

    if isinstance(atual[nome], dict):
        return f"'{nome}' é uma pasta, não um arquivo."

    if atual[nome] is None:
        return "(arquivo vazio)"

    return atual[nome]

def listar_arquivos():
    atual = obter_diretorio_atual()

    arquivos = []

    for nome, conteudo in atual.items():
        if conteudo is None:
            arquivos.append(nome)

    return arquivos

def deletar_arquivo(nome):
    atual = obter_diretorio_atual()

    if nome in atual and atual[nome] is None:
        del atual[nome]
        salvar_filesystem()
        return f"Arquivo '{nome}' deletado com sucesso."

    return f"O arquivo '{nome}' não existe."

def obter_caminho():
    return "C:\\" + "\\".join(diretorio_atual[1:])

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
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memoria))
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
    print("diretorio atual: " + obter_caminho())

def copiar_arquivo(origem, destino):
    atual = obter_diretorio_atual()
    if destino in atual:
        return f"Erro: o arquivo '{destino}' já existe."
    if origem in atual and atual[origem] is None:
        conteudo = atual[origem]
        atual[destino] = conteudo
        salvar_filesystem()
        return f"Arquivo '{origem}' copiado para '{destino}' com sucesso."
    elif origem in atual and isinstance(atual[origem], dict):
        return f"'{origem}' é uma pasta, não um arquivo."
    elif origem in atual and atual[origem] is not None:
        getContent = atual[origem]
        atual[destino] = getContent
        salvar_filesystem()
        return f"Arquivo '{origem}' copiado para '{destino}' com sucesso."
    else:
        return f"Erro: o arquivo '{origem}' não existe."