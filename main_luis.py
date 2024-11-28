import pygame
import random
from config import largura_ecra, altura_ecra, velocidade_fundo
from jogador import Jogador
from inimigos import Inimigo
from personagens import AnimacaoParado, AnimacaoAndar, AnimacaoDisparar, AnimacaoAtingido
from menu import menu
from fadeinout import fade_in_out
from sons import Sons

# Variáveis globais para controle do estado do jogo
play = False
pontuacao = 0  # Variável para a pontuação
sons = Sons()  # Inicia o som

def gerar_inimigo():
    tipo = random.choice([1, 2, 3])  # Escolhe aleatoriamente o tipo do inimigo
    pos_y = random.randint(50, altura_ecra - 50)  # Posição vertical aleatória
    return Inimigo(tipo, pos_y)

# Função para exibir a tela de Game Over
def tela_game_over(ecra, fundo):
    global pontuacao
    mensagem = "GAME OVER"
    submensagem = f"Pontuação Final: {pontuacao}"
    opcoes = ["Reiniciar", "Sair"]

    # Exibe a mensagem de Game Over no centro da tela
    fonte_titulo = pygame.font.Font(None, 64)
    texto_mensagem = fonte_titulo.render(mensagem, True, (255, 0, 0))  # Vermelho para o título
    ecra.blit(texto_mensagem, (largura_ecra // 2 - texto_mensagem.get_width() // 2, altura_ecra // 3))

    # Exibe a pontuação final
    fonte_pontuacao = pygame.font.Font(None, 48)
    texto_pontuacao = fonte_pontuacao.render(submensagem, True, (255, 255, 0))  # Amarelo para a pontuação
    ecra.blit(texto_pontuacao, (largura_ecra // 2 - texto_pontuacao.get_width() // 2, altura_ecra // 2))

    # Chama o menu sem o título
    escolha = menu(ecra, largura_ecra, altura_ecra, fundo, opcoes, mensagem, submensagem, exibir_titulo=False)

    # Atualiza a tela para mostrar as informações
    pygame.display.update()

    # Retorna a escolha do jogador
    if escolha == "Reiniciar":
        pontuacao = 0  # Reseta a pontuação ao reiniciar o jogo
        return True  # Reiniciar o jogo
    elif escolha == "Sair":
        pygame.quit()
        exit()

# Função principal do jogo
def play_game():
    global play, pontuacao
    pontuacao = 0  # Reseta a pontuação ao iniciar um novo jogo
    ecra = pygame.display.set_mode((largura_ecra, altura_ecra))  # Inicializa a janela do jogo
    pygame.display.set_caption("Goku Invaders")
    fundo = pygame.image.load("images/bg.png").convert_alpha()
    fundo = pygame.transform.scale(fundo, (largura_ecra, altura_ecra))  # Ajusta o fundo ao tamanho da tela
    sons.tocar_musica_fundo()

    # Inicializa o jogador e define animações
    jogador = Jogador(100, altura_ecra / 2 - 64 / 2)
    jogador.adicionar_animacao("parado", AnimacaoParado())
    jogador.adicionar_animacao("andar", AnimacaoAndar())
    jogador.adicionar_animacao("disparar", AnimacaoDisparar())
    jogador.adicionar_animacao("atingido", AnimacaoAtingido())
    jogador.definir_animacao("parado")  # Necessária para iniciar a animação
    jogador.vida = 100
    jogador.disparando = False  # Adiciona estado para controlar o disparo

    inimigos = []  # Lista para armazenar inimigos
    relogio = pygame.time.Clock()  # Inicia o relógio para controlar o FPS
    posicao_fundo_x = 0  # Posição inicial do fundo
    a_funcionar = True

    # Loop principal do jogo
    while a_funcionar:
        delta_tempo = relogio.tick(60) / 1000  # Calcula o tempo entre frames, 60hz

        # Gera inimigos aleatórios periodicamente
        if random.randint(1, 100) < 2:  # Probabilidade de gerar um inimigo a cada frame
            inimigos.append(gerar_inimigo())

        # Processa eventos de entrada
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                a_funcionar = False
                play = False  # Define play como False para retornar ao menu
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and not jogador.disparando:
                    jogador.disparar()  # Ativa o disparo
                    jogador.definir_animacao("disparar")
                    jogador.disparando = True  # Define o estado como disparando
                elif evento.key == pygame.K_ESCAPE:  # Verifica se a tecla Esc foi pressionada
                    pause_menu(ecra, fundo)  # Chama a função de pausa
                    jogador.definir_animacao("parado")  # Restaura o estado após a pausa
            elif evento.type == pygame.KEYUP:
                if evento.key == pygame.K_SPACE:
                    jogador.disparando = False  # Libera o estado de disparo
                    tecla = pygame.key.get_pressed()
                    # Define a animação correta após o disparo
                    if tecla[pygame.K_UP] or tecla[pygame.K_DOWN]:
                        jogador.definir_animacao("andar")
                    else:
                        jogador.definir_animacao("parado")

        # Verifica as teclas pressionadas para movimento vertical
        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_UP] and jogador.pos_y > 0:
            jogador.pos_y -= 5
            if not jogador.disparando:  # Não muda a animação se estiver disparando
                jogador.definir_animacao("andar")
        elif tecla[pygame.K_DOWN] and jogador.pos_y < altura_ecra - 64:
            jogador.pos_y += 5
            if not jogador.disparando:  # Não muda a animação se estiver disparando
                jogador.definir_animacao("andar")

        # Atualiza a posição do fundo para movimento contínuo
        posicao_fundo_x -= velocidade_fundo
        if posicao_fundo_x <= -largura_ecra:
            posicao_fundo_x = 0

        # Desenha o fundo em movimento
        ecra.blit(fundo, (posicao_fundo_x, 0))
        ecra.blit(fundo, (posicao_fundo_x + largura_ecra, 0))

        for projetil in jogador.projeteis[:]:  # Cópia para remoção segura
            for inimigo in inimigos[:]:  # Outra cópia para remoção segura
                if inimigo.verificar_colisao(projetil):
                    jogador.projeteis.remove(projetil)  # Remove o projétil
                    inimigo.vidas -= 1  # Reduz a vida do inimigo
                    sons.tocar_disparo()

                    if inimigo.vidas <= 0:  # Se a vida do inimigo chegar a zero
                        inimigos.remove(inimigo)  # Remove o inimigo da lista
                        pontuacao += 10  # Adiciona pontos
                    break 

# Atualiza e desenha cada inimigo
        for inimigo in inimigos[:]:
            inimigo.atualizar(delta_tempo, jogador)
            inimigo.desenhar(ecra)

    # Verifica colisão com o jogador
        for inimigo in inimigos[:]:  # Cópia da lista para remoção segura
            if inimigo.vivo and pygame.Rect(inimigo.pos_x, inimigo.pos_y, 50, 50).colliderect(
            pygame.Rect(jogador.pos_x, jogador.pos_y, 50, 50)):
                dano = {1: 30, 2: 50, 3: 70}[inimigo.tipo]  # Define o dano dependendo do tipo do inimigo
                jogador.vida -= dano  # Diminui a vida do jogador
                sons.tocar_colisao()  # Toca som de colisão

                if jogador.vida <= 0:
                    print("Jogador morreu!")
                    a_funcionar = False  # Termina o jogo se a vida do jogador acabar
                    sons.tocar_game_over()  # Toca som de game over
                if tela_game_over(ecra, fundo):
                    play_game()  # Reinicia o jogo
                else:
                    play = False  # Exibe a tela de Game Over


# Atualiza a posição dos projéteis e do jogador
        jogador.atualizar(delta_tempo)
        jogador.desenhar(ecra)

# Exibe a vida e pontuação do jogador na tela
        fonte = pygame.font.Font(None, 36)
        vida_texto = fonte.render(f"Vida: {jogador.vida}", True, (255, 0, 0))
        score_texto = fonte.render(f"Score: {pontuacao}", True, (255, 255, 0))
        ecra.blit(vida_texto, (10, 10))
        ecra.blit(score_texto, (largura_ecra - 150, 10))
        pygame.display.update()



# Função para exibir a pontuação ao final
def mostrar_score():
    global pontuacao
    print(f"Sua pontuação final foi: {pontuacao}")  # Substitua por exibição gráfica, se necessário
    pygame.time.wait(2000)  # Espera 2 segundos para simular a exibição da pontuação

# Função de pausa que exibe o menu de pausa
def pause_menu(ecra, fundo):
    global play
    while True:
        # Exibe o menu com título (ou sem título, dependendo da escolha)
        escolha = menu(ecra, largura_ecra, altura_ecra, fundo, ["Continuar", "Score", "Quit"], exibir_titulo=True)
        if escolha == "Continuar":
            return  # Apenas retorna, mantendo o estado do jogo
        elif escolha == "Score":
            mostrar_score()
        elif escolha == "Quit":
            pygame.quit()
            exit()

# Configuração inicial do menu
def iniciar_jogo():
    global play
    ecra = pygame.display.set_mode((largura_ecra, altura_ecra))  # Inicializa a janela do menu
    fundo = pygame.image.load("images/try1.jpg").convert_alpha()  # Carrega a imagem de fundo
    fundo = pygame.transform.smoothscale(fundo, (largura_ecra, altura_ecra))  # Redimensiona suavemente
    sons.tocar_musica_menu()

    # Loop principal para exibir o menu e reagir à seleção do jogador
    while True:
        # Exibe o menu inicial com título
        escolha = menu(ecra, largura_ecra, altura_ecra, fundo, ["Play", "Score", "Quit"])
        if escolha == "Play":
            fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 20)
            play = True
            play_game()  # Inicia o jogo
            fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 20)
        elif escolha == "Score":
            mostrar_score()
        elif escolha == "Quit":
            pygame.quit()
            break

# Inicializa o jogo
iniciar_jogo()
