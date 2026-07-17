import pygame
import random
from dataclasses import dataclass

pygame.init()

altura = 800
largura = 600
tela = pygame.display.set_mode((altura,largura))

relogio = pygame.time.Clock()#numero de fps

bombas = []
explosoes= []

ultimo_spaw = pygame.time.get_ticks()#calcular o último tempo em que o jogo começou a rodar
intervalo = 300# cria uma bomba a cada 300 milisegundos

imagem_bombas = pygame.image.load("Piskel - Bomb.png").convert_alpha()
imagem_nave = pygame.image.load("Piskel - Nave.png").convert_alpha()
imagem_explosao = pygame.image.load("explosao.png").convert_alpha()
imagem_fundo = pygame.image.load("galaxia.jpg").convert_alpha()

#posição inicial das imagens de fundo
imagem_1 = 0
imagem_2 = -largura

velocidade_imagem = 2

tamanho_nave, tamanho_bomba, tamanho_explosao = 100,100,70

imagem_nave_redimensionada = pygame.transform.scale(imagem_nave,(tamanho_nave,tamanho_nave))

imagem_bomba_redimensionada  = pygame.transform.scale(imagem_bombas,(tamanho_bomba,tamanho_bomba))

imagem_explosao_redimensionada = pygame.transform.scale(imagem_explosao,(tamanho_explosao,tamanho_explosao))

imagem_fundo_redimensionada = pygame.transform.scale(imagem_fundo,(altura,largura))

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

#criação de rect para poder fazer colisões
rect_nave = imagem_nave_redimensionada.get_rect(topleft=(nave_localizacao.x,nave_localizacao.y))

#o mascára de pixel serve para ignorar as áreas transparentes e só detectar colisões quando os pixels visíveis realmente se sobrepõem.
mask_nave = pygame.mask.from_surface(imagem_nave_redimensionada)
mask_bomba = pygame.mask.from_surface(imagem_bomba_redimensionada)   
   
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
    
    #atribuição das coordenadas x e y da nave aos rects para a colisão acontecer no lugar correto
    rect_nave.x = nave_localizacao.x
    rect_nave.y = nave_localizacao.y
    
    tela.blit(imagem_nave_redimensionada,rect_nave)

    agora = pygame.time.get_ticks()#calcular o tempo de jogo atual

    #aqui faz o cálculo de quanto em quanto tempo a próxima bomba cairá da tela. OBS: cada bomba cai depois de 1 segundo
    if agora - ultimo_spaw >= intervalo:
        posicao_x = random.randint(0,altura-tamanho_bomba)#posições aleatórias na horizontal das bombas
        posicao_y = -50#começar da posição -50 na vertical 
        velocidade_bomba = random.randint(7,8)
        #criação de rect para poder fazer colisões
        rect_bomba = imagem_bomba_redimensionada.get_rect(topleft=(posicao_x,posicao_y))
        bombas.append([rect_bomba, velocidade_bomba])

        ultimo_spaw = agora#atualizar para o último tempo

    for bomba in bombas[:]:#criar várias copias de bombas de modo que cada uma seja única
        rect_bomba = bomba[0]
        vel_bomba = bomba[1]

        rect_bomba.y += vel_bomba#soma a localização da bomba + sua velocidade para trazer movimento de cair

        if rect_bomba.y > largura:#se a posisão da bomba na vertical for maior que o limite da tela...
            bombas.remove(bomba)#ela é apagada
        else:#senão
            tela.blit(imagem_bomba_redimensionada,rect_bomba)#será desenhada na tela
        
        #o offset serve para dizer quantos pixels de distância há entre a bomba e nave antes de ocorrer a explosão
        offset = (rect_bomba.x - rect_nave.x, rect_bomba.y - rect_nave.y)

        #o overlap serve como um ponto de encontro, assim que o valor 1 do pixel da bomba encontra o da nave, a colisão acontece e a bomba é apagada
        if mask_nave.overlap(mask_bomba,offset):
            tempo_colisao = pygame.time.get_ticks()
            explosoes.append([rect_bomba.copy(), tempo_colisao])
            bombas.remove(bomba)

    tela.blit(imagem_nave_redimensionada,rect_nave)

    tempo_atual = pygame.time.get_ticks()

    for explosao in explosoes[:]:#criar várias copias de explosões de modo que cada uma seja única
        rect_exp = explosao[0]
        tempo_nascimento = explosao[1]
        if tempo_atual - tempo_nascimento < 300:#depois de 300 milisegundos a explosao some da tela antes disso ela é mostrada
            tela.blit(imagem_explosao_redimensionada,rect_exp)
        else:
            explosoes.remove(explosao)

    pygame.display.flip()#atualização da tela para apróximos frames
    relogio.tick(60)# fps máximo suportado

pygame.quit()