# Define your Player class, create_deck(), shuffle_deck(), and other game logic functions here
class PlayerClass:
    def __init__(self, name, client):
        self.name = name
        self.deck = []
        self.hand = []
        self.fields = [['field1', []], ['field2', []], ['field3', []]]
        self.max_mana = 1
        self.manapool = 1
        self.turn_ended = False
        self.wonCount = 0
        self.fieldCardCount = [0, 0, 0]

    # Create a method that draws a card from the deck
    def draw(self):
        if len(self.deck) > 0:
            self.hand.append(self.deck.pop())

    # Create a method that plays a card from the hand
    def play(self, card, fieldIndex):
        if card in self.hand and 0 <= fieldIndex < len(self.fields):
            self.fields[fieldIndex][1].append(self.hand.pop(self.hand.index(card)))
            self.fieldCardCount[fieldIndex] += 1