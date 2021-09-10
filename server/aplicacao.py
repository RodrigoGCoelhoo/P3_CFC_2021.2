#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
import numpy as np
from PIL import Image
import io
import random

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM4"                  # Windows(variacao de)


def main():

    
    '''
    

        # SORTEIA A QUANTIDADE E OS COMANDOS
        numero_bytes = random.randint(10,30)
        print()
        print("O NÚMERO SORTEADO FOI {}".format(numero_bytes))
        print()
        time.sleep(1)

        # LISTA DE POSSIVEIS BYTES
        lista_comandos = ['00FF','00','0F','F0','FF00','FF']
        BYTE_DUPLO = '02'
        BYTE_FINAL = 'FA'

        # inicializando as listas
        lista_bytes = []

        for _ in range(numero_bytes):
            c = random.choice(lista_comandos)

            if len(c) == 2:
                c_bytes = bytes.fromhex(c)
                lista_bytes.append(c_bytes)
            
            elif len(c) == 4:
                lista_bytes.append(bytes.fromhex(BYTE_DUPLO))
                lista_bytes.append(bytes.fromhex(c[0:2]))
                lista_bytes.append(bytes.fromhex(c[2:4]))

        lista_bytes.append(bytes.fromhex(BYTE_FINAL))


        tamanho_lista = bytes([len(lista_bytes)])


        print("A LISTA DE BYTES QUE SERÁ ENVIADA É : \n {}".format(lista_bytes))
        time.sleep(1)


        enviado = b''
        for b in lista_bytes:
            enviado += b

        print()
        time.sleep(1)
        print(tamanho_lista)
        print(enviado)
        time.sleep(1)
        print()
        


        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print()
        print()
        print("############# COMUNIÇÃO INICIADA! #############")
        print()
        time.sleep(1)
        
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são uma lista de bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        
        with open("imagem.jpg", 'rb') as file:
            imagem = file.read()
            
        txBuffer = bytearray(imagem)

    
        #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
        print(f'SERÃO ENVIADOS {len(txBuffer)} BYTES')
        print()
        time.sleep(1)

        #finalmente vamos transmitir os dados. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        print("A TRANSIMSSÃO VAI COMEÇAR!")
        print()
        time.sleep(1)
        #tente entender como o método send funciona!
        #Cuidado! Apenas trasmitimos arrays de bytes! Nao listas!
          
          

        com1.sendData(txBuffer)

        print("DADOS ENVIADOS")
        print()
        time.sleep(1)
       
        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # Tente entender como esse método funciona e o que ele retorna
        txSize = com1.tx.getStatus()

        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.

        print("A RECEPÇÃO VAI COMEÇAR")
        print()
        time.sleep(1)
        
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen
      
        #acesso aos bytes recebidos
        txLen = len(txBuffer) '''


# COMEÇA AQUI A PARTE DO CLIENT!!!


    try:
        HANDSHAKE = False
        RECEBI_PACKAGE = False
        DELTA = 0.01


        com1 = enlace(serialName)
        com1.enable()
        com1.rx.fisica.flush()
        print("ESTOU PRONTO PRA RECEBER!")


        ###### HANDSHAKE #######
        while not HANDSHAKE:
            com1.rx.fisica.flush()
            rxBuffer, nRx = com1.getData(15)
            time.sleep(DELTA)
            print("numero restante de bytes do handshake: {}".format(com1.rx.getBufferLen()))
            if rxBuffer:
                print("RECEBI O HANDHAKE")
                HANDSHAKE = True
                quantidade_package = rxBuffer[10]
                print(quantidade_package)
                handshake_volta = 10 * b"\x00" + b"\xff\xaa\xff\xaa"
                com1.sendData(handshake_volta)
                time.sleep(DELTA)
                print("MANDEI DE VOLTA O HANDHAKE")


        imagem_bytes = b""
        ###### LEITURA DOS ARQUIVOS ######
        i = 1
        while i < quantidade_package + 1:

            ### LENDO O HEAD ###
            rxBuffer, nrx = com1.getData(10)
            #time.sleep(DELTA)
            id_recebido, total_packages_recebido, bytes_diferentes_recebido, tamanho_payload_recebido = rxBuffer[0], rxBuffer[1], rxBuffer[2], rxBuffer[3]


            print("#"*70 + "\n")
            print(f'ID: {id_recebido}, TOTAL: {total_packages_recebido}, BYTES DIFERENTES: {bytes_diferentes_recebido}, TAMANHO PAYLOAD: {tamanho_payload_recebido}' + "\n")

            

            ### LENDO O PAYLOAD ###
            rxBuffer, nrx = com1.getData(tamanho_payload_recebido)
            payload_atual = rxBuffer
            imagem_bytes += rxBuffer

            ### LENDO O EOP ###
            rxBuffer, nrx = com1.getData(4)
            eop = rxBuffer

            ### VERIFICAÇÕES ###
            listaBytes = []
            for j in range(tamanho_payload_recebido):
                listaBytes.append(payload_atual[j])
            bytes_diferentes = len(set(listaBytes))

            ### ERRO NO ID ###
            if id_recebido != i:
                print("ID DEU DIFERENTE")

            
            ### ERRO NOS TIPOS DE BYTES ###
            elif bytes_diferentes_recebido != bytes_diferentes:
                print("BYTES NÃO DERAM MATCH")

            ### ERRO NO EOP ###
            elif eop != b"\xff\xaa\xff\xaa":
                print("PROBLEMA NO EOP")

            ### CHEGOU TUDO CERTO ###
            else:
                i+=1

            resposta = 10 * b"\x00" + i.to_bytes(1, "big") + b"\xff\xaa\xff\xaa"


            com1.sendData(resposta)

            #time.sleep(DELTA)

        print("CONVERTENDO OS BYTES PARA IMAGEM")

        imagem_recebida = Image.open(io.BytesIO(imagem_bytes)) 
        imagem_recebida.save("rgb.png")

        print("CONVERSÃO FEITA COM SUCESSO :)")

        
        # Encerra comunicação
        print("-------------------------")
        print("COMUNICAÇÃO ENCERRADA!")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    # so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()

