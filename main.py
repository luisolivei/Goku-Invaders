import pygame

# Tamanho da tela
x = 800
y = 600

# Caminho para o sprite sheet
sprite_sheet_path = "images/14491.gif"

# Dados dos quadros: cada item da lista é uma tupla (x, y, largura, altura)
# Ajusta as coordenadas e tamanhos conforme necessário
quadros = [
    (0, 2304, 64, 64),
    (64, 2304, 70, 64),
    (136, 2304, 70, 64),
    (136+64, 2304, 70, 64),
    (136+128, 2304, 70, 64),
    # Adiciona mais coordenadas para cada quadro
]

animation_speed = 0.01  # Velocidade de transição dos quadros

pygame.init()

# Iniciar tela
screen = pygame.display.set_mode((x, y))
pygame.display.set_caption("Goku-Invaders")

# Carregar fundo
bg = pygame.image.load("images/bg.png").convert_alpha()
bg = pygame.transform.scale(bg, (x, y))

# Carregar sprite sheet do personagem
sprite_sheet = pygame.image.load(sprite_sheet_path).convert()

# Definir o fundo como transparente 
color_key = (144, 176, 216)  # cor RGB a elimar do sprite
sprite_sheet.set_colorkey(color_key)

# Posicionamento do personagem
pos_player_x = 100
pos_player_y = y / 2 - quadros[0][3] / 2  # Alinha com a altura do primeiro quadro

# Variáveis de animação
frame_index = 0
time_since_last_frame = 0

# Função para pegar um quadro específico
def get_frame(sheet, frame_index):
    frame_data = quadros[frame_index]
    frame_rect = pygame.Rect(
        frame_data[0], frame_data[1],  # posição x, y
        frame_data[2], frame_data[3]   # largura, altura
    )
    frame = sheet.subsurface(frame_rect)
    return frame

running = True

while running:
    # Calcular o tempo de transição dos quadros
    time_since_last_frame += animation_speed
    if time_since_last_frame >= 1:
        frame_index = (frame_index + 1) % len(quadros)  # Loop pelos quadros
        time_since_last_frame = 0

    # Processar eventos
    for event in pygame.event.get():
        if event.type =pythonm= pygame.QUIT:
            running = False

    # Atualizar o fundo
    screen.blit(bg, (0, 0))
    rel_x = x % bg.get_rect().width
    screen.blit(bg, (rel_x - bg.get_rect().width, 0))
    if rel_x < 800:
        screen.blit(bg, (rel_x, 0))

    # definição de teclas para movimentar o player
    tecla = pygame.key.get_pressed()
    if tecla[pygame.K_UP] and pos_player_y > 1:
        pos_player_y -= 1
    if tecla[pygame.K_DOWN] and pos_player_y < y - 50:
        pos_player_y += 1

#Velocidade movimento tela
    x -= 0.2

    # Desenhar personagem animado
    player_frame = get_frame(sprite_sheet, frame_index)
    screen.blit(player_frame, (pos_player_x, pos_player_y))

    # Atualizar tela
    pygame.display.update()

pygame.quit()
