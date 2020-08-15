import random
import time

class Card:
    def __init__(self, suite, number):
        self.suite = suite
        self.number = number

    def printCard(self):
        print('Suite: ' + self.suite + ' Number: ' + self.number)

class Deck:
    def __init__(self, cards = []):
        self.cards = cards
        self.initialize()

    def initialize(self):
        for s in ['hearts', 'spades', 'diamonds', 'clubs']:
            for n in ['2','3','4','5','6','7','8','9','10','J','Q','K','A']:
                self.cards.append(Card(s,n))
        random.shuffle(self.cards)

    def dealInit(self, players):
        for player in players:
            for x in range(5):
                player.addToHand(self.cards.pop())

    def dealRest(self, players):
        while len(self.cards)>0:
            for player in players:
                player.addToHand(self.cards.pop())


class Player():
    def __init__(self, name):
        self.name = name
        self.hand = {'hearts': [], 'spades': [], 'diamonds': [], 'clubs': []}

    #implemented sorted list
    def addToHand(self, card):
        if (len(self.hand[card.suite]) == 0):
            self.hand[card.suite].append(card)
            return
        numbers = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
        low=0
        hi = len(self.hand[card.suite])
        while(low < hi):
            mid = low + ((hi-low)//2)
            if(numbers.index(self.hand[card.suite][mid].number)>numbers.index(card.number)):
                hi = mid
            else:
                low = mid+1

        if low >= len(self.hand[card.suite]):
            self.hand[card.suite].append(card)
        else:
            self.hand[card.suite].insert(low,card)

    def printHand(self):
        for suite, cardlist in self.hand.items():
            print('\n' + suite + ' cards')
            for card in self.hand[suite]:
                card.printCard()

    def chooseSuite(self):
        pass

    #returns Card
    #both versions have to check that human or auto choice is valid
    def choose(self, choices):
        pass

    #rules:
        #chosen card must be suite of first card in choices if player has such a card in hand
        #if player does not have the leading suite, can use any other suite
    def followsRules(self, choice, choices):
        if len(choices)>0:
            leading_suite = choices[0].suite
        else:
            leading_suite = choice.suite
        choice_suite = choice.suite

        if (leading_suite == choice_suite):
            return True
        else:
            #if there are cards in hand with leading suite, return false
            if len(self.hand[leading_suite]) > 0:
                return False
            return True



class AutoPlayer(Player):

    def __init__(self, name):
        super().__init__(name)

    def chooseSuite(self):
        return random.choice(['hearts', 'spades', 'clubs', 'diamonds'])

    def choose(self, choices):
        random_choice = ''
        first_time=True
        while(first_time or (not self.followsRules(random_choice, choices))):
            random_suite = random.choice(['hearts', 'spades', 'clubs', 'diamonds'])
            if (len(self.hand[random_suite])==0):
                continue
            random_choice = random.choice(self.hand[random_suite])
            first_time=False
        self.hand[random_suite].remove(random_choice)

        time.sleep(2)

        return random_choice

class HumanPlayer(Player):

    def __init__(self, name):
        super().__init__(name)

    def chooseSuite(self):
        print('\nHere are your first five cards: ')
        self.printHand()
        chosen_suite = input('Choose the trump suite for the game: ')
        chosen_suite = chosen_suite.lower()
        return chosen_suite

    def choose(self, choices):
        time.sleep(1)
        print('\nIt\'s your turn! Here is your hand: ')
        self.printHand()

        print('\nChoose a card to play')

        while(True):
            input_suite = input('Suite: ')
            input_number = input('Number: ')

            input_suite = input_suite.lower()
            input_number = input_number.upper()

            numbers = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']

            low = 0
            hi = len(self.hand[input_suite])
            while (low < hi):
                mid = low + ((hi-low)//2)
                if numbers.index(self.hand[input_suite][mid].number) > numbers.index(input_number):
                    hi = mid
                else:
                    low = mid + 1

            if (len(self.hand[input_suite]) > 0 and low <= len(self.hand[input_suite])):
                chosen_card = self.hand[input_suite][low-1]
                if (chosen_card.number == input_number and self.followsRules(chosen_card,choices)):
                    self.hand[input_suite].remove(chosen_card)
                    return chosen_card


            print('You can\'t play that card. Either it doesn\'t follow the rules or it doesn\'t exist. Try again')


class Round:
    def __init__(self, players, first, trumpSuite):
        self.players = players
        self.first = first
        self.trumpSuite = trumpSuite
        self.choices = []

    def play(self):
        i = self.players.index(self.first)
        counter = 0
        while (i < self.players.index(self.first)+4 ):
            self.choices.append(self.players[i%4].choose(self.choices))
            print('\n'+ self.players[i%4].name + ':')
            self.choices[counter].printCard()
            i+=1
            counter+=1

    #assumes self.choices has 4 elements
    #returns Player
    #basic rules:
        #trump suite wins over leading suite
        #leading suite wins over all other suites, so if nobody has trump or leading, first player wins
    def whoWon(self):
        highest_number = '2'
        highest_number_trump_suite = '2'
        trump_played = False
        winner_index_choices = 0
        winner_trump_index_choices = 0
        leading_suite = self.choices[0].suite
        numbers = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
        for choice in self.choices:
            if choice.suite == self.trumpSuite:
                if not trump_played:
                    trump_played = True
                if numbers.index(choice.number) >= numbers.index(highest_number_trump_suite):
                    highest_number_trump_suite = choice.number
                    winner_trump_index_choices = self.choices.index(choice)
            if choice.suite == leading_suite:
                if numbers.index(choice.number) >= numbers.index(highest_number):
                    highest_number = choice.number
                    winner_index_choices = self.choices.index(choice)

        if trump_played:
            return self.players[(self.players.index(self.first)+winner_trump_index_choices)%4]
        else:
            return self.players[(self.players.index(self.first)+winner_index_choices)%4]

class Game:

    should_print_rules = input('Welcome to Hokm! Do you want to read the rules?')
    should_print_rules.lower()
    if (should_print_rules == 'yes'):
        print('Hokm is an Iranian card game played with two teams, two players on each team. It is played multiple times until one of the teams wins 7 games.\n\nDuring each game, the hakem is chosen based on who won the last game. After each player is dealt five cards, the hakem is allowed to look at his/her five cards to decide the trump suite for the game. Then the rest of the deck is dealt evenly to everyone.\n\nEach game is played in rounds until there are no more cards left in the players\' hands\'. During each round, each player puts down a card one by one. A player wins a round when his/her card has the highest number and the right suite. Suite rules: \n\tThe first player to put down a card decides the leading suite for the round\n\tOnly if a player does not have a card of the leading suite is he/she allowed to play a card of a different suite\n\tThe trump suite always wins over the leading suite.\nThe hakem plays first for the first round, then in subsequent rounds the winner of the previous round playes first.')
    time.sleep(3)

    #initialize 4 players (will have to change for multiplayer)
    player1 = HumanPlayer('player 1')
    player2 = AutoPlayer('player 2')
    player3 = AutoPlayer('player 3')
    player4 = AutoPlayer('player 4')
    players = [player1, player2, player3, player4]

    print('\nYou are player 1')
    time.sleep(1)
    print('\nPlayers 1 and 3 are on Team 1. Players 2 and 4 are on Team 2')

    team1score = 0
    team2score = 0
    team1rounds = 0
    team2rounds = 0

    #choose 1st Hakem
    hakem = random.choice(players)

    #for when autoplayers are smarter...previousCards may be sufficient
    previousRounds = []

    deck = Deck()
    handSize = 13

    team1LastRoundWinner = player1
    team2LastRoundWinner = player2

    first = hakem

    while team1score<7 and team2score<7:

        time.sleep(1)
        print('\nThe hakem is ' + hakem.name +'!')

        deck.dealInit(players)
        trumpSuite = hakem.chooseSuite()

        time.sleep(1)
        print('\nThe hakem has chosen ' + trumpSuite)
        deck.dealRest(players)

        time.sleep(1)
        print('\nHere is your hand: ')
        player1.printHand()
        time.sleep(3)

        while (handSize > 0):
            time.sleep(2)
            print('\n'+ first.name + ' plays first')

            crntRound = Round(players, first, trumpSuite)
            crntRound.play()
            handSize-=1
            roundWinner = crntRound.whoWon()
            time.sleep(1)
            print('\n' + roundWinner.name + ' is the round winner!')

            if roundWinner == player1 or roundWinner == player3 :
                team1rounds+=1
                if roundWinner == player1:
                    team1LastRoundWinner = player1
                else:
                    team1LastRoundWinner = player3
            else:
                team2rounds+=1
                if roundWinner == player2:
                    team2LastRoundWinner = player2
                else:
                    team2LastRoundWinner = player4

            time.sleep(2)
            print('\nTeam 1 has round score: ' + str(team1rounds))
            print('Team 2 has round score: ' + str(team2rounds))

            previousRounds.append(crntRound)

            first = roundWinner

        time.sleep(1)
        if team1rounds > team2rounds :
            team1score+=1
            if team1LastRoundWinner == player1:
                hakem = player1
            else:
                hakem = player3
            print('\nTeam 1 won this game!')
        elif team2rounds > team1rounds :
            team2score+=1
            if team2LastRoundWinner == player2:
                hakem = player2
            else:
                hakem = player4
            print('\nTeam 2 won this game!')
        else :
            if roundWinner == player1 or roundWinner == player3 :
                team1score+=1
                if team1LastRoundWinner == player1:
                    hakem = player1
                else:
                    hakem = player3
                print('\nTeam 1 won this game!')
            else :
                team2score+=1
                if team2LastRoundWinner == player2:
                    hakem = player2
                else:
                    hakem = player4
                print('\nTeam 2 won this game!')

        time.sleep(2)
        print('\nTeam 1 has won ' + str(team1score) + ' games!')
        print('Team 2 has won ' + str(team2score) + ' games!')

        previousRounds.clear()
        deck.initialize()
        handSize = 13
        team1rounds = 0
        team2rounds = 0

    time.sleep(3)
    if team1score == 7:
        print("\nTeam 1 Won!")
    else:
        print("\nTeam 2 Won!")
