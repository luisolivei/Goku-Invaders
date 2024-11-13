import pygame
from projetil import Projetil
from jogador import Jogador
#from inimigo import Inimigo1, Inimigo2, Inimigo3, Inimigo4 - vários inimigos

#colisao de sprites- colisao perfeita - adicionar estas linhas à classe correspondente

self.mask = pygame.mask.from_surface(self.imagem) #criar uma mascara à volta do sprite do inimigo 1
self.mask = pygame.mask.from_surface(self.imagem) #criar uma mascara à volta do sprite do inimigo 2
self.mask = pygame.mask.from_surface(self.imagem) #criar uma mascara à volta do sprite do inimigo 3
self.mask = pygame.mask.from_surface(self.imagem) #criar uma mascara à volta do sprite do inimigo 4

#grupo obstaculos- guarda as sprites que podem colidir com o goku
grupo_obstaculos = pygame.sprite.Group()
grupo_obstaculos.add(inimigo1)
grupo_obstaculos.add(inimigo2)
grupo_obstaculos.add(inimigo3)
grupo_obstaculos.add(inimigo4)

colisoes= pygame.sprite.spritecollide(chama,grupo_obstaculos, True, pygame.sprite.collide_mask)

