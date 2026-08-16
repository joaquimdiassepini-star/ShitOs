import json
import os

ARQUIVO_USUARIOS = "users.json"

usuarios = {}
usuario_atual = None


def carregar_usuarios():
    global usuarios

    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as arquivo:
            usuarios = json.load(arquivo)

    else:
        usuarios = {
            "root": {
                "senha": "root",
                "nivel": "admin"
            },
            "guest": {
                "senha": "guest",
                "nivel": "guest"
            }
        }

        salvar_usuarios()


def salvar_usuarios():
    with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as arquivo:
        json.dump(
            usuarios,
            arquivo,
            indent=4,
            ensure_ascii=False
        )


carregar_usuarios()


permissoes_comandos = {
    "exit": "guest",
    "help": "guest",
    "echo": "guest",
    "cls": "guest",
    "math": "guest",
    "dir": "guest",
    "cd": "guest",
    "cat": "guest",
    "pwd": "guest",
    "fetch": "guest",
    "ps": "guest",
    "users": "guest",
    "login": "guest",
    "logout": "guest",

    "mkdir": "user",
    "touch": "user",
    "write": "user",
    "copy": "user",
    "rename": "user",
    "move": "user",
    "del": "user",
    "rmdir": "user",

    "start": "user",
    "taskkill": "admin",
    "useradd": "admin",
}


def login(nome, senha):
    global usuario_atual

    if nome not in usuarios:
        return "Usuário não existe."

    if usuarios[nome]["senha"] != senha:
        return "Senha incorreta."

    usuario_atual = nome

    return f"Login realizado com sucesso. Bem-vindo, {nome}."


def logout():
    global usuario_atual

    if usuario_atual is None:
        return "Nenhum usuário está logado."

    nome = usuario_atual
    usuario_atual = None

    return f"Usuário '{nome}' desconectado."


def quem_sou():
    if usuario_atual is None:
        return "Nenhum usuário está logado."

    return usuario_atual


def listar_usuarios():
    return list(usuarios.keys())

def criar_usuario(nome, senha, nivel):
    if not eh_admin():
        return "Permissão negada. Apenas administradores podem criar usuários."

    if nome in usuarios:
        return f"Erro: o usuário '{nome}' já existe."

    niveis_validos = ("guest", "user", "admin")

    if nivel not in niveis_validos:
        return "Erro: nível inválido. Use guest, user ou admin."

    usuarios[nome] = {
        "senha": senha,
        "nivel": nivel
    }

    salvar_usuarios()

    return f"Usuário '{nome}' criado com sucesso."

def nivel_usuario():
    if usuario_atual is None:
        return None

    return usuarios[usuario_atual]["nivel"]


def eh_admin():
    if usuario_atual is None:
        return False

    return usuarios[usuario_atual]["nivel"] == "admin"


def tem_permissao(nivel_necessario):
    if usuario_atual is None:
        return False

    niveis = {
        "guest": 1,
        "user": 2,
        "admin": 3
    }

    nivel_atual = niveis[usuarios[usuario_atual]["nivel"]]

    return nivel_atual >= niveis[nivel_necessario]


def verificar_permissao_comando(comando):
    comandos_publicos = (
        "login",
        "logout",
        "whoami",
        "users"
    )

    if comando in comandos_publicos:
        return True

    if comando not in permissoes_comandos:
        return True

    return tem_permissao(permissoes_comandos[comando])
