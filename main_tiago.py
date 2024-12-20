#main.py é ficheiro principal do jogo

import pygame
import random
from config import largura_ecra, altura_ecra, velocidade_fundo,caminho_fonte
from jogador import Jogador
from inimigos import InimigoFinal
from personagens import AnimacaoParado, AnimacaoAndar, AnimacaoDisparar, AnimacaoAtingido, AnimacaoDispararEspecial
from menu import menu, pause_menu, tela_game_over
from fadeinout import fade_in_out
from sons import Sons
from niveis import carregar_fundo,gerar_inimigo,mostrar_historia,mostrar_tela_final,reproduzir_video,avancar_nivel
from highscore import mostrar_highscore
from Instrucoes import tela_instrucoes

# Variáveis globais para controle do estado do jogo
play = False
pontuacao = 0  # Variável para a pontuação
nivel = 1  # Variável para o nível atual
sons = Sons()  # Inicia o som

# Função principal do jogo

def play_game():
    global play, pontuacao, nivel, tempo_inicio_jogo
    tempo_inicio_jogo = 0
    pontuacao = 0  # Reseta a pontuação ao iniciar um novo jogo
    nivel = 1  # Reseta o nível ao iniciar
    ecra = pygame.display.set_mode((largura_ecra, altura_ecra))  # Inicializa a janela do jogo
    pygame.display.set_caption("Goku Invaders")
    mostrar_historia(ecra, nivel)
    fundo = carregar_fundo(nivel)  # Carrega o fundo de acordo com o nível
    fundo = pygame.transform.scale(fundo, (largura_ecra, altura_ecra))  # Ajusta o fundo ao tamanho da tela
    sons.tocar_musica_fundo(nivel)

    # Inicializa o jogador e define animações
    jogador = Jogador(100, altura_ecra / 2 - 64 / 2)
    jogador.adicionar_animacao("parado", AnimacaoParado())
    jogador.adicionar_animacao("andar", AnimacaoAndar())
    jogador.adicionar_animacao("disparar", AnimacaoDisparar())
    jogador.adicionar_animacao("atingido", AnimacaoAtingido())
    jogador.adicionar_animacao("disparar2",AnimacaoDispararEspecial())
    jogador.definir_animacao("parado")  # Necessária para iniciar a animação
    jogador.vida = 100
    jogador.disparando = False  # Adiciona estado para controlar o disparo
    jogador.temporizador = 0  # Temporizador para controlar a tempo de animaçoes com necessidade de reset para "parado"

    inimigos = []  # Lista para armazenar inimigos
    inimigo_final = None  # Inicializa a variável no início da função  
    relogio = pygame.time.Clock()  # Inicia o relógio para controlar o FPS
    posicao_fundo_x = 0  # Posição inicial do fundo
    a_funcionar = True

    # Loop principal do jogo
    while a_funcionar:
        delta_tempo = relogio.tick(60) / 1000  # Calcula o tempo entre frames, 60hz
        fps = relogio.get_fps()

        # Imprimir o FPS no terminal para debug
        print(f"FPS: {fps:.2f}", end="\r")  # A impressão com '\r' sobrescreve a linha no terminal

        # Gera inimigos aleatórios periodicamente
        # Aumenta a probabilidade com o nível, mas limita o número de inimigos
        probabilidade_inimigos = max(1, 150 + nivel * 20)  # Reduz a chance de gerar inimigos com o aumento de nível
        if random.randint(1, probabilidade_inimigos) == 1:
            inimigos.append(gerar_inimigo(nivel))

        # Lógica de níveis
        if nivel == 1 and pontuacao >= 500:  # Nível 1: 800 pontos para avançar
            nivel += 1
            fundo = avancar_nivel(ecra, nivel, largura_ecra, altura_ecra, sons, jogador, inimigos)

        elif nivel == 2 and pontuacao >= 1200:  # Nível 2: 2000 pontos para avançar
            nivel += 1
            fundo = avancar_nivel(ecra, nivel, largura_ecra, altura_ecra, sons, jogador, inimigos)

        elif nivel == 3 and pontuacao >= 2000:  # Nível 3: 3600 pontos para avançar
            nivel += 1
            fundo = avancar_nivel(ecra, nivel, largura_ecra, altura_ecra, sons, jogador, inimigos)

        elif nivel == 4 and inimigo_final is None:  # Nível 4: Final
                # No nível final, cria o inimigo final apenas uma vez
            inimigo_final = InimigoFinal(largura_ecra - 100, altura_ecra // 2, altura_ecra) 
        
        elif nivel > 4:
            sons.tocar_musica_fundo(nivel)
            reproduzir_video("imagens/tryf.mp4", ecra)
            mostrar_tela_final(ecra, largura_ecra, altura_ecra, caminho_fonte)  # Exibe a tela de "Jogo Completo"
            iniciar_jogo()  # Volta ao menu inicial
            return  # Finaliza o loop principal
   
        # Processa eventos de entrada
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                a_funcionar = False
                play = False  # Define play como False para retornar ao menu
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and not jogador.disparando:
                    jogador.disparar()  # Ativa o disparo
                    #jogador.definir_animacao("disparar")
                    jogador.disparando = True
                elif evento.key == pygame.K_x:
                    if jogador.ataque_especial_desbloqueado:  # Apenas executa se desbloqueado
                        jogador.disparar2()
                        sons.tocar_disparo2()
                        jogador.temporizador = 1  # Define a duração da animação
                        print("disparado ataque especial")   
                    else:
                        print(f"ataque especial nao desbloqueado, {jogador.kills_recent}/3")

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
                elif evento.key == pygame.K_x:  # Verifica se a tecla X foi levantada
                    jogador.definir_animacao("parado")  # Define a animação como parado

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
        if nivel < 4: 
            posicao_fundo_x -= velocidade_fundo
            if posicao_fundo_x <= -largura_ecra:
                posicao_fundo_x = 0
            ecra.blit(fundo, (posicao_fundo_x, 0))  # Fundo em movimento
            ecra.blit(fundo, (posicao_fundo_x + largura_ecra, 0))
        else:
            ecra.blit(fundo, (0, 0))  # Fundo estático no nível 4

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
                        pontuacao += {1: 50, 2: 100, 3: 150, 4: 100, 5: 50}[inimigo.tipo]
                        jogador.incrementar_kill()
                    break

        # Atualizar e desenhar o Projetil2
        if jogador.projetil2:
            jogador.projetil2.atualizar(delta_tempo)  # Atualiza a posição do projetil2
            jogador.projetil2.desenhar(ecra)  # Desenha o projetil2 na tela

            # Verifica colisão do projetil2 com o inimigo_final
            if jogador.projetil2 and jogador.projetil2.ativo:
                if inimigo_final:  # Verifica se o inimigo final foi criado
                    raio_colisao = pygame.Rect(jogador.projetil2.x, jogador.projetil2.y, largura_ecra, 30)  # Área do projetil2
                    if raio_colisao.colliderect(pygame.Rect(inimigo_final.x, inimigo_final.y, 140, 100)):
                        inimigo_final.vidas -= 1
                        print(f"Dano ao inimigo final! Vidas restantes: {inimigo_final.vidas}")
                        if inimigo_final.vidas <= 0:
                            pontuacao += 1000
                            inimigo_final.vivo = False
                            nivel += 1

        # Verificar colisões do Projetil2 com inimigos
        if jogador.projetil2 and jogador.projetil2.ativo:
            for inimigo in inimigos[:]:
                raio_colisao = pygame.Rect(jogador.projetil2.x, jogador.projetil2.y, largura_ecra, 30)  # Área do raio
                inimigo_colisao = pygame.Rect(inimigo.pos_x, inimigo.pos_y, 90, 70)  # Área do inimigo

                if raio_colisao.colliderect(inimigo_colisao):
                    inimigo.vidas -= 1  # Aplica dano ao inimigo
                    if inimigo.vidas <= 0:
                        pontuacao += {1: 50, 2: 100, 3: 150, 4:50, 5:100}[inimigo.tipo]  # Adiciona pontos
                        inimigo.animacao_atual = "morto"  # Define a animação de morte para o inimigo
                        #inimigos.remove(inimigo)  # Remove o inimigo morto

        # Atualiza e desenha cada inimigo
        for inimigo in inimigos[:]:
            estado = inimigo.atualizar(delta_tempo, jogador)
            inimigo.desenhar(ecra)

            if estado == "fora":  # Saiu pela esquerda remove score 
                pontuacao -= {1: 50, 2: 100, 3: 150, 4: 100, 5: 50}[inimigo.tipo]
                inimigos.remove(inimigo)
                
        if inimigo_final: #iniciar o inimigo final
            inimigo_final.atualizar(delta_tempo)
            inimigo_final.desenhar(ecra)

            for projetil in inimigo_final.projeteis[:]:
                if pygame.Rect(projetil.x, projetil.y, 32, 32).colliderect( #se jogador atingido por projectil inimigo
                    pygame.Rect(jogador.pos_x, jogador.pos_y, 64, 64)
                ):
                    jogador.vida -= 10  # Reduz a vida do jogador ao ser atingido
                    sons.tocar_colisao()
                    jogador.definir_animacao("atingido") 
                    jogador.temporizador = 0.3  # Define a duração da animação "atingido" passa a "parado"
                    inimigo_final.projeteis.remove(projetil)  # Remove o projétil após colisão
                    # Verifica colisão com projéteis

            for projetil in jogador.projeteis[:]:
                if inimigo_final.verificar_colisao(projetil):
                    jogador.projeteis.remove(projetil)
                    sons.tocar_disparo()
                    print(f"Dano ao inimigo final! Vidas restantes: {inimigo_final.vidas}")

                    if not inimigo_final.vivo:
                        pontuacao += 1000  # Pontuação especial para derrotar o inimigo final
                        #inimigo_final = None  # Remove o inimigo final após ser derrotado
                        nivel += 1  # Avança para o próximo nível( neste caso fim do jogo)
                    
        
        # Atualiza o temporizador da animação "atingido"
        if jogador.temporizador > 0:
            jogador.temporizador -= delta_tempo
            if jogador.temporizador <= 0:
                jogador.definir_animacao("parado")  # Retorna para a animação padrão

        # Verifica colisão com o jogador
        for inimigo in inimigos[:]:
            if inimigo.vivo and pygame.Rect(inimigo.pos_x, inimigo.pos_y, 50, 50).colliderect(
                pygame.Rect(jogador.pos_x, jogador.pos_y, 50, 50)
            ):
                dano = {1: 30, 2: 50, 3: 70, 4: 30, 5: 30 }[inimigo.tipo]  # Define o dano dependendo do tipo do inimigo
                jogador.vida -= dano  # Diminui a vida do jogador
                sons.tocar_colisao()  # Toca som de colisão

                # Remove o inimigo após colisão com o jogador
                inimigos.remove(inimigo)
                
                # Ativa a animação "atingido" no jogador
                jogador.definir_animacao("atingido")
                jogador.temporizador = 0.3  # Define a duração da animação "atingido" 

        # Verifica colisões do jogador
        if jogador.vida <= 0:
            if tela_game_over(ecra, fundo):
                play_game()
            else:
                play = False

        # Atualiza a posição dos projéteis e do jogador
        jogador.atualizar(delta_tempo)
        jogador.desenhar(ecra)

        # Carregar a imagem do coração no início
        caminho_coracao = "imagens/coracao.png"  # Substitua pelo caminho correto
        imagem_coracao = pygame.image.load(caminho_coracao)
        imagem_coracao = pygame.transform.scale(imagem_coracao, (40, 40))  # Redimensiona, se necessário

        # Exibe a vida, pontuação e nível na tela
        fonte = pygame.font.Font(caminho_fonte, 40)  # Define o tamanho da fonte ()
        vida_texto = fonte.render(f"{jogador.vida}", True, (255, 0, 0))
        score_texto = fonte.render(f"Score: {pontuacao}", True, (255, 255, 0))
        nivel_texto = fonte.render(f"Nível: {nivel}", True, (255, 165, 0))
        aviso_x = fonte.render(f"Kamehameah tecla X!!", True, (255, 0, 0))
        if jogador.ataque_especial_desbloqueado==True:
            texto_largura = aviso_x.get_width()
            ecra.blit(aviso_x, ((largura_ecra - texto_largura) // 2, 50))
        score_texto = fonte.render(f"Score: {pontuacao}", True, (255, 255, 0))
        nivel_texto = fonte.render(f"Nível: {nivel}", True, (255, 165, 0))
        ecra.blit(imagem_coracao, (10, 10))  # Desenha o coração na posição desejada
        ecra.blit(vida_texto, (60, 10))
        ecra.blit(score_texto, (largura_ecra - 190, 10))
        ecra.blit(nivel_texto, (largura_ecra - 470, 8))  # Exibe o nível abaixo da vida
        pygame.display.update()

# Configuração inicial do menu
def iniciar_jogo():
    global play
    
    ecra = pygame.display.set_mode((largura_ecra, altura_ecra))  # Inicializa a janela do menu
    fundo = pygame.image.load("imagens/imagem_inicial.jpg").convert_alpha()  # Carrega a imagem de fundo
    fundo = pygame.transform.smoothscale(fundo, (largura_ecra, altura_ecra))  # Redimensiona suavemente
    sons.tocar_musica_menu()

    # Loop principal para exibir o menu e reagir à seleção do jogador
    while True:
        # Exibe o menu inicial com título
        escolha = menu(ecra, largura_ecra, altura_ecra, fundo, ["Jogar","Highscore", "Sair"])
        if escolha == "Jogar":
            tela_instrucoes(ecra, largura_ecra, altura_ecra)
            fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 20)
            play = True
            play_game()  # Inicia o jogo
            fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 20)
        elif escolha == "Highscore":
            fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 20)
            mostrar_highscore(ecra,fundo)
            fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 20)
        elif escolha == "Sair":
            fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 20)
            pygame.quit()
            break

# Inicializa o jogo, entra no menu incial
iniciar_jogo()