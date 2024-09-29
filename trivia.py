import requests
import random
import html

difficulty = ['random', 'easy', 'medium', 'hard']
points_by_difficulty = {'easy': 1, 'medium': 2, 'hard': 3}


def get_categories() -> dict:
    response = requests.get('https://opentdb.com/api_category.php')
    data = response.json()
    data.update({'trivia_categories': [{'id': 0, 'name': 'Random'}] + data['trivia_categories']})
    return data['trivia_categories']

def get_amount_of_questions_per_category(category_id) -> dict:
    response = requests.get(f'https://opentdb.com/api_count.php?category={category_id}')
    data = response.json()
    return data['category_question_count']

def choose_category(categories) -> tuple:   
        print('\n' + 'Choose a category: ' + '\n')
        for i, category in enumerate(categories, 1):
            print(f'{i}. {category["name"]}')
        category_choice = input('\n' + 'Enter the number of your choice: ')
        return categories[int(category_choice) - 1]['id'], categories[int(category_choice) - 1]['name']

def define_points_to_win() -> int:
    points_to_win = input('Enter the amount of points needed to win: ')
    return int(points_to_win)

def player_amount() -> int:
    number_of_players = input('How many players: ')
    return int(number_of_players)

def init_players(number_of_players) -> dict:
    players = {}  
    [players.update({f'Player {i}': 0}) for i in range(1, number_of_players + 1)]

    return players

def choose_difficulty() -> str:  
        print('\n' + 'Choose a difficulty: ' + '\n')
        for i, level in enumerate(difficulty, 1):
            print(f'{i}. {level.capitalize()}')
        difficulty_choice = input('\n' + 'Enter the number of your choice: ')
        return difficulty[int(difficulty_choice) - 1]

def get_players() -> dict:
    players = init_players(player_amount())  
    return players

def get_category() -> tuple:
    category = choose_category(categories)
    return category

def get_difficulty() -> str:
    difficulty_choice = choose_difficulty()
    return difficulty_choice

def get_points_to_win() -> int:
    points_to_win = define_points_to_win()
    return points_to_win

def get_session_token() -> str:
    response = requests.get('https://opentdb.com/api_token.php?command=request')
    token = response.json()
    return token['token']

def get_trivia(token, category, difficulty_choice) -> list:   
    if category[0] != 0:
        question_amounts = get_amount_of_questions_per_category(category[0])    
        if difficulty_choice == "random":
            question_key = 'total_question_count'
            amount_of_questions = int(question_amounts[question_key])
        else:
            for option in difficulty:
                if option == difficulty_choice.lower():
                    question_key = 'total_' + option + '_question_count'
                    amount_of_questions = int(question_amounts[question_key])

    else:
        amount_of_questions = 50
            
    url = f'https://opentdb.com/api.php?amount={amount_of_questions}&token={token}'

    if category[0] != 0:
        url = f'{url}&category={category[0]}'
    if difficulty_choice.lower() != 'random':
        url = f'{url}&difficulty={difficulty_choice}'

    response = requests.get(url)
    data = response.json()

    if data['response_code'] == 4:
        return data['response_code']

    return data['results']


def ask_questions(questions, players, points_to_win, current_player) -> tuple:
    options = {}
    
    for question in questions:

        question_difficulty = question['difficulty']    
        print('\n' + 'Current player ' + str(current_player) + '\n')
        decoded_correct_answer = [html.unescape(question['correct_answer'])]
        decoded_incorrect_answers = [html.unescape(answer) for answer in question['incorrect_answers']]
        answers = decoded_correct_answer + decoded_incorrect_answers
        random.shuffle(answers)
        decoded_question = html.unescape(question['question'])
        print(decoded_question + '\n')

        for i, answer in enumerate(answers, 1):
            if answer == decoded_correct_answer[0]:
                options.update({'Correct': [i, answer]})
            print(f"{i}. {answer}")   

        player_answer = input('\n' + 'Enter your answer: ')

        if player_answer == str(options['Correct'][0]) or player_answer == str(options['Correct'][1]):
            print(f'\n' + 'Correct!' + ' Player ' + str(current_player) + ' gained ' + str(points_by_difficulty[question_difficulty]) + ' points.') 
            players[f'Player {current_player}'] += points_by_difficulty[question_difficulty]

            if players[f'Player {current_player}'] >= points_to_win:
                print(f'Player {current_player} wins!')
                return True, current_player
        else:
            print('\n' + 'Incorrect!' + '\n' + f'The correct answer was: {question["correct_answer"]}' + '\n')
        
        current_player += 1

        if current_player > len(players):
            current_player = 1
            print('\n' + 'Current points: ' + '\n')
            for player, points in players.items():
                print(f'{player}: {points} points')
    
    return False, current_player

def game_manager() -> None:
    isWon = False
    token = get_session_token()
    players = get_players()
    category = get_category()
    difficulty_choice = get_difficulty()
    points_to_win = get_points_to_win()
    print('\n' + 'Amount of players: ' + str(len(players)) + '\n')
    print('Category: ' + category[1] + '\n')
    print('Difficulty: ' + difficulty_choice.capitalize() + '\n')
    print('Points to win: ' + str(points_to_win) + '\n')

    confirm = input('Confirm choices (y/n): ')
    if confirm != 'y':
        players = get_players()
        category = get_category()
        difficulty_choice = get_difficulty()
        points_to_win = get_points_to_win()
    

    print('\n' + 'Let the game begin!' + '\n')

    current_player = 1

    while not isWon:
        
        questions = get_trivia(token, category, difficulty_choice)

        if questions == 4:
            print('All questions have been used in this category and difficulty. Please choose another category or difficulty.' + '\n')
            input('Press enter to continue...')
            token = get_session_token()
            category = get_category()
            difficulty_choice = get_difficulty()
            questions = get_trivia(token, category, difficulty_choice)

        game_status = ask_questions(questions, players, points_to_win, current_player)
        isWon = game_status[0]
        current_player = game_status[1]

categories = get_categories()
game_manager()
            


