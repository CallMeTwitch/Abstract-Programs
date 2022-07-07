# ###############################
# Close to full working Chess Game.
# Doesn't see checkmate, Does see check.
# Type in the piece start & end position to move.
# Exmaple:
# E2
# E4
# Will move white's e2 pawn to e4
# ###############################

# Imports
from time import sleep
import sys

turn = 1

# Store Pieces
black = {q:'♖♘♗♕♔♗♘♖♙♙♙♙♙♙♙♙'[q] for q in range(16)}
white = {q:'♟♟♟♟♟♟♟♟♜♞♝♛♚♝♞♜'[q - 48] for q in range(48, 64)}
moved = [0] * 64

en_passent = -1

# Show Board
def show():
    board = {**white, **black}
    output = f'{"White" if turn else "Black"}\n  A B C D E F G H\n'

    for y in range(8):
        output += str(8 - y) + ' '
        for x in range(8):
            output += board[y * 8 + x] + ' ' if y * 8 + x in board else '⬜' if y % 2 == x % 2 else '⬛'
        output += ' ' + str(8 - y) + '\n'
    
    output += '  A B C D E F G H\n'

    sys.stdout.write("\x1b[1A\x1b[2K" * 14)
    sys.stdout.write(output)

# Check if Position Vulnerable
def check(c = None):
    if c == None:
        pieces = {value:key for key, value in [black, white][turn].items()}
        c = pieces[['♔', '♚'][turn]]

    for q in valid_moves(not turn, check_ = True):
        if q[1] == c:
            return True

    return False

# Return all Valid Moves
def valid_moves(turn, check_ = False):
    pieces = [black, white][turn]
    not_pieces = [black, white][not turn]

    for q in pieces:
        # King
        if pieces[q] in '♔♚':
            # Castle
            if not check_:
                if not moved[[4, 60][turn]]:
                    # Right
                    if not moved[[7, 63][turn]] and not any(w[turn] in {**black, **white} for w in [[5, 61], [6, 62]]):
                        if not any(check(w[turn]) for w in [[4, 60], [5, 61], [6, 62]]):
                            yield [q, q + 2]

                    # Left
                    if not moved[[0, 56][turn]] and not any(w[turn] in {**black, **white} for w in [[1, 57], [2, 58], [3, 59]]):
                        if not any(check(w[turn]) for w in [[4, 60], [3, 59], [2, 58]]):
                            yield [q, q - 2]
            # Left
            if q % 8 and q - 1 not in pieces:
                yield [q, q - 1]
            
            # Up Left
            if q % 8 and q > 7 and q - 9 not in pieces:
                yield [q, q - 9]

            # Up
            if q > 7 and q - 8 not in pieces:
                yield [q, q - 8]

            # Up Right
            if q > 7 and q % 8 != 7 and q - 7 not in pieces:
                yield [q, q - 7]

            # Right
            if q % 8 != 7 and q + 1 not in pieces:
                yield [q, q + 1]

            # Right Down
            if q % 8 != 7 and q < 56 and q + 9 not in pieces:
                yield [q, q + 9]

            # Down
            if q < 56 and q + 8 not in pieces:
                yield [q, q + 8]

            # Down Left
            if q < 56 and q % 8 and q + 7 not in pieces:
                yield [q, q + 7]
        
        # Queen
        elif pieces[q] in '♕♛':
            # Left
            q2 = q
            while (q2 % 8 and q2 - 1 not in pieces and q2 not in not_pieces):
                yield [q, q2 - 1]
                q2 -= 1
            
            # Up Left
            q2 = q
            while (q2 % 8 and q2 > 7 and q2 - 9 not in pieces and q2 not in not_pieces):
                yield [q, q2 - 9]
                q2 -= 9
            
            # Up
            q2 = q
            while (q2 > 7 and q2 - 8 not in pieces and q2 not in not_pieces):
                yield [q, q2 - 8]
                q2 -= 8

            # Up Right
            q2 = q
            while (q2 > 7 and q2 % 8 != 7 and q2 - 7 not in pieces and q2 not in not_pieces):
                yield [q, q2 - 7]
                q2 -= 7

            # Right
            q2 = q
            while (q2 % 8 != 7 and q2 + 1 not in pieces and q2 not in not_pieces):
                yield [q, q2 + 1]
                q2 += 1

            # Right Down
            q2 = q
            while (q2 % 8 != 7 and q2 < 56 and q2 + 9 not in pieces and q2 not in not_pieces):
                yield [q, q2 + 9]
                q2 += 9
                
            # Down
            q2 = q
            while (q2 < 56 and q2 + 8 not in pieces and q2 not in not_pieces):
                yield [q, q2 + 8]
                q2 += 8

            # Down Left
            q2 = q
            while (q2 < 56 and q2 % 8 and q2 + 7 not in pieces and q2 not in not_pieces):
                yield [q, q2 + 7]
                q2 += 7

        # Rook
        elif pieces[q] in '♖♜':
            # Left
            q2 = q
            while (q2 % 8 and q2 - 1 not in pieces and q2 not in not_pieces):
                yield [q, q2 - 1]
                q2 -= 1

            # Up
            q2 = q
            while (q2 > 7 and q2 - 8 not in pieces and q2 not in not_pieces):
                yield [q, q2 - 8]
                q2 -= 8

            # Right
            q2 = q
            while (q2 % 8 != 7 and q2 + 1 not in pieces and q2 not in not_pieces):
                yield [q, q2 + 1]
                q2 += 1

            # Down
            q2 = q
            while (q2 < 56 and q2 + 8 not in pieces and q2 not in not_pieces):
                yield [q, q2 + 8]
                q2 += 8
        
        # Bishop
        elif pieces[q] in '♗♝':
            # Up Left
            q2 = q
            while (q2 % 8 and q2 > 7 and q2 - 9 not in pieces and q2 not in not_pieces):
                yield [q, q2 - 9]
                q2 -= 9

            # Up Right
            q2 = q
            while (q2 > 7 and q2 % 8 != 7 and q2 - 7 not in pieces and q2 not in not_pieces):
                yield [q, q2 - 7]
                q2 -= 7

            # Right Down
            q2 = q
            while (q2 % 8 != 7 and q2 < 56 and q2 + 9 not in pieces and q2 not in not_pieces):
                yield [q, q2 + 9]
                q2 += 9

            # Down Left
            q2 = q
            while (q2 < 56 and q2 % 8 and q2 + 7 not in pieces and q2 not in not_pieces):
                yield [q, q2 + 7]
                q2 += 7

        # Knight
        elif pieces[q] in '♘♞':
            # -1, 2
            if q > 15 and q % 8 and q - 17 not in pieces:
                yield [q, q - 17]
            
            # 1, 2
            if q > 15 and q % 8 != 7 and q - 15 not in pieces:
                yield [q, q - 15]

            # -2, 1
            if q > 7 and q % 8 > 1 and q - 10 not in pieces:
                yield [q, q  - 10]

            # 2, 1
            if q > 7 and q % 8 < 6 and q - 6 not in pieces:
                yield [q, q - 6]

            # -2, -1
            if q < 56 and q % 8 > 1 and q + 6 not in pieces:
                yield [q, q + 6]

            # 2, -1
            if q < 56 and q % 8 < 6 and q + 10 not in pieces:
                yield [q, q + 10]

            # -1, -2
            if q < 48 and q % 8 and q + 15 not in pieces:
                yield [q, q + 15]

            # 1, -2
            if q < 48 and q % 8 != 7 and q + 17 not in pieces:
                yield [q, q + 17]

        # Pawn
        elif pieces[q] in '♙♟':
            # Up
            if [q + 8, q - 8][turn] not in {**pieces, **not_pieces}:
                yield [q, [q + 8, q - 8][turn]]
                
                # Up Two
                if [q + 16, q - 16][turn] not in {**pieces, **not_pieces} and not moved[q]:
                    yield [q, [q + 16, q - 16][turn]]
            
            # Right Capture
            if q % 8 != 7:
                if [q + 9, q - 7][turn] in not_pieces or en_passent == q + 1:
                    yield [q, [q + 9, q - 7][turn]]

            # Left Capture
            if q % 8:
                if [q + 7, q - 9][turn] in not_pieces or en_passent == q - 1:
                    yield [q, [q + 7, q - 9][turn]]

# Convert Chess Notation to Grid Number
def convert(c):
    return ord(c[0]) - ord('A') + (8 - int(c[1])) * 8

# Play
while True:
    show()

    # Take Input
    c1, c2 = input(), input() 
    if not (c1[0].isupper() and c1[1].isdigit() and c2[0].isupper() and c2[1].isdigit() and len(c1) == len(c2) == 2):
        print('Invalid Notation')
        sleep(1.5)
        continue

    # Chess Notation to Index
    c1, c2 = convert(c1), convert(c2)

    # In Case of Invalid Move
    tempb, tempw = black.copy(), white.copy()

    # If Move is Valid
    if [c1, c2] in valid_moves(turn):
        # If Take Piece: Remove Piece from Dict
        if c2 in [black, white][not turn]:
            del [black, white][not turn][c2]

        # Else If Piece is Pawn and Moved Diagonally: Take Piece (En Passent)
        elif [black, white][turn][c1] in '♙♟' and abs(c2 - c1) in [7, 9]:
            if c2 - c1 == [7, -9][turn]:
                del [black, white][not turn][c1 - 1]
            
            if c2 - c1 == [9, -7][turn]:
                del [black, white][not turn][c1 + 1]

        # Move Piece
        [black, white][turn][c2] = [black, white][turn][c1]
        del [black, white][turn][c1]

        # Clear En Passent
        en_passent = -1
        if [black, white][turn][c2] in '♙♟':
            # Pawn Promotion
            if [c2 > 55, c2 < 8][turn]:
                [black, white][turn][c2] = ['♕', '♛'][turn]

            # En Passent
            if abs(c2 - c1) == 16:
                en_passent = c2
        
        # Castling
        if [black, white][turn][c2] in '♔♚' and abs(c2 - c1) == 2:
            if c2 == [6, 62][turn]:
                [black, white][turn][[5, 61][turn]] = [black, white][turn][[7, 63][turn]]
                del [black, white][turn][[7, 63][turn]]
            elif c2 == [2, 58][turn]:
                [black, white][turn][[3, 59][turn]] = [black, white][turn][[0, 56][turn]]
                del [black, white][turn][[0, 56][turn]]
        moved[c2] = 1

        if check():
            print("You're in Check!")
            sleep(1.5)
            black, white = tempb, tempw
            continue

        # Next Turn
        turn = not turn

    else:
        print('Invalid move!')
        sleep(1.5)