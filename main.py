import pygame

pygame.init()
WIDTH = 800
HEIGHT = 500
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("BlackKnight Puzzle")
pygame.font.Font("build/web/assets/NightPumpkind-1GpGv.ttf", 20)
small_font = pygame.font.Font("build/web/assets/Blacknorthdemo-mLE25.ttf", 20)
big_font = pygame.font.Font("build/web/assets/Blacknorthdemo-mLE25.ttf", 60)
timer = pygame.time.Clock()
fps = 60

# Game variables and images
white_pieces = ['bishop', 'bishop', 'bishop', 'bishop', 'rook', 'knight','knight','knight','knight', 'rook', 'rook', 'rook']
white_locations = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0),
                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (4,2)]
black_pieces = ['knight']
black_locations = [(0, 0)]
selection = 100
valid_moves = []
move_count = 0  # New variable to track number of moves

black_knight = pygame.image.load('build/web/assets/images/black knight.png')
black_knight = pygame.transform.scale(black_knight, (80, 80))
white_rook = pygame.image.load('build/web/assets/images/white rook.png')
white_rook = pygame.transform.scale(white_rook, (80, 80))
white_knight = pygame.image.load('build/web/assets/images/white knight.png')
white_knight = pygame.transform.scale(white_knight, (80, 80))
white_bishop = pygame.image.load('build/web/assets/images/white bishop.png')
white_bishop = pygame.transform.scale(white_bishop, (80, 80))

white_images = [white_knight, white_bishop,  white_rook]
black_images = [black_knight]
piece_list = ['knight','bishop', 'rook']

def draw_board():
    for i in range(9):
        column = i % 4
        row = i // 4
        pygame.draw.rect(screen, 'light blue', [500, 200, 100, 100])
        if row % 2 == 0:
            pygame.draw.rect(screen, 'light gray', [400 - (column * 200), row * 100, 100, 100])
        else:
            pygame.draw.rect(screen, 'light gray', [500 - (column * 200), row * 100, 100, 100])
    pygame.draw.rect(screen, 'gray', [0, 300, WIDTH - 200, 100])
    pygame.draw.rect(screen, 'gold', [0, 300, WIDTH - 200, 100], 5)
    screen.blit(big_font.render('Black Knight:', True, 'black'), (0, 230))
    screen.blit(small_font.render('Use standard chess movements to get the Black Knight to', True, 'black'), (20, 320))
    screen.blit(small_font.render('the light blue square!! (CAPTURES NOT ALLOWED, NO COLOR TURNS).', True, 'black'), (20, 340))
    screen.blit(small_font.render(f'Moves: {move_count}', True, 'black'), (650, 20))  # Display move count
    for i in range(7):
        pygame.draw.line(screen, 'black', (0, 100 * i), (600, 100 * i), 2)
        pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i, 200), 2)
    pygame.draw.line(screen, 'black', (400, 0), (400, 300), 2)
    pygame.draw.line(screen, 'black', (500, 0), (500, 300), 2)
    pygame.draw.line(screen, 'black', (600, 0), (600, 300), 2)
    pygame.draw.line(screen, 'black', (600, 0), (600, 400), 2)

def draw_pieces():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        screen.blit(white_images[index], (white_locations[i][0] * 100 + 10, white_locations[i][1] * 100 + 10))
        if selection == i:
            pygame.draw.rect(screen, 'red', [white_locations[i][0] * 100 + 1, white_locations[i][1] * 100 + 1, 100, 100], 2)
    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        screen.blit(black_images[index], (black_locations[i][0] * 100 + 10, black_locations[i][1] * 100 + 10))
        if selection == i + len(white_pieces):
            pygame.draw.rect(screen, 'blue', [black_locations[i][0] * 100 + 1, black_locations[i][1] * 100 + 1, 100, 100], 2)

def draw_play_again_button():
    pygame.draw.rect(screen, 'red', [650, 400, 120, 50])  # Draw button rectangle
    screen.blit(small_font.render('Play  Again', True, 'black'), (660, 415))  # Draw button text

def reset_game():
    global white_locations, black_locations, move_count, winner
    white_locations = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0),
                       (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (4,2)]
    black_locations = [(0, 0)]
    move_count = 0
    winner = ""

def check_options(piece, location):
    moves_list = []
    if piece == 'knight':
        moves_list = check_knight(location)
    elif piece == 'bishop':
        moves_list = check_bishop(location)
    elif piece == 'rook':
        moves_list = check_rook(location)
    return moves_list

def check_knight(position):
    moves_list = []
    targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if is_on_board(target) and target not in white_locations and target not in black_locations:
            moves_list.append(target)
    return moves_list

def check_rook(position):
    moves_list = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for direction in directions:
        for i in range(1, 6):
            target = (position[0] + direction[0] * i, position[1] + direction[1] * i)
            if not is_on_board(target) or target in white_locations or target in black_locations:
                break
            moves_list.append(target)
    return moves_list

def check_bishop(position):
    moves_list = []
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    for direction in directions:
        for i in range(1, 6):
            target = (position[0] + direction[0] * i, position[1] + direction[1] * i)
            if not is_on_board(target) or target in white_locations or target in black_locations:
                break
            moves_list.append(target)
    return moves_list

def is_on_board(position):
    if position[1] < 2:
        return 0 <= position[0] <= 5
    elif position[1] == 2:
        return 4 <= position[0] <= 5
    return False

def draw_valid(valid_moves):
    for move in valid_moves:
        pygame.draw.circle(screen, 'red', (move[0] * 100 + 50, move[1] * 100 + 50), 10)

# Main game loop
run = True
winner = ""
while run:
    timer.tick(fps)
    screen.fill('dark gray')
    draw_board()
    draw_pieces()
    draw_play_again_button()
    
    if selection != 100 and winner == "":
        if selection < len(white_pieces):
            valid_moves = check_options(white_pieces[selection], white_locations[selection])
        else:
            valid_moves = check_options(black_pieces[0], black_locations[0])
        draw_valid(valid_moves)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if the "Play Again" button is clicked, reset game regardless of winner status
            if 650 <= event.pos[0] <= 770 and 400 <= event.pos[1] <= 450:
                reset_game()  # Reset game when "Play Again" is clicked
                winner = ""   # Clear the winner
            
            if winner == "":  # Only handle piece movement if there is no winner
                x_coord = event.pos[0] // 100
                y_coord = event.pos[1] // 100
                click_coords = (x_coord, y_coord)
                
                if click_coords in white_locations:
                    selection = white_locations.index(click_coords)
                elif click_coords in black_locations:
                    selection = black_locations.index(click_coords) + len(white_pieces)
                elif selection != 100 and click_coords in valid_moves:
                    if selection < len(white_pieces):
                        white_locations[selection] = click_coords
                    else:
                        black_locations[selection - len(white_pieces)] = click_coords

                        # Check win condition
                        if black_locations[0] == (5, 2):
                            winner = f"Black Knight wins in {move_count} moves!"
                    
                    move_count += 1  # Increment move count
                    selection = 100
                    valid_moves = []
                else:
                    selection = 100
                    valid_moves = []

    # Display the winner if there is one
    if winner:
        screen.blit(big_font.render(winner, True, 'gold'), (0, 430))

    pygame.display.flip()

pygame.quit()