import socket
import threading

HOST = '0.0.0.0'
PORT = 59429

#TCP Connection
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))

server.listen()

clients = []
nicknames = []

#Sends Messages to all clients
def broadcast(message):
    for client in clients:
        client.send(message)

#Handles individual clients
def handle(client):
    while True:
        try:
            message = client.recv(1024) #Gets message from client
            broadcast(message) # broadcats message to all clients
        except:
            # if client disconnects
            index = clients.index(client)
            clients.remove(client)
            nickname = nicknames[index]
            broadcast(f"user left the server!\n".encode('ascii'))
            client.close()
            nicknames.remove(nickname)
            break

#Listens servers and accepts new connections
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}!")
        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024).decode("utf-8") #Gets Nickname from the Clients
        nicknames.append(client)
        clients.append(client)

        print(f"Nickname of the client  is {nickname}") #To Server
        broadcast(f" {nickname} connected to the server!\n".encode("utf-8")) #To Clients
        client.send("Connected to server\n".encode("utf-8")) #To this clients


        thread = threading.Thread(target=handle, args=(client,)) #Target function is handle()
        thread.start() # Starts the threading

print("Server Running...")
receive()

