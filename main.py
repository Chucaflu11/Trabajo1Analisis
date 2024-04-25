import pygame
import sys
import os

def load_assets(directory):
    assets = {}
    for file_name in os.listdir(directory):
        if file_name.endswith('.png'):
            asset_name = os.path.splitext(file_name)[0]
            assets[asset_name] = pygame.image.load(os.path.join(directory, file_name))
    return assets

def print_assets(screen, assets):
    screen.blit(assets['Logo'], (650, 30))
    screen.blit(assets['Titulo'], (850, 80))
    screen.blit(assets['M_circulo'], (850, 380))
    screen.blit(assets['N_circulo'], (1040, 380))
    screen.blit(assets['Flechita'], (795, 397))
    screen.blit(assets['Icono_Matriz'], (700, 355))

# Función para manejar eventos de entrada
def handle_input_events(input_boxes, buttons):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        for box in input_boxes:
            box.handle_event(event)
        for button in buttons:
            button.handle_event(event)

# Clase para crear un cuadro de entrada
class InputBox:
    def __init__(self, x, y, width, height, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_inactive = pygame.Color((93, 137, 145))
        self.color_active = pygame.Color((9, 51, 58))
        self.color = self.color_inactive
        self.text = text
        self.font = pygame.font.Font(None, 16)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Si se hace clic en el cuadro de entrada, activarlo
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            # Cambiar el color del cuadro según si está activo o no
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            # Si el cuadro de entrada está activo, manejar los eventos de teclado
            if self.active:
                if event.key == pygame.K_RETURN:
                    # Si se presiona Enter, dejar de editar
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    # Si se presiona retroceso, eliminar un carácter
                    self.text = self.text[:-1]
                else:
                    # Agregar caracteres al texto
                    self.text += event.unicode

    def draw(self, screen):
        txt_surface = self.font.render(self.text, True, self.color)
        width = max(105, txt_surface.get_width()+10)
        self.rect.w = width
        screen.blit(txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)
    
    def get_text(self):
        return self.text
    
class Button:
    def __init__(self, x, y, image_name, callback):
        self.image = image_name
        self.rect = self.image.get_rect(topleft=(x, y))
        self.callback = callback

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Board:
    def __init__(self, x, y, width, height, m, n, matrix):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.m = m
        self.n = n
        self.matrix = matrix
        self.cell_width = width // n
        self.cell_height = height // m
        self.colors = {0: pygame.Color('white'), 1: pygame.Color((157, 129, 137)), 2: pygame.Color((106, 190, 167))}

    def draw(self, screen):
        # Draw the main rectangle
        pygame.draw.rect(screen, pygame.Color('black'), pygame.Rect(self.x, self.y, self.width, self.height), 2)

        # Draw the cells
        for i in range(self.m):
            for j in range(self.n):
                cell_x = self.x + j * self.cell_width
                cell_y = self.y + i * self.cell_height
                cell_color = self.colors[self.matrix[i][j]]
                pygame.draw.rect(screen, cell_color, pygame.Rect(cell_x, cell_y, self.cell_width, self.cell_height))

                # Draw a black border around the cell
                pygame.draw.rect(screen, pygame.Color('black'), pygame.Rect(cell_x, cell_y, self.cell_width, self.cell_height), 1)

def print_values(value1, value2):
    print("Valor 1:", value1.get_text())
    print("Valor 2:", value2.get_text())

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()

    assets = load_assets('assets')

    matrix = [[2, 1, 1], [2, 1, 1], [1, 1, 2], [1, 1, 2]]  # Replace this with your actual matrix
    board = Board(93, 98, 400, 400, 4, 3, matrix)    

    input_box1 = InputBox(910, 397, 105, 27)
    input_box2 = InputBox(1101, 397, 105, 27)
    input_boxes = [input_box1, input_box2]

    print_button = Button(950, 500, assets['SET'], lambda: print_values(input_box1, input_box2))
    dropdown_button = Button(500, 85, assets['Icono_Lista_Soluciones'], lambda: print_values(input_box1, input_box2))
    right_button = Button(440, 500, assets['Flecha_Siguiente'], lambda: print_values(input_box1, input_box2))
    left_button = Button(90, 500, assets['Flecha_Anterior'], lambda: print_values(input_box1, input_box2))

    done = False

    buttons = [print_button, dropdown_button, right_button, left_button]

    while not done:
        handle_input_events(input_boxes, buttons)
        screen.fill((251, 241, 243))
        print_assets(screen, assets)

        board.draw(screen)

        for box in input_boxes:
            box.draw(screen)

        print_button.draw(screen)
        dropdown_button.draw(screen)
        right_button.draw(screen)
        left_button.draw(screen)

        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()
