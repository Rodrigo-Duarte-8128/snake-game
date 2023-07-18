import pygame
import sys
import random
import json


class SnakeSegment(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.rect = pygame.Rect(x_pos, y_pos, 25, 25)
        self.direction = "left"
        self.next_direction_queue = []

    def update_direction(self):
        keys = pygame.key.get_pressed()
        if keys.count(True) < 2:
            if keys[pygame.K_w] and self.direction != "down":
                if self.next_direction_queue:
                    if self.next_direction_queue[-1] != "up":
                        self.next_direction_queue += ["up"]
                else:
                    self.next_direction_queue += ["up"]
            if keys[pygame.K_a] and self.direction != "right":
                if self.next_direction_queue:
                    if self.next_direction_queue[-1] != "left":
                        self.next_direction_queue += ["left"]
                else:
                    self.next_direction_queue += ["left"]
            if keys[pygame.K_s] and self.direction != "up":
                if self.next_direction_queue:
                    if self.next_direction_queue[-1] != "down":
                        self.next_direction_queue += ["down"]
                else:
                    self.next_direction_queue += ["down"]
            if keys[pygame.K_d] and self.direction != "left":
                if self.next_direction_queue:
                    if self.next_direction_queue[-1] != "right":
                        self.next_direction_queue += ["right"]
                else:
                    self.next_direction_queue += ["right"]

        if self.rect.topleft[0] % 25 == 0 and self.rect.topleft[1] % 25 == 0:
            if self.next_direction_queue:
                self.direction = self.next_direction_queue.pop(0)

    def move(self):
        if self.direction == "up":
            self.rect.centery -= snake_speed
        elif self.direction == "down":
            self.rect.centery += snake_speed
        elif self.direction == "right":
            self.rect.centerx += snake_speed
        elif self.direction == "left":
            self.rect.centerx -= snake_speed

    def out_of_bounds(self):
        if self.rect.top < - snake_speed // 2 or self.rect.right > width + snake_speed // 2 \
                or self.rect.left < - snake_speed // 2 or self.rect.bottom > height + snake_speed // 2:
            return True
        return False


FPS = 50
width = 800
height = 500
last_score = 0

try:
    with open("max_score.json", "r") as f:
        max_score_dict = json.load(f)
        max_score = max_score_dict["score"]
except:
    max_score = 0



snake_speed = 5

lattice = []
for i in range(width):
    for j in range(height):
        if i % 25 == 0 and j % 25 == 0:
            lattice += [(i, j)]

pygame.init()

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")
background = pygame.Rect(0, 0, width, height)

# Fonts
title_font = pygame.font.SysFont("Cambria", 40, False, False)
instruction_font = pygame.font.SysFont("Cambria", 30, False, False)
last_score_font = pygame.font.SysFont("Cambria", 20)
max_score_font = pygame.font.SysFont("Cambria", 20)
lost_font = pygame.font.SysFont("Cambria", 30)
try_again_font = pygame.font.SysFont("Cambria", 20)
main_menu_font = pygame.font.SysFont("Cambria", 20)
score_font = pygame.font.SysFont("Cambria", 20)

# Groups
snake_head = SnakeSegment(width // 2, height // 2)
snake_segments_list = [snake_head]


food = pygame.Rect(200, 250, 25, 25)

clock = pygame.time.Clock()


def draw_play_screen():
    pygame.draw.rect(screen, "White", background)
    score_font_surf = score_font.render(f"Score: {last_score}", True, "Gray")
    score_font_rect = score_font_surf.get_rect(topleft=(10, 10))
    screen.blit(score_font_surf, score_font_rect)
    pygame.draw.rect(screen, "Red", food)
    for segment in snake_segments_list:
        pygame.draw.rect(screen, "Black", segment.rect)

    pygame.display.update()


def draw_title_screen():
    pygame.draw.rect(screen, "White", background)
    title_surf = title_font.render("Welcome to the Game of Snake!", True, "Black")
    title_rect = title_surf.get_rect(center=(width // 2, height // 2 - 50))
    instruction_surf = instruction_font.render("(Press SPACEBAR to start)", True, "Black")
    instruction_rect = instruction_surf.get_rect(center=(width // 2, height // 2 + 50))
    last_score_surf = last_score_font.render(f"Last Score: {last_score}", True, "Black")
    last_score_rect = last_score_surf.get_rect(midbottom=(width // 4, height - 50))
    max_score_surf = max_score_font.render(f"Max Score: {max_score}", True, "Black")
    max_score_rect = max_score_surf.get_rect(midbottom=(3 * width // 4, height - 50))

    screen.blit(max_score_surf, max_score_rect)
    screen.blit(last_score_surf, last_score_rect)
    screen.blit(instruction_surf, instruction_rect)
    screen.blit(title_surf, title_rect)
    pygame.display.update()


def draw_lost_screen():
    pygame.draw.rect(screen, "White", background)
    score_font_surf = score_font.render(f"Score: {last_score}", True, "Gray")
    score_font_rect = score_font_surf.get_rect(topleft=(10, 10))
    screen.blit(score_font_surf, score_font_rect)
    pygame.draw.rect(screen, "Red", food)
    for segment in snake_segments_list:
        pygame.draw.rect(screen, "Black", segment.rect)

    lost_font_surf = lost_font.render(
        "Better luck next time" if last_score <= max_score else "Congrats! You beat your max score!", True, "Gray")
    lost_font_rect = lost_font_surf.get_rect(center=(width // 2, height // 2 - 100))
    try_again_font_surf = try_again_font.render("Press SPACEBAR to try again", True, "Gray")
    try_again_font_rect = try_again_font_surf.get_rect(midbottom=(width // 4, height - 50))
    main_menu_font_surf = main_menu_font.render("Press ESC for MAIN MENU", True, "Gray")
    main_menu_font_rect = main_menu_font_surf.get_rect(midbottom=(3 * width // 4, height - 50))

    screen.blit(main_menu_font_surf, main_menu_font_rect)
    screen.blit(try_again_font_surf, try_again_font_rect)
    screen.blit(lost_font_surf, lost_font_rect)
    pygame.display.update()


def move_snake(segments_list):
    segments_list.reverse()
    for idx, segment in enumerate(segments_list):
        if idx == len(segments_list) - 1:
            segment.update_direction()
            segment.move()
        else:
            if segments_parallel_collide_after(segments_list, idx):
                continue

            vel_vector = segments_list[idx + 1].rect.centerx - segment.rect.centerx, \
                segments_list[idx + 1].rect.centery - segment.rect.centery

            segment.rect.centerx += vel_vector[0]
            segment.rect.centery += vel_vector[1]

    segments_list.reverse()


def snake_hits_itself(segments_list):
    # the snake will hit itself if the head's position coincides with a segment position where the segment is not
    # the neck
    if len(segments_list) >= 3:
        for i in range(2, len(segments_list)):
            if segments_list[0].rect.colliderect(segments_list[i].rect):
                return True
    return False


def segments_parallel_collide(rect1, rect2):
    if rect1.left == rect2.left and rect1.right == rect2.right:
        if max(rect1.top, rect2.top) < min(rect1.bottom, rect2.bottom):
            return True
        else:
            return False
    elif rect1.top == rect2.top and rect1.bottom == rect2.bottom:
        if max(rect1.left, rect2.left) < min(rect1.right, rect2.right):
            return True
        else:
            return False
    else:
        return False


def segments_parallel_collide_after(segments_list, idx):
    # returns true if there is a parallel collide somewhere in the segments_list after index i
    for i in range(idx, len(segments_list) - 1):
        if segments_parallel_collide(segments_list[i].rect, segments_list[i + 1].rect):
            return True
    return False


def food_valid_lattice_positions(segments_list):
    invalid_positions = []
    for segment in segments_list:
        invalid_positions += [segment.rect.topleft]
    r = []
    for point in lattice:
        if point not in invalid_positions:
            r += [point]
    return r


game_state = "title screen"
while True:
    if game_state == "play":

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if snake_head.rect.center == food.center:
            snake_segments_list += [SnakeSegment(
                snake_segments_list[-1].rect.topleft[0], snake_segments_list[-1].rect.topleft[1])]
            random_food_position = random.choice(food_valid_lattice_positions(snake_segments_list))
            food = pygame.Rect(random_food_position[0], random_food_position[1], 25, 25)
            last_score += 1

        move_snake(snake_segments_list)
        draw_play_screen()

        if snake_head.out_of_bounds() or snake_hits_itself(snake_segments_list):
            game_state = "lost"

    elif game_state == "title screen":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    last_score = 0
                    game_state = "play"
        draw_title_screen()

    elif game_state == "lost":
        if last_score > max_score:
            max_score = last_score

            with open("max_score.json", "w") as f:
                json.dump({"score": max_score}, f)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_state = "play"
                    # reset game
                    snake_head.rect.topleft = (width // 2, height // 2)
                    snake_head.direction = "left"
                    snake_segments_list = [snake_head]
                    food = pygame.Rect(200, 250, 25, 25)
                    last_score = 0
                if event.key == pygame.K_ESCAPE:
                    game_state = "title screen"
                    # reset game
                    snake_head.rect.topleft = (width // 2, height // 2)
                    snake_head.direction = "left"
                    snake_segments_list = [snake_head]
                    food = pygame.Rect(200, 250, 25, 25)

        draw_lost_screen()

    clock.tick(FPS)


