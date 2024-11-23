def input_hex_size():
    while True:
        try:
            size = int(input("Unesite veličinu stranice pravilnog šestougla (4-8): "))
            if size in [4, 5, 6, 7, 8]:
                return size
            else:
                print("Pogrešan unos. Pokušajte ponovo.")
        except ValueError:
            print("Pogrešan unos. Pokušajte ponovo.")

def draw_hexagon(size):
    n = size
    total_width = 2 * n - 1  # Ukupna širina šestoougla
    total_height = 2 * n - 1  # Ukupna visina šestoougla

    # Kreiramo praznu tabelu
    board = [[' ' for _ in range(total_width)] for _ in range(total_height)]

    # Gornji deo šestougla
    for i in range(n):
        for j in range(n + i):  # Povećavamo broj tačaka sa svakim redom
            index = total_width // 2 - i + 2 * j  # Računanje tačaka u svakom redu
            if 0 <= index < total_width:
                board[i][index] = '•'

    # Donji deo šestougla (simetrično)
    for i in range(n - 1):
        for j in range(i + n - 1):  # Smanjujemo broj tačaka u svakom sledećem redu
            index = total_width // 2 - (n - 2 - i) + 2 * j
            if 0 <= index < total_width:
                board[n + i][index] = '•'

    # Ispisivanje šestougla
    for row in board:
        print(' '.join(row))

# Unos veličine stranice
hex_size = input_hex_size()
# Crtanje šestougla
draw_hexagon(hex_size)
