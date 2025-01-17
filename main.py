#main.py é ficheiro principal do jogo

import pygame
import random
from config import largura_ecra, altura_ecra, velocidade_fundo,caminho_fonte
from jogador import Jogador
from inimigos import InimigoFinal
from personagens import AnimacaoParado, AnimacaoAndar, AnimacaoDisparar, AnimacaoAtingido, AnimacaoDispararEspecial
from menu import menu, pause_menu
from fadeinout import fade_in_out
from sons import Sons
from niveis import carregar_fundo,gerar_inimigo,mostrar_historia,mostrar_tela_final,reproduzir_video,avancar_nivel
from highscore import mostrar_highscore, carregar_highscore, salvar_highscore
from Instrucoes import tela_instrucoes

# Variáveis globais para controle do estado do jogo
play = False # Variável para controlar o estado do jogo
pontuacao = 0  # Variável para a pontuação
nivel = 1  # Variável para o nível atual
sons = Sons()  # Inicia o som
# Variável para controlar o estado do som
musica_on = True  # A música começa ligada

# Função principal do jogo

def play_game():
    global play, pontuacao, nivel, tempo_inicio_jogo # Variáveis globais
    tempo_inicio_jogo = 0 # Variável para rastrear o tempo de inicio do jogo
    pontuacao = 0  # Reseta a pontuação ao iniciar um novo jogo
    nivel = 1  # Reseta o nível ao iniciar
    highscore = carregar_highscore() # Le o highscore do arquivo
    ecra = pygame.display.set_mode((largura_ecra, altura_ecra))  # Inicializa a janela do jogo
    pygame.display.set_caption("Goku Invaders")
    mostrar_historia(ecra, nivel)
    fundo = carregar_fundo(nivel)  # Carrega o fundo de acordo com o nível
    fundo = pygame.transform.scale(fundo, (largura_ecra, altura_ecra))  # Ajusta o fundo ao tamanho da tela
    sons.tocar_musica_fundo(nivel)
    musica_on = True #funciona dentro do loop, com tecla M para parar som nos niveis
    

    # Inicializa o jogador e define animações
    jogador = Jogador(100, altura_ecra / 2 - 64 / 2)
    jogador.adicionar_animacao("parado", AnimacaoParado())
    jogador.adicionar_animacao("andar", AnimacaoAndar())
    jogador.adicionar_animacao("disparar", AnimacaoDisparar())
    jogador.adicionar_animacao("atingido", AnimacaoAtingido())
    jogador.adicionar_animacao("disparar2",AnimacaoDispararEspecial())
    jogador.definir_animacao("parado")  # Necessária para iniciar a animação
    jogador.vida = 100 # Inicializa a vida do jogador
    jogador.disparando = False  # Adiciona estado para controlar o disparo
    jogador.temporizador = 0  # Temporizador para controlar a tempo de animaçoes com necessidade de reset para "parado"

    inimigos = []  # Lista para armazenar inimigos
    inimigo_final = None  # Inicializa a variável no início da função  
    relogio = pygame.time.Clock()  # Inicia o relógio para controlar o FPS
    posicao_fundo_x = 0  # Posição inicial do fundo
    a_funcionar = True  # Variável de controle do loop

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
        if nivel == 1 and pontuacao >= 800:  # Nível 1: 800 pontos para avançar
            nivel += 1
            fundo = avancar_nivel(ecra, nivel, largura_ecra, altura_ecra, sons, jogador, inimigos)

        elif nivel == 2 and pontuacao >= 1800:  # Nível 2: 1800 pontos para avançar
            nivel += 1
            fundo = avancar_nivel(ecra, nivel, largura_ecra, altura_ecra, sons, jogador, inimigos)

        elif nivel == 3 and pontuacao >= 3000:  # Nível 3: 300 pontos para avançar
            nivel += 1
            fundo = avancar_nivel(ecra, nivel, largura_ecra, altura_ecra, sons, jogador, inimigos)

        elif nivel == 4 and inimigo_final is None:  # Nível 4: Final
                # No nível final, cria o inimigo final apenas uma vez
            inimigo_final = InimigoFinal(largura_ecra - 100, altura_ecra // 2, altura_ecra) 

        
        elif nivel > 4:
            sons.tocar_musica_fundo(nivel)
            fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 30)# Exibe o score final antes do vídeo
            mostrar_score_final(ecra, largura_ecra, altura_ecra, pontuacao, caminho_fonte)
            fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 30)
            reproduzir_video("imagens/historia/video_final.mp4", ecra)
            fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 30)
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
                elif evento.key == pygame.K_x:  # Verifica se a tecla X foi pressionada
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

                #parar musica fudno durante os niveis, existe somente por motivos de testar. não funciona como mute 
                elif evento.key == pygame.K_m:  # Verifica se a tecla M foi pressionada
                    if sons.mutado:  # Se o som estiver mutado
                        sons.desligar()  # Desmutar o som
                        musica_on = True  # Ativa a música de fundo
                    else:  # Se o som não estiver mutado
                        sons.ligar()  # Muta o som
                        musica_on = False  # Desliga a música de fundo  

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
                            if pontuacao > highscore: # Atualiza o highscore, se necessário
                                print("Novo highscore")
                                highscore = pontuacao
                                salvar_highscore(highscore)

                            inimigo_final.vivo = False
                            nivel += 1

        # Verificar colisões do Projetil2 com inimigos
        if jogador.projetil2 and jogador.projetil2.ativo:
            for inimigo in inimigos[:]:
                if inimigo.animacao_atual == "morto": # Ignora colisao com inimigos mortos
                    continue

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
                        if pontuacao > highscore:# Atualiza o highscore, se necessário
                            print("Novo highscore")
                            highscore = pontuacao
                            salvar_highscore(highscore)
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

        # Variável para armazenar o status da música
        musica_status_texto = "Som: ON" if musica_on else "Som: OFF"

# Fonte para o texto de status
        fonte_status = pygame.font.Font(caminho_fonte, 30)
        status_texto = fonte_status.render(musica_status_texto, True, (255, 255, 255))  # Texto em branco  # Ajuste o tamanho conforme necessário
        # Carregar a imagem do icone coração no início
        caminho_coracao = "imagens/icons/coracao.png"  # Caminho da imagem do coração
        imagem_coracao = pygame.image.load(caminho_coracao)  # Carrega a imagem
        imagem_coracao = pygame.transform.scale(imagem_coracao, (40, 40))  # Redimensiona a imagem

        caminho_x = "imagens/icons/teclas/x.png"  # Caminho da imagem do botão X
        imagem_x = pygame.image.load(caminho_x)  # Carrega a imagem
        imagem_x = pygame.transform.scale(imagem_x, (40, 40))  # Redimensiona a imagem

        # Exibe a vida, pontuação e nível na tela
        fonte = pygame.font.Font(caminho_fonte, 40)  # Define o tamanho da fonte
        vida_texto = fonte.render(f"{jogador.vida}", True, (255, 0, 0))
        score_texto = fonte.render(f"Score: {pontuacao}", True, (255, 255, 0))
        nivel_texto = fonte.render(f"Nível: {nivel}", True, (255, 165, 0))
        aviso_x = fonte.render(f"Kamehameah", True, (255, 165, 0))

        # Verifica se o ataque especial está desbloqueado
        if jogador.ataque_especial_desbloqueado:
    # Calcula a posição da tecla X logo abaixo do nível
            pos_x = largura_ecra - 520  # Alinha horizontalmente com o texto do nível
            pos_y = 8 + nivel_texto.get_height() + 10  # 10px abaixo do texto do nível
            ecra.blit(imagem_x, (pos_x, pos_y))  # Exibe a tecla X abaixo do nível

            # Exibe o texto "Kamehameha!" ao lado direito da tecla X
            texto_x_pos = pos_x + imagem_x.get_width() + 5  # Espaçamento de 5px à direita da imagem X
            texto_y_pos = pos_y + (imagem_x.get_height() - aviso_x.get_height()) // 2  # Centraliza verticalmente
            ecra.blit(aviso_x, (texto_x_pos, texto_y_pos))

        # Exibe os outros elementos
        ecra.blit(imagem_coracao, (10, 10))  # Desenha o coração na posição desejada
        ecra.blit(vida_texto, (60, 10))  # Exibe a vida na posição desejada
        ecra.blit(score_texto, (largura_ecra - 190, 10))  # Exibe a pontuação no canto superior direito
        ecra.blit(nivel_texto, (largura_ecra - 470, 8))  # Exibe o nível à esquerda do score
        ecra.blit(status_texto, ( largura_ecra - 80, altura_ecra - 30))  # Posição na parte inferior da tela
        pygame.display.update()  # Atualiza a tela

# Configuração inicial do menu
def iniciar_jogo():
    global play
    pygame.display.set_caption("Goku Invaders")  # Define o título da janela
    ecra = pygame.display.set_mode((largura_ecra, altura_ecra))  # Inicializa a janela do menu
    fundo = pygame.image.load("imagens/Backgrounds/imagem_inicial.jpg").convert_alpha()  # Carrega a imagem de fundo
    fundo = pygame.transform.smoothscale(fundo, (largura_ecra, altura_ecra))  # Redimensiona suavemente
    sons.tocar_musica_menu()

    # Loop principal para exibir o menu e reagir à seleção do jogador
    while True:
        # Exibe o menu inicial com título
        escolha = menu(ecra, largura_ecra, altura_ecra, fundo, ["Jogar","Highscore", "Sair"]) # Exibe o menu
        if escolha == "Jogar": # Se o jogador escolher "Jogar"
            tela_instrucoes(ecra, largura_ecra, altura_ecra) # Exibe as instruções
            fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 20) # Faz a transição de fade
            play = True # Define o estado do jogo como "jogando"
            play_game()  # Inicia o jogo
            fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 20) # Faz a transição de fade
        elif escolha == "Highscore": # Se o jogador escolher "Highscore"
            fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 20)
            mostrar_highscore(ecra,fundo) # Exibe o highscore
            fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 20)
        elif escolha == "Sair": # Se o jogador escolher "Sair"
            fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 20)
            pygame.quit() # Fecha o jogo
            break

# Função para exibir a tela de Game Over
def tela_game_over(ecra, fundo): 
    sons.parar_musica_fundo()
    sons.tocar_game_over()
    fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 60)
    global pontuacao # Variável global para a pontuação
    highscore = carregar_highscore() # Le o highscore do arquivo
    novo_recorde = False  # Variável para rastrear se o highscore foi batido

    # Atualiza o highscore, se necessário
    if pontuacao > highscore:
        highscore = pontuacao
        salvar_highscore(highscore)
        novo_recorde = True  # Marca que o jogador bateu o recorde

    mensagem = "GAME OVER"
    submensagem = f"Score: {pontuacao} | Highscore: {highscore}"
    if novo_recorde: # Se o jogador bateu o recorde, adiciona a mensagem
        submensagem + f" Parabéns! Novo recorde!"
    opcoes = ["Reiniciar", "Sair"]

    try:
        # Carregar a imagem de Game Over
        imagem_game_over = pygame.image.load("imagens/Backgrounds/imagem_inicial.jpg").convert_alpha()
        imagem_game_over = pygame.transform.scale(imagem_game_over, (largura_ecra, altura_ecra))
    except pygame.error as e:
        print(f"Erro ao carregar imagem: {e}")
        return

    # Exibe a imagem de fundo
    ecra.blit(imagem_game_over, (0, 0))

    # Exibe a mensagem de Game Over no centro da tela
    fonte_titulo = pygame.font.Font(None, 64)
    texto_mensagem = fonte_titulo.render(mensagem, True, (255, 165, 0))
    ecra.blit(texto_mensagem, (largura_ecra // 2 - texto_mensagem.get_width() // 2, altura_ecra // 3))

    # Exibe a pontuação final
    fonte_pontuacao = pygame.font.Font(None, 48)
    texto_pontuacao = fonte_pontuacao.render(submensagem, True, (255, 255, 0))
    ecra.blit(texto_pontuacao, (largura_ecra // 2 - texto_pontuacao.get_width() // 2, altura_ecra // 2))

    # Chama o menu sem o título
    escolha = menu(ecra, largura_ecra, altura_ecra, fundo, opcoes, mensagem, submensagem, exibir_titulo=False)

    fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 20)
    pygame.display.update()

    if escolha == "Reiniciar":
        pontuacao = 0
        return True
    elif escolha == "Sair":
        pygame.quit()
        exit()

# Função para exibir a pontuação final
def mostrar_score_final(ecra, largura_ecra, altura_ecra, pontuacao, caminho_fonte, tempo_exibicao=2000):
    # Carrega a fonte para exibir o texto
    fonte = pygame.font.Font(caminho_fonte, 40)
    
    # Cria o texto de "Pontuação Final"
    texto_pontuacao = fonte.render(f"Pontuação Final: {pontuacao}", True, (255, 255, 255))
    
    # Define a posição do texto no centro da tela
    posicao_texto = texto_pontuacao.get_rect(center=(largura_ecra // 2, altura_ecra // 2 - 50))
    
    # Preenche o fundo da tela com preto
    ecra.fill((0, 0, 0))  # Fundo preto
    
    # Exibe o texto de pontuação final imediatamente após preencher o fundo
    ecra.blit(texto_pontuacao, posicao_texto)
    
    # Atualiza a tela para mostrar a pontuação
    pygame.display.flip()

    # Aguarda o tempo especificado para exibir a pontuação final
    pygame.time.delay(tempo_exibicao)  
    
    
    # Limpa a tela após a exibição da pontuação
    ecra.fill((0, 0, 0))  # Limpa a tela com fundo preto
    pygame.display.flip()

# Inicializa o jogo, entra no menu incial
iniciar_jogo() 