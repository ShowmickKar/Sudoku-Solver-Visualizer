import pygame
import random

RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)


class Cell:
    def __init__(self, value, screen_width, window, row, column):
        self.window = window
        self.screen_width = screen_width
        self.size = screen_width / 9
        self.value = value
        self.row = row
        self.column = column
        if self.value:
            self.color = BLUE
            self.default = True
        else:
            self.color = RED
            self.default = False

    def draw(self, window):
        if self.value:
            font = pygame.font.SysFont("times new roman", 30)
            value = font.render(str(self.value), False, self.color)
            window.blit(
                value,
                (
                    self.row * self.size + self.size // 2 - 6,
                    self.column * self.size + self.size // 2 - 13,
                ),
            )
