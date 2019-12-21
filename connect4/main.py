import board
import graphics
import pygame
import pygame.gfxdraw
import pyoneer.animation
import pyoneer.interpolation
import random


def render():

    screen.fill((255, 255, 255))

    draw_pieces()
    draw_board()
    draw_select_box()

    draw_game_state()
    draw_fps()

    pygame.display.flip()


def draw_board():

    for i in range(1, 6):
        pygame.draw.line(screen, BLACK, (0, i*2*PIECE_RADIUS), (screen.get_width(), i*2*PIECE_RADIUS), 3)

    for j in range(1, 7):
        pygame.draw.line(screen, BLACK, (j*2*PIECE_RADIUS, 0), (j*2*PIECE_RADIUS, screen.get_height()), 3)


def draw_select_box():

    if current_column in b.available_columns:
        pygame.draw.rect(
            screen,
            RED if current_player == 1 else YELLOW,
            (current_column*2*PIECE_RADIUS, 0, 2*PIECE_RADIUS, screen.get_height()),
            5
        )


def draw_pieces():

    for piece in gfx_pieces:
        piece.draw(screen)


def draw_game_state():

    if game_state == board.Board.CONTINUE:
        return

    pygame.draw.rect(screen, WHITE, (screen.get_width()/2 - 175, screen.get_height()/2 - 80, 350, 160))
    pygame.draw.rect(screen, BLACK, (screen.get_width()/2 - 175, screen.get_height()/2 - 80, 350, 160), 4)

    win_text = FONT_60.render(
        "Player 1 wins" if game_state == board.Board.P_ONE_WIN else
        "Player 2 wins" if game_state == board.Board.P_TWO_WIN else
        "Stalemate",
        True,
        BLACK
    )
    restart_text = FONT_40.render(
        "Press space to restart",
        True,
        BLACK
    )
    screen.blit(
        win_text,
        (
            screen.get_width()/2 - win_text.get_width()/2,
            screen.get_height()/2 - win_text.get_height()/2 - 20
        )
    )
    screen.blit(
        restart_text,
        (
            screen.get_width()/2 - restart_text.get_width()/2,
            screen.get_height()/2 - restart_text.get_height()/2 + win_text.get_height()/2 + 20
        )
    )


def draw_fps():

    fps = FONT_20.render(str(int(CLOCK.get_fps())), True, BLACK)
    screen.blit(fps, (screen.get_width() - fps.get_width() - 10, 10))


def play_piece(col, callback=None, args=()):
    global current_player, gfx_pieces

    # Check if game is over
    if game_state != board.Board.CONTINUE:
        print("Game has concluded, will not play piece")        # TODO: FIX BUG WHERE AI WINS
        return

    if current_player == 1:  # Player 1 is red
        row = b.p_one_play(col)
        current_player = 2

    else:
        row = b.p_two_play(col)
        current_player = 1

    # Animation and graphics
    dest = (col * 2 * PIECE_RADIUS + PIECE_RADIUS, row * 2 * PIECE_RADIUS + PIECE_RADIUS)
    start = [dest[0], -PIECE_RADIUS]

    interpolator = pyoneer.interpolation.LinearInterpolator(PIECE_SPEED)
    anim = pyoneer.animation.Animation(start, dest, None, interpolator, lambda *_: callback(*args) if callback else lambda *_: print())
    service.add_animation(anim)

    # RED is player one but current_player is toggled first thing so the opposite must be checked
    gfx_pieces.append(graphics.GFXDisc(RED if current_player == 2 else YELLOW, anim))


def mainloop():
    global current_column, current_player, running, gfx_pieces, game_state

    while running:
        game_state = b.game_state
        delta = CLOCK.tick(FPS_CAP)
        service.update(delta)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

            elif e.type == pygame.MOUSEBUTTONDOWN:

                if b.game_state == board.Board.CONTINUE:
                    current_column = e.pos[0] // (2*PIECE_RADIUS)

                    if current_column in b.available_columns:
                        if current_player == 1:         # Player 1 is user, Player 2 is AI
                            print(random.choice(b.available_columns))
                            play_piece(current_column, callback=play_piece, args=(random.choice(b.available_columns),))


            elif e.type == pygame.MOUSEMOTION:
                current_column = e.pos[0] // (PIECE_RADIUS*2)

            elif e.type == pygame.KEYUP:

                if e.key == pygame.K_SPACE:
                    if game_state != board.Board.CONTINUE:

                        b.reset()
                        gfx_pieces = []
                        current_player = 1
                        game_state = board.Board.CONTINUE

        render()


if __name__ == "__main__":

    pygame.init()

    WHITE  = (255, 255, 255)
    BLACK  = (0,   0,   0)
    RED    = (225, 0,   0)
    YELLOW = (225, 225, 0)

    PIECE_RADIUS = 50

    FONT_20 = pygame.font.Font(None, 20)
    FONT_40 = pygame.font.Font(None, 40)
    FONT_60 = pygame.font.Font(None, 60)
    CLOCK = pygame.time.Clock()
    FPS_CAP = 120
    PIECE_SPEED = 1000

    screen = pygame.display.set_mode((7*2*PIECE_RADIUS, 6*2*PIECE_RADIUS))

    # Connect 4
    b = board.Board()
    current_column = 0
    current_player = 1
    game_state = board.Board.CONTINUE

    # Animations
    service = pyoneer.animation.AnimationService()
    gfx_pieces = []

    running = True
    mainloop()
