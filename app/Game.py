import pygame
import os
import time
import random


class Game:
    def __init__(self, size, caption, icon_path):
        """Initialize the Rock Paper Scissors game.
        
        Args:
            size: Tuple of (width, height) for the game window
            caption: String to display in the window title bar
            icon_path: Path to the window icon image
        """
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption(caption)

        # Configure keyboard input - 200ms initial delay, 25ms repeat interval
        pygame.key.set_repeat(200, 25)

        # Load and set the window icon from the provided path
        icon = pygame.image.load(icon_path)
        pygame.display.set_icon(icon)

        # Initialize default system font at size 36 for all game text
        self.font = pygame.font.Font(None, 36)

        # Load game assets and setup display rectangles
        self.init_imgs()
        self.init_rects()

        # Setup animation timing - used for shuffling computer's hand
        self.prev_time = time.time()
        self.shuffling_hand = True

        self.top_instruction = "Choose your move:"
        self.bottom_instruction = "Press R, P, or S to play"

        # Initialize choices and scores
        self.computer_ch = 0
        self.player_ch = 0
        self.computer_score = 0
        self.player_score = 0

        self.computer_wins = (
            (0, 2),
            (1, 0),
            (2, 1)
        )
        self.player_wins = (
            (2, 0),
            (0, 1),
            (1, 2)
        )

    
    def init_imgs(self):
        """Load and prepare all game images.
        
        Loads rock, paper, and scissors images from the res directory
        and scales them to 100x100 pixels for consistent display.
        """
        # Load and scale hand gesture images
        self.rock_image = pygame.image.load(os.path.join("res", "rock.png"))
        self.rock_image = pygame.transform.scale(self.rock_image, (100, 100))

        self.paper_image = pygame.image.load(os.path.join("res", "paper.png"))
        self.paper_image = pygame.transform.scale(self.paper_image, (100, 100))

        self.scissors_image = pygame.image.load(os.path.join("res", "scissors.png"))
        self.scissors_image = pygame.transform.scale(self.scissors_image, (100, 100))
    

    def init_rects(self):
        """Initialize and position all game rectangles.
        
        Creates rectangles for both computer (top) and player (bottom) hands.
        Positions them in the center of their respective screen halves:
        - Computer's hand at y=150 (top half)
        - Player's hand at y=450 (bottom half)
        All hands are centered horizontally at x=200.
        """
        # Create rectangles for computer's hand (top)
        self.rock_rect_top = self.rock_image.get_rect()
        self.paper_rect_top = self.paper_image.get_rect()
        self.scissors_rect_top = self.scissors_image.get_rect()

        # Create rectangles for player's hand (bottom)
        self.rock_rect_bottom = self.rock_image.get_rect()
        self.paper_rect_bottom = self.paper_image.get_rect()
        self.scissors_rect_bottom = self.scissors_image.get_rect()

        # Position computer's hand in top half (y=150)
        self.rock_rect_top.center = (200, 150)
        self.paper_rect_top.center = (200, 150)
        self.scissors_rect_top.center = (200, 150)

        # Position player's hand in bottom half (y=450)
        self.rock_rect_bottom.center = (200, 450)
        self.paper_rect_bottom.center = (200, 450)
        self.scissors_rect_bottom.center = (200, 450)

    
    # Render function
    def render(self):
        # Clear the screen with a dark background
        self.screen.fill((20, 20, 20))

        # Render the text and scores
        text_computer = self.font.render("Computer", True, (255, 255, 255))
        text_player = self.font.render("Player", True, (255, 255, 255))
        text_computer_score = self.font.render(f"{self.computer_score}", True, (255, 255, 255))
        text_player_score = self.font.render(f"{self.player_score}", True, (255, 255, 255))
        
        # Get text rectangles for centering
        text_computer_rect = text_computer.get_rect(center=(200, 280))  # Computer text
        text_player_rect = text_player.get_rect(center=(200, 320))  # Player text
        text_computer_score_rect = text_computer_score.get_rect(center=(200, 240))  # Computer score above
        text_player_score_rect = text_player_score.get_rect(center=(200, 360))  # Player score below
        
        # Render additional instruction text
        text_top_instruction = self.font.render(self.top_instruction, True, (255, 255, 255))
        text_bottom_instruction = self.font.render(self.bottom_instruction, True, (255, 255, 255))
        
        # Position instruction text
        text_top_instruction_rect = text_top_instruction.get_rect(center=(200, 50))  # Above top image
        text_bottom_instruction_rect = text_bottom_instruction.get_rect(center=(200, 550))  # Below bottom image
        
        # Draw a white horizontal line in the middle
        pygame.draw.line(self.screen, (255, 255, 255), (0, 300), (400, 300), 2)
        
        # Draw all text elements
        self.screen.blit(text_top_instruction, text_top_instruction_rect)
        self.screen.blit(text_computer_score, text_computer_score_rect)
        self.screen.blit(text_computer, text_computer_rect)
        self.screen.blit(text_player, text_player_rect)
        self.screen.blit(text_player_score, text_player_score_rect)
        self.screen.blit(text_bottom_instruction, text_bottom_instruction_rect)
        
        # Draw computer hand
        if self.computer_ch == 0:
            self.screen.blit(self.rock_image, self.rock_rect_top)
        elif self.computer_ch == 1:
            self.screen.blit(self.paper_image, self.paper_rect_top)
        elif self.computer_ch == 2:
            self.screen.blit(self.scissors_image, self.scissors_rect_top)
            
        # Draw player hand
        if self.player_ch == 0:
            self.screen.blit(self.rock_image, self.rock_rect_bottom)
        elif self.player_ch == 1:
            self.screen.blit(self.paper_image, self.paper_rect_bottom)
        elif self.player_ch == 2:
            self.screen.blit(self.scissors_image, self.scissors_rect_bottom)
            
        # Update the display
        pygame.display.flip()

    
    # Shuffle hand
    def shuffle_hand(self):
        self.computer_ch += 1
        if self.computer_ch == 3:
            self.computer_ch = 0


    def random_choice(self):
        """Generate computer's move randomly.
        
        Randomly selects between:
        0 = Rock
        1 = Paper
        2 = Scissors
        """
        self.computer_ch = random.randint(0, 2)

    def score(self):
        """Calculate round result and update scores.
        
        Compares computer and player choices using predefined winning combinations.
        Updates scores and display messages based on the outcome.
        """
        ch_tuple = (self.computer_ch, self.player_ch)
        
        # Check win conditions and update scores
        if ch_tuple in self.computer_wins:
            self.computer_score += 1
            self.top_instruction = "Computer wins!"
        elif ch_tuple in self.player_wins:
            self.player_score += 1
            self.top_instruction = "You win!"
        else:
            self.top_instruction = "Draw!"

        # Update instruction for next round
        self.bottom_instruction = "Press any key to continue."


    def handle_keypress(self, key):
        """Handle keyboard input for game controls.
        
        During gameplay:
        - R key: Select Rock (0)
        - P key: Select Paper (1)
        - S key: Select Scissors (2)
        
        After round:
        - Any key: Start new round
        """
        if self.playing:
            # Handle move selection during gameplay
            if key == pygame.K_r:      # Rock
                self.player_ch = 0
                self.shuffling_hand = False
            elif key == pygame.K_p:    # Paper
                self.player_ch = 1
                self.shuffling_hand = False
            elif key == pygame.K_s:    # Scissors
                self.player_ch = 2
                self.shuffling_hand = False
            else:
                return  # Ignore other keys during gameplay

            # Process round end
            self.playing = False
            self.shuffling_hand = False
            self.random_choice()
            self.score()
        else:
            # Start new round
            self.playing = True
            self.shuffling_hand = True
            self.top_instruction = "Choose your move:"
            self.bottom_instruction = "Press R, P, or S to play"


    def loop(self):
        """Main game loop.
        
        Handles:
        - Event processing (quit signals and keyboard input)
        - Computer hand animation
        - Screen rendering
        
        The loop runs continuously until the game is quit.
        """
        # Process all pending events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                # Handle Alt+F4 for graceful exit
                if event.key == pygame.K_F4 and pygame.key.get_mods() & pygame.KMOD_ALT:
                    self.running = False
                else:
                    self.handle_keypress(event.key)

        # Animate computer's hand if shuffling
        current_time = time.time()
        if self.shuffling_hand and current_time - self.prev_time >= 0.2:
            self.shuffle_hand()
            self.prev_time = current_time

        # Update display
        self.render()


    def start_game(self):
        """Start and run the game.
        
        Initializes game state and enters the main game loop.
        Continues running until the game is quit, then performs cleanup.
        """
        self.running = True  # Controls the main game loop
        self.playing = True  # Controls the gameplay state
        while self.running:
            self.loop()
        self.quit_game()
    
    def quit_game(self):
        """Clean up and exit the game.
        
        Properly closes Pygame and releases system resources.
        """
        pygame.quit()

