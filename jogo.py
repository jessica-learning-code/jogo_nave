import pygame
import random

pygame.init()

tamanho_tela = (800,600)
tela = pygame.display.set_mode(tamanho_tela)
relogio = pygame.time.Clock()

BRANCO = (255,255,255)

qtdbombas = 50
bombas = []

imagem_bombas = pygame.image.load("Piskel - Bomb.png")

#estrelas aparecem aleatóriamento do topo 
for i in range(qtdbombas):
    posicao_x = random.randint(0,750)
    posicao_y = 0
    velocidade_bombas = random.randint(1,2)
    tamanho_bombas = random.randint(50,60)
    imagem_redimencionada = pygame.transform.scale(imagem_bombas,(tamanho_bombas,tamanho_bombas))
    bombas.append([posicao_x,posicao_y,velocidade_bombas,imagem_redimencionada])


fim_jogo = False


while not fim_jogo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            fim_jogo = True

    tela.fill(BRANCO)

    for bomba in bombas:
        bomba[1] += bomba[2]
        

        if bomba[1] > 600:
            bomba[1] = -20
            bomba[0] = random.randint(0,750)
    tela.blit(bomba[3],(bomba[0],bomba[1]))

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()