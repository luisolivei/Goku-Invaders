import pygame
import random
from config import largura_ecra, altura_ecra, velocidade_fundo,caminho_fonte
from jogador import Jogador
from inimigos import Inimigo
from personagens import AnimacaoParado, AnimacaoAndar, AnimacaoDisparar, AnimacaoAtingido, AnimacaoDispararEspecial
from menu import menu
from fadeinout import fade_in_out
from sons import Sons
from niveis import carregar_fundo,gerar_inimigo,mostrar_historia,mostrar_tela_final

# Variáveis globais para controle do estado do jogo
play = False
pontuacao = 0  # Variável para a pontuação
nivel = 1  # Variável para o nível atual
sons = Sons()  # Inicia o som
 
def tela_game_over(ecra, fundo):
    fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 60)
    global pontuacao
    mensagem = "GAME OVER"
    submensagem = f"Score: {pontuacao}"
    opcoes = ["Reiniciar", "Sair"]

    try:
        # Carregar a imagem de Game Over
        imagem_game_over = pygame.image.load("images/11.png").convert_alpha()  # Caminho para a imagem
        imagem_game_over = pygame.transform.scale(imagem_game_over, (largura_ecra, altura_ecra))  # Ajusta a imagem para a tela
    except pygame.error as e:
        print(f"Erro ao carregar imagem: {e}")
        return  # Caso a imagem não carregue, não continua a função

    # Exibe a imagem de fundo
    ecra.blit(imagem_game_over, (0, 0))

    # Exibe a mensagem de Game Over no centro da tela
    fonte_titulo = pygame.font.Font(None, 64)
    texto_mensagem = fonte_titulo.render(mensagem, True, (255, 165, 0))  # Cor para o título
    ecra.blit(texto_mensagem, (largura_ecra // 2 - texto_mensagem.get_width() // 2, altura_ecra // 3))

    # Exibe a pontuação final
    fonte_pontuacao = pygame.font.Font(None, 48)
    texto_pontuacao = fonte_pontuacao.render(submensagem, True, (255, 255, 0))  # Cor para a pontuação
    ecra.blit(texto_pontuacao, (largura_ecra // 2 - texto_pontuacao.get_width() // 2, altura_ecra // 2))

    # Chama o menu sem o título
    escolha = menu(ecra, largura_ecra, altura_ecra, fundo, opcoes, mensagem, submensagem, exibir_titulo=False)

    fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 20)

    pygame.display.update()  # Atualiza a tela para garantir que a imagem seja visível

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
    sons.tocar_musica_fundo(nivel)

    # Inicializa o jogador e define animações
    jogador = Jogador(100, altura_ecra / 2 - 64 / 2)
    jogador.adicionar_animacao("parado", AnimacaoParado())
    jogador.adicionar_animacao("andar", AnimacaoAndar())
    jogador.adicionar_animacao("disparar", AnimacaoDisparar())
    jogador.adicionar_animacao("atingido", AnimacaoAtingido())
    jogador.adicionar_animacao("disparar2", AnimacaoDispararEspecial())
    jogador.definir_animacao("parado")  # Necessária para iniciar a animação
    jogador.vida = 100
    jogador.disparando = False  # Adiciona estado para controlar o disparo
    jogador.temporizador_atingido = 0  # Temporizador para controlar a animação "atingido"

    inimigos = []  # Lista para armazenar inimigos
    relogio = pygame.time.Clock()  # Inicia o relógio para controlar o FPS
    posicao_fundo_x = 0  # Posição inicial do fundo
    a_funcionar = True

    # Loop principal do jogo
    while a_funcionar:
        delta_tempo = relogio.tick(60) / 1000  # Calcula o tempo entre frames, 60hz

        # Gera inimigos aleatórios periodicamente
        # Aumenta a probabilidade com o nível, mas limita o número de inimigos
        probabilidade_inimigos = max(1, 150 + nivel * 20)  # Reduz a chance de gerar inimigos com o aumento de nível
        if random.randint(1, probabilidade_inimigos) == 1:
            inimigos.append(gerar_inimigo(nivel))

# Verifica se o jogador atingiu o próximo nível
    # Verifica se o jogador atingiu o próximo nível
        if nivel == 1 and pontuacao >= 800:  # Nível 1: 800 pontos para avançar
            nivel += 1
            if nivel > 3:  # Limita o jogo ao nível 3
                mostrar_tela_final(ecra)  # Exibe a tela de "Jogo Completo"
                iniciar_jogo()  # Volta ao menu inicial
                return  # Finaliza o loop principal
            fundo = carregar_fundo(nivel)  # Muda o fundo conforme o nível
            print(f"Parabéns! Você avançou para o nível {nivel}")
            mostrar_historia(ecra, nivel)

            # Toca a música correspondente ao nível
            sons.tocar_musica_fundo(nivel)

            # Limpar inimigos e projéteis
            inimigos.clear()
            jogador.projeteis.clear()

            jogador.disparando = False
            jogador.definir_animacao("parado")

        elif nivel == 2 and pontuacao >= 2000:  # Nível 2: 2000 pontos para avançar
            nivel += 1
            if nivel > 3:  # Limita o jogo ao nível 3
                mostrar_tela_final(ecra)  # Exibe a tela de "Jogo Completo"
                iniciar_jogo()  # Volta ao menu inicial
                return  # Finaliza o loop principal
            fundo = carregar_fundo(nivel)  # Muda o fundo conforme o nível
            print(f"Parabéns! Você avançou para o nível {nivel}")
            mostrar_historia(ecra, nivel)

            # Toca a música correspondente ao nível
            sons.tocar_musica_fundo(nivel)

            # Limpar inimigos e projéteis
            inimigos.clear()
            jogador.projeteis.clear()

            jogador.disparando = False
            jogador.definir_animacao("parado")

        elif nivel == 3 and pontuacao >= 3550:  # Nível 3: 3550 pontos para avançar
            nivel += 1
            if nivel > 3:  # Limita o jogo ao nível 3
                mostrar_tela_final(ecra)  # Exibe a tela de "Jogo Completo"
                iniciar_jogo()  # Volta ao menu inicial
                return  # Finaliza o loop principal
            fundo = carregar_fundo(nivel)  # Muda o fundo conforme o nível
            print(f"Parabéns! Você avançou para o nível {nivel}")
            mostrar_historia(ecra, nivel)

            # Toca a música correspondente ao nível
            sons.tocar_musica_fundo(nivel)

            # Limpar inimigos e projéteis
            inimigos.clear()
            jogador.projeteis.clear()

            jogador.disparando = False
            jogador.definir_animacao("parado")


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
                elif evento.key == pygame.K_x:
                    if jogador.ataque_especial_desbloqueado:  # Apenas executa se desbloqueado
                        jogador.disparar2()
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
                elif evento.key == pygame.K_x:
                    if jogador.projetil2:  # Retorna ao estado parado após soltar X
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

        # Atualização e colisões de projéteis normais
        for projetil in jogador.projeteis[:]:  # Cópia para remoção segura
            for inimigo in inimigos[:]:  # Outra cópia para remoção segura
                if inimigo.verificar_colisao(projetil):
                    jogador.projeteis.remove(projetil)  # Remove o projétil
                    sons.tocar_disparo()

                    # Adiciona pontuação somente se o inimigo foi morto
                    if inimigo.vidas <= 0 and inimigo.animacao_atual == "morto":
                        pontuacao += {1: 50, 2: 100, 3: 150}[inimigo.tipo]
                        jogador.incrementar_kill()  # Incrementa o contador de kills para desbloqueio do ataque especial
                    break

        # Atualizar e desenhar o Projetil2
        if jogador.projetil2:
            jogador.projetil2.atualizar(delta_tempo, tecla[pygame.K_x])  # Passa estado da tecla X
            jogador.projetil2.desenhar(ecra)

            # Colisões do Projetil2 com inimigos
            for inimigo in inimigos[:]:
                if pygame.Rect(jogador.projetil2.raio_fim_x, jogador.projetil2.y, 64, 32).colliderect(
                    pygame.Rect(inimigo.pos_x, inimigo.pos_y, 50, 50)
                ):
                    inimigo.vidas -= 10
                    if inimigo.vidas <= 0:
                        pontuacao += {1: 50, 2: 100, 3: 150}[inimigo.tipo]
                        jogador.incrementar_kill()  # Incrementa o contador de kills caso inimigo morra
                        inimigos.remove(inimigo)  # Remove o inimigo morto

        # Atualiza e desenha cada inimigo
        for inimigo in inimigos[:]:
            estado = inimigo.atualizar(delta_tempo, jogador)
            inimigo.desenhar(ecra)

            if estado == "fora":  # Saiu pela esquerda
                pontuacao -= {1: 50, 2: 100, 3: 150}[inimigo.tipo]
                inimigos.remove(inimigo)

        # Verifica colisão com o jogador
        # Atualiza o temporizador da animação "atingido"
        if jogador.temporizador_atingido > 0:
            jogador.temporizador_atingido -= delta_tempo
            if jogador.temporizador_atingido <= 0:
                jogador.definir_animacao("parado")  # Retorna para a animação padrão
        for inimigo in inimigos[:]:
            if inimigo.vivo and pygame.Rect(inimigo.pos_x, inimigo.pos_y, 50, 50).colliderect(
                pygame.Rect(jogador.pos_x, jogador.pos_y, 50, 50)
            ):
                dano = {1: 30, 2: 50, 3: 70}[inimigo.tipo]  # Define o dano dependendo do tipo do inimigo
                jogador.vida -= dano  # Diminui a vida do jogador
                sons.tocar_colisao()  # Toca som de colisão

                # Remove o inimigo após colisão com o jogador
                inimigos.remove(inimigo)
                
                # Ativa a animação "atingido" no jogador
                jogador.definir_animacao("atingido")
                jogador.temporizador_atingido = 0.3  # Define a duração da animação "atingido" (0.5 segundos)


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
        fonte = pygame.font.Font(caminho_fonte, 40)  # Define o tamanho da fonte ()
        vida_texto = fonte.render(f"Vida: {jogador.vida}", True, (255, 0, 0))
        score_texto = fonte.render(f"Score: {pontuacao}", True, (255, 255, 0))
        nivel_texto = fonte.render(f"Nível: {nivel}", True, (255, 165, 0))
        ecra.blit(vida_texto, (10, 10))
        ecra.blit(score_texto, (largura_ecra - 190, 10))
        ecra.blit(nivel_texto, (largura_ecra - 470, 8))  # Exibe o nível abaixo da vida
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
