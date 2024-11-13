import pygame
from config import largura_ecra, altura_ecra, velocidade_fundo
from jogador import Jogador
from personagens import AnimacaoParado, AnimacaoAndar, AnimacaoDisparar, AnimacaoAtingido
from menu import menu
from fadeinout import fade_in_out

# Função principal do jogo
def play_game():
    global play
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
    jogador.definir_animacao("parado")  # Necessária para iniciar a animação

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

                elif evento.key == pygame.K_ESCAPE:  # Verifica se a tecla Esc foi pressionada
                    play = True
                    return    
            
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
    print("Exibindo pontuação...")  # Aqui você poderia substituir por código para exibir a pontuação na tela
    pygame.time.wait(2000)  # Espera 2 segundos para simular a exibição da pontuação

# Configuração inicial do menu
def iniciar_jogo():
    global play
    ecra = pygame.display.set_mode((largura_ecra, altura_ecra))  # Inicializa a janela do menu
    fundo = pygame.image.load("images/bg.png").convert_alpha()  # Imagem de fundo para o menu
    fundo = pygame.transform.scale(fundo, (largura_ecra, altura_ecra))

    

    # Loop principal para exibir o menu e reagir à seleção do jogador
    while True:
        escolha = menu(ecra, largura_ecra, altura_ecra, fundo)  # Chama a função menu e aguarda a escolha do jogador
        if escolha == "play" or escolha == "resume":
            fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 20)
            play_game()  # Inicia o jogo

            play = True
            # Executa o fade-in quando retorna ao menu após o jogo
            fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 20)
            if play == "resume":
                continue
        elif escolha == "score":
            fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 20)
            mostrar_score()  # Exibe a pontuação
            fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 20)
        elif escolha == "quit":
            fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 20)
            break  # Sai do loop e fecha o jogo

    pygame.quit()

# Inicializa o jogo
iniciar_jogo()
