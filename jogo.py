import pygame
import random
from dataclasses import dataclass

pygame.init()

altura = 800
largura = 600
tela = pygame.display.set_mode((altura,largura))

relogio = pygame.time.Clock()#numero de fps

CINZA = (70,86,94)

bombas = []

ultimo_spaw = pygame.time.get_ticks()#calcular o último tempo em que o jogo começou a rodar
intervalo = 1000# cria uma bomba a cada 1 segundo

imagem_bombas = pygame.image.load("Piskel - Bomb.png").convert_alpha()
imagem_nave = pygame.image.load("Piskel - Nave.png").convert_alpha()

imagem_fundo = pygame.image.load("galaxia.jpg").convert_alpha()
imagem_fundo_redimensionada = pygame.transform.scale(imagem_fundo,(altura,largura))


#posição inicial das imagens de fundo
imagem_1 = 0
imagem_2 = -largura

velocidade_imagem = 3

tamanho_nave = 100
imagem_nave_redimensionada = pygame.transform.scale(imagem_nave,(tamanho_nave,tamanho_nave))

#movimentos da nave
mover_direita  = False
mover_esquerda = False

#criação de uma classe para passar os parâmetros de posição e velocidade da nave
@dataclass
class NaveLocalizacao:
    x : int
    y : int

nave_localizacao = NaveLocalizacao(x=350, y=510)
velocidade_nave = 8
   
fim_jogo = False

while not fim_jogo:

    #move as duas imagens para baixo
    imagem_1 += velocidade_imagem
    imagem_2 += velocidade_imagem

    #se as imagens 1 e 2 sairem da tela, reposicione
    if imagem_1 >= largura:
        imagem_1 = -largura +  (imagem_1 - largura)

    if imagem_2 >= largura :
        imagem_2 = -largura + (imagem_2 - largura)

    
    tela.blit(imagem_fundo_redimensionada,(0,imagem_1))
    tela.blit(imagem_fundo_redimensionada,(0,imagem_2))
    
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            fim_jogo = True

        if evento.type == pygame.KEYDOWN:#se usuário precionar alguma seta...
            if evento.key == pygame.K_RIGHT:#caso seja a seta direita, vá para direita
                mover_direita = True
            if evento.key == pygame.K_LEFT:#caso seja a seta esquerda, vá para esquerda
                mover_esquerda = True
        if evento.type == pygame.KEYUP:##se usuário não precionar nenhuma seta...
            if evento.key == pygame.K_RIGHT:#não ocorre movimentação para direita
                mover_direita = False
            if evento.key == pygame.K_LEFT:#não ocorre movimentação para esquerda
                mover_esquerda = False

    if mover_direita:
        nave_localizacao.x += velocidade_nave#soma localização da nave + velocidade para movimentar para direita
    if mover_esquerda:
        nave_localizacao.x -= velocidade_nave#subtrai localização da nave - velocidade para movimentar para esquerda

    #limitação da nave dentro da tela
    if nave_localizacao.x < 0:
        nave_localizacao.x = 0
    if nave_localizacao.x + imagem_nave_redimensionada.get_width() > altura:
        nave_localizacao.x = altura - imagem_nave_redimensionada.get_width()

    tela.blit(imagem_nave_redimensionada,(nave_localizacao.x, nave_localizacao.y))

    agora = pygame.time.get_ticks()#calcular o tempo de jogo atual

    #aqui faz o cálculo de quanto em quanto tempo a próxima bomba cairá da tela. OBS: cada bomba cai depois de 1 segundo
    if agora - ultimo_spaw >= intervalo:
        posicao_x = random.randint(0,750)#posições aleatórias entre 0 e 750 na horizontal
        posicao_y = -50#começar da posição -50 na vertical 
        velocidade_bomba = random.randint(4,5)
        tamanho_bomba = 100
        imagem_bomba_redimensionada  = pygame.transform.scale(imagem_bombas,(tamanho_bomba,tamanho_bomba))
        bombas.append([posicao_x, posicao_y, velocidade_bomba])

        ultimo_spaw = agora#atualizar para o último tempo

    for bomba in bombas[:]:#criar várias copias de bombas de modo que cada uma seja única
        bomba[1] += bomba[2]#somar posição vertical + velocidade para fazer as bombas cairem
        if bomba[1] > 600:#se a posisão da bomba na vertical for maior que o limite da tela...
            bombas.remove(bomba)#ela é apagada
        else:#senão
            tela.blit(imagem_bomba_redimensionada,(bomba[0],bomba[1]))#será desenhada na tela

    pygame.display.flip()#atualização da tela para apróximos frames
    relogio.tick(60)# fps máximo suportado

pygame.quit()