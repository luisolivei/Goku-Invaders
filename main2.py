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
nivel = 1  # Variável para o nível atual
sons = Sons()  # Inicia o som

def mostrar_tela_final(ecra):
    """
    Exibe uma tela de conclusão com mensagem de "Jogo Completo" e créditos.
    """
    fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 20)
    # Define o fundo da tela final
    fundo_final = pygame.image.load("images/try2.jpg").convert_alpha()  # Imagem de fundo final
    fundo_final = pygame.transform.scale(fundo_final, (largura_ecra, altura_ecra))
    ecra.blit(fundo_final, (0, 0))

    # Exibe o texto "Jogo Completo"
    fonte_titulo = pygame.font.Font(None, 64)
    titulo = fonte_titulo.render("Jogo Completo!", True, (255, 255, 0))  # Texto amarelo
    ecra.blit(titulo, (largura_ecra // 2 - titulo.get_width() // 2, altura_ecra // 3))

    # Exibe os créditos
    fonte_creditos = pygame.font.Font(None, 36)
    creditos = [
        "Obrigado por jogar!",
        "Criado por: Tiago Bastos, Luis Oliveira, Carina Gameiro, Aleff Almeida e Guilherme Borges",
        "Desenvolvido em Python com Pygame"
    ]
    for i, linha in enumerate(creditos):
        texto_creditos = fonte_creditos.render(linha, True, (255, 255, 0))  # Texto amarelo
        ecra.blit(texto_creditos, (largura_ecra // 2 - texto_creditos.get_width() // 2, altura_ecra // 2 + i * 40))

    # Atualiza a tela e espera alguns segundos
    pygame.display.update()
    pygame.time.wait(10000)  # Aguarda 5 segundos antes de voltar ao menu

    fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 20)


def mostrar_historia(ecra, nivel):
    """
    Função que exibe uma tela de história com uma imagem e um botão 'Continuar'.
    """
    fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 20)
    # Carregar a imagem da história baseada no nível
    if nivel == 1:
        imagem_historia = pygame.image.load("images/try4.jpg").convert_alpha()
        texto_historia = "Você é o herói que precisa salvar o universo!"
    elif nivel == 2:
        imagem_historia = pygame.image.load("images/bg2.png").convert_alpha()
        texto_historia = "Avançando para um novo desafio... Prepare-se!"
    elif nivel == 3:
        imagem_historia = pygame.image.load("images/bg3.png").convert_alpha()
        texto_historia = "O confronto final se aproxima!" 
    
    
    imagem_historia = pygame.transform.scale(imagem_historia, (largura_ecra, altura_ecra))  # Ajusta a imagem ao tamanho da tela

    # Desenha a imagem de fundo
    ecra.blit(imagem_historia, (0, 0))

    # Exibe o texto da história
    fonte = pygame.font.Font(None, 48)
    texto = fonte.render(texto_historia, True, (255, 255, 255))  # Texto em branco
    ecra.blit(texto, (largura_ecra // 2 - texto.get_width() // 2, altura_ecra // 3))

    # Desenha o botão "Continuar"
    fonte_botao = pygame.font.Font(None, 36)
    texto_botao = fonte_botao.render("Continuar", True, (255, 0, 0))  # Texto do botão em vermelho
    botao_rect = pygame.Rect(largura_ecra // 2 - texto_botao.get_width() // 2, altura_ecra // 2 + 100, texto_botao.get_width(), texto_botao.get_height())
    
    pygame.draw.rect(ecra, (0, 0, 0), botao_rect)  # Fundo do botão (preto)
    ecra.blit(texto_botao, (largura_ecra // 2 - texto_botao.get_width() // 2, altura_ecra // 2 + 100))  # Texto do botão

    pygame.display.update()  # Atualiza a tela

    # Espera até que o jogador clique no botão "Continuar"
    continuar = False
    while not continuar:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_rect.collidepoint(evento.pos):  # Verifica se o clique foi dentro do botão
                    continuar = True  # Quando o jogador clica, a história termina e o jogo continua

    fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 20)


# Função para carregar o fundo de acordo com o nível
def carregar_fundo(nivel):
    if nivel == 1:
        fundo = pygame.image.load("images/bg3.png").convert_alpha()  # Fundo do nível 1
    elif nivel == 2:
        fundo = pygame.image.load("images/bg2.png").convert_alpha()  # Fundo do nível 2
    elif nivel == 3:
        fundo = pygame.image.load("images/bg.png").convert_alpha()  # Fundo do nível 3
    else:
        fundo = pygame.image.load("images/bg.png").convert_alpha()  # Fundo padrão

    # Redimensiona o fundo para o tamanho da tela
    return pygame.transform.scale(fundo, (largura_ecra, altura_ecra)) 



def gerar_inimigo(nivel):
    if nivel == 1:
        tipo = random.choice([1, 2])  # Apenas inimigos do tipo 1 e 2 no nível 1
    elif nivel == 2:
        tipo = random.choice([2, 3])  # Apenas inimigos do tipo 2 e 3 no nível 2
    elif nivel == 3:
        tipo = 3  # Apenas inimigos do tipo 3 no nível 3
    else:
        tipo = random.choice([1, 2, 3])  # Para níveis superiores, inclui todos os tipos
    
    pos_y = random.randint(50, altura_ecra - 50)  # Posição vertical aleatória
    return Inimigo(tipo, pos_y)

# Função para exibir a tela de Game Over
def tela_game_over(ecra, fundo):
    fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 20)
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

    fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 20)

    # Atualiza a tela para mostrar as informações
    #pygame.display.update()

    # Retorna a escolha do jogador
    if escolha == "Reiniciar":
        pontuacao = 0  # Reseta a pontuação ao reiniciar o jogo
        return True  # Reiniciar o jogo
    elif escolha == "Sair":
        pygame.quit()
        exit()

# Função principal do jogo

def play_game():
    global play, pontuacao, nivel
    pontuacao = 0  # Reseta a pontuação ao iniciar um novo jogo
    nivel = 1  # Reseta o nível ao iniciar
    ecra = pygame.display.set_mode((largura_ecra, altura_ecra))  # Inicializa a janela do jogo
    pygame.display.set_caption("Goku Invaders")
    fundo = carregar_fundo(nivel)  # Carrega o fundo de acordo com o nível
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
        # Aumenta a probabilidade com o nível, mas limita o número de inimigos
        probabilidade_inimigos = max(1, 150 - nivel * 20)  # Reduz a chance de gerar inimigos com o aumento de nível
        if random.randint(1, probabilidade_inimigos) == 1:
            inimigos.append(gerar_inimigo(nivel))

# Verifica se o jogador atingiu o próximo nível
        if pontuacao >= nivel * 500:  # A cada 500 pontos por nível
            nivel += 1
            if nivel > 3:  # Limita o jogo ao nível 3
                mostrar_tela_final(ecra)  # Exibe a tela de "Jogo Completo"
                iniciar_jogo()  # Volta ao menu inicial
                return  # Finaliza o loop principal
            fundo = carregar_fundo(nivel)  # Muda o fundo conforme o nível
            print(f"Parabéns! Você avançou para o nível {nivel}")
            mostrar_historia(ecra, nivel)

    # Limpar inimigos
            inimigos.clear()



        # Processa eventos de entrada
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                a_funcionar = False
                play = False  # Define play como False para retornar ao menu
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and not jogador.disparando:
                    jogador.disparar()  # Ativa o disparo
                    jogador.definir_animacao("disparar")
                    jogador.disparando = True
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

        # Desenha o fundo em movimento contínuo (duas camadas de fundo)
        ecra.blit(fundo, (posicao_fundo_x, 0))  # A primeira camada do fundo
        ecra.blit(fundo, (posicao_fundo_x + largura_ecra, 0))  # A segunda camada do fundo

        for projetil in jogador.projeteis[:]:  # Cópia para remoção segura
            for inimigo in inimigos[:]:  # Outra cópia para remoção segura
                if inimigo.verificar_colisao(projetil):
                    jogador.projeteis.remove(projetil)  # Remove o projétil
                    sons.tocar_disparo()

                    # Adiciona pontuação somente se o inimigo foi morto
                    if inimigo.vidas <= 0 and inimigo.animacao_atual == "morto":
                        pontuacao += {1: 50, 2: 100, 3: 150}[inimigo.tipo]
                    break

        # Atualiza e desenha cada inimigo
        for inimigo in inimigos[:]:
            estado = inimigo.atualizar(delta_tempo, jogador)
            inimigo.desenhar(ecra)

            if estado == "fora":  # Saiu pela esquerda
                pontuacao -= {1: 50, 2: 100, 3: 150}[inimigo.tipo]
                inimigos.remove(inimigo)

        # Verifica colisão com o jogador
        for inimigo in inimigos[:]:
            if inimigo.vivo and pygame.Rect(inimigo.pos_x, inimigo.pos_y, 50, 50).colliderect(
                pygame.Rect(jogador.pos_x, jogador.pos_y, 50, 50)
            ):
                dano = {1: 30, 2: 50, 3: 70}[inimigo.tipo]  # Define o dano dependendo do tipo do inimigo
                jogador.vida -= dano  # Diminui a vida do jogador
                sons.tocar_colisao()  # Toca som de colisão

                # Remove o inimigo após colisão com o jogador
                inimigos.remove(inimigo)

        # Verifica colisões do jogador
        if jogador.vida <= 0:
            if tela_game_over(ecra, fundo):
                play_game()
            else:
                play = False

        # Atualiza a posição dos projéteis e do jogador
        jogador.atualizar(delta_tempo)
        jogador.desenhar(ecra)

        # Exibe a vida, pontuação e nível na tela
        fonte = pygame.font.Font(None, 36)
        vida_texto = fonte.render(f"Vida: {jogador.vida}", True, (255, 0, 0))
        score_texto = fonte.render(f"Score: {pontuacao}", True, (255, 255, 0))
        nivel_texto = fonte.render(f"Nível: {nivel}", True, (0, 255, 0))
        ecra.blit(vida_texto, (10, 10))
        ecra.blit(score_texto, (largura_ecra - 150, 10))
        ecra.blit(nivel_texto, (10, 50))  # Exibe o nível abaixo da vida
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
            fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 20)
            pygame.quit()
            break

# Inicializa o jogo
iniciar_jogo()
