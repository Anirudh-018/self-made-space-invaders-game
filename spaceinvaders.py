import pygame as pg
from pygame.locals import*
from os import path
import random
pg.init()
pg.mixer.init()
#colors
red=(255,0,0)
black=(0,0,0)
blue=(0,0,255)
white=(255,255,255)
green=(0,255,0)
#path
snd=path.join(path.dirname(__file__),'snd')
game=path.join(path.dirname(__file__),'img')
#images load
back_image=pg.image.load(path.join(game,'back.png'))
back_rect=back_image.get_rect()
win_img=pg.image.load(path.join(game,'space.jpg'))
win=pg.transform.scale(win_img,(500,700))
player_img=pg.image.load(path.join(game,'enemyRed3.png'))
life=pg.transform.scale(player_img,(15,15))
mob_list=[pg.image.load(path.join(game,'meteorBrown_big1.png')),pg.image.load(path.join(game,'meteorBrown_big2.png')),pg.image.load(path.join(game,'meteorBrown_big3.png')),pg.image.load(path.join(game,'meteorBrown_big4.png')),
          pg.image.load(path.join(game,'meteorBrown_med1.png')),pg.image.load(path.join(game,'meteorBrown_med3.png')),
          pg.image.load(path.join(game,'meteorBrown_small1.png')),pg.image.load(path.join(game,'meteorBrown_small2.png'))]
laser_img=pg.image.load(path.join(game,'laserRed16.png'))
power={}
power['shield']=pg.image.load(path.join(game,'shield_gold.png'))
power['gun']=pg.image.load(path.join(game,'bolt_gold.png'))
explo={}
explo['lg']=[]
explo['sm']=[]
for i in range (1,24):
    file='expl_01_0 ('+str(i)+').png'
    img=pg.image.load(path.join(game,file))
    img.set_colorkey(black)
    img_lg=pg.transform.scale(img,(75,75))
    img_sm=pg.transform.scale(img,(50,50))
    explo['lg'].append(img_lg)
    explo['sm'].append(img_sm)
#sound
shoot_snd=pg.mixer.Sound(path.join(snd,'Laser_Shoot.wav'))
expl=[pg.mixer.Sound(path.join(snd,'Explosion.wav')),pg.mixer.Sound(path.join(snd,'Explosion2.wav'))]
g0=pg.mixer.Sound(path.join(snd,'g0.wav'))
#points
font_name=path.join(game,'kenvector_future.ttf')
#buttons
but=pg.image.load('C:/Users/Chandrika/Desktop/game/img/buttonRed.png')
def point(surf,write,size,x,y):
    font=pg.font.Font(font_name,size)
    text=font.render(write,True,white)
    text_rect=text.get_rect()
    text_rect.midtop=(x,y)
    surf.blit(text,text_rect)

clok=pg.time.Clock()
fps=65
screen=pg.display.set_mode((500,700))
red=(255,0,0)
black=(0,0,0)
blue=(0,0,255)
white=(255,255,255)
green=(0,255,0)
class player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image=pg.transform.scale(player_img,(85,85))
        self.image.set_colorkey(black)
        self.rect=self.image.get_rect()
        self.radius=int(self.rect.width//2)
        self.rect.x=100
        self.rect.y=550
        self.speedx=0
        self.speedy=0
        self.shield=100
        self.shot=pg.time.get_ticks()
        self.pow=pg.time.get_ticks()
        self.lives=3
        self.power=1
        self.pow=pg.time.get_ticks()
    def powerup(self):
        self.pow=pg.time.get_ticks()
        player.power+=1
    def shoot(self):
        now=pg.time.get_ticks()
        if now-self.shot>=200:
            self.shot=now
            if self.power==1:
                bullet=Bullet(self.rect.centerx,self.rect.top)
                sp.add(bullet)
                bullets.add(bullet)
                shoot_snd.play()
            if self.power>=2:
                bullet1=Bullet(self.rect.left,self.rect.centery)
                bullet2=Bullet(self.rect.right,self.rect.centery)
                sp.add(bullet1)
                bullets.add(bullet1)
                sp.add(bullet2)
                bullets.add(bullet2)
                shoot_snd.play()
    def update(self):
        if self.power>=2 and pg.time.get_ticks()-self.pow>=5000:
            self.power-=1
            self.pow=pg.time.get_ticks()
        self.speedx=0
        keys=pg.key.get_pressed()
        if keys[K_LEFT]:
            self.speedx=-15
        if keys[K_RIGHT]:
            self.speedx=15
        if keys[K_SPACE]:
            self.shoot()
        self.rect.x+=self.speedx
        if self.rect.right>=500:
            self.rect.right=500
        if self.rect.left<=0:
            self.rect.left=0
class mob(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image=random.choice(mob_list)
        self.rect=self.image.get_rect()
        self.image.set_colorkey(black)
        self.size=int((self.rect.width)/2)
        self.rect.x=random.randint(50,400)
        self.rect.y=random.randint(-30,-10)
        self.speedy=random.randint(40,50)
        self.speedx=random.randint(-3,3)
    def update(self):
        self.rect.x+=self.speedx
        self.rect.y+=self.speedy
        if self.rect.y>710 or self.rect.left<-10 or self.rect.right>510:
            self.rect.x=random.randint(100,600)
            self.rect.y=random.randint(-100,-30)
            self.speedy=random.randint(1,8)
class Bullet(pg.sprite.Sprite):
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)
        self.image=pg.transform.scale(laser_img,(25,25))
        self.image.set_colorkey(white)
        self.rect=self.image.get_rect()
        self.rect.bottom=y
        self.rect.centerx=x
        self.speedy=-10
    def update(self):
        self.rect.y+=self.speedy
        if self.rect.bottom<0:
            self.kill()
class powe(pg.sprite.Sprite):
    def __init__(self,center,typ):
        pg.sprite.Sprite.__init__(self)
        self.type=typ
        self.image=power[self.type]
        self.image.set_colorkey(black)
        self.rect=self.image.get_rect()
        self.rect.center=center
        self.speedy=5
    def update(self):
        self.rect.y+=self.speedy
        if self.rect.top>700:
            self.kill()
class explosion(pg.sprite.Sprite):
    def __init__(self,center,size):
        pg.sprite.Sprite.__init__(self)
        self.size=size
        self.image=explo[self.size][0]
        self.rect=self.image.get_rect()
        self.rect.center=center
        self.frames=0
        self.last=pg.time.get_ticks()
        self.frame_rate=50
    def update(self):
        now=pg.time.get_ticks()
        if now-self.last>=self.frame_rate:
            self.last=now
            self.frames+=1
            if self.frames==len(explo[self.size]):
                self.kill()
        else:
            center=self.rect.center
            self.image=explo[self.size][self.frames]
            self.rect=self.image.get_rect()
            self.rect.center=center
score=0
game_over=True
run=True
#groups
sp=pg.sprite.Group()
explosions=pg.sprite.Group()
players=pg.sprite.Group()
mobs=pg.sprite.Group()
bullets=pg.sprite.Group()
powerups=pg.sprite.Group()
player=player()
sp.add(player)
#functions
def newmob():
    m=mob()
    mobs.add(m)
    sp.add(m)
for i in range(3):
    newmob()
def high_score():
    high=open('C:/Users/Chandrika/Desktop/game/si_highscore.txt','r+')
    v=high.read()
    d=int(v)
    if d<score:
        high.seek(0)
        high.write(str(score))
    high.close()
    return v
def bar(pct,x,y,sc):
    len=100
    width=10
    ins=pg.Rect(x,y,pct,width)
    out=pg.Rect(x,y,len,width)
    pg.draw.rect(sc,green,ins)
    pg.draw.rect(sc,white,out,2)
def lives(surf,lives,x,y,img):
    img_rect=img.get_rect()
    img_rect.x=x
    img_rect.y=y
    surf.blit(img,(x,y))
def lifes(surf,write,size,x,y):
    font=pg.font.Font(font_name,size)
    text=font.render(write,True,white)
    text_rect=text.get_rect()
    text_rect.x=x
    text_rect.y=y
    surf.blit(text,text_rect)
def txt(surf,write,size,x,y):
    font=pg.font.Font(font_name,size)
    text=font.render(write,True,black)
    surf.blit(text,(x,y))
def button(x,y,write):
    screen.blit(but,(x,y))
    txt(screen,write,25,x+8,y+5)
def close(x,y):
    but=pg.image.load('C:/Users/Chandrika/Desktop/game/img/UI/numeralX.png')
    img=pg.transform.scale(but,(30,30))
    screen.blit(img,(x,y))
def go():
    global run
    screen.blit(win,back_rect)
    txt(screen,'SPACE INVADERS',45,10,700/4)
    button(140,350,'start game')
    txt(screen,'high score is : '+high_score(),25,75,450)
    pg.display.flip()
    wait=True
    while wait:
        clok.tick(fps)
        for event in pg.event.get():
            if event.type==pg.QUIT:
                pg.quit()
                run=False
            if event.type==pg.MOUSEBUTTONDOWN:
                mx,my=pg.mouse.get_pos()
                if 140<mx<360 and 350<my<385:
                    pg.time.delay(500)
                    wait=False
while run:
    for event in pg.event.get():
        if event.type==pg.QUIT:
            high_score()
            run=False
        if event.type==pg.MOUSEBUTTONDOWN:
            mx,my=pg.mouse.get_pos()
            if 10<=my<=40 and 450<=mx<=490:
                high_score()
                run=False
    if game_over:
        go()
        game_over=False
        for i in range(7):
            newmob()
        score=0
        player.lives=3
    clok.tick(fps)
    sp.update()
    #bullet and mob
    hit=pg.sprite.groupcollide(mobs,bullets,True,True)
    for i in hit:
        score+=60- i.size
        if random.random()>.8:
            po=powe(i.rect.center,random.choice(['shield','gun']))
            powerups.add(po)
            sp.add(po)
        random.choice(expl).play()
        a=explosion(i.rect.center,'lg')
        sp.add(a)
        newmob()
    #player and mob
    hit=pg.sprite.spritecollide(player,mobs,True,pg.sprite.collide_circle)
    for i in hit:
        c=explosion(i.rect.center,'lg')
        sp.add(c)
        player.shield-=(i.size)//2
        newmob()
    if player.shield<=0:
        z=explosion(player.rect.center,'sm')
        sp.add(z)
        player.rect.center=(100,600)
        player.lives-=1
        player.shield=100
        if player.lives==0:
            g0.play()
            game_over=True
            screen.fill(black)
    #powerup
    hit=pg.sprite.spritecollide(player,powerups,True,pg.sprite.collide_circle)
    for i in hit:
        if po.type=='shield':
            player.shield+=20
            if player.shield>100:
                player.shield=100
        if po.type=='gun':
            player.power+=2
    screen.blit(back_image,back_rect)
    sp.draw(screen)
    bar(player.shield,5,5,screen)
    close(450,10)
    lives(screen,player.lives,370,5,life)
    lifes(screen,'x'+str(player.lives),18,400,5)
    point(screen,str(score),18,250,10)
    pg.display.flip()
pg.quit()
