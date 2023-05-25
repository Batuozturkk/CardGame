import Player
import Cards
import random

# Create a function that creates a deck of cards
def create_deck():
    deck = []
    for i in range(0, 10):
        deck.append(Cards.cards[random.randint(0, len(Cards.cards) - 1)])
    return deck

# Create a function that shuffles a deck of cards
def shuffle_deck(deck):
    random.shuffle(deck)
    return deck

# Create a function that calculates the sum of the cards on the field
def calculate_field_powers(curret_player):
    field_powers = {}

    # Calculate field powers for the current player
    current_field_sums = [sum(card.power for card in field) for field in curret_player.fields]
    field_powers[curret_player.name] = current_field_sums

    return field_powers
