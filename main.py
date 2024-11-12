# main.py
import pygame
from config import largura_ecra, altura_ecra, velocidade_fundo
from jogador import Jogador
from personagens import AnimacaoParado, AnimacaoAndar, AnimacaoDisparar, AnimacaoAtingido
from menu import menu

# Função principal do jogo
def play():
    # Configurações para o fundo e ambiente de jogo
    ecra = pygame.display.set_mode((largura_ecra, altura_ecra))  # Inicializa a janela do jogo
    pygame.display.set_caption("Goku Invaders")
    fundo = pygame.image.load("images/bg.png").convert_alpha()
    fundo = pygame.transform.scale(fundo, (largura_ecra, altura_ecra))  # Ajusta o fundo ao tamanho da tela

    # Inicializa o jogador e define animações
    jogador = Jogador(100, altura_ecra / 2 - 64 / 2)
    jogador.adicionar_animacao("parado", AnimacaoParado())
    jogador.adicionar_animacao("andar", AnimacaoAndar())
    jogador.adicionar_animacao("disparar", AnimacaoDisparar())
    jogador.adicionar_animacao("atingido", AnimacaoAtingido())
    jogador.definir_animacao("parado")  # necessária para iniciar
    
    a_funcionar = True
    relogio = pygame.time.Clock()
    posicao_fundo_x = 0  # Posição inicial do fundo

    # Loop principal do jogo
    while a_funcionar:
        delta_tempo = relogio.tick(60) / 1000  # Calcula o tempo entre frames

        # Processa eventos de entrada
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                a_funcionar = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    jogador.disparar()
            elif evento.type == pygame.KEYUP:
                if evento.key == pygame.K_SPACE:
                    jogador.definir_animacao("parado")  # Retorna à animação "parado" ao soltar a tecla

        # Verifica as teclas pressionadas para movimento vertical
        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_UP] and jogador.pos_y > 0:
            jogador.pos_y -= 5
            jogador.definir_animacao("andar")
        elif tecla[pygame.K_DOWN] and jogador.pos_y < altura_ecra - 64:
            jogador.pos_y += 5
            jogador.definir_animacao("andar")
#        else:
#            jogador.definir_animacao("parado")  # Muda para "parado" se não estiver a mover

        # Atualiza a posição do fundo para movimento contínuo
        posicao_fundo_x -= velocidade_fundo
        if posicao_fundo_x <= -largura_ecra:
            posicao_fundo_x = 0

        # Desenha o fundo em movimento
        ecra.blit(fundo, (posicao_fundo_x, 0))
        ecra.blit(fundo, (posicao_fundo_x + largura_ecra, 0))

        # Atualiza a posição dos projéteis e do jogador
        jogador.atualizar(delta_tempo)

        # Desenha o jogador e projéteis na tela
        jogador.desenhar(ecra)

        pygame.display.update()

# Função para exibir a pontuação
def mostrar_score():
    print("Exibindo pontuação...")
    pygame.time.wait(2000)  # Espera 2 segundos para simular a exibição da pontuação

# Configuração inicial do menu
def iniciar_jogo():
    ecra = pygame.display.set_mode((largura_ecra, altura_ecra))  # Inicializa a janela do menu
    fundo = pygame.image.load("images/bg.png").convert_alpha() #imagem fundo menu
    fundo = pygame.transform.scale(fundo, (largura_ecra, altura_ecra))

    # Loop principal para exibir o menu e reagir à seleção do jogador
    while True:
        escolha = menu(ecra, largura_ecra, altura_ecra, fundo)  # Chamada correta da função menu
        if escolha == "play":
            play()  # Chama a função play para iniciar o jogo
        elif escolha == "score":
            mostrar_score()  # Chama a função mostrar_score para exibir a pontuação
        elif escolha == "quit":
            break  # Sai do loop e fecha o jogo

    pygame.quit()

# Inicializa o jogo
iniciar_jogo()
