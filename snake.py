"""
Snake Game by Aneesh Bukya

This Snake game is a simple implementation of the classic Snake game using Python and the Tkinter library
for creating the graphical user interface. The player controls a snake that moves around the game board
and tries to eat food to increase its length. The game continues until the snake collides with the wall
or itself.

Features:
- Control the snake's direction with arrow keys (left, right, up, down).
- The snake grows in length when it consumes food.
- The game keeps track of the player's score.
- The game ends when the snake collides with the wall or itself, displaying a "Game Over" message.

Game Constants:
- GAME_WIDTH: Width of the game board in pixels.
- GAME_HEIGHT: Height of the game board in pixels.
- SPEED: Speed of the snake's movement.
- SPACE_SIZE: Size of each square space on the game board.
- BODY_PARTS: Initial length of the snake.
- SNAKE_COLOR: Color of the snake.
- FOOD_COLOR: Color of the food.
- BACKGROUND_COLOR: Background color of the game board.

Classes:
- Snake: Represents the snake in the game.
- Food: Represents the food that the snake can eat.

Functions:
- next_turn(snake, food): Handles the logic for each game turn, including moving the snake and checking for collisions.
- change_direction(new_direction): Changes the direction of the snake based on user input.
- check_collisions(snake): Checks for collisions between the snake and the wall or itself.
- game_over(): Displays a "Game Over" message when the game ends.

How to Play:
1. Use arrow keys (left, right, up, down) to control the snake's direction.
2. Try to eat the red food squares to increase your score.
3. Avoid colliding with the walls or the snake's own body.
4. The game ends when you collide, and a "Game Over" message is displayed.

Author: Aneesh Bukya
"""
from tkinter import *
import random

# Constants for game configuration
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 50
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

class Snake:

    def __init__(self):
        """
        Initialize the Snake object.

        The Snake class represents the snake in the game.

        Attributes:
        - body_size: Initial length of the snake.
        - coordinates: List to store the coordinates of each body part.
        - squares: List to store the graphical square elements on the canvas representing the snake.
        """
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        # Initialize the snake's coordinates
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        # Create graphical squares representing the snake on the canvas
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:

    def __init__(self):
        """
        Initialize the Food object.

        The Food class represents the food that the snake can eat.

        Attributes:
        - coordinates: List to store the coordinates of the food item.
        """
        # Generate random coordinates for the food
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        # Create graphical oval representing the food on the canvas
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


def next_turn(snake, food):
    """
    Handle the logic for each game turn.

    This function moves the snake, checks for collisions, and updates the game state accordingly.

    Args:
    - snake: Snake object representing the game's snake.
    - food: Food object representing the game's food.
    """
    x, y = snake.coordinates[0]

    # Move the snake based on the current direction
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    # Create a new square for the snake's head
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    # Check if the snake has eaten the food
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()
    else:
        # Remove the tail of the snake (last coordinate and square) if it didn't eat food
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    # Check for collisions with walls or itself
    if check_collisions(snake):
        game_over()
    else:
        # Schedule the next turn
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    """
    Change the direction of the snake based on user input.

    Args:
    - new_direction: New direction for the snake ('left', 'right', 'up', or 'down').
    """
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction


def check_collisions(snake):
    """
    Check for collisions between the snake and walls or itself.

    Args:
    - snake: Snake object representing the game's snake.

    Returns:
    - True if a collision is detected, False otherwise.
    """
    x, y = snake.coordinates[0]

    # Check for collisions with walls
    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    # Check for collisions with itself (body parts)
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_over():
    """
    Display a "Game Over" message on the canvas when the game ends.
    """
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")

# Create the main game window and initialize game variables...


window = Tk()
window.title("Snake game")
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()