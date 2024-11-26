import pygame

def menu(ecra, largura_ecra, altura_ecra, fundo, opcoes, mensagem=None, submensagem=None, exibir_titulo=True):
    pygame.font.init()
    font_titulo = pygame.font.Font("fonts/Saiyan-Sans.ttf", 100)  # Fonte para o título
    font_botoes = pygame.font.Font("fonts/Saiyan-Sans.ttf", 60)   # Fonte para os botões
    font_mensagem = pygame.font.Font("fonts/Saiyan-Sans.ttf", 80)  # Fonte para mensagens principais
    font_submensagem = pygame.font.Font("fonts/Saiyan-Sans.ttf", 50)  # Fonte para submensagens

    # Texto do título
    if exibir_titulo:
        titulo_text = font_titulo.render("Goku Invaders", True, (255, 255, 255))
        titulo_rect = titulo_text.get_rect(center=(largura_ecra // 2, altura_ecra // 4.5))

    # Definindo as cores
    botao_cor = (166, 148, 131)
    botao_hover_cor = (255, 70, 70)
    sombra_cor = (50, 50, 50)

    # Botões e suas posições
    botoes = {opcao: (largura_ecra // 2, altura_ecra // 2 + i * 100) for i, opcao in enumerate(opcoes)}

    # Dimensões fixas dos botões (largura e altura)
    largura_botao = 300
    altura_botao = 70

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
            ecra.blit(titulo_text, titulo_rect)

        # Renderiza mensagens opcionais, se fornecidas
        if mensagem:
            ecra.blit(mensagem_text, mensagem_rect)
        if submensagem:
            ecra.blit(submensagem_text, submensagem_rect)

        # Checa a posição do mouse para os efeitos de hover
        mouse_pos = pygame.mouse.get_pos()
        for texto, posicao in botoes.items():
            # Renderizar o texto do botão
            botao_texto = font_botoes.render(texto, True, (255, 255, 255))
            # Definir retângulo do botão com largura e altura fixas
            botao_rect = pygame.Rect(0, 0, largura_botao, altura_botao)
            botao_rect.center = posicao

            # Caixa de sombra
            sombra_rect = botao_rect.copy()
            sombra_rect.topleft = (botao_rect.topleft[0] + 4, botao_rect.topleft[1] + 4)
            pygame.draw.rect(ecra, sombra_cor, sombra_rect, border_radius=12)

            # Efeito de hover (mudança de cor e "elevação" da caixa do botão)
            if botao_rect.collidepoint(mouse_pos):
                pygame.draw.rect(ecra, botao_hover_cor, botao_rect, border_radius=12)
            else:
                pygame.draw.rect(ecra, botao_cor, botao_rect, border_radius=12)

            # Desenha o texto do botão centralizado dentro do retângulo
            botao_texto_rect = botao_texto.get_rect(center=botao_rect.center)
            ecra.blit(botao_texto, botao_texto_rect)

        # Detecta eventos de clique nos botões
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return "quit"
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Verifica se o botão esquerdo do mouse foi clicado
                    # Checa cada botão individualmente
                    for texto, posicao in botoes.items():
                        botao_rect = pygame.Rect(0, 0, largura_botao, altura_botao)
                        botao_rect.center = posicao
                        if botao_rect.collidepoint(evento.pos):
                            return texto  # Retorna o texto do botão clicado
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return "quit"  # Permite sair do menu com ESC

        pygame.display.update()
