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
import sys
import random

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
serialName = "/dev/cu.usbmodem14101"  # Mac    (variacao de)
#serialName = "COM6"                  # Windows(variacao de)

DELTA = 0.01
EOP_END = b"\xFF\xAA\xFF\xAA"

def main():
    
    try:
    
        # Crinado objeto enlace com a porte serial
        com1 = enlace(serialName)
        
        # Ativando comunicação --> inicia os threads e a comunicação serial 
        com1.enable()
        if com1.connected:
            print("Conexão Cliente-Arduino estabelecida com sucesso")
            time.sleep(0.5)
            com1.rx.fisica.flush()
            com1.tx.fisica.flush()
        else:
            sys.exit()

        with open("rgb.png", "rb") as file:
            imagem = file.read()

        nPayloads = len(imagem) // 114 + 1

        print(f"Packages: {nPayloads}")

        i = 1
        while True:
            print(f"Handshake Nº{i}")
            handshake = 10*b"\x00" + nPayloads.to_bytes(1,"big") + EOP_END

            com1.sendData(handshake)
            rxBuffer, nRx = com1.getData(14)

            if rxBuffer == None:
                resposta = input("Servidor inativo. Tentar novamente? S/N\n")
                i += 1
            else:
                break

            if resposta in ["N", "n"]:
                print("\n---------------------")
                print("Comunicação encerrada")
                print("---------------------")
                com1.disable()
                sys.exit()

        print("Handshake bem-sucedido")

        id_ = 2

        while id_ < nPayloads + 1:

            # Construindo componentes do HEAD            
            marcador = id_ * 114
            payload = imagem[marcador - 114 : marcador]
            tamanhoPayload = len(payload)

            listaBytes = []
            for i in range(tamanhoPayload):
                listaBytes.append(payload[i])
            bytesDiferentes = len(set(listaBytes))
            
            head = id_.to_bytes(1,"big") + nPayloads.to_bytes(1,"big") + bytesDiferentes.to_bytes(1,"big") + tamanhoPayload.to_bytes(1,"big") + 6*bytes.fromhex("00")

            package = head + payload + EOP_END

            com1.sendData(package)

            rxBuffer, nRx = com1.getData(15)
            
            id_ = rxBuffer[10]

            print(f"Pacote {id_} enviado")
            


        print("Envio completo")

        # Encerra comunicação
        print("\n---------------------")
        print("Comunicação encerrada")
        print("---------------------")
        com1.disable()

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
