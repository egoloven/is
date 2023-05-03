import random
import heapq
import pygame
import sys

# Maze generation
def create_grid(width, height):
    return [['#' for _ in range(width)] for _ in range(height)]

def is_valid_cell(x, y, width, height):
    return 0 <= x < width and 0 <= y < height

def prim_maze_generation(width, height):
    maze = create_grid(width, height)
    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]

    start_x, start_y = random.randrange(0, width, 2), random.randrange(0, height, 2)
    maze[start_y][start_x] = '.'

    frontier = [(start_x, start_y)]
    while frontier:
        x, y = frontier.pop(random.randint(0, len(frontier) - 1))

        for i in range(4):
            nx, ny = x + dx[i] * 2, y + dy[i] * 2
            if is_valid_cell(nx, ny, width, height) and maze[ny][nx] == '#':
                maze[y + dy[i]][x + dx[i]] = '.'
                maze[ny][nx] = '.'
                frontier.append((nx, ny))

    return maze

# Pathfinding algorithms
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def neighbors(maze, pos):
    x, y = pos
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze) and maze[ny][nx] == ".":
            yield (nx, ny)

def greedy_move(src, dest, maze, visited):
    next_moves = []
    for neighbor in neighbors(maze, src):
        dist = heuristic(neighbor, dest)
        visit_count = visited.get(neighbor, 0)
        next_moves.append((dist, visit_count, neighbor))

    if not next_moves:
        return src

    next_moves.sort(key=lambda x: (x[1], x[0]))  # Sort by visit_count, then by distance
    next_move = next_moves[0][2]

    visited[next_move] = visited.get(next_move, 0) + 1
    return next_move



def a_star(src, dest, maze):
    frontier = [(heuristic(src, dest), 0, src)]
    came_from = {src: None}
    cost_so_far = {src: 0}

    while frontier:
        _, cost, current = heapq.heappop(frontier)

        if current == dest:
            break

        for neighbor in neighbors(maze, current):
            new_cost = cost + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, dest)
                heapq.heappush(frontier, (priority, new_cost, neighbor))
                came_from[neighbor] = current

    return came_from

def a_star_move(src, dest, maze):
    came_from = a_star(src, dest, maze)
    if dest not in came_from:
        return src

    current = dest
    while came_from[current] != src:
        current = came_from[current]

    return current

# Visualization
def draw_maze(screen, maze, pos1, pos2, reward, cell_size):
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            color = (0, 0, 0) if cell == "#" else (255, 255, 255)
            pygame.draw.rect(screen, color, pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size))

    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(reward[0] * cell_size, reward[1] * cell_size, cell_size, cell_size))
    pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(pos1[0] * cell_size, pos1[1] * cell_size, cell_size, cell_size))
    pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(pos2[0] * cell_size, pos2[1] * cell_size, cell_size, cell_size))

def find_free_position(maze):
    while True:
        x = random.randint(0, len(maze[0]) - 1)
        y = random.randint(0, len(maze) - 1)
        if maze[y][x] == ".":
            return x, y

def visualize_maze(maze, pos1, pos2, reward, cell_size=20):
    pygame.init()

    width, height = len(maze[0]) * cell_size, len(maze) * cell_size
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Maze Visualization")

    clock = pygame.time.Clock()

    visited1 = {pos1: 1}
    visited2 = {pos2: 1}

    while pos1 != reward or pos2 != reward:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_maze(screen, maze, pos1, pos2, reward, cell_size)
        pygame.display.flip()

        if pos1 != reward:
            pos1 = greedy_move(pos1, reward, maze, visited1)

        if pos2 != reward:
            pos2 = a_star_move(pos2, reward, maze)

        clock.tick(2)

    print("Both players have reached the reward!")
    pygame.time.delay(2000)
    pygame.quit()

width, height = 45, 45
maze = prim_maze_generation(width, height)

reward_pos = find_free_position(maze)
pos1 = find_free_position(maze)
pos2 = find_free_position(maze)

visualize_maze(maze, pos1, pos2, reward_pos)
