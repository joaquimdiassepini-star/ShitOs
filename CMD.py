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
    copiar_arquivo
)

from Kernel import inc
import os
def Terminal():
    inc()
    comandosterminal = (
        "exit - Sai do terminal",
        "help - Exibe esta mensagem de ajuda",
        "echo - Exibe o texto fornecido",
        "cls - Limpa a tela do terminal"
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
        "copy - Copia um arquivo para outro local"
        )
    while True:
        Comando = input(obter_caminho() + "> ")
        comandoquebrado = Comando.split()
        if len(comandoquebrado) == 0:
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
            case _:
                print("Comando não reconhecido.")