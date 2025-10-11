import pygame
import sys
import time
import random

from HandSprite import HandSprite
from utils import resource_path


class Game:
    """Main game class for Rock Paper Scissors.
    
    This class manages the entire game including window setup, sprite management,
    user input handling, game logic, sound effects, and display rendering.
    The game supports both mouse and keyboard controls, features animated
    computer moves, and keeps track of player and computer scores.
    """

    def __init__(self, size, caption, icon_path):
        """Initialize the Rock Paper Scissors game.
        
        Sets up the game window, loads resources, initializes sprites and sound effects,
        and prepares the initial game state.
        
        Args:
            size (tuple): Window dimensions as (width, height)
            caption (str): Text to display in the window title bar
            icon_path (str): Path to the window icon image file
        
        Attributes initialized:
            screen: Main display surface
            font: Game text font
            clock: Frame rate controller
            computer_score, player_score: Game scores
            playing: Current game state
            shuffling_hand: Computer animation state
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

        # Initialize game clock for controlling frame rate
        self.clock = pygame.time.Clock()

        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.computer_hand = pygame.sprite.GroupSingle()
        self.player_hands = pygame.sprite.Group()

        # Load game assets and setup sprites
        self.init_imgs()
        self.init_sprites()
        self.init_sfx()

        # Setup animation timing - used for shuffling computer's hand
        self.prev_time = time.time()
        self.shuffling_hand = True

        self.top_instruction = "Choose your move:"
        self.bottom_instruction = "Click on an image to play"

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
        self.rock_image = pygame.image.load(resource_path("res/rock.png"))
        self.rock_image = pygame.transform.scale(self.rock_image, (100, 100))

        self.paper_image = pygame.image.load(resource_path("res/paper.png"))
        self.paper_image = pygame.transform.scale(self.paper_image, (100, 100))

        self.scissors_image = pygame.image.load(resource_path("res/scissors.png"))
        self.scissors_image = pygame.transform.scale(self.scissors_image, (100, 100))
    

    def init_sprites(self):
        """Initialize and position all game sprites.
        
        Creates sprite objects for both computer (top) and player (bottom) hands.
        Positions them in their respective screen positions:
        - Computer's hand at y=150 (top)
        - Player's hands at y=450 (bottom)
        """
        # Create computer's hand sprite (initially rock)
        self.computer_sprite = HandSprite(self.rock_image, (200, 150))
        self.computer_sprite.type = 0
        self.computer_hand.add(self.computer_sprite)

        # Create player's hand sprites
        # Left rock
        self.rock_left = HandSprite(self.rock_image, (75, 450))
        self.rock_left.type = 0
        
        # Center paper
        self.paper_center = HandSprite(self.paper_image, (200, 450))
        self.paper_center.type = 1
        
        # Right scissors
        self.scissors_right = HandSprite(self.scissors_image, (325, 450))
        self.scissors_right.type = 2

        # Add player sprites to group
        self.player_hands.add(self.rock_left)
        self.player_hands.add(self.paper_center)
        self.player_hands.add(self.scissors_right)
        
        # Selected player hand (shown after choice)
        self.player_choice = HandSprite(self.rock_image, (200, 450))
        self.player_choice.type = 0  # Initially rock


    def init_sfx(self):
        """Initialize game sound effects.
        
        Loads sound files from the res directory:
        - win.wav: Played on player victory
        - loss.wav: Played on computer victory
        - draw.wav: Played on tie games
        - shuffling.wav: Background sound during computer's turn
        
        Each sound is loaded as a Pygame Sound object for efficient playback.
        Sound files should be in .wav format for best compatibility.
        """
        self.win_sfx = pygame.mixer.Sound(resource_path("res/win.wav"))
        self.loss_sfx = pygame.mixer.Sound(resource_path("res/loss.wav"))
        self.draw_sfx = pygame.mixer.Sound(resource_path("res/draw.wav"))
        self.shuffling_sfx = pygame.mixer.Sound(resource_path("res/shuffling.wav"))

    
    def render(self):
        """Render the current game state to the screen.
        
        Draws all game elements in the following order:
        1. Background (dark color)
        2. Score display and player labels
        3. Instruction text (top and bottom)
        4. Center dividing line
        5. Computer's current hand (top)
        6. Player's hand(s) (bottom):
           - During play: All three options
           - After choice: Selected hand only
        
        All text is centered and white on dark background.
        """
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
        
        # Update computer's sprite image based on choice
        if self.computer_ch == 0:
            self.computer_sprite.image = self.rock_image
        elif self.computer_ch == 1:
            self.computer_sprite.image = self.paper_image
        elif self.computer_ch == 2:
            self.computer_sprite.image = self.scissors_image
        
        # Draw computer hand
        self.computer_hand.draw(self.screen)
            
        # Draw player hands
        if self.playing:
            self.player_hands.draw(self.screen)
        else:
            # Update and draw player's choice
            if self.player_ch == 0:
                self.player_choice.image = self.rock_image
            elif self.player_ch == 1:
                self.player_choice.image = self.paper_image
            elif self.player_ch == 2:
                self.player_choice.image = self.scissors_image
            self.screen.blit(self.player_choice.image, self.player_choice.rect)

        # Update the display
        pygame.display.flip()

    
    def shuffle_hand(self):
        """Animate computer's hand by cycling through options.
        
        Called periodically during the player's turn to create
        an animation effect. Cycles through:
        0 -> 1 -> 2 -> 0 (Rock -> Paper -> Scissors -> Rock)
        
        The animation runs at a fixed interval (0.2 seconds)
        controlled by the main game loop.
        """
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


    def update_score(self):
        """Calculate round result and update scores.
        
        Determines the winner based on classic Rock Paper Scissors rules:
        - Rock beats Scissors
        - Paper beats Rock
        - Scissors beats Paper
        
        Updates:
        - Player and computer scores
        - Display messages for next round
        - Plays appropriate sound effect (win/loss/draw)
        """
        ch_tuple = (self.computer_ch, self.player_ch)
        
        # Check win conditions and update scores
        if ch_tuple in self.computer_wins:
            self.computer_score += 1
            self.top_instruction = "Computer wins!"
            self.loss_sfx.play()
        elif ch_tuple in self.player_wins:
            self.player_score += 1
            self.top_instruction = "You win!"
            self.win_sfx.play()
        else:
            self.top_instruction = "Draw!"
            self.draw_sfx.play()

        # Update instruction for next round
        self.bottom_instruction = "Click anywhere to continue."


    def handle_mouse_click(self, pos):
        """Handle mouse clicks on the game images.
        
        During gameplay:
        - Left rock image: Select Rock (0)
        - Center image: Select Paper (1)
        - Right scissors image: Select Scissors (2)
        
        After round:
        - Any click: Start new round
        """
        if self.playing:
            # Check if click is on any of the player hands
            clicked_sprites = [s for s in self.player_hands if s.rect.collidepoint(pos)]
            if clicked_sprites:
                sprite = clicked_sprites[0]
                self.player_ch = sprite.type
                self.shuffling_hand = False
            else:
                return  # Click was not on any image
            
            # Process round end
            self.playing = False
            self.shuffling_hand = False
            self.shuffling_sfx.stop()
            self.random_choice()
            self.update_score()
        else:
            # Start new round
            self.playing = True
            self.shuffling_hand = True
            self.top_instruction = "Choose your move:"
            self.bottom_instruction = "Click on an image to play"
            self.shuffling_sfx.play()


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
            self.shuffling_sfx.stop()
            self.random_choice()
            self.score()
        else:
            # Start new round
            self.playing = True
            self.shuffling_hand = True
            self.top_instruction = "Choose your move:"
            self.bottom_instruction = "Press R, P, or S to play"
            self.shuffling_sfx.play()


    def loop(self):
        """Main game loop handling all real-time game updates.
        
        Processes in order:
        1. Event handling:
           - Window close (X button)
           - Mouse clicks (left button only)
           - Keyboard input (R,P,S keys)
           - Alt+F4 for quick exit
        
        2. Animation updates:
           - Computer's hand shuffling (if active)
           - Timing controlled by self.prev_time
        
        3. Display updates:
           - Renders current game state
           - Maintains 60 FPS using game clock
        
        The loop continues until self.running is set to False.
        """
        # Process all pending events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle mouse clicks
                if event.button == 1:  # Left click
                    self.handle_mouse_click(event.pos)
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
        
        # Control the frame rate (60 FPS)
        self.clock.tick(60)


    def start_game(self):
        """Start and run the game.
        
        Entry point for the game that:
        1. Sets initial game state (running=True, playing=True)
        2. Starts the background shuffling sound
        3. Enters the main game loop
        4. Handles graceful shutdown when game ends
        
        The game runs until either:
        - Player closes the window
        - Player presses Alt+F4
        - An unhandled exception occurs
        """
        self.running = True  # Controls the main game loop
        self.playing = True  # Controls the gameplay state
        self.shuffling_sfx.play()
        while self.running:
            self.loop()
        self.quit_game()
    

    def quit_game(self):
        """Clean up and exit the game.
        
        Performs graceful shutdown:
        1. Stops all running sounds
        2. Closes the Pygame display
        3. Releases system resources
        4. Exits the program
        
        This ensures no resources are left hanging when the game closes.
        """
        pygame.quit()
        sys.exit()

