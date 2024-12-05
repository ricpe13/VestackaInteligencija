import matplotlib.pyplot as plt
import random

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

    for row in range(len(points_per_row)):
        ax.text(-1, -row, chr(65 + row), fontsize=12, ha='right', va='center')
    for col in range(max_cols):
        first_col_offset = (max_cols - points_per_row[0]) / 2
        ax.text(col + first_col_offset, 1, str(col), fontsize=12, ha='center', va='bottom')

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
        print("Linija već postoji!")
        return

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
                    if triangle_count[player] > max_triangles / 2:
                        print(f"Igrač {player} je pobedio!")
                        plt.ioff()
                        plt.show()
                        return True
    return False

def draw_triangle_label(triangle, label):
    avg_x = sum(node_positions[row][col][0] for row, col in triangle) / 3
    avg_y = sum(node_positions[row][col][1] for row, col in triangle) / 3
    ax.text(avg_x, avg_y, label, fontsize=20, ha='center', va='center', color='black')

def human_turn(symbol, color):
    print(f"Unesite koordinate za liniju (4 tačke) u formatu 'row col':")
    points = []
    for _ in range(4):
        row, col = map(int, input().split())
        points.append((row, col))
    return add_line(points, symbol, color)

def computer_turn(symbol, color):
    attempts = 0
    while attempts < 100:
        row = random.randint(0, len(points_per_row) - 1)
        col_start = random.randint(0, points_per_row[row] - 4)
        direction = random.choice(['horizontal', 'diagonal_down', 'diagonal_up'])

        if direction == 'horizontal':
            points = [(row, col_start + i) for i in range(4)]
        elif direction == 'diagonal_down':
            if row + 3 < len(points_per_row) and all(col_start + i < points_per_row[row + i] for i in range(4)):
                points = [(row + i, col_start + i) for i in range(4)]
            else:
                attempts += 1
                continue
        elif direction == 'diagonal_up':
            if row - 3 >= 0 and all(col_start + i < points_per_row[row - i] for i in range(4)):
                points = [(row - i, col_start + i) for i in range(4)]
            else:
                attempts += 1
                continue

        valid = True
        for i in range(1, len(points)):
            if points[i] not in potential_neighbors[points[i-1]]:  # Provera validnosti suseda
                valid = False
                break

        if valid and tuple(sorted(points)) not in drawn_lines:
            return add_line(points, symbol, color)
        attempts += 1
    print("Računar nije uspeo da pronađe validan potez.")
    return False

draw_hexagonal_board_with_values(4)

def play_game(first_player, first_symbol):
    current_player = first_player
    symbols = {'human': 'X' if first_symbol == 'X' else 'O',
               'computer': 'O' if first_symbol == 'X' else 'X'}
    colors = {'X': 'blue', 'O': 'green'}

    while True:
        if current_player == 'human':
            game_over = human_turn(symbols['human'], colors[symbols['human']])
            current_player = 'computer'
        else:
            game_over = computer_turn(symbols['computer'], colors[symbols['computer']])
            current_player = 'human'
        if game_over or triangle_count['X'] > max_triangles / 2 or triangle_count['O'] > max_triangles / 2:
            break


first_player = input("Ko igra prvi? (human/computer): ")
first_symbol = input("Koji simbol prvi igrač koristi? (X/O): ")
play_game(first_player, first_symbol)


print(f"X je zauzeo {triangle_count['X']} trouglova.")
print(f"O je zauzeo {triangle_count['O']} trouglova.")

plt.ioff()
plt.show()
