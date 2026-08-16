from filesystem import (
    criar_pasta,
    listar_pastas,
    criar_arquivo,
    listar_arquivos,
    deletar_arquivo,
    deletar_pasta,
    mudar_diretorio,
    obter_diretorio_atual,
    obter_caminho,
    escrever_arquivo,
    ler_arquivo,
    fetch,
    copiar_arquivo,
    renomear_arquivo,
    eh_pasta,
    eh_arquivo,
    mover_arquivo,
)
from processes import (
    listar_processos,
    iniciar_processo,
    finalizar_processo,
    atualizar_processos
)
from users import (
    login,
    logout,
    quem_sou,
    listar_usuarios,
    eh_admin,
    tem_permissao,
    verificar_permissao_comando,
    criar_usuario,
)
from Kernel import inc
import os
def Terminal():
    inc()
    comandosterminal = (
        "exit - Sai do terminal",
        "help - Exibe esta mensagem de ajuda",
        "echo - Exibe o texto fornecido",
        "cls - Limpa a tela do terminal",
        "math - Realiza operações matemáticas básicas",
        "mkdir - Cria uma nova pasta",
        "touch - Cria um novo arquivo",
        "dir - Lista pastas e arquivos no diretório atual",
        "del - Deleta um arquivo",
        "rmdir - Deleta uma pasta",
        "cd - Muda o diretório atual",
        "write - Escreve conteúdo em um arquivo",
        "cat - Lê o conteúdo de um arquivo",
        "pwd - Exibe o caminho do diretório atual",
        "fetch - Exibe informações do sistema",
        "copy - Copia um arquivo para outro local",
        "move - Move um arquivo para outro local",
        "rename - Renomeia um arquivo",
        "ps - Lista os processos em execução",
        "start - Inicia um processo",
        "taskkill - Finaliza um processo",
        "login - Faz login no sistema",
        "logout - Sai da conta atual",
        "whoami - Mostra o usuário atual",
        "users - Lista os usuários",
        )
    while True:
        atualizar_processos()

        Comando = input(obter_caminho() + "> ")
        comandoquebrado = Comando.split()

        if len(comandoquebrado) == 0:
            continue

        if not verificar_permissao_comando(comandoquebrado[0]):
            print("Permissão negada.")
            continue

        match comandoquebrado[0]:
            case "exit":
                print("Saindo do terminal...")
                break
            case "help":
                print("Comandos disponíveis:")
                for comando in comandosterminal:
                    print(comando)
            case "echo":
                print(" ".join(comandoquebrado[1:]))
            case "cls":
                os.system("cls" if os.name == "nt" else "clear")
                inc()
            case "math":
                if len(comandoquebrado) < 4:
                    print("Uso: math <número1> <operador> <número2>")
                    continue
                num1 = float(comandoquebrado[1])
                operador = comandoquebrado[2]
                num2 = float(comandoquebrado[3])
                if operador == "+":
                    resultado = num1 + num2
                elif operador == "-":
                    resultado = num1 - num2
                elif operador == "*":
                    resultado = num1 * num2
                elif operador == "/":
                    if num2 == 0:
                        print("Erro: Divisão por zero.")
                        continue

                    resultado = num1 / num2
                else:
                    print("Operador inválido. Use +, -, * ou /")
                    continue
                print(f"Resultado: {resultado}")
            case "mkdir":
                resultado = criar_pasta(comandoquebrado[1])
                print(resultado)
            case "touch":
                resultado = criar_arquivo(comandoquebrado[1])
                print(resultado)
            case "dir":
                print("Pastas:")
                for pasta in listar_pastas():
                    print(f"    {pasta}")
                print("Arquivos:")
                for arquivo in listar_arquivos():
                    print(f"    {arquivo}")
            case "del":
                if len(comandoquebrado) < 2:
                    print("Uso: del <arquivo>")
                    continue
                resultado = deletar_arquivo(comandoquebrado[1])
                print(resultado)

            case "rmdir":
                if len(comandoquebrado) < 2:
                    print("Uso: rmdir <pasta>")
                    continue
                if not tem_permissao("user"):
                    print("Permissão negada.")
                    continue
                resultado = deletar_pasta(comandoquebrado[1])
                print(resultado) 

            case "cd":
                if len(comandoquebrado) < 2:
                    print("Uso: cd <pasta>")
                    continue

                resultado = mudar_diretorio(comandoquebrado[1])
                print(resultado)
            case "write":
                if len(comandoquebrado) < 3:
                    print("Uso: write <arquivo> <texto>")
                    continue

                nome = comandoquebrado[1]
                conteudo = " ".join(comandoquebrado[2:])

                resultado = escrever_arquivo(nome, conteudo)
                print(resultado)

            case "cat":
                if len(comandoquebrado) < 2:
                    print("Uso: cat <arquivo>")
                    continue

                resultado = ler_arquivo(comandoquebrado[1])
                print(resultado)

            case "pwd":
                print(obter_caminho())

            case "fetch":
                fetch()
            case "copy":
                if len(comandoquebrado) < 3:
                    print("Uso: copy <arquivo_origem> <arquivo_destino>")
                    continue
                
                resultado = copiar_arquivo(comandoquebrado[1], comandoquebrado[2])
                print(resultado)
            case "rename":
                if len(comandoquebrado) < 3:
                    print("Uso: rename <arquivo_antigo> <arquivo_novo>")
                    continue
                resultado = renomear_arquivo(comandoquebrado[1], comandoquebrado[2])
                print(resultado)
            case "move":
                if len(comandoquebrado) < 3:
                    print("Uso: move <arquivo_origem> <arquivo_destino>")
                    continue
                resultado = mover_arquivo(comandoquebrado[1], comandoquebrado[2])
                print(resultado)
            case "ps":
                atualizar_processos()
                listar_processos()
            case "start":
                if len(comandoquebrado) < 2:
                    print("Uso: start <comando>")
                    continue

                comando = " ".join(comandoquebrado[1:])

                resultado = iniciar_processo(comando)
                print(resultado)
            case "taskkill":
                if len(comandoquebrado) < 2:
                    print("Uso: taskkill <PID>")
                    continue

                try:
                   pid = int(comandoquebrado[1])
                except ValueError:
                    print("Erro: o PID deve ser um número.")
                    continue

                resultado = finalizar_processo(pid)
                print(resultado)
            case "whoami":
                print(quem_sou())

            case "logout":
                print(logout())

            case "users":
                for usuario in listar_usuarios():
                    print(usuario)
            case "login":
                if len(comandoquebrado) < 2:
                    print("Uso: login <usuario>")
                    continue

                nome = comandoquebrado[1]
                senha = input("Senha: ")

                print(login(nome, senha))
            case "useradd":
                if len(comandoquebrado) < 4:
                    print("Uso: useradd <nome> <senha> <nivel>")
                    continue

                nome = comandoquebrado[1]
                senha = comandoquebrado[2]
                nivel = comandoquebrado[3]

                resultado = criar_usuario(nome, senha, nivel)
                print(resultado)
            case _:
                print("Comando não reconhecido.")
