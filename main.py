import pygame
import random
from config import largura_ecra, altura_ecra, velocidade_fundo
from jogador import Jogador
from inimigos import Inimigo
from personagens import AnimacaoParado, AnimacaoAndar, AnimacaoDisparar, AnimacaoAtingido
from menu import menu
from fadeinout import fade_in_out
from sons import Sons

# Variável global para controle do estado do jogo
play = False
sons = Sons() # Inicia o som

# Função para gerar inimigos de forma aleatória
def gerar_inimigo():
    tipo = random.choice([1, 2, 3])  # Escolhe aleatoriamente o tipo do inimigo
    pos_y = random.randint(50, altura_ecra - 50)  # Posição vertical aleatória
    return Inimigo(tipo, pos_y)

# Função principal do jogo
def play_game():
    global play

    # Configurações para o fundo e ambiente de jogo
    ecra = pygame.display.set_mode((largura_ecra, altura_ecra))  # Inicializa a janela do jogo
    pygame.display.set_caption("Goku Invaders")
    fundo = pygame.image.load("images/bg.png").convert_alpha()
    fundo = pygame.transform.scale(fundo, (largura_ecra, altura_ecra))  # Ajusta o fundo ao tamanho da tela
    

    # Toca a música de fundo
    sons.tocar_musica_fundo()

    # Inicializa o jogador e define animações
    jogador = Jogador(100, altura_ecra / 2 - 64 / 2)  # Define a posição inicial do jogador
    jogador.adicionar_animacao("parado", AnimacaoParado())
    jogador.adicionar_animacao("andar", AnimacaoAndar())
    jogador.adicionar_animacao("disparar", AnimacaoDisparar())
    jogador.adicionar_animacao("atingido", AnimacaoAtingido())
    jogador.definir_animacao("parado")  # Necessária para iniciar a animação

    # Define a vida inicial do jogador
    jogador.vida = 100

    inimigos = []  # Lista para armazenar inimigos
    relogio = pygame.time.Clock()  # Inicia o relógio para controlar o FPS
    posicao_fundo_x = 0  # Posição inicial do fundo

    a_funcionar = True

    # Loop principal do jogo
    while a_funcionar:
        delta_tempo = relogio.tick(60) / 1000  # Calcula o tempo entre frames, 60hrz

        # Gera inimigos aleatórios periodicamente
        if random.randint(1, 100) < 2:  # Probabilidade de gerar um inimigo a cada frame
            inimigos.append(gerar_inimigo())

        # Processa eventos de entrada
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                a_funcionar = False
                play = False  # Define play como False para retornar ao menu
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    jogador.disparar()
                    jogador.definir_animacao("disparar")  # Define a animação de disparo

                elif evento.key == pygame.K_ESCAPE:  # Verifica se a tecla Esc foi pressionada
                    play = False
                    return  # Retorna ao menu
            
            elif evento.type == pygame.KEYUP:
                if evento.key == pygame.K_SPACE:
                    # Após soltar a tecla de disparo, retorna à animação de andar ou parado
                    tecla = pygame.key.get_pressed()
                    if tecla[pygame.K_UP] or tecla[pygame.K_DOWN]:
                        jogador.definir_animacao("andar")  # Continua com a animação de movimento
                    else:
                        jogador.definir_animacao("parado")  # Retorna à animação parado se não houver movimento

        # Verifica as teclas pressionadas para movimento vertical
        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_UP] and jogador.pos_y > 0:
            jogador.pos_y -= 5
            if not tecla[pygame.K_SPACE]:
                jogador.definir_animacao("andar")
        elif tecla[pygame.K_DOWN] and jogador.pos_y < altura_ecra - 64:
            jogador.pos_y += 5
            if not tecla[pygame.K_SPACE]:
                jogador.definir_animacao("andar")

        # Atualiza a posição do fundo para movimento contínuo
        posicao_fundo_x -= velocidade_fundo
        if posicao_fundo_x <= -largura_ecra:
            posicao_fundo_x = 0

        # Desenha o fundo em movimento
        ecra.blit(fundo, (posicao_fundo_x, 0))
        ecra.blit(fundo, (posicao_fundo_x + largura_ecra, 0))

        # Atualiza e desenha cada inimigo
        for inimigo in inimigos[:]:  # Cópia da lista para remoção segura
            inimigo.atualizar(delta_tempo, jogador)
            inimigo.desenhar(ecra)

            # Verifica colisão do inimigo com o jogador
            if pygame.Rect(inimigo.pos_x, inimigo.pos_y, 50, 50).colliderect(
                pygame.Rect(jogador.pos_x, jogador.pos_y, 50, 50)):
                # Diminui a vida do jogador com base no tipo do inimigo
                dano = {1: 30, 2: 50, 3: 70}[inimigo.tipo] 
                jogador.vida -= dano
                inimigos.remove(inimigo)  # Remove o inimigo após a colisão
                sons.tocar_colisao() # Toca som de colisao
                if jogador.vida <= 0:
                    print("Jogador morreu!")
                    a_funcionar = False  # Termina o jogo se a vida do jogador acabar
                    sons.tocar_game_over()
            

            # Verifica colisão com projéteis do jogador
            for projetil in jogador.projeteis[:]:
                if inimigo.verificar_colisao(projetil):
                    jogador.projeteis.remove(projetil)  # Remove o projétil que colidiu
                    sons.tocar_disparo()  # Toca som de disparo
            

            # Remove inimigo se estiver morto
            if not inimigo.vivo:
                inimigos.remove(inimigo)

        # Atualiza a posição dos projéteis e do jogador
        jogador.atualizar(delta_tempo)

        # Desenha o jogador e projéteis na tela
        jogador.desenhar(ecra)

        # Exibe a vida do jogador na tela
        fonte = pygame.font.Font(None, 36)
        vida_texto = fonte.render(f"Vida: {jogador.vida}", True, (255, 0, 0))
        ecra.blit(vida_texto, (10, 10))

        pygame.display.update()

# Função para exibir a pontuação
def mostrar_score():
    print("Exibindo pontuação...")  # Aqui poderias substituir por código para exibir a pontuação na tela
    pygame.time.wait(2000)  # Espera 2 segundos para simular a exibição da pontuação

# Configuração inicial do menu
def iniciar_jogo():
    global play
    ecra = pygame.display.set_mode((largura_ecra, altura_ecra))  # Inicializa a janela do menu
    fundo = pygame.image.load("images/bg.png").convert_alpha()  # Imagem de fundo para o menu
    fundo = pygame.transform.scale(fundo, (largura_ecra, altura_ecra))  # Ajusta a imagem de fundo ao tamanho da tela
    sons.tocar_musica_menu()
    
    # Loop principal para exibir o menu e reagir à seleção do jogador
    while True:
        escolha = menu(ecra, largura_ecra, altura_ecra, fundo)  # Chama a função menu e aguarda a escolha do jogador
        
        
        if escolha == "play":
            fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 20)  # Executa o fade-in ao iniciar o jogo
            play = True
            play_game()  # Inicia o jogo

            # Executa o fade-out ao retornar ao menu após o jogo
            fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 20)
            if play:  # Se play estiver True, continua o loop para retornar ao jogo
                continue
        elif escolha == "score":
            fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 20)
            mostrar_score()  # Exibe a pontuação
            fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 20)
        elif escolha == "quit":
            fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 20)
            break  # Sai do loop e fecha o jogo

            # Para a música ao sair do jogo
            sons.parar_musica_fundo()

    pygame.quit()

# Inicializa o jogo
iniciar_jogo()