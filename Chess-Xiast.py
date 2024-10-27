#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pygame
import chess
import random

# Tahta boyutları
SQUARE_SIZE = 64
BOARD_SIZE = SQUARE_SIZE * 8  # 8 satır ve 8 sütun

# Pygame'i başlat
pygame.init()
pygame.font.init()  # Font sistemini başlat
screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
pygame.display.set_caption("Xiast Chess")

# Renk tanımlamaları
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Menü seçenekleri
menu_options = ["Yeni Oyun", "Çıkış"]

# Taş görsellerini saklayacak sözlük
piece_images = {}

# Resim yükleme ve boyutlandırma fonksiyonu
def load_and_scale_image(file_path):
    image = pygame.image.load(file_path)
    return pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))

# Taş görsellerini bir kez yükleyip saklama fonksiyonu
def load_images():
    for piece_type in [chess.PAWN, chess.ROOK, chess.KNIGHT, chess.BISHOP, chess.QUEEN, chess.KING]:
        for color in [chess.WHITE, chess.BLACK]:
            piece = chess.Piece(piece_type, color)
            image_name = get_piece_image_name(piece)
            piece_images[piece.symbol()] = load_and_scale_image(f"pieces/{image_name}")

# Taş resim isimlerini döndür
def get_piece_image_name(piece):
    piece_dict = {
        chess.PAWN: 'P',
        chess.ROOK: 'R',
        chess.KNIGHT: 'N',
        chess.BISHOP: 'B',
        chess.QUEEN: 'Q',
        chess.KING: 'K'
    }
    return f"{'w' if piece.color == chess.WHITE else 'b'}{piece_dict[piece.piece_type]}.png"

# Tahtayı çizme fonksiyonu
def draw_board(board, selected_square=None):
    for i in range(8):
        for j in range(8):
            square_color = WHITE if (i + j) % 2 == 0 else (125, 135, 150)
            pygame.draw.rect(screen, square_color, (j * SQUARE_SIZE, i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            piece_position = board.piece_at(chess.square(j, 7 - i))
            if piece_position is not None:
                piece_symbol = piece_position.symbol()
                piece_image = piece_images.get(piece_symbol)
                if piece_image:
                    screen.blit(piece_image, (j * SQUARE_SIZE, i * SQUARE_SIZE))
    
    # Seçilen kareyi vurgulama
    if selected_square is not None:
        selected_col = chess.square_file(selected_square)
        selected_row = 7 - chess.square_rank(selected_square)
        pygame.draw.rect(screen, GREEN, (selected_col * SQUARE_SIZE, selected_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)

# Taş hareket ettirme fonksiyonu
def move_piece(board, start_square, end_square):
    move = chess.Move(start_square, end_square)
    if move in board.legal_moves:
        board.push(move)
        return True
    else:
        print("Geçersiz hamle!")
        return False

# Kazanan rengi gösterme fonksiyonu
def show_winner(winner_color):
    font = pygame.font.Font(None, 74)
    text = font.render(f"{'Beyaz' if winner_color == chess.WHITE else 'Siyah'} kazandı!", True, GREEN)
    screen.blit(text, (BOARD_SIZE // 2 - text.get_width() // 2, BOARD_SIZE // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)  # Mesajı ekranda 3 saniye göster

# Menü ekranını çizme fonksiyonu
def draw_menu(selected_option):
    screen.fill(WHITE)
    font = pygame.font.Font(None, 74)
    title_text = font.render("Satranç Oyunu", True, BLACK)
    screen.blit(title_text, (BOARD_SIZE // 2 - title_text.get_width() // 2, BOARD_SIZE // 4))

    for i, option in enumerate(menu_options):
        option_text = font.render(option, True, WHITE)
        option_rect = option_text.get_rect(center=(BOARD_SIZE // 2, BOARD_SIZE // 2 + i * 100))
        background_color = (0, 0, 255) if selected_option == i else (255, 165, 0)
        pygame.draw.rect(screen, background_color, option_rect.inflate(20, 20), border_radius=10)
        screen.blit(option_text, option_rect)

# Menü seçim fonksiyonu
def menu_selection(pos):
    for i, option in enumerate(menu_options):
        option_rect = pygame.Rect(0, 0, 0, 0)
        option_text = pygame.font.Font(None, 74).render(option, True, BLACK)
        option_rect = option_text.get_rect(center=(BOARD_SIZE // 2, BOARD_SIZE // 2 + i * 100))
        if option_rect.collidepoint(pos):
            return i
    return -1

# Ana oyun döngüsü
def main():
    load_images()  # Taş görsellerini yükle
    running = True
    selected_option = 0
    while running:
        draw_menu(selected_option)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        play_game()
                    elif selected_option == 1:
                        running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked_option = menu_selection(pos)
                if clicked_option != -1:
                    if clicked_option == 0:
                        play_game()
                    elif clicked_option == 1:
                        running = False

    pygame.quit()

# Basit bir yapay zeka ile siyahın hamlesini yapma fonksiyonu
def ai_move(board):
    legal_moves = list(board.legal_moves)
    if legal_moves:
        move = random.choice(legal_moves)
        board.push(move)

# Oyun oynama fonksiyonu
def play_game():
    board = chess.Board()
    selected_square = None
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                col = mouse_x // SQUARE_SIZE
                row = 7 - (mouse_y // SQUARE_SIZE)
                clicked_square = chess.square(col, row)

                if selected_square is None:
                    piece = board.piece_at(clicked_square)
                    if piece is not None and piece.color == chess.WHITE:
                        selected_square = clicked_square
                else:
                    if move_piece(board, selected_square, clicked_square):
                        selected_square = None
                        if not board.is_game_over():
                            ai_move(board)
                    else:
                        selected_square = None

        screen.fill(WHITE)
        draw_board(board, selected_square)

        if board.is_checkmate():
            winner_color = not board.turn
            show_winner(winner_color)
            running = False

        pygame.display.flip()

if __name__ == "__main__":
    main()


# In[ ]:




