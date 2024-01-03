# 2. Refactoring des Snake-Spiels von
# https://github.com/Carla-Codes/simple-snake-game-python/blob/main/snake.py

# Anpassungen:
# - Logik klarer durch Hilfsfunktionen, zB crossed_boundary
# - Erste Vorbereitungen um play_game unabhängig von curses zu machen:
#   Fast alle curses-Aufrufe in Funktionen ausgelagert
#   --> soll später das View-Interface werden

import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint


def init_curses() -> curses.window:
    curses.initscr()  # initialize
    window = curses.newwin(30, 60, 0, 0)  # Neues Fenster H=30, W=60
    window.keypad(True)  # enable keypad
    curses.noecho()  # turn off automatic echoing of keys to the screen
    curses.curs_set(0)  # hide the cursor
    window.nodelay(True)  # makes it possible to not wait for the user input
    return window


def draw_static_elements(window: curses.window, score: int) -> None:
    window.border(0)  # draw a border around the window
    # display the score and title
    window.addstr(0, 2, "Score: " + str(score) + " ")
    window.addstr(0, 27, " SNAKE! ")


def game_aborted(key) -> bool:
    return key == 27


def compute_timeout(snake: list) -> int:
    return 140 - (len(snake) // 5 + len(snake) // 10) % 120


def refresh_and_get_key(window: curses.window, old_key: int) -> int:
    # refreshes the screen and then waits for the user to hit a key
    # TODO: Trennung der Darstellung vom Abfragen der Events
    event = window.getch()
    return old_key if event == -1 else event


def compute_head_position(head: list[int], key: int) -> list[int]:
    # Alte Version (schwer nachvollziehbar):
    # return [
    #     head[0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1),
    #     head[1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1),
    # ]

    # Neue Version (klarer, aber länger; das ändern wir später noch):
    hy, hx = head
    if key == KEY_DOWN:
        return [hy + 1, hx]
    elif key == KEY_UP:
        return [hy - 1, hx]
    elif key == KEY_LEFT:
        return [hy, hx - 1]
    elif key == KEY_RIGHT:
        return [hy, hx + 1]
    else:
        return head


def crossed_boundary(snake: list, window: curses.window) -> bool:
    max_y, max_x = window.getmaxyx()
    return (
        snake[0][0] == 0
        or snake[0][0] == max_y - 1
        or snake[0][1] == 0
        or snake[0][1] == max_x - 1
    )


def has_eaten_itself(snake: list) -> bool:
    return snake[0] in snake[1:]


def generate_new_food_position(snake: list, window: curses.window) -> list[int]:
    max_y, max_x = window.getmaxyx()
    while True:
        food = [randint(1, max_y - 2), randint(1, max_x - 2)]
        if food in snake:
            continue
        return food


def play_game(window: curses.window) -> int:
    score = 0
    key = KEY_RIGHT
    snake = [[5, 8], [5, 7], [5, 6]]
    food = [10, 25]

    while True:
        if game_aborted(key):
            break

        draw_static_elements(window, score)
        window.addch(food[0], food[1], "O")
        new_timeout = compute_timeout(snake)
        window.timeout(new_timeout)
        key = refresh_and_get_key(window, key)

        # Move the snake
        head_pos = compute_head_position(snake[0], key)
        snake.insert(0, head_pos)

        if crossed_boundary(snake, window):
            break

        if has_eaten_itself(snake):
            break

        # When snake eats the food
        if snake[0] == food:
            score += 1
            food = generate_new_food_position(snake, window)
        else:
            last = snake.pop()
            window.addch(last[0], last[1], " ")
        window.addch(snake[0][0], snake[0][1], "#")

    return score


def main() -> None:
    window = init_curses()
    score = play_game(window)
    curses.endwin()  # close the window and end the game
    print("\nScore: " + str(score))


if __name__ == "__main__":
    main()
