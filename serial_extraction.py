import serial
import time
import struct

decimal_round = 5

serialPort = serial.Serial(
    port="COM3", baudrate=1382400, bytesize=8, timeout=2, stopbits=serial.STOPBITS_TWO
)
# serialString = ""  # Used to hold data coming over UART
# while 1:
#     # Read data out of the buffer until a carraige return / new line is found
#     serialString = serialPort.readline()

#     # Print the contents of the serial data
#     try:
#         print(serialString.decode("hex"))
#     except:
#         pass    

data = []
flag = 0

while True:
    
    

    # Leia o primeiro byte
    byte = serialPort.read(1)


    # Se encontrar o valor 0x0A
    if byte == b'\x0A':
        # Leia o próximo byte
        next_byte = serialPort.read(1)
        
        if next_byte ==b'\x14':
            
            flag = 0
            

        # Verifica se o próximo byte é 0x13 (13 bytes)
        if next_byte == b'\x13':
            # Salva os próximos 13 bytes em 'data'
            data = [serialPort.read(1) for _ in range(13)]
            
            # Subdividir os dados
            TotalPhase = data[1:5]   # Índices 1, 2, 3, 4
            BreathPhase = data[5:9]  # Índices 5, 6, 7, 8
            HeartPhase = data[9:13]  # Índices 9, 10, 11, 12

            # Imprimir os resultados
            TotalPhase_bytes = b''.join(data[1:5])   # Índices 1, 2, 3, 4
            BreathPhase_bytes = b''.join(data[5:9])  # Índices 5, 6, 7, 8
            HeartPhase_bytes = b''.join(data[9:14])  # Índices 9, 10, 12, 13             
            
            # Converter bytes para ponto flutuante
            TotalPhase = struct.unpack('<f', TotalPhase_bytes)[0]  # Big-endian float
            BreathPhase = struct.unpack('<f', BreathPhase_bytes)[0]
            HeartPhase = struct.unpack('<f', HeartPhase_bytes)[0]
            
            # Imprimir os resultados
            print(f"Dados recebidos e convertidos: TotalPhase (float): {round(TotalPhase, decimal_round)} BreathPhase (float): {round(BreathPhase,decimal_round)} HeartPhase (float): {round(HeartPhase,decimal_round)}")

            
            # Reiniciar a lista data paraz aguardar um novo 0x0A
            data = []
            flag = 1

        if next_byte == b'\x16' and flag == 1:
            # Salva os próximos 9 bytes em 'data'
            data = [serialPort.read(1) for _ in range(9)]
            
            # Subdividir os dados
            Distance = data[5:9]   # Índices 5, 6, 7, 8
            
            # Imprimir os resultados
            Distance_bytes = b''.join(data[5:9])  # Índices 5, 6, 7, 8
            
            # Converter bytes para ponto flutuante
            Distance = struct.unpack('<f', Distance_bytes)[0]   # Big-endian float
            
            # Imprimir os resultados
            print(f"Distance(float): {round(Distance, decimal_round)}")

            
            # Reiniciar a lista data para aguardar um novo 0x0A
            data = []

    # time.sleep(0.05)  # Delay entre impressões
