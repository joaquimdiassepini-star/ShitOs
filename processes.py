import subprocess

processos = {
    1: {
        "nome": "Kernel",
        "status": "RUNNING",
        "processo": None
    },
    2: {
        "nome": "Terminal",
        "status": "RUNNING",
        "processo": None
    }
}


def listar_processos():
    print("PID    NOME       STATUS")

    for pid, processo in processos.items():
        print(f"{pid:<6}{processo['nome']:<11}{processo['status']}")


def iniciar_processo(comando):
    novo_pid = max(processos.keys()) + 1

    try:
        processo = subprocess.Popen(comando, shell=True)

        processos[novo_pid] = {
            "nome": comando,
            "status": "RUNNING",
            "processo": processo
        }

        return f"Processo '{comando}' iniciado com PID {novo_pid}."

    except Exception as erro:
        return f"Erro ao iniciar processo: {erro}"


def atualizar_processos():
    for pid, processo in processos.items():
        if processo["processo"] is not None:
            if processo["processo"].poll() is not None:
                processo["status"] = "STOPPED"


def finalizar_processo(pid):
    if pid not in processos:
        return f"Processo com PID {pid} não existe."

    if processos[pid]["nome"] == "Kernel":
        return "Erro: não é possível finalizar o Kernel."

    processo = processos[pid]["processo"]

    if processo is not None:
        processo.terminate()

    nome = processos[pid]["nome"]

    del processos[pid]

    return f"Processo '{nome}' com PID {pid} finalizado."
