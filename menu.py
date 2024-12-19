import pygame
from config import largura_ecra, altura_ecra
from highscore import carregar_highscore,salvar_highscore
from fadeinout import fade_in_out

def menu(ecra, largura_ecra, altura_ecra, fundo, opcoes, mensagem=None, submensagem=None, exibir_titulo=True):
    pygame.font.init()
    # Configuração das fontes
    font_titulo = pygame.font.Font("fonts/Saiyan-Sans.ttf", 100)  # Fonte para o título
    font_botoes = pygame.font.Font("fonts/Saiyan-Sans.ttf", 60)   # Fonte para os botões
    font_mensagem = pygame.font.Font("fonts/Saiyan-Sans.ttf", 80)  # Fonte para mensagens principais
    font_submensagem = pygame.font.Font("fonts/Dest.otf", 50)  # Fonte para submensagens

    # Texto do título
    if exibir_titulo:
        texto_antes_o = "G"
        texto_o = "O"
        texto_depois_o = "ku Invaders"

        titulo_antes_o = font_titulo.render(texto_antes_o, True, (255, 255, 255))  # Branco
        titulo_o = font_titulo.render(texto_o, True, (255, 165, 0))  # Laranja
        titulo_depois_o = font_titulo.render(texto_depois_o, True, (255, 255, 255))  # Branco

        total_largura = (
            titulo_antes_o.get_width() +
            titulo_o.get_width() +
            titulo_depois_o.get_width()
        )
        posicao_inicial_x = (largura_ecra - total_largura) // 2
        posicao_y = altura_ecra // 4.5

    # Botões e suas posições
    botoes = {opcao: (largura_ecra // 2, altura_ecra // 2 + i * 100) for i, opcao in enumerate(opcoes)}

    # Dimensões fixas dos botões (largura e altura)
    largura_botao = 250
    altura_botao = 68

    # Mensagens opcionais
    if mensagem:
        mensagem_text = font_mensagem.render(mensagem, True, (255, 0, 0))
        mensagem_rect = mensagem_text.get_rect(center=(largura_ecra // 2, altura_ecra // 6))

    if submensagem:
        submensagem_text = font_submensagem.render(submensagem, True, (255, 255, 0))
        submensagem_rect = submensagem_text.get_rect(center=(largura_ecra // 2, altura_ecra // 3.5))

    # Loop principal do menu
    while True:
        ecra.blit(fundo, (0, 0))  # Fundo do menu

        # Renderiza o título se necessário
        if exibir_titulo:
            ecra.blit(titulo_antes_o, (posicao_inicial_x, posicao_y))
            ecra.blit(titulo_o, (posicao_inicial_x + titulo_antes_o.get_width(), posicao_y))
            ecra.blit(titulo_depois_o, (posicao_inicial_x + titulo_antes_o.get_width() + titulo_o.get_width(), posicao_y))

        # Renderiza mensagens opcionais, se fornecidas
        if mensagem:
            ecra.blit(mensagem_text, mensagem_rect)
        if submensagem:
            ecra.blit(submensagem_text, submensagem_rect)

        # Checa a posição do mouse para os efeitos de hover
        mouse_pos = pygame.mouse.get_pos()
        for texto, posicao in botoes.items():
            # Cria uma superfície semi-transparente para o botão
            botao_surface = pygame.Surface((largura_botao, altura_botao), pygame.SRCALPHA)
            sombra_surface = pygame.Surface((largura_botao, altura_botao), pygame.SRCALPHA)

            # Cores ajustadas com maior transparência
            sombra_surface.fill((50, 50, 50, 100))  # Sombra mais transparente
            if pygame.Rect(0, 0, largura_botao, altura_botao).move(posicao[0] - largura_botao // 2, posicao[1] - altura_botao // 2).collidepoint(mouse_pos):
                # Alteração da cor de hover para um laranja suave
                botao_surface.fill((255, 165, 0, 150))  # Hover: laranja suave com transparência
            else:
                botao_surface.fill((166, 148, 131, 10))  # Normal: bege mais transparente

            # Desenhar sombra primeiro
            ecra.blit(sombra_surface, (posicao[0] - largura_botao // 2 + 4, posicao[1] - altura_botao // 2 + 4))
            # Desenhar botão transparente
            ecra.blit(botao_surface, (posicao[0] - largura_botao // 2, posicao[1] - altura_botao // 2))

            # Renderizar texto do botão
            botao_texto = font_botoes.render(texto, True, (255, 255, 255))
            botao_texto_rect = botao_texto.get_rect(center=posicao)
            ecra.blit(botao_texto, botao_texto_rect)

        # Detecta eventos de clique nos botões
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return "quit"
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Verifica se o botão esquerdo do mouse foi clicado
                    for texto, posicao in botoes.items():
                        botao_rect = pygame.Rect(0, 0, largura_botao, altura_botao)
                        botao_rect.center = posicao
                        if botao_rect.collidepoint(evento.pos):
                            return texto  # Retorna o texto do botão clicado
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return "quit"  # Permite sair do menu com ESC

        pygame.display.update()

# Função de pausa que exibe o menu de pausa
def pause_menu(ecra, fundo):
    global play
    while True:
        # Exibe o menu com título (ou sem título, dependendo da escolha)
        escolha = menu(ecra, largura_ecra, altura_ecra, fundo, ["Continuar", "Sair"], exibir_titulo=True)
        if escolha == "Continuar":
            return  # Apenas retorna, mantendo o estado do jogo
        elif escolha == "Sair":
            pygame.quit()
            exit()


def tela_game_over(ecra, fundo):
    fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 60)
    global pontuacao
    highscore = carregar_highscore()
    novo_recorde = False  # Variável para rastrear se o highscore foi batido

    # Atualiza o highscore, se necessário
    if pontuacao > highscore:
        highscore = pontuacao
        salvar_highscore(highscore)
        novo_recorde = True  # Marca que o jogador bateu o recorde

    mensagem = "GAME OVER"
    submensagem = f"Score: {pontuacao} | Highscore: {highscore}"
    if novo_recorde:
        submensagem + f" Parabéns! Novo recorde!"
    opcoes = ["Reiniciar", "Sair"]

    try:
        # Carregar a imagem de Game Over
        imagem_game_over = pygame.image.load("images/11.png").convert_alpha()
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
    


