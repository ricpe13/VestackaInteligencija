import matplotlib.pyplot as plt
import random

def get_valid_game_mode_input():
    while True:
        try:
            mode = int(input("Koji mod zelis (1 - human vs computer / 2 - human vs human): ").strip())
            if mode in [1, 2]:
                return mode
            else:
                print("Pogrešan unos! Unesite 1 ili 2.")
        except ValueError:
            print("Pogrešan unos! Unesite 1 ili 2.")

def get_player_names_for_mode_2():
    player_1 = input("Unesi ime prvog igraca: ").strip()
    player_2 = input("Unesi ime drugog igraca: ").strip()
    return player_1, player_2

def draw_hexagonal_board_with_values(n):
    global node_positions, fig, ax, points_per_row, max_cols, drawn_lines, neighbors, triangles, triangle_count, max_triangles, potential_neighbors
    if n == 4:
        points_per_row = [4, 5, 6, 7, 6, 5, 4]
    elif n == 5:
        points_per_row = [5, 6, 7, 8, 9, 8, 7, 6, 5]
    elif n == 6:
        points_per_row = [6, 7, 8, 9, 10, 11, 10, 9, 8, 7, 6]
    elif n == 7:
        points_per_row = [7, 8, 9, 10, 11, 12, 13, 12, 11, 10, 9, 8, 7]
    elif n == 8:
        points_per_row = [8, 9, 10, 11, 12, 13, 14, 15, 14, 13, 12, 11, 10, 9, 8]

    max_cols = max(points_per_row)
    max_triangles = calculate_max_triangles(points_per_row)

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')

    node_positions = []
    drawn_lines = set()
    neighbors = {}
    potential_neighbors = {}
    triangles = []
    triangle_count = {'X': 0, 'O': 0}

    for row, num_points in enumerate(points_per_row):
        row_positions = []
        for col in range(num_points):
            x = col + (max_cols - num_points) / 2
            y = -row
            row_positions.append((x, y))
            ax.plot(x, y, 'o', color='blue', markersize=8)
        node_positions.append(row_positions)

    # Dodavanje oznaka redova (A, B, C...)
    for row in range(len(points_per_row)):
        ax.text(-1, -row, chr(65 + row), fontsize=12, ha='right', va='center')

    # Dodavanje oznaka kolona (1, 2, 3...) iznad i ispod table
    for col in range(max_cols):
        first_col_offset = (max_cols - points_per_row[0]) / 2
        ax.text(col + first_col_offset, 1, str(col + 1), fontsize=12, ha='center', va='bottom')  # Iznad table
        ax.text(col + first_col_offset, -len(points_per_row), str(col + 1), fontsize=12, ha='center',
                va='top')  # Ispod table

    ax.axis('off')
    plt.ion()

    # Definisanje potencijalnih suseda za svaku tačku
    for row in range(len(points_per_row)):
        for col in range(points_per_row[row]):
            potential_neighbors[(row, col)] = get_potential_neighbors(row, col)


def calculate_max_triangles(points_per_row):
    n = len(points_per_row)
    middle_index = n // 2
    return sum([(2 * x - 1) for i, x in enumerate(points_per_row) if i != middle_index])

def get_potential_neighbors(row, col):
    potential = []
    if row > 0:  # Tačke iznad
        potential.append((row - 1, col))
        if col < points_per_row[row - 1] - 1:
            potential.append((row - 1, col + 1))
    if row < len(points_per_row) - 1:  # Tačke ispod
        potential.append((row + 1, col))
        if col > 0:
            potential.append((row + 1, col - 1))
    if col > 0:  # Tačke levo
        potential.append((row, col - 1))
    if col < points_per_row[row] - 1:  # Tačke desno
        potential.append((row, col + 1))
    return potential

def add_line(points, player, color='red'):
    points = sorted(points)
    points_tuple = tuple(points)
    if points_tuple in drawn_lines:
        return False, "Linija već postoji!"

    x_values = [node_positions[row][col][0] for row, col in points]
    y_values = [node_positions[row][col][1] for row, col in points]
    ax.plot(x_values, y_values, color=color, linewidth=2)

    for i in range(len(points)):
        row, col = points[i]
        if (row, col) not in neighbors:
            neighbors[(row, col)] = set()
        if i > 0:
            prev_row, prev_col = points[i - 1]
            if (prev_row, prev_col) not in neighbors:
                neighbors[(prev_row, prev_col)] = set()
            neighbors[(row, col)].add((prev_row, prev_col))
            neighbors[(prev_row, prev_col)].add((row, col))
        if i < len(points) - 1:
            next_row, next_col = points[i + 1]
            if (next_row, next_col) not in neighbors:
                neighbors[(next_row, next_col)] = set()
            neighbors[(row, col)].add((next_row, next_col))
            neighbors[(next_row, next_col)].add((row, col))

    drawn_lines.add(points_tuple)
    plt.pause(0.1)

    for i in range(len(points)):
        row, col = points[i]
        for neighbor in neighbors[(row, col)]:
            common_neighbors = neighbors[(row, col)].intersection(neighbors[neighbor])
            for common_neighbor in common_neighbors:
                triangle = sorted([(row, col), neighbor, common_neighbor])
                if triangle not in triangles:
                    triangles.append(triangle)
                    draw_triangle_label(triangle, player)
                    triangle_count[player] += 1
                    plt.pause(0.1)  # Ažuriraj prikaz odmah nakon iscrtavanja simbola trougla
                    if triangle_count[player] > max_triangles / 2:
                        print(f"Igrač sa simbolom {player} je pobedio!")
                        display_game_over_message()
                        plt.ioff()
                        plt.show()
                        return True, None
    return False, None



def draw_triangle_label(triangle, label):
    avg_x = sum(node_positions[row][col][0] for row, col in triangle) / 3
    avg_y = sum(node_positions[row][col][1] for row, col in triangle) / 3
    ax.text(avg_x, avg_y, label, fontsize=20, ha='center', va='center', color='black')
    plt.draw()  # Osvežavanje prikaza odmah nakon što je simbol postavljen


def interpret_command_with_dd(row, col, direction):
    middle_row = len(points_per_row) // 2  # Red sa najviše tačaka (najduži red)

    points = [(row, col)]

    for _ in range(3):  # Potrebno je da dodamo još tri tačke
        if row < middle_row:  # Ako smo iznad srednjeg reda
            next_row = row + 1
            next_col = col + 1
        else:  # Ako smo u srednjem ili ispod srednjeg reda
            next_row = row + 1
            next_col = col

        # Provera validnosti naredne tačke
        if next_row >= len(points_per_row) or next_col >= points_per_row[next_row]:
            return None, "Potez nije validan (prelazi granice table)."

        row, col = next_row, next_col
        points.append((row, col))

    return points, None


def interpret_command_with_d(row, col, direction):
    points = [(row, col)]

    for _ in range(3):  # Potrebno je da dodamo još tri tačke
        col += 1

        # Provera validnosti sledeće tačke
        if col >= points_per_row[row]:
            return None, "Potez nije validan (prelazi granice table)."

        points.append((row, col))

    return points, None


def interpret_command_with_dl(row, col, direction):
    """
    Obrada komande za potez prema dole levo (DL).

    Args:
        row (int): Početni red.
        col (int): Početna kolona.
        direction (str): Smer poteza ("DL").

    Returns:
        list: Lista tačaka [(row, col), ...] koje čine potez.
        str: Poruka o grešci ako potez nije validan.
    """
    points = [(row, col)]
    middle_row = len(points_per_row) // 2  # Središnji (najduži) red

    for i in range(1, 4):  # Dodavanje još tri tačke
        next_row = row + i  # Pomera se na sledeći red

        if next_row >= len(points_per_row):  # Provera granica
            return None, "Potez nije validan (prelazi granice table)"

        # Provera sledeće kolone u zavisnosti od prelaza
        if row < middle_row and next_row >= middle_row:
            # Prelazak iznad na ispod najdužeg reda
            next_col = col - (next_row - middle_row)
        elif row >= middle_row:
            # Redovi ispod najdužeg reda (smanjuje se za i)
            next_col = col - i
        else:
            # Redovi iznad najdužeg reda (kolona ostaje ista)
            next_col = col

        # Provera validnosti sledeće tačke
        if next_col < 0 or next_col >= points_per_row[next_row]:
            return None, "Potez nije validan (prelazi granice table)"

        points.append((next_row, next_col))

    return points, None

def human_turn(symbol, color):
    while True:
        print(f"Unesi potez (npr. A 1 D, A 1 DD, A 1 DL):")
        command = input().split()
        if len(command) != 3:
            print("Pogrešan format unosa! Pokušaj ponovo.")
            continue

        row_letter, col, direction = command
        row_letter = row_letter.upper()  # Normalizacija reda na veliko slovo
        direction = direction.upper()   # Normalizacija pravca na veliko slovo

        try:
            # Konverzija slova u indeks reda
            row = ord(row_letter) - ord('A')
            # Konverzija kolone u indeks
            col = int(col) - 1

            # Provera validnosti reda i kolone
            if row < 0 or row >= len(points_per_row):
                print("Pogrešan red! Pokušaj ponovo.")
                raise ValueError

            if col < 0 or col >= points_per_row[row]:
                print("Pogrešna kolona! Pokušaj ponovo.")
                raise ValueError

            # Obrada pravca
            if direction == 'D':
                points, error = interpret_command_with_d(row, col, direction)
            elif direction == 'DD':
                points, error = interpret_command_with_dd(row, col, direction)
            elif direction == 'DL':
                points, error = interpret_command_with_dl(row, col, direction)
            else:
                print("Nepoznat pravac! Pokušajte ponovo.")
                continue

            if error:
                print(error)
                continue

            # Dodavanje linije na osnovu izračunatih tačaka
            game_over, message = add_line(points, symbol, color)
            if not game_over and message:
                print(message)
            else:
                return game_over, None

        except ValueError:
            print("Pogrešno je uneto, unesi ponovo.")


def computer_turn(symbol, color):
    attempts = 0
    while attempts < 100:
        row = random.randint(0, len(points_per_row) - 1)
        col = random.randint(0, points_per_row[row] - 1)
        direction = random.choice(['D', 'DL', 'DD'])

        if direction == 'D':
            points, error = interpret_command_with_d(row, col, direction)
        elif direction == 'DL':
            points, error = interpret_command_with_dl(row, col, direction)
        elif direction == 'DD':
            points, error = interpret_command_with_dd(row, col, direction)
        else:
            error = "Nepoznat pravac"

        if error:
            attempts += 1
            continue

        # Provera da li su tačke već povezane
        if tuple(sorted(points)) not in drawn_lines:
            return add_line(points, symbol, color)

        attempts += 1

    print("Računar nije uspeo da pronađe validan potez.")
    return False, None


def get_valid_size_input():
    while True:
        try:
            size = int(input("Unesi velicinu table (4-8): ").strip())
            if size >= 4 and size <= 8:
                return size
            else:
                print("Pogrešan unos! Unesite broj između 4 i 8.")
        except ValueError:
            print("Pogrešan unos! Unesite broj između 4 i 8.")

def get_valid_player_input():
    while True:
        player = input("Ko igra prvi? (human/computer): ").strip().lower()
        if player in ['human', 'computer']:
            return player
        else:
            print("Pogrešan unos! Molimo unesite 'human' ili 'computer'.")

def get_valid_symbol_input():
    while True:
        symbol = input("Koji simbol prvi igrac koristi? (X/O): ").strip().upper()
        if symbol in ['X', 'O']:
            return symbol
        else:
            print("Pogrešan unos! Molimo unesite 'X' ili 'O'.")

def display_game_over_message():
    """
    Prikazuje poruku 'Završena igra' preko table.
    """
    # Dimenzije i boje
    rect_width = max_cols
    rect_height = len(points_per_row) / 2
    rect_color = 'black'
    text_color = 'white'

    # Koordinate pravougaonika (centar tabele)
    center_x = max_cols / 2
    center_y = -len(points_per_row) / 2

    # Crtanje pravougaonika preko cele table
    ax.add_patch(plt.Rectangle(
        (center_x - rect_width / 2, center_y - rect_height / 2),
        rect_width, rect_height, color=rect_color, zorder=2
    ))

    # Dodavanje teksta preko pravougaonika
    ax.text(center_x, center_y, 'ZAVRŠENA IGRA', fontsize=30, ha='center', va='center', color=text_color, zorder=3)
    plt.draw()


# Glavni deo programa
size = get_valid_size_input()
game_mode = get_valid_game_mode_input()  # Dodajemo unos za mod igre

# Ako je izabrano 2, tražimo imena igrača
if game_mode == 2:
    player_1, player_2 = get_player_names_for_mode_2()
    print(f"Prvi igrač je: {player_1}")
    print(f"Drugi igrač je: {player_2}")
    first_player = 'human'  # Početni igrač je ljudski
    first_symbol = get_valid_symbol_input()  # Unos simbola (X ili O)
else:
    first_player = get_valid_player_input()
    first_symbol = get_valid_symbol_input()

draw_hexagonal_board_with_values(size)
plt.show(block=False)  # Ovo omogućava otvaranje prozora odmah nakon postavljanja pitanja za simbol

# Započinjemo igru
current_player = first_player

while True:
    if game_mode == 1:
        # Mod: human vs computer
        if current_player == 'human':
            game_over, _ = human_turn(first_symbol, 'blue')
            current_player = 'computer'
        else:
            game_over, _ = computer_turn('O', 'red')
            current_player = 'human'
    elif game_mode == 2:
        # Mod: human vs human
        if current_player == 'human':
            game_over, _ = human_turn(first_symbol, 'blue')
            current_player = 'human_2'
        else:
            game_over, _ = human_turn('O', 'red')
            current_player = 'human'

    if game_over:
        display_game_over_message()
        print(f"{player_1} je zauzeo {triangle_count['X']} trouglova.")
        print(f"{player_2} je zauzeo {triangle_count['O']} trouglova.")
        break

plt.ioff()  # Isključuje interaktivni mod nakon završetka igre
plt.show()  # Prikazuje finalnu tablu