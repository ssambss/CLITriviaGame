import requests
import random

difficulty = ['easy', 'medium', 'hard']



def player_amount():

    number_of_players = input('How many players: ')
    return int(number_of_players)

def init_players(number_of_players):

    players = {}  
    [players.update({f'Player {i}': 0}) for i in range(1, number_of_players + 1)]
    print('\n' + f'Number of players: {len(players)}' + '\n')

    return players

def game_manager():
    isWon = False
    token = get_session_token()
    players = init_players(player_amount())
    while not isWon:
        questions = get_trivia(token)
        isWon = ask_questions(questions, players)
        

def get_trivia(token):

    response = requests.get(f'https://opentdb.com/api.php?amount=2&token={token}')
    data = response.json()
    return data['results']

def get_session_token():

    response = requests.get('https://opentdb.com/api_token.php?command=request')
    token = response.json()
    return token['token']


def ask_questions(questions, players):

    current_player = 1
    
    for question in questions:
        print('Current player ' + str(current_player) + '\n')
        answers = question['incorrect_answers'] + [question['correct_answer']]
        random.shuffle(answers)
        print(question['question'] + '\n')
        for i, answer in enumerate(answers, 1):
            print(f"{i}. {answer}")    
        player_answer = input('\n' + 'Enter your answer: ')
        if player_answer == question['correct_answer']:
            print('Correct!')    
            players[f'Player {current_player}'] += 1

            if players[f'Player {current_player}'] == 1:
                print(f'Player {current_player} wins!')
                return True
        else:
            print('Incorrect!' + '\n' + f'The correct answer was: {question["correct_answer"]}' + '\n')
        current_player += 1

        if current_player > len(players):
            current_player = 1
    
    return False


game_manager()
            


