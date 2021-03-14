import numpy as np
import pygame, sys
import socket
import threading

HOST = '127.0.0.1' #please change accordingly
PORT = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((HOST,PORT))
s.connect((HOST,PORT))

def create_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True  #if shut down then will close the thread
    thread.start()

def receive_data():
    while True:
        data = s.recv(1024).decode()
        print(data)

create_thread(receive_data)

pygame.init()

width = 722
height = 730
size = (width, height)
clock = pygame.time.Clock()
bg_surface = pygame.image.load('assets/final-board.png')
red_token = pygame.image.load('assets/red-token.png')
hit_sound =  pygame.mixer.Sound('sound-effect/hit-sound.mp3')
victory_sound = pygame.mixer.Sound('sound-effect/victory.mp3')
pygame.display.set_caption("ConnectFour")

RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

def completeGame():
    return 0


def create_board():
    board = np.zeros((6, 7))
    return board

board = create_board()
game_over = False
turn = 0

def insert(n, piece):
    for x in range(len(board) - 1, -1, -1):
        if (board[x][n - 1] == 0):
            board[x][n - 1] = piece
            break

def check_win(piece, board):
    status = False
    # check horizontal
    for x in range(len(board)):
        for y in range(3):
            if (board[x][y] == piece and board[x][y + 1] == piece and board[x][y + 2] == piece and board[x][
                y + 3] == piece):
                status = True
                break
    # check vertical
    for x in range(3):
        for y in range(len(board)):
            if (board[x][y] == piece and board[x + 1][y] == piece and board[x + 2][y] == piece and board[x + 3][
                y] == piece):
                status = True
                break
    # check positive slope
    for x in range(3, len(board), 1):
        for y in range(4):
            if (board[x][y] == piece and board[x - 1][y + 1] == piece and board[x - 2][y + 2] == piece and board[x - 3][
                y + 3] == piece):
                status = True
                break
    # check negative slope
    for x in range(3, len(board), 1):
        for y in range(3, 7, 1):
            if (board[x][y] == piece and board[x - 1][y - 1] == piece and board[x - 2][y - 2] == piece and board[x - 3][
                y - 3] == piece):
                status = True
                break
    return status

def is_valid_location(selection,board):
    return board[0][selection-1] == 0

def get_selection(pos_x):
    if pos_x <= 107:
        return 1
    elif pos_x > 107 and pos_x <= 207:
        return 2
    elif pos_x > 207 and pos_x <= 307:
        return 3
    elif pos_x > 307 and pos_x <= 407:
        return 4
    elif pos_x > 407 and pos_x <= 507:
        return 5
    elif pos_x > 507 and pos_x <= 607:
        return 6
    else:
        return 7

def draw_circle(board):
    for c in range(7):
        for r in range(6):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (c * 100 + 56, r * 100 + 163), 40)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (c * 100 + 56, r * 100 + 163), 40)
    pygame.display.update()

def follow_cursor(turn, board):
    for c in range(7):
        for r in range(6):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (c * 100 + 56, r * 100 + 163), 40)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (c * 100 + 56, r * 100 + 163), 40)
    pos_x = pygame.mouse.get_pos()[0]
    if turn == 0:
        pygame.draw.circle(screen, RED, (pos_x, 63), 40)
    else:
        pygame.draw.circle(screen, YELLOW, (pos_x, 63), 40)
    pygame.display.update()

screen = pygame.display.set_mode(size)
screen.fill('white')
screen.blit(bg_surface, (0, 108))
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            if not game_over:
                follow_cursor(turn,board)
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            if turn == 0:
                pos_x = pygame.mouse.get_pos()[0]
                selection = get_selection(pos_x)
                send_data = str(selection).encode()
                s.send(send_data)
                if(is_valid_location(selection, board)):
                    hit_sound.play()
                    insert(selection, 1)
                    if (check_win(1, board)):
                        victory_sound.play()
                        game_over = True
                        board = create_board()
                        print("Player 1 wins")
                else:
                    print("Please try again!")
                    continue

            else:
                pos_x = pygame.mouse.get_pos()[0]
                selection = get_selection(pos_x)
                if (is_valid_location(selection, board)):
                    insert(selection, 2)
                    hit_sound.play()
                    if (check_win(2, board)):
                        victory_sound.play()
                        game_over = True
                        board = create_board()
                        print("Player 2 wins")
                else:
                    print("Please try again!")
                    continue


            draw_circle(board)
            turn += 1
            turn = turn % 2

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over == True:
                    board = create_board()
                    game_over = False


            draw_circle(board)
            screen.fill('white')
            screen.blit(bg_surface, (0, 108))
            clock.tick(60)



        screen.fill('white')
        screen.blit(bg_surface, (0, 108))
        clock.tick(60)