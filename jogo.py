import pygame
import random

pygame.init()

tamanho_tela = (800,600)
tela = pygame.display.set_mode(tamanho_tela)

BRANCO = (0,0,0)

qtdbombas = 50
bombas = []

imagem_bombas = pygame.image.load("Piskel - Bomb.png")

#estrelas aparecem aleatóriamento do topo 
for i in range(qtdbombas):
    posicao_x = random.randint(0,750)
    posicao_y = 0
    velocidade_bombas = random.randint(5,10)
    tamanho_bombas = random.randint(10,20)
    imagem_bombas = pygame.transform.scale(imagem_bombas,(tamanho_bombas,tamanho_bombas))
    bombas.append([posicao_x,posicao_y,velocidade_bombas,imagem_bombas])


fim_jogo = False

while not fim_jogo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            fim_jogo = True

    tela.fill(BRANCO)

    tela.blit(bombas[3],(bombas[0],bombas[1]))

pygame.quit()