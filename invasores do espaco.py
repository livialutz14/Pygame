import pygame
from pygame.font import *
import random

#define o tamanho da janela
width=900
height=600

sys_font=None
bullets=[]
cooldown=1000 #tempo usado está em ms
contador=0

#define as imagens 
def load():
    global fundo,nave,inimigo,nave2,inimigo2,barulho,sys_font,rectInimigo,som,boom,boom2
    pygame.display.set_caption('Invasores do espaço')
    clock=pygame.time.Clock()
    fundo=pygame.image.load('fundo.png')
    nave=pygame.image.load('nave.png')
    inimigo=pygame.image.load('inimigo.png')
    nave2=pygame.transform.scale(nave,(100,100))
    inimigo2=pygame.transform.scale(inimigo,(100,100))
    boom=pygame.image.load('boom.png')
    boom2=pygame.transform.scale(boom,(100,100))
    sys_font=Font(get_default_font(), 50)
    som=pygame.mixer.Sound('Bam sound effect.MP3')
    pygame.mixer.music.load('Bam sound effect.MP3')
    pygame.mixer.Sound.set_volume(som,0.1)
   
#configurando o player
player={
    'xNave':0,
    'yNave':500,
    'deltaPlayer':0
}

#Configurando o inimigo
enemy={
    'xInimigo':100,
    'yInimigo':30,
    'collidido':False
}

contaAtaque=0 #conta tempo de collisão
#Função update
def update(dt):
    global vXInimigo,vYInimigo,bullets,cooldown,rectInimigo,contaAtaque
    rectInimigo=inimigo2.get_rect(center=(enemy['xInimigo']+50,enemy['yInimigo']+50))
    enemy['xInimigo']+=0.1*dt*vXInimigo
    enemy['yInimigo']+=0.1*dt*vYInimigo
    
    if(player['xNave']==enemy['xInimigo']):
        enemy['xInimigo']-=250
        player['yNave']+=15
        enemy['yInimigo']+=15
        
        if(player['yNave']==enemy['yInimigo']):
            enemy['yInimigo']=40
    #mudança na posição da nave e inimigo
    
    if(enemy['xInimigo']>800):
        vXInimigo=-vXInimigo
        
    if(enemy['yInimigo']>=(height-100)):
        vYInimigo=-vYInimigo
        
    if(enemy['xInimigo']<=0):
        enemy['xInimigo']=0
        vXInimigo=-vXInimigo
        
    if(enemy['yInimigo']<=0):
        enemy['yInimigo']=0
        vYInimigo=-vYInimigo
        
    player['xNave']+=(player['deltaPlayer']*dt*0.3)
    
    if(player['xNave']<20):
        player['xNave']=20
        
    if(player['xNave']+100>width-20):
        player['xNave']=width-20-100
        
    #dá cada tiro
    bulletsNova=[]
    
    for i in range(0,len(bullets)):
        b=bullets[i]
        if b[1]>-10:
            b=(b[0],b[1]-(dt * 0.3))
            bulletsNova.append(b)
            
    bullets=bulletsNova
    
    if (cooldown<10000): 
        cooldown+=dt
        
    if(enemy['collidido']==True):
        contaAtaque+=dt
        
        if(contaAtaque>500):
            enemy['collidido']=False
            contaAtaque=0

#lê teclas

def keyPressed():
    global bullets,cooldown
    
    #leitura do teclado para a nave
    
    keys=pygame.key.get_pressed()
    if(keys[pygame.K_LEFT]): #tecla esquerda
        player['deltaPlayer'] = -2
        
    elif(keys[pygame.K_RIGHT]): #tecla direita
        player['deltaPlayer'] = 2
        
    else:
        player['deltaPlayer'] = 0
        
    #move o tiro
    
    if(cooldown>1000):
        if(keys[pygame.K_SPACE]):
            cooldown = 0
            b=(player['xNave'],player['yNave'])
            bullets.append(b) 

#desenhar na tela
def DrawScreen(screen):
    global nave2,inimgo2,sys_font,bullets,contador,rectInimigo
    screen.blit(fundo,(0,0))
    screen.blit(inimigo2,(enemy['xInimigo'],enemy['yInimigo']))
    screen.blit(nave2,(player['xNave'],player['yNave']))
    
    #desenhando o tiro
    
    for b in bullets:
        tiro=pygame.Rect((b[0]+50),b[1],5,60)
        pygame.draw.rect(screen,(255,0,0),tiro,8)
        
        if(tiro.colliderect(rectInimigo)): 
            contador+=1
            enemy['collidido']=True
            bullets.remove(b)
            pygame.mixer.Sound.play(som)
            
    if(enemy['collidido']==True):
         screen.blit(boom2,(enemy['xInimigo'],enemy['yInimigo']))
         
    #escrevendo
    
    t=sys_font.render("Pontos: %d"%contador,False,(0, 255, 0))
    screen.blit(t,t.get_rect(top=30,right=880))

#Loop principal

def mainLoop(screen):
    global bullets,contador
    running=True
    while(running):
        
        #fecha o jogo
        
        for event in pygame.event.get():
            if(event.type==pygame.QUIT):
                running=False
                break
                
        clock.tick(60)
        dt=clock.get_time()
        
        #imagens do jogo
        
        DrawScreen(screen)
        keyPressed()
        update(dt)
        pygame.display.update()
        

#inicializa o pygame

pygame.init()
pygame.mixer.init()

#desenha a janela

screen=pygame.display.set_mode((width,height))

clock=pygame.time.Clock()
load()
vXInimigo=3
vYInimigo=3
mainLoop(screen)
pygame.quit()       
        
            
        


