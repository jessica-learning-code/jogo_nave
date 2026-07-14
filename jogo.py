import pygame
import random

pygame.init()

tamanho_tela = (800,600)
tela = pygame.display.set_mode(tamanho_tela)

relogio = pygame.time.Clock()

BRANCO = (255,255,255)

bombas = []

ultimo_spaw = pygame.time.get_ticks()
intervalo = 2000# cria uma bomba a cada 300 milisegundos


imagem_bombas = pygame.image.load("Piskel - Bomb.png")
imagem_nave = pygame.image.load("Piskel - Nave.png")


tamanho_nave = 100
imagem_nave_redimensionada = pygame.transform.scale(imagem_nave,(tamanho_nave,tamanho_nave))

x = 790#posição horizontal da nave
velocidade = 10

   
fim_jogo = False

while not fim_jogo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            fim_jogo = True

    tela.fill(BRANCO)

    agora = pygame.time.get_ticks()

    if agora - ultimo_spaw >= intervalo:
        posicao_x = random.randint(0,750)
        posicao_y = -50
        velocidade = random.randint(1,2)
        tamanho_bomba = 70
        imagem_bomba_redimensionada  = pygame.transform.scale(imagem_bombas,(tamanho_bomba,tamanho_bomba))
        bombas.append([posicao_x, posicao_y, velocidade, imagem_bomba_redimensionada])

        ultimo_spaw = agora#atualizar para o último tempo

    for bomba in bombas[:]:
        bomba[1] += bomba[2]#somar posição vertical + velocidade para fazer as bombas cairem
        if bomba[1] > 600:
            bombas.remove(bomba)
        else:
            tela.blit(bomba[3],(bomba[0],bomba[1]))


    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and x < 800-tamanho_nave:
                x += velocidade
            if event.key == pygame.K_LEFT and x > 0:
                x -= velocidade
        tela.blit(imagem_bomba_redimensionada)       

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()