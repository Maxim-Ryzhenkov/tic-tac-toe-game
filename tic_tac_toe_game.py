import os
import time

GAME_FIELD = [["-", "-", "-"],
              ["-", "-", "-"],
              ["-", "-", "-"]]
FIELD_SIZE = len(GAME_FIELD)
FIELD_SIZE_INDEX = list(range(FIELD_SIZE))

X_SIGN = "x"
O_SIGN = "o"
FREE_SIGN = "-"
CURSOR_SIGN = "?"
EXIT_KEY = "q"
ARROWS = ["a", "s", "w", "d"]

PLAYER_1 = {"name": "Игрок 1", "sign": X_SIGN}
PLAYER_2 = {"name": "Игрок 2", "sign": O_SIGN}
CURRENT_PLAYER = PLAYER_1
CURSOR_POSITION = {'row': 0, 'column': 0}

MESSAGE = f"""{'=' * 60}
Выход из игры - "{EXIT_KEY}"
Поставить крестик или нолик в свой ход -"Пробел"
Перемещайте курсор стрелками         W(вверх)
                            A(влево) S(вниз) D(вправо)
(Нажатие каждой клавиши завершается нажатием 'Enter')
{'=' * 60}
"""


def get_first_free_position(field: list) -> tuple or None:
    """ Получить позицию первой свободной клетки на поле. """
    for row_number in FIELD_SIZE_INDEX:
        for column_number in FIELD_SIZE_INDEX:
            if field[row_number][column_number] == FREE_SIGN:
                return row_number, column_number
    return None


def is_line_full(line) -> bool:
    """ Есть ли в линии свободные клетки? """
    return FREE_SIGN not in line


def get_column(index: int) -> list:
    """ Получить колонку по индексу """
    return [line[index] for line in GAME_FIELD]


def get_row(index: int) -> list:
    """ Получить ряд по индексу """
    return GAME_FIELD[index]


def get_diagonal_up_to_down() -> list:
    """ Получить диагональ идущую сверху слева - вниз вправо. """
    return [GAME_FIELD[row][column] for row, column in zip(FIELD_SIZE_INDEX, FIELD_SIZE_INDEX)]


def get_diagonal_down_to_up() -> list:
    """ Получить диагональ идущую снизу слева - вверх направо. """
    return [GAME_FIELD[row][column] for row, column in zip(reversed(FIELD_SIZE_INDEX), FIELD_SIZE_INDEX)]


def is_line_completed(line: list, sign: str) -> bool:
    """ Проверить, заполнена ли вся линия крестиками либо ноликами. """
    if len(line) != FIELD_SIZE:
        raise ValueError(f"Ожидается линия длиной {FIELD_SIZE} символа. Получено {line}")
    return all(item == sign for item in line)


def get_cursor_position_value() -> str:
    """ Получить значение из клетки в которой находится курсор. """
    return GAME_FIELD[CURSOR_POSITION['row']][CURSOR_POSITION['column']]


def set_cursor_position_value(value):
    """ Установить значение клетки в которой находится курсор. """
    GAME_FIELD[CURSOR_POSITION['row']][CURSOR_POSITION['column']] = value


def set_cursor_position(row_number: int, column_number: int):
    global CURSOR_POSITION
    CURSOR_POSITION.update({'row': row_number, 'column': column_number})


def move_cursor(arrow: str):
    current_row, current_column = CURSOR_POSITION['row'], CURSOR_POSITION['column']
    if arrow == "a" and current_column > 0:
        set_cursor_position(row_number=current_row, column_number=current_column - 1)
    elif arrow == "d" and current_column < FIELD_SIZE_INDEX[-1]:
        set_cursor_position(row_number=current_row, column_number=current_column + 1)
    elif arrow == "w" and current_row > 0:
        set_cursor_position(row_number=current_row-1, column_number=current_column)
    elif arrow == "s" and current_row < FIELD_SIZE_INDEX[-1]:
        set_cursor_position(row_number=current_row+1, column_number=current_column)
    else:
        raise ValueError(f"Получена неправильная кнопка {arrow}. Допустимые значения: {ARROWS}")


def get_game_field_copy() -> list:
    """ Получить копию игрового поля. """
    return [row.copy() for row in GAME_FIELD]


def update_game_field(field):
    """ Обновить состояние игрового поля """
    global GAME_FIELD
    GAME_FIELD = [row.copy() for row in field]


def render_field(render_cursor=True):
    """ Нарисовать игровое поле. """
    print(f"   {'  '.join(map(str, FIELD_SIZE_INDEX))}")
    field = get_game_field_copy()
    if render_cursor:
        field[CURSOR_POSITION['row']][CURSOR_POSITION['column']] = CURSOR_SIGN
    for line_number in FIELD_SIZE_INDEX:
        line = '  '.join(field[line_number])
        print(f"{line_number}  {line}")


def switch_player():
    """ Поменять текущего игрока. """
    return PLAYER_1 if CURRENT_PLAYER == PLAYER_2 else PLAYER_2


def is_player_win() -> bool:
    """ Проверить, собрал ли игрок полную линию. """
    if any([any(is_line_completed(get_row(number), CURRENT_PLAYER['sign']) for number in FIELD_SIZE_INDEX),
            any(is_line_completed(get_column(number), CURRENT_PLAYER['sign']) for number in FIELD_SIZE_INDEX),
            is_line_completed(get_diagonal_down_to_up(), CURRENT_PLAYER['sign']),
            is_line_completed(get_diagonal_up_to_down(), CURRENT_PLAYER['sign'])]):
        return True
    else:
        return False


def exit_game():
    print("Игра прервана пользователем!")
    exit(0)


if __name__ == "__main__":

    print("Игра в крестики-нолики.")
    PLAYER_1['name'] = input("Введите имя первого игрока (играет крестиками): ")
    PLAYER_2['name'] = input("Введите имя второго игрока (играет ноликами): ")

    while True:
        # Цикл игры
        while True:
            # Цикл хода игрока
            os.system('cls')
            print(MESSAGE)
            print(f"Сейчас ходит {CURRENT_PLAYER['name']}. Поставьте '{CURRENT_PLAYER['sign']}' в свободной клетке.")
            render_field(render_cursor=True)

            # Игрок нажимает клавишу-команду + 'Enter'
            command = input().lower()

            if command in ARROWS:
                # Игрок перемещает курсор
                print(f"Нажата стрелка '{command}'")
                move_cursor(arrow=command)

            elif command == EXIT_KEY:
                # Игрок прерывает игру
                exit_game()

            elif command == " " or command == CURRENT_PLAYER["sign"]:
                # Игрок ставит крестик или нолик на поле
                if get_cursor_position_value() != FREE_SIGN:
                    print(f"Сделать ход можно только на свободной клетке! ")
                    render_field(render_cursor=False)
                    time.sleep(3)
                    continue

                set_cursor_position_value(CURRENT_PLAYER["sign"])
                if is_player_win():
                    # Если игрок выиграл - игра завершается
                    print(f"{CURRENT_PLAYER['name']} выиграл! Игра окончена.")
                    render_field(render_cursor=False)
                    exit(0)

                # Если не выиграл
                free_position = get_first_free_position(GAME_FIELD)
                if not free_position:
                    print("Игра закончена, потому что все ходы исчерпаны! Кажется у нас ничья!")
                    exit(0)
                # Установить курсор на свободную клетку поля и передать ход другому игроку
                row, column = free_position
                set_cursor_position(row_number=row, column_number=column)
                CURRENT_PLAYER = switch_player()
                break
            else:
                print(f"Получена неизвествная клавиша-команда '{command}'. \n"
                      f"Используйте команды, указанные в подсказке к игре.")
                time.sleep(3)
                continue
