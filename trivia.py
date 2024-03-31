import requests
import random

difficulty = ['easy', 'medium', 'hard', 'random']
points_by_difficulty = {'easy': 1, 'medium': 2, 'hard': 3}



def get_categories():

    response = requests.get('https://opentdb.com/api_category.php')
    data = response.json()
    data.update({'trivia_categories': [{'id': 0, 'name': 'Random'}] + data['trivia_categories']})
    return data['trivia_categories']


def choose_category(categories):   
        print('\n' + 'Choose a category: ' + '\n')
        for i, category in enumerate(categories, 1):
            print(f'{i}. {category["name"]}')
        category_choice = input('\n' + 'Enter the number of your choice: ')
        return categories[int(category_choice) - 1]['id'], categories[int(category_choice) - 1]['name']

def define_points_to_win():
    points_to_win = input('Enter the amount of points needed to win: ')
    return int(points_to_win)

def player_amount():
    number_of_players = input('How many players: ')
    return int(number_of_players)


def init_players(number_of_players):
    players = {}  
    [players.update({f'Player {i}': 0}) for i in range(1, number_of_players + 1)]

    return players


def choose_difficulty():  
        print('\n' + 'Choose a difficulty: ' + '\n')
        for i, level in enumerate(difficulty, 1):
            print(f'{i}. {level.capitalize()}')
        difficulty_choice = input('\n' + 'Enter the number of your choice: ')
        return difficulty[int(difficulty_choice) - 1]


def game_manager():
    isWon = False
    token = get_session_token()
    players = init_players(player_amount())
    category = choose_category(categories)
    difficulty_choice = choose_difficulty()
    points_to_win = define_points_to_win()
    print('\n' + 'Amount of players: ' + str(len(players)) + '\n')
    print('Category: ' + category[1] + '\n')
    print('Difficulty: ' + difficulty_choice.capitalize() + '\n')
    print('Points to win: ' + str(points_to_win) + '\n')

    confirm = input('Confirm choices (y/n): ')
    if confirm != 'y':
        game_manager()

    print('\n' + 'Let the game begin!' + '\n')

    current_player = 1

    while not isWon:
        questions = get_trivia(token, category, difficulty_choice)
        game_status = ask_questions(questions, players, points_to_win, current_player)
        isWon = game_status[0]
        current_player = game_status[1]
        

def get_trivia(token, category, difficulty):
    url = f'https://opentdb.com/api.php?amount=50&token={token}'

    if category[0] != 0:
        url = f'{url}&category={category[0]}'  
    if difficulty != 'random':
        url = f'{url}&difficulty={difficulty}'

    response = requests.get(url)
    data = response.json()
    return data['results']


def get_session_token():
    response = requests.get('https://opentdb.com/api_token.php?command=request')
    token = response.json()
    return token['token']


def ask_questions(questions, players, points_to_win, current_player):
    options = {}
    
    for question in questions:

        question_difficulty = question['difficulty']    
        print('\n' + 'Current player ' + str(current_player) + '\n')
        answers = question['incorrect_answers'] + [question['correct_answer']]
        random.shuffle(answers)
        print(question['question'] + '\n')

        for i, answer in enumerate(answers, 1):
            if answer == question['correct_answer']:
                options.update({'Correct': [i, answer]})
            print(f"{i}. {answer}")   

        player_answer = input('\n' + 'Enter your answer: ')

        if player_answer == str(options['Correct'][0]) or player_answer == str(options['Correct'][1]):
            print('\n' + 'Correct!')    
            players[f'Player {current_player}'] += points_by_difficulty[question_difficulty]

            if players[f'Player {current_player}'] >= points_to_win:
                print(f'Player {current_player} wins!')
                return True
        else:
            print('\n' + 'Incorrect!' + '\n' + f'The correct answer was: {question["correct_answer"]}' + '\n')
        
        current_player += 1

        if current_player > len(players):
            current_player = 1
            print('\n' + 'Current points: ' + '\n')
            for player, points in players.items():
                print(f'{player}: {points} points')
    
    return False, current_player


categories = get_categories()
game_manager()
            


