import pygame
import chess
import os

# --- 1. Configuration Constants ---
SQUARE_SIZE = 80
BOARD_SIZE = SQUARE_SIZE * 8
SCREEN_WIDTH = BOARD_SIZE + 200  # Extra space for a side panel
SCREEN_HEIGHT = BOARD_SIZE
FPS = 60

# --- 2. Pygame Initialization ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cool Python Chess")
clock = pygame.time.Clock()

# --- 3. Asset Loading ---

# Define the expected piece names based on python-chess symbols
PIECE_IMAGE_KEYS = {
    'p': 'bP', 'n': 'bN', 'b': 'bB', 'r': 'bR', 'q': 'bQ', 'k': 'bK',
    'P': 'wP', 'N': 'wN', 'B': 'wB', 'R': 'wR', 'Q': 'wQ', 'K': 'wK'
}

def load_pieces():
    """Loads and scales all piece images."""
    pieces = {}
    
    # Check if 'assets' folder exists
    if not os.path.isdir('assets'):
        print("Error: 'assets' folder not found.")
        print("Please create an 'assets' folder with images (wP.png, bK.png, etc.).")
        # Use a dummy placeholder if no assets found to prevent crash
        for name in PIECE_IMAGE_KEYS.values():
            pieces[name] = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
            pieces[name].fill((150, 150, 150))
        return pieces

    for key, name in PIECE_IMAGE_KEYS.items():
        try:
            img_path = os.path.join("assets", f"{name}.png")
            img = pygame.image.load(img_path).convert_alpha()
            pieces[name] = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))
        except pygame.error:
            print(f"Warning: Could not load image {name}.png from assets folder.")
            # Placeholder for missing image
            pieces[name] = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
            pieces[name].fill((200, 0, 0)) # Red box for missing asset
            
    return pieces

PIECES = load_pieces()

# --- 4. Drawing Functions ---

def draw_board(screen, board):
    """Draws the chessboard background and pieces based on the current state."""
    
    # Define colors
    LIGHT_SQUARE_COLOR = (240, 217, 181)
    DARK_SQUARE_COLOR = (181, 136, 99)

    for row in range(8):
        for col in range(8):
            color = LIGHT_SQUARE_COLOR if (row + col) % 2 == 0 else DARK_SQUARE_COLOR
            
            # Draw the square
            pygame.draw.rect(screen, color, 
                             (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            
            # Get the chess square index (0 to 63)
            square_index = chess.square(col, 7 - row)
            piece = board.piece_at(square_index)
            
            if piece:
                # Get the single character symbol (p, N, k, Q, etc.)
                symbol = piece.symbol()
                # Use the mapping to get the image key (bP, wN, wK, wQ, etc.)
                image_key = PIECE_IMAGE_KEYS.get(symbol)
                
                if image_key and image_key in PIECES:
                    screen.blit(PIECES[image_key], (col * SQUARE_SIZE, row * SQUARE_SIZE))

def highlight_square(screen, col, row, color):
    """Draws a semi-transparent overlay on a specific square."""
    s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
    s.fill(color)
    screen.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))

# --- 5. Main Game Loop ---

def main():
    game_board = chess.Board()
    running = True
    
    # Stores (col, row) of the selected square in Pygame coordinates
    selected_square_coords = None 
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # --- Handle Mouse Click ---
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Left click
                x, y = event.pos
                col = x // SQUARE_SIZE
                row = y // SQUARE_SIZE
                
                # Ensure click is within the board boundaries
                if 0 <= col < 8 and 0 <= row < 8:
                    clicked_coords = (col, row)
                    
                    # Convert Pygame coordinates (col, row) to chess square name (e.g., e2)
                    # Note: Pygame row 0 is top (rank 8), row 7 is bottom (rank 1)
                    chess_square_name = chess.square_name(chess.square(col, 7 - row))
                    
                    if selected_square_coords:
                        # --- Second Click: Attempt to make a move ---
                        start_col, start_row = selected_square_coords
                        start_square_name = chess.square_name(chess.square(start_col, 7 - start_row))
                        
                        move_uci = start_square_name + chess_square_name
                        
                        try:
                            move = chess.Move.from_uci(move_uci)
                            
                            # Simple promotion fix (assumes Q promotion for now)
                            if game_board.piece_at(move.from_square).piece_type == chess.PAWN and \
                               (chess.square_rank(move.to_square) == 7 or chess.square_rank(move.to_square) == 0):
                                move_uci += 'q' # Add queen promotion
                                move = chess.Move.from_uci(move_uci)

                            if move in game_board.legal_moves:
                                game_board.push(move)
                            
                        except ValueError:
                            pass # Not a valid UCI move
                        
                        selected_square_coords = None # Reset selection
                        
                    else:
                        # --- First Click: Select a piece ---
                        piece = game_board.piece_at(chess.parse_square(chess_square_name))
                        
                        # Only select if it's a piece belonging to the current player's turn
                        if piece and piece.color == game_board.turn:
                            selected_square_coords = clicked_coords
        
        # --- Drawing ---
        screen.fill((40, 40, 40)) # Dark background for the rest of the screen
        draw_board(screen, game_board)
        
        # Highlight the selected square
        if selected_square_coords:
            highlight_square(screen, 
                             selected_square_coords[0], 
                             selected_square_coords[1], 
                             (255, 255, 0, 150)) # Yellow transparent highlight

        # Display game status (in the side panel area)
        font = pygame.font.Font(None, 36)
        status_text = "Turn: " + ("White" if game_board.turn == chess.WHITE else "Black")
        
        if game_board.is_checkmate():
            status_text = "CHECKMATE! " + ("Black Wins" if game_board.turn == chess.WHITE else "White Wins")
        elif game_board.is_stalemate():
            status_text = "STALEMATE (Draw)"
        elif game_board.is_check():
            status_text += " (CHECK)"

        text_surface = font.render(status_text, True, (255, 255, 255))
        screen.blit(text_surface, (BOARD_SIZE + 20, 20))


        # --- Update Display ---
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()