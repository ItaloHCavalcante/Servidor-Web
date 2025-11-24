from socket import *
import sys

# Definindo porta que será utilizada pelo servidor
portaServer = 6789

# Criando o socket TCP
serverSocket = socket(AF_INET, SOCK_STREAM) #AF_INET--> indica que será utilizado o IPv4


serverSocket.bind(('', portaServer)) # Associa o socket com a porta definida em todas as interfaces de rede --> ('')
serverSocket.listen(1) # Prepara o socket para aceitar conexões, o argumento(1) indica que suporta apenas 1 conexão pendente

while True:  # Esperando por uma conexão
    print('Servidor pronto para ser utilizado...')
    connectionSocket, addr = serverSocket.accept() # Bloqueia o programa até que um socket tentar se conectar,
                                                   #e ele retornará um novo socket de conexão dedicado ao cliente (addr)
    
    try:
        message = connectionSocket.recv(2024).decode() # Indica que o socket receberá até 2024 bytes do cliente,
                                                       #em seguida irá decodificar-los (Ex: 01010110 --> 'Hello Word')

        # Analisará a requisição para obter o nome do arquivo
        filename = message.split()[1]  # O split dividirá o arquivo em partes (método, caminho, vesão)

        # Abre o arquivo, o indice indica que a '/' inicial será dispensada
        f = open(filename[1:])

        # Lê o conteúdo do arquivo
        outputdata = f.read()

        # Envia uma linha de status HTTP 200 OK, e depois linhas em branco para indicar o fim do cabeçalho e inicio da mensagem
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())

        # Envia o conteúdo do arquivo ao cliente
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode()) # O índice indica que a cada looping ele enviará um caractere
        connectionSocket.send("\r\n".encode())
        # Encerra a conexão com o cliente
        connectionSocket.close()

    except IOError:
        # Caso o arquivo não seja encontrado, envia o ERROR 404
        connectionSocket.send("HTTP/1.1 404 Not FOund\r\n\r\n".encode())
        connectionSocket.send("<html><body><h1>404 Not found</h1></body></html>".encode())

        # Encerra a conexão com o SOCKET do cliente
        connectionSocket.close()


