# #########################
# Simple Blackjack Game
#
# Code written for
# entertainment.
# #########################

# Imports
from os import system
import random

# Card Class
class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
    
    # Name
    def __repr__(self):
        return ' of '.join((self.value, self.suit))

# Deck Class
class Deck:
    def __init__(self):
        # Make Deck
        suits = ['Spades', 'Clubs', 'Hearts', 'Diamonds']
        values = ['A'] + [str(q) for q in range(2, 11)] + ['J', 'Q', 'K']
        self.cards = [Card(s, v) for s in suits for v in values]

    # Shuffle
    def shuffle(self):
        random.shuffle(self.cards)

    # Draw Card
    def draw(self):
        return self.cards.pop(0)

# Hand Class
class Hand:
    def __init__(self, dealer = False):
        self.dealer = dealer
        self.cards = []
        self.value = 0

    # Add Card to Hand
    def add_card(self, card):
        self.cards.append(card)

    # Get Value of Hand
    def get_value(self):
        self.value = 0
        ace = 0
        for card in self.cards:
            if card.value.isnumeric():
                self.value += int(card.value)
            elif card.value in ['J', 'Q', 'K']:
                self.value += 10
            else:
                ace += 1
                self.value += 11

        for _ in range(ace):
            if self.value > 21:
                self.value -= 10
        return self.value

    # Display Hand
    def display(self):
        if self.dealer:
            print("\nDealer's Hand is: ")
            print('Hidden')
            for q in self.cards[1:]:
                print(q)
        else:
            print('\nYour Hand is: ')
            for card in self.cards:
                print(card)
            print(f'value: {self.get_value()}')

class Bank:
    def __init__(self):
        self.account = 100
        self.bet = -1

    def win(self):
        self.account += self.bet
        self.bet = 0

    def lose(self):
        self.account -= self.bet
        self.bet = 0

    def tie(self):
        self.bet = 0

# Game Class
class Game:
    def __init__(self):
        self.playing = True

    # Check for Blackjack
    def check_blackjack(self):
        player, dealer = False, False
        if self.player_hand.value == 21:
            player = True
        if self.dealer_hand.value == 21:
            dealer = True
        return player, dealer

    # Check if Busted
    def busted(self, player = True):
        if player:
            return self.player_hand.get_value() > 21
        else:
            return self.dealer_hand.get_value() > 21

    def check(self, bet, account):
        if type(bet) == float:
            return bet > account or bet < 0
        else:
            return False

    # Play Game
    def play(self):
        bank = Bank()
        while self.playing:
            print(f'Account Standing: ${bank.account}')
            while type(bank.bet) != float or self.check(bank.bet, bank.account):
                bank.bet = input('Bet: ')
                try:
                    bank.bet = float(bank.bet)

                    if bank.bet < 0:
                        print('Please Place a Positive Bet.')
                    if bank.bet > bank.account:
                        print('Not Enough Funds. Please Place a Smaller Bet.')
                except:
                    print('Please bet Number.')

            # Get Deck, Shuffle and Deal
            self.deck = Deck()
            self.deck.shuffle()

            self.player_hand = Hand()
            self.dealer_hand = Hand(dealer = True)

            for _ in range(2):
                self.player_hand.add_card(self.deck.draw())
                self.dealer_hand.add_card(self.deck.draw())

            self.player_hand.display()
            self.dealer_hand.display()

            # While Game is not Over
            game_over = False
            while not game_over:
                # Check for Blackjack
                player_blackjack, dealer_blackjack = self.check_blackjack()

                game_over = True
                if player_blackjack and dealer_blackjack:
                    print('Both Players have Blackjack! Draw!')
                    bank.tie()
                    break
                elif player_blackjack:
                    print('Player has Blackjack! Player Wins!')
                    bank.win()
                    break
                elif dealer_blackjack:
                    print('Dealer has Blackjack! Dealer Wins!')
                    bank.lose()
                    break
                else:
                    game_over = False
                
                # Get Player Action
                action = 3
                while action not in [1, 2]:
                    action = input('\n1: Hit, 2: Stand\n')
                    try: 
                        action = int(action)
                    except: 
                        pass
                    if action not in [1, 2]:
                        print('Please Choose Either 1 or 2.')

                # Hit
                if action == 1:
                    self.player_hand.add_card(self.deck.draw())
                    self.player_hand.display()

                    if self.busted():
                        print('\nBusted! Dealer Wins!')
                        bank.lose()
                        game_over = True

                # Stand
                else:
                    player_value, dealer_value = self.player_hand.get_value(), self.dealer_hand.get_value()
                    while dealer_value < 17:
                        self.dealer_hand.add_card(self.deck.draw())
                        dealer_value = self.dealer_hand.get_value()
                    
                    self.dealer_hand.display()

                    if self.busted(player = False):
                        print('\nDealer Busted! Player Wins!')
                        bank.win()
                    elif self.check_blackjack()[1]:
                        print('Dealer has Blackjack! Dealer Wins!')
                        bank.lose()

                    else:
                        print('\nGame Over!')
                        print(f'Your Hand: {player_value}')
                        print(f'Dealer Hand: {dealer_value}')

                        if player_value > dealer_value:
                            print('You Win!')
                            bank.win()
                        elif dealer_value > player_value:
                            bank.lose()
                            print('Dealer Wins!')
                        else:
                            print('Tie!')
                            bank.tie()

                    game_over = True

            # Play Again
            again = 'blank'
            while again not in ['n', 'y']:
                again = input('\nPlay Again? (y/n): ')
                if again not in ['n', 'y']:
                    print('Please Select Either y or n.')

            if again == 'n':
                print('Thanks for Playing!')
                self.playing = False
            else:
                system('cls')
                game_over = False

g = Game()
g.play()