#
# NWEN 241 Programming Assignment 5
# kgame.py Python Source File
#
# Name:         CHRISTOPHER CORBETT
# Student ID:   300370980
#
# IMPORTANT: Implement the functions specified in kgame.h here.
# You are free to implement additional functions that are not specified in kgame.h here.
#

import random

# This is the title of the game
KGAME_TITLE = "The K-Game (Python Edition)"

# This is the file name of the saved game state
KGAME_SAVE_FILE = "kgame.sav"

# Number of tiles per side
KGAME_SIDES = 4

# Output buffer size in bytess
KGAME_OUTPUT_BUFLEN = ((18*40)+1)

# Arrow keys
dirs = { 'UP': 1, 'DOWN': 2, 'LEFT': 3, 'RIGHT': 4 }

# Keys accepted by game
inputs = { 'LOAD': 5, 'SAVE': 6, 'EXIT': 7}


def kgame_init(game):
    game['score'] = 0
    game['board'] = [[' ' for x in range(KGAME_SIDES)] for y in range(KGAME_SIDES)]


def kgame_add_random_tile(game):
    # find random, but empty tile
    # FIXME: will go to infinite loop if no empty tile

    # return/don't add tile if there are no empty spaces on the board
    count = 0
    for i in range(0, KGAME_SIDES):
        for j in range(0, KGAME_SIDES):
            if game['board'][i][j] != ' ':
                count += 1

    if count == 16: return

    while True:
        row = random.randint(0, KGAME_SIDES-1)
        col = random.randint(0, KGAME_SIDES-1)
        if game['board'][row][col] == ' ':
            break

    # place to the random position 'A' or 'B' tile
    game['board'][row][col] = 'A'
    if random.randint(0, 2) == 1:
        game['board'][row][col] = 'B'


def kgame_render(game):
    # FIXME: Implement correctly (task 1)

    # PRINT GAME SCORE
    output_buffer = "\n\n   Current Score: " + str(game['score']) + "\n   "

    # PRINT TOP BORDER OF GAME FIELD
    for i in range(0, KGAME_SIDES):
        output_buffer += "+---"
    output_buffer += "+"

    # PRINT GAME FIELD/CHARACTERS
    for i in range(0, KGAME_SIDES):
        output_buffer += "\n   |"
        for j in range(0, KGAME_SIDES):
            if game['board'][i][j] == ' ':
                output_buffer += "   |"
            else:
                output_buffer += " " + game['board'][i][j] + " |"

        # PRINT HORIZONTAL BORDERS INSIDE GAME FIELD
        output_buffer += "\n   +"
        for i2 in range(0, KGAME_SIDES):
                output_buffer += "---+"

    return output_buffer


def kgame_is_won(game):
    # FIXME: Implement correctly (task 2)

    # RETURNS TRUE IF A K TILE IS FOUND/THE GAME IS WON
    for i in range(0, KGAME_SIDES):
        for j in range(0, KGAME_SIDES):
            if game['board'][i][j] == 'K':
                return True

    return False


def kgame_is_move_possible(game):
    # FIXME: Implement correctly (task 3)

    # RETURNS TRUE IF THERE ARE ANY EMPTY TILES ON THE BOARD
    for i in range(0, KGAME_SIDES):
        for j in range(0, KGAME_SIDES):
            if game['board'][i][j] == ' ':
                return True

    for i in range(0, KGAME_SIDES):
        for j in range(0, KGAME_SIDES-1):
            if game['board'][i][j] == game['board'][i][j+1]:
                return True

    for i in range(0, KGAME_SIDES-1):
        for j in range(0, KGAME_SIDES):
            if game['board'][i][j] == game['board'][i+1][j]:
                return True

    return False


# RETURNS THE VALUE OF THE PIECES BEING MERGED, MULTIPLIED BY TWO.
def update_score(piece):

    score = 0
    if piece == 'A':
        score = 2
    elif piece == 'B':
        score = 4
    elif piece == 'C':
        score = 8
    elif piece == 'D':
        score = 16
    elif piece == 'E':
        score = 32
    elif piece == 'F':
        score = 64
    elif piece == 'G':
        score = 128
    elif piece == 'H':
        score = 256
    elif piece == 'I':
        score = 512
    elif piece == 'J':
        score = 1024
    elif piece == 'K':
        score = 2048
    return score*2


# RETURNS THE NEW CHARACTER AS A RESULT OF THE MERGE
def increment_char(piece):

    new_char = ''
    if piece == 'A':
        new_char = 'B'
    elif piece == 'B':
        new_char = 'C'
    elif piece == 'C':
        new_char = 'D'
    elif piece == 'D':
        new_char = 'E'
    elif piece == 'E':
        new_char = 'F'
    elif piece == 'F':
        new_char = 'G'
    elif piece == 'G':
        new_char = 'H'
    elif piece == 'H':
        new_char = 'I'
    elif piece == 'I':
        new_char = 'J'
    elif piece == 'J':
        new_char = 'K'
    return new_char


def kgame_update(game, direction):
    # FIXME: Implement correctly (task 4)

    # I HAVE COMMENTED THE FIRST 'RIGHT' PART ONLY.
    # OTHER DIRECTIONS ARE EXACT SAME LOGIC YET OBVIOUSLY VICE VERSA/ETC FOR ROW/COL SWITCHES ETC

    # RIGHT
    if direction == 4:

        # START AT TOP ROW AND SECOND FROM RIGHT COL(J = KGAME_SIDES - 2).
        # WE DON'T NEED TO CHECK FAR RIGHT COL AS IT CANNOT SLIDE FURTHER RIGHT.
        # ^ THIS PREVENTS OUT OF BOUNDS ERRORS WHEN CHECKING +1'S
        for i in range(0, KGAME_SIDES):

            # COUNT COUNTS HOW MANY TIMES A TILE HAS MERGED
            # WE ONLY ALLOW ONE MERGE PER TILE/PER ROW
            # COUNT RESETS EACH ROW ITERATION.
            # COUNT STARTS AT MINUS ONE SO THAT WHEN IN THE 0th ROW IT STILL CHECKS
            # (BECAUSE COUNT = MOVE BEFORE THE 'BREAK' CALL)
            count = -1
            for j in range(KGAME_SIDES - 2, -1, -1):
                if game['board'][i][j] != ' ':
                    # SLIDE UNTIL ALL IN ROW HAVE MOVED
                    for move in range(j, KGAME_SIDES-1):
                        if game['board'][i][move+1] == ' ':
                            game['board'][i][move + 1] = game['board'][i][move]
                            game['board'][i][move] = ' '

                        # IF THERE ARE TWO ADJACENT TILES, THEN MERGE THEM AND UPDATE SCORE.
                        # THE COUNT ONLY ALLOWS TWO TILES TO MERGE ONCE PER ROW.
                        # (STOPS BBBB ENDING UP AS D, RATHER, IT STOPS AT --CC)
                        if game['board'][i][move] == game['board'][i][move+1] and count != move:
                            (game['board'])[i][move + 1] = increment_char((game['board'])[i][move + 1])
                            game['score'] += update_score(game['board'][i][move])
                            game['board'][i][move] = ' '
                            count = move
                            break

        kgame_add_random_tile(game)
        return True

    # LEFT
    elif direction == 3:
        for i in range(0, KGAME_SIDES):
            count = -1
            for j in range(1, KGAME_SIDES):
                if game['board'][i][j] != ' ':
                    for move in range(j, 0, -1):
                        if game['board'][i][move-1] == ' ':
                            game['board'][i][move-1] = game['board'][i][move]
                            game['board'][i][move] = ' '
                        if game['board'][i][move] == game['board'][i][move-1] and count != move:
                            (game['board'])[i][move - 1] = increment_char((game['board'])[i][move - 1])
                            game['score'] += update_score(game['board'][i][move])
                            game['board'][i][move] = ' '
                            count = move
                            break
        kgame_add_random_tile(game)
        return True

    # UP
    elif direction == 1:
        for j in range(0, KGAME_SIDES):
            count = -1
            for i in range(1, KGAME_SIDES):
                if game['board'][i][j] != ' ':
                    for move in range(i, 0, -1):
                        if game['board'][move-1][j] == ' ':
                            game['board'][move-1][j] = game['board'][move][j]
                            game['board'][move][j] = ' '
                        if game['board'][move][j] == game['board'][move-1][j] and count != move:
                            (game['board'])[move-1][j] = increment_char((game['board'])[move-1][j])
                            game['score'] += update_score(game['board'][move][j])
                            game['board'][move][j] = ' '
                            count = move
                            break
        kgame_add_random_tile(game)
        return True

    # DOWN
    elif direction == 2:
        for j in range(0, KGAME_SIDES):
            count = -1
            for i in range(KGAME_SIDES-2, -1, -1):
                if game['board'][i][j] != ' ':
                    for move in range(i, KGAME_SIDES-1):
                        if game['board'][move+1][j] == ' ':
                            game['board'][move+1][j] = game['board'][move][j]
                            game['board'][move][j] = ' '
                        if game['board'][move][j] == game['board'][move+1][j] and count != move:
                            (game['board'])[move+1][j] = increment_char((game['board'])[move+1][j])
                            game['score'] += update_score(game['board'][move][j])
                            game['board'][move][j] = ' '
                            count = move
                            break
        kgame_add_random_tile(game)
        return True

    else:
        return False


def kgame_save(game):
    # FIXME: Implement correctly (task 5)

    # DECLARE OUTPUT FILE TO WRITE TO.
    output = open(KGAME_SAVE_FILE, "w")

    # ITERATE THROUGH GAME BOARD. WRITE TO FILE APPROPRIATELY.
    for i in range(0, KGAME_SIDES):
        for j in range(0, KGAME_SIDES):
            if game['board'][i][j] == ' ':
                output.write('-')
            else:
                output.write(game['board'][i][j])

    output.write(" " + str(game['score']))

    output.close()

    return True


def kgame_load(game):
    # FIXME: Implement correctly (task 6)

    count = 0

    # RETURNS FALSE IF THE FILE IS NULL OR NON-EXISTENT

    input_file = None
    try:
        input_file = open(KGAME_SAVE_FILE, "r")
    except:
        return False

    # READS THE INPUT FILE TO A STRING.
    # THIS ALLOWS EASY GETTING OF CHARACTERS AND SCORE
    file_string = input_file.read()

    # GETS CHARACTER AT COUNT INDEX OF FILE STRING. FILL BOARD APPROPRIATELY.
    for i in range(0, KGAME_SIDES):
        for j in range(0, KGAME_SIDES):
            if file_string[count] == '-':
                game['board'][i][j] = ' '
            else:
                game['board'][i][j] = file_string[count]
            count += 1

    # COUNT = 17 IS ALWAYS THE START OF THE SCORE.
    count = 17
    score = ''

    # CONCATENATE TO SCORE
    while count < len(file_string):
        score += file_string[count]
        count += 1

    # CAST SCORE FROM STRING TO INT AND PASS TO GAME[SCORE].
    game['score'] = int(score)

    input_file.close()

    return True
