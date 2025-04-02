import pygame
import random
import math


pygame.init()

# Размер окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("paint")

# Функция для случайного цвета
def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Переменные
color = random_color()
line_width = 2  # Начальная толщина линии
eraser_size = 10  # Размер ластика
drawing = False
mode = "pencil"  # pencil, eraser, square, right_triangle, equilateral_triangle, circle, rhombus
start_pos = None
last_pos = None  
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255, 255, 255)) 

# Основной цикл
running = True
while running:
    screen.fill((255, 255, 255))
    screen.blit(canvas, (0, 0))  # Отображаем холст

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:  # Смена цвета
                color = random_color()
            elif event.key == pygame.K_p:  # Карандаш
                mode = "pencil"
            elif event.key == pygame.K_e:  # Ластик
                mode = "eraser"
            elif event.key == pygame.K_1:
                mode = "square"
            elif event.key == pygame.K_2:
                mode = "right_triangle"
            elif event.key == pygame.K_3:
                mode = "equilateral_triangle"
            elif event.key == pygame.K_4:
                mode = "circle"
            elif event.key == pygame.K_5:
                mode = "rhombus"

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # ЛКМ - увеличить толщину линии или размер ластика
                if mode == "eraser":
                    eraser_size += 2
                else:
                    line_width += 1
            elif event.button == 3:  # ПКМ - уменьшить толщину линии или размер ластика
                if mode == "eraser":
                    eraser_size = max(2, eraser_size - 2)
                else:
                    line_width = max(1, line_width - 1)

            start_pos = event.pos  # Запоминаем начальную точку
            last_pos = event.pos  # Запоминаем последнюю точку для карандаша

        elif event.type == pygame.MOUSEBUTTONUP:
            if start_pos:
                end_pos = event.pos
                x1, y1 = start_pos
                x2, y2 = end_pos
                w, h = abs(x2 - x1), abs(y2 - y1)

                
                if mode == "square":
                    pygame.draw.rect(canvas, color, (x1, y1, w, w), 1)
                elif mode == "right_triangle":
                    pygame.draw.polygon(canvas, color, [(x1, y1), (x1, y1 + h), (x1 + w, y1 + h)], 1)
                elif mode == "equilateral_triangle":
                    h = (math.sqrt(3) / 2) * w
                    pygame.draw.polygon(canvas, color, [(x1, y1), (x1 + w, y1), (x1 + w // 2, y1 - h)], 1)
                elif mode == "circle":
                    pygame.draw.circle(canvas, color, (x1, y1), min(w, h) // 2, 1)
                elif mode == "rhombus":
                    pygame.draw.polygon(canvas, color, [(x1, y1), (x1 + w // 2, y1 - h // 2), 
                                                        (x1, y1 - h), (x1 - w // 2, y1 - h // 2)], 1)

    # Рисование карандашом 
    if pygame.mouse.get_pressed()[0]:
        if mode == "pencil":
            current_pos = pygame.mouse.get_pos()
            if last_pos:
                pygame.draw.line(canvas, color, last_pos, current_pos, line_width)
            last_pos = current_pos
        elif mode == "eraser":
            pygame.draw.circle(canvas, (255, 255, 255), pygame.mouse.get_pos(), eraser_size)  # Стираем белым

    if not pygame.mouse.get_pressed()[0]:  # Если кнопку отпустили, сброс last_pos
        last_pos = None

    pygame.display.flip()

pygame.quit()
