import socket
import threading
import Game, Player

# Define the server host and port
HOST = 'localhost'  # Replace with your desired host address or leave as 'localhost' for local testing
PORT = 12345  # Replace with your desired port number

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(2)

# List to store connected clients
clients = []
# int current_turn
current_turn = 0
global current_player

# Function to handle individual client connections
def handle_client(client_socket, client_number):
    global current_turn
    player1 = Player.PlayerClass('Player1', client_socket)

    # Create a deck for each player
    player1.deck = Game.create_deck()

    # Shuffle each player's deck
    player1.deck = Game.shuffle_deck(player1.deck)

    # Draw 2 cards for each player
    for i in range(0, 3):
        player1.draw()

    current_player = player1

    while True:
        # Receive data from the client
        data = client_socket.recv(1024).decode('utf-8')
        
        # Process the received data
        if data:
            # Process the received data based on game logic
            if clients.index(client_socket) == current_turn:
                if data.lower() == "play":
                    # Send the card index input request to the client
                    client_socket.send("Enter the index of the card you want to play: ".encode('utf-8'))
                    
                    # Receive the card index from the client
                    card_index = int(client_socket.recv(1024).decode('utf-8'))
                    
                    # Send the field index input request to the client
                    client_socket.send("Enter the index of the field you want to add the card to: ".encode('utf-8'))
                    
                    # Receive the field index from the client
                    field_index = int(client_socket.recv(1024).decode('utf-8'))
                    
                    # Check if the card index and field index are valid
                    if card_index < len(current_player.hand) and field_index < 3:
                        # Get the selected card from the player's hand
                        card = current_player.hand[card_index]
                        
                        # Check if the player has enough mana to play the card
                        if current_player.manapool >= card.mana:
                            # Play the selected card from the player's hand
                            current_player.play(card, field_index)
                            
                            # Print the played card index on the server
                            print("Player", clients.index(client_socket) + 1, "played card index:", card_index)
                            
                            # Update the player's mana
                            current_player.manapool -= card.mana
                            
                            # Send the name of the played card to the client
                            response = "Played " + card.name

                        else:
                            # Insufficient mana to play the card
                            response = "Insufficient mana to play the card"
                    else:
                        # Invalid card index or field index
                        response = "Invalid card or field index"
                    
                    client_socket.send(response.encode('utf-8'))

                elif data.lower() == "fields":
                    response = "\nFields:\n"
                    
                    for field_index, field in enumerate(current_player.fields):
                        response += f"\tField {field_index + 1}\n"
                        for card in field[1]:
                            response += f"\t\t{card.name} | Mana: {card.mana} | Attack: {card.attack}\n"
                    
                    # Send the response to the client
                    client_socket.send(response.encode('utf-8'))

                elif data.lower() == "hand":
                    response = "\n Hand:"
                    for card in current_player.hand:
                        card_info = f"\t{card.name} - {card.description} | Mana: {card.mana} | Attack: {card.attack}"
                        response += "\n" + card_info + "\n"
                    client_socket.send(response.encode('utf-8'))

                elif data.lower() == "mana":
                    response = "Mana: " + str(current_player.manapool)
                    client_socket.send(response.encode('utf-8'))

                elif data.lower() == "end":
                    # End the current player's turn
                    response = "Turn ended"
                    client_socket.send(response.encode('utf-8'))
                    switch_turns()  # Switch turns
                    current_player = clients[current_turn]  # Set the current player to the next player

                elif data.lower() == "whoami":
                    response = "Player: " + str(clients.index(client_socket))
                    client_socket.send(response.encode('utf-8'))

                response = "Response from server"
                client_socket.send(response.encode('utf-8'))
            else:
                # It's not this player's turn, so ignore the input
                response = "It's not your turn"
                client_socket.send(response.encode('utf-8'))
        else:
            print("Client", client_number, "disconnected")
            client_socket.close()
            clients.remove(client_socket)
            break
    
    # Close the client connection
    client_socket.close()


def switch_turns():
    global current_turn  # Declare current_turn as a global variable
    current_turn = 1 - current_turn  # Switch turns

# Function to accept and handle client connections
def accept_clients():
    client_number = 1
    print("Waiting for clients to connect...")
    while True:
        # Accept a client connection
        client_socket, address = server_socket.accept()
        print("Client", client_number, "connected:", address)

        # Add the client to the list of connected clients
        clients.append(client_socket)
        
        # Start a new thread to handle the client
        threading.Thread(target=handle_client, args=(client_socket, address)).start()

        client_number += 1
        if client_number > 2:
            break
    print("Two players have connected. The game will now start.\n")

# Start accepting client connections
accept_clients()