import pygame
import random
import requests
from cell import Cell

pygame.init()
pygame.font.init()

font = pygame.font.SysFont("times new roman", 30)

DIMENTION = 660
WIDTH = 540
window = pygame.display.set_mode((DIMENTION, DIMENTION))
pygame.display.set_caption("SUDOKU")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)


def draw(window, WIDTH, grid, active_cell, hovering_cell, warning):
    window.fill(WHITE)
    for i in range(1, 11):
        color = BLACK
        if (i - 1) % 3 == 0:
            pygame.draw.line(
                window,
                color,
                (grid[0][0].size, grid[0][0].size * i - 1),
                (10 * grid[0][0].size, grid[0][0].size * i - 1),
            )
            pygame.draw.line(
                window,
                color,
                (grid[0][0].size, grid[0][0].size * i + 1),
                (10 * grid[0][0].size, grid[0][0].size * i + 1),
            )
            pygame.draw.line(
                window,
                color,
                (grid[0][0].size * i - 1, grid[0][0].size),
                (grid[0][0].size * i - 1, 10 * grid[0][0].size),
            )
            pygame.draw.line(
                window,
                color,
                (grid[0][0].size * i + 1, grid[0][0].size),
                (grid[0][0].size * i + 1, 10 * grid[0][0].size),
            )
        pygame.draw.line(
            window,
            color,
            (grid[0][0].size, grid[0][0].size * i),
            (10 * grid[0][0].size, grid[0][0].size * i),
        )
        pygame.draw.line(
            window,
            color,
            (grid[0][0].size * i, grid[0][0].size),
            (grid[0][0].size * i, 10 * grid[0][0].size),
        )

    for row in grid:
        for cell in row:
            cell.draw(window)

    if hovering_cell is not None and hovering_cell:
        select_cell(window, grid[hovering_cell[0] - 1][hovering_cell[1] - 1], BLUE)
    if active_cell is not None:
        select_cell(window, grid[active_cell[0] - 1][active_cell[1] - 1], RED)
    if warning:
        messege = font.render("Illigal Move!", False, RED)
        window.blit(messege, (grid[0][0].size, WIDTH + grid[0][0].size + 15))

    pygame.display.update()


def select_cell(window, cell, color):
    pygame.draw.line(
        window,
        color,
        (cell.row * cell.size - 1, cell.column * cell.size - 1),
        (cell.row * cell.size - 1, cell.column * cell.size + cell.size - 1),
    )
    pygame.draw.line(
        window,
        color,
        (cell.row * cell.size, cell.column * cell.size),
        (cell.row * cell.size, cell.column * cell.size + cell.size),
    )
    pygame.draw.line(
        window,
        color,
        (cell.row * cell.size + 1, cell.column * cell.size + 1),
        (cell.row * cell.size + 1, cell.column * cell.size + cell.size + 1),
    )

    pygame.draw.line(
        window,
        color,
        (cell.row * cell.size - 1, cell.column * cell.size - 1),
        (cell.row * cell.size + cell.size - 1, cell.column * cell.size - 1),
    )
    pygame.draw.line(
        window,
        color,
        (cell.row * cell.size, cell.column * cell.size),
        (cell.row * cell.size + cell.size, cell.column * cell.size),
    )
    pygame.draw.line(
        window,
        color,
        (cell.row * cell.size + 1, cell.column * cell.size + 1),
        (cell.row * cell.size + cell.size + 1, cell.column * cell.size + 1),
    )

    pygame.draw.line(
        window,
        color,
        (cell.row * cell.size - 1 + cell.size, cell.column * cell.size + cell.size - 1),
        (cell.row * cell.size - 1, cell.column * cell.size + cell.size - 1),
    )
    pygame.draw.line(
        window,
        color,
        (cell.row * cell.size + cell.size, cell.column * cell.size + cell.size),
        (cell.row * cell.size, cell.column * cell.size + cell.size),
    )
    pygame.draw.line(
        window,
        color,
        (cell.row * cell.size + 1 + cell.size, cell.column * cell.size + cell.size + 1),
        (cell.row * cell.size + 1, cell.column * cell.size + cell.size + 1),
    )

    pygame.draw.line(
        window,
        color,
        (cell.row * cell.size + cell.size - 1, cell.column * cell.size + cell.size - 1),
        (cell.row * cell.size + cell.size - 1, cell.column * cell.size - 1),
    )
    pygame.draw.line(
        window,
        color,
        (cell.row * cell.size + cell.size, cell.column * cell.size + cell.size),
        (cell.row * cell.size + cell.size, cell.column * cell.size),
    )
    pygame.draw.line(
        window,
        color,
        (cell.row * cell.size + cell.size + 1, cell.column * cell.size + cell.size + 1),
        (cell.row * cell.size + cell.size + 1, cell.column * cell.size + 1),
    )


def welcome_screen():
    pass


def reset(win, window):
    pygame.time.delay(500)
    if win:
        messege = font.render("Congrats!! Press SPACE to start a new game", False, RED)
        window.blit(messege, (WIDTH // 9, +15))
    else:
        messege = font.render("Press SPACE to start a new game", False, RED)
        window.blit(messege, (WIDTH // 9, +15))

    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.time.delay(2000)
                    main(WIDTH)


def create_grid(WIDTH, size, window):
    response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")
    grid_blueprint = response.json()["board"]
    print(grid_blueprint)
    grid = [
        [Cell(grid_blueprint[i - 1][j - 1], WIDTH, window, j, i) for j in range(1, 10)]
        for i in range(1, 10)
    ]
    return grid_blueprint, grid


def get_cell_location(position, grid):
    x, y = position
    for row in grid:
        for cell in row:
            if (
                cell.row * cell.size <= y <= cell.row * cell.size + cell.size
                and cell.column * cell.size <= x <= cell.column * cell.size + cell.size
            ):
                return cell


def is_valid(grid, active_cell, number):
    row = active_cell[0] - 1
    column = active_cell[1] - 1
    if grid[row][column].default:
        return False
    for i in range(9):
        if grid[row][i].value == number:
            return False
        if grid[i][column].value == number:
            return False
    row_start = (row // 3) * 3
    column_start = (column // 3) * 3
    for i in range(row_start, row_start + 3):
        for j in range(column_start, column_start + 3):
            if grid[i][j].value == number:
                return False
    return True


def finished(grid):
    for row in grid:
        for cell in row:
            if not cell.value:
                return False
    return True


def nextFreeSpace(grid):
    for i in range(9):
        for j in range(9):
            if not grid[i][j].value:
                return i, j
    return None, None


def sudoku_solver(grid, hovering_cell, active_cell, window):
    row, column = nextFreeSpace(grid)
    if row == None:
        return True
    for guess in range(1, 10):
        if is_valid(grid, [row + 1, column + 1], guess):
            grid[row][column].value = guess
            draw(window, WIDTH, grid, [row + 1, column + 1], False, False)
            if sudoku_solver(grid, hovering_cell, active_cell, window):
                return True
        grid[row][column].value = 0
    return False


def main(WIDTH):
    grid_blueprint, grid = create_grid(WIDTH, WIDTH // 9, window)
    active_cell = None
    hovering_cell = None
    warning = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                cell = get_cell_location(position, grid)
                if cell == None:
                    continue
                if event.button == 1:
                    active_cell = [cell.row, cell.column]
                if event.button == 3:
                    if [cell.row, cell.column] == active_cell:
                        if not grid[active_cell[0] - 1][active_cell[1] - 1].default:
                            grid[active_cell[0] - 1][active_cell[1] - 1].value = 0
                        active_cell = None

            if event.type == pygame.MOUSEMOTION:
                position = pygame.mouse.get_pos()
                cell = get_cell_location(position, grid)
                if cell is not None:
                    hovering_cell = [cell.row, cell.column]

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    grid = [
                        [
                            Cell(grid_blueprint[i - 1][j - 1], WIDTH, window, j, i)
                            for j in range(1, 10)
                        ]
                        for i in range(1, 10)
                    ]
                    sudoku_solver(grid, False, active_cell, window)
                if event.key == pygame.K_r:
                    reset(False, window)
                if event.key == pygame.K_LEFT and active_cell is not None:
                    if active_cell[1] > 1:
                        active_cell[1] -= 1
                if event.key == pygame.K_RIGHT and active_cell is not None:
                    if active_cell[1] < 9:
                        active_cell[1] += 1
                if event.key == pygame.K_UP and active_cell is not None:
                    if active_cell[0] > 1:
                        active_cell[0] -= 1
                if event.key == pygame.K_DOWN and active_cell is not None:
                    if active_cell[0] < 9:
                        active_cell[0] += 1
                number = event.key - 48
                if 0 < number < 10:
                    if (
                        active_cell is not None
                        and not grid[active_cell[0] - 1][active_cell[1] - 1].default
                        and is_valid(grid, active_cell, number)
                    ):
                        grid[active_cell[0] - 1][active_cell[1] - 1].value = number
                    else:
                        warning = True

        draw(window, WIDTH, grid, active_cell, hovering_cell, warning)
        if warning:
            pygame.time.delay(150)
            warning = False
        if finished(grid):
            reset(True, window)


if __name__ == "__main__":
    main(WIDTH)