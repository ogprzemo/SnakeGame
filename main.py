from tkinter import *
import random

GAME_WIDTH = 500
GAME_HEIGHT = 500
SPACE_SIZE = 20
BODY_PARTS = 3
SNAKE_SPEED = 100
SNAKE_COLOR = "green"
FOOD_COLOR = "red"
BACKGROUND_COLOR = "black"

class Snake:
    def __init__(self):
        self.length = BODY_PARTS
        self.coordinates = [[0, 0]] * BODY_PARTS
        self.squares = []

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

    def grow(self):
        last_x, last_y = self.coordinates[-1]
        square = canvas.create_rectangle(last_x, last_y, last_x + SPACE_SIZE, last_y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
        self.squares.append(square)
        self.coordinates.append([last_x, last_y])

class Food:
    def __init__(self):
        self.coordinates = self.generate_food_position()
        self.square = canvas.create_oval(self.coordinates[0], self.coordinates[1],
                                         self.coordinates[0] + SPACE_SIZE, self.coordinates[1] + SPACE_SIZE,
                                         fill=FOOD_COLOR, tag="food")

    def generate_food_position(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        return [x, y]

    def refresh(self):
        self.coordinates = self.generate_food_position()
        canvas.coords(self.square, self.coordinates[0], self.coordinates[1],
                      self.coordinates[0] + SPACE_SIZE, self.coordinates[1] + SPACE_SIZE)

def next_snake_turn(snake, food):
    if game_over_flag:
        return

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, [x, y])
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score: " + str(score))
        food.refresh()
        snake.grow()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    check_collision(snake)

    window.after(SNAKE_SPEED, next_snake_turn, snake, food)

def move_snake(new_direction):
    global direction
    if new_direction == "up" and direction != "down":
        direction = new_direction
    elif new_direction == "down" and direction != "up":
        direction = new_direction
    elif new_direction == "left" and direction != "right":
        direction = new_direction
    elif new_direction == "right" and direction != "left":
        direction = new_direction

def check_collision(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        game_over()
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            game_over()

def game_over():
    global game_over_flag
    game_over_flag = True
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2, text="GAME OVER", fill="red", font=("Arial", 24))
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 30, text="Press 'R' to Restart", fill="white", font=("Arial", 14))

def restart_game():
    global snake, food, score, direction, game_over_flag

    canvas.delete("all")
    score = 0
    direction = "down"
    game_over_flag = False
    label.config(text="Score: " + str(score))

    snake = Snake()
    food = Food()

    next_snake_turn(snake, food)

window = Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
direction = "down"
game_over_flag = False

label = Label(window, text="Score: " + str(score), font=("Arial", 20))
label.pack()

canvas = Canvas(window, width=GAME_WIDTH, height=GAME_HEIGHT, bg=BACKGROUND_COLOR)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int(screen_width / 2 - window_width / 2)
y = int(screen_height / 2 - window_height / 2)

window.geometry(f"{window_width}x{window_height}+{int(x)}+{int(y)}")

window.bind("<Up>", lambda event: move_snake("up"))
window.bind("<Down>", lambda event: move_snake("down"))
window.bind("<Left>", lambda event: move_snake("left"))
window.bind("<Right>", lambda event: move_snake("right"))

window.bind("r", lambda event: restart_game() if game_over_flag else None)

snake = Snake()
food = Food()

next_snake_turn(snake, food)

window.mainloop()