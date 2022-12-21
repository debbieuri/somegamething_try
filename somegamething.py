
import pygame,random,math
pygame.init()

ccc=[(255,255,255),(0,0,255),(255,0,0),(255,255,0),(0,255,255)]#add more ..?
class firework:
    def __init__(self,t,a,g,p,c,r,q):
        self.q=q
        self.t=t
        self.r=r
        self.pos=p
        self.going=g
        self.a=a
        self.b=True
        if c==0:
            self.c=random.choice(ccc)
        else:
            self.c=c
    def update(self):
        if self.b:
            if self.t==1:
                pygame.draw.line(G.d,(0,0,0),self.pos,(self.pos[0]+self.going[0],self.pos[1]+self.going[1]),2)
                pygame.draw.line(G.d,self.c,self.pos,(self.pos[0]+self.going[0],self.pos[1]+self.going[1]))
                self.going[1]+=G.ws[1]/1000
            elif self.t==2:
                pygame.draw.circle(G.d,(0,0,0),(self.pos[0]+self.going[0],self.pos[1]+self.going[1]),self.r+1)
                pygame.draw.circle(G.d,self.c,(self.pos[0]+self.going[0],self.pos[1]+self.going[1]),self.r)
                self.going[1]+=G.ws[1]/1000
            else:
                pass#############
            self.pos[0]+=self.going[0]
            self.pos[1]+=self.going[1]
            if self.pos[0]>G.ws[0] or self.pos[0]<0 or self.pos[1]>G.ws[1] or self.pos[1]<-G.ws[1]/4:
                return False
            if self.a:
                if self.pos[1]<G.ws[1]*self.q:
                    self.p=[]
                    for i in range(300):#360
                        x=random.random()*30+5
                        z=random.random()*90#uh...
                        g=[math.sin(z)*x*random.choice([-1,1]),10+math.cos(z)*x*random.choice([-1,1])]
                        self.p.append(firework(self.t,False,g.copy(),self.pos.copy(),self.c,random.randint(1,4),0))
                    self.b=False
        else:
            x=0
            for p in range(len(self.p)):
                if not self.p[p-x].update():
                    self.p.pop(p-x)
                    x+=1
            if len(self.p)==0:
                return False
        return True

class game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.s = [40,50,10,20,10,11,17,6]#..?
        self.t = 7#1 ####amount of turns/guesses
        self.n = 4#1 ####length of guess
        self.ws = [self.s[1]*self.n+self.s[2]*3+(self.n+1)//2*self.s[6]+self.s[7],self.s[0]*self.t+self.s[3]*(self.t-1)+4*self.s[4]+self.s[0]]
        self.d = pygame.display.set_mode(self.ws)
        self.cc = [(255,0,0),(255,100,00),(250,0,250),(220,220,0),(0,255,0),(20,20,240)]
        self.mcc = [(60,150,60),(0,0,0),(255,255,255)]#markings...
        self.bgc = (100,200,100)
        self.pm = []
        self.w = [random.randint(0,len(self.cc)-1) for i in range(self.n)]
        print(self.w,'<winning')
        self.p = [[0 for i in range(self.n)]]
        self.pr = [pygame.rect.Rect(self.s[1]*i+self.s[2],self.ws[1]-self.s[4]-self.s[0],self.s[0],self.s[0]) for i in range(self.n)]
        self.pc = pygame.rect.Rect(self.ws[0]-((self.n+1)//2*self.s[6]+self.s[7])-self.s[2],self.ws[1]-self.s[4]-self.s[0],((self.n+1)//2*self.s[6]+self.s[7]),self.s[0])

    def markingtime(self):
        p,w,m=[],[],[]
        for i in range(self.n):
            if self.w[i] == self.p[-1][i]:
                m.append(1)#black
            else:
                p.append(self.p[-1][i])
                w.append(self.w[i])
        if len(m)==self.n:
            self.gamedone(True)
        for i in w:
            for j in range(len(p)):
                if p[j]==i:
                    m.append(2)#white
                    p.pop(j)
                    break
        self.pm.append(m)
        if len(self.p)==self.t:
            self.gamedone(False)
        self.p.append([0 for i in range(self.n)])
        y=len(self.p)-1
        self.pr = [pygame.rect.Rect(self.s[1]*x+self.s[2],self.ws[1]-(self.s[0]*y+self.s[3]*y+self.s[4])-self.s[0],self.s[0],self.s[0]) for x in range(self.n)]
        self.pc = pygame.rect.Rect(self.ws[0]-((self.n+1)//2*self.s[6]+self.s[7])-self.s[2],self.ws[1]-(self.s[0]*y+self.s[3]*y+self.s[4])-self.s[0],((self.n+1)//2*self.s[6]+self.s[7]),self.s[0])

    def gamedone(self,won):
        font = pygame.font.SysFont('bell',60)#get a more fancy font 
        self.pc=pygame.rect.Rect(self.ws[0],self.ws[1],self.pc[2],self.pc[3])
        self.display()
        print('you win!' if won else 'you lose!')
        for i in range(self.n):
            pygame.draw.rect(self.d,self.cc[self.w[i]],(self.s[1]*i+self.s[2],self.s[4],self.s[0],self.s[0]))
        text = font.render('you win!' if won else 'you lose!',True,(0,0,0))
        self.d.blit(text,((self.ws[0]-text.get_width())//2+2,(self.ws[1]-text.get_height())//2+2))
        self.d.blit(text,((self.ws[0]-text.get_width())//2-2,(self.ws[1]-text.get_height())//2-2))
        base=pygame.surface.Surface(self.ws)
        base.blit(self.d,(0,0))
        f=[firework(random.randint(1,3),True,[0,-self.ws[1]/20],[random.randint(int(self.ws[0]/4),int(self.ws[0]/4*3)),self.ws[1]],0,2,random.random()/2+0.4) for _ in range(3)]
        rgb=[250,0,250]
        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    fsdkjklsfwfs
            if rgb==[250,0,250]:
                up=[0,1,-1]
            if rgb==[0,250,250]:
                up=[1,-1,0]
            if rgb==[250,250,0]:
                up=[-1,0,1]
            rgb=[rgb[0]+up[0],rgb[1]+up[1],rgb[2]+up[2]]
            self.d.blit(base,(0,0))
            text = font.render('you win!' if won else 'you lose!',True,rgb)
            self.d.blit(text,((self.ws[0]-text.get_width())//2,(self.ws[1]-text.get_height())//2))
            for ff in f:
                if not ff.update():
                    f.remove(ff)
                    f.append(firework(random.randint(1,3),True,[random.randint(-10,10),-self.ws[1]/20],[random.randint(int(self.ws[0]/4),int(self.ws[0]/4*3)),self.ws[1]],0,2,random.random()/2+0.4))
            pygame.display.update()
            self.clock.tick(30)

    def display(self):
        self.d.fill(self.bgc)
        pygame.draw.rect(self.d,self.mcc[0],(0,0,self.ws[0],2*self.s[4]+self.s[0]))
        for y in range(len(self.p)):
            for x in range(self.n):
                pygame.draw.rect(self.d,self.cc[self.p[y][x]],(self.s[1]*x+self.s[2],self.ws[1]-(self.s[0]*y+self.s[3]*y+self.s[4])-self.s[0],self.s[0],self.s[0]))
                pygame.draw.line(self.d,(0,0,0),(self.s[1]*x+self.s[2],self.ws[1]-(self.s[0]*y+self.s[3]*y+self.s[4])-self.s[0]),(self.s[0]+self.s[1]*x+self.s[2],self.ws[1]-(self.s[0]*y+self.s[3]*y+self.s[4])-self.s[0]),2)#outline
                pygame.draw.line(self.d,(0,0,0),(self.s[1]*x+self.s[2],self.ws[1]-(self.s[0]*y+self.s[3]*y+self.s[4])-self.s[0]),(self.s[1]*x+self.s[2],self.s[0]+self.ws[1]-(self.s[0]*y+self.s[3]*y+self.s[4])-self.s[0]),2)#outline
                pygame.draw.line(self.d,(0,0,0),(self.s[0]+self.s[1]*x+self.s[2],self.ws[1]-(self.s[0]*y+self.s[3]*y+self.s[4])-self.s[0]),(self.s[0]+self.s[1]*x+self.s[2],self.s[0]+self.ws[1]-(self.s[0]*y+self.s[3]*y+self.s[4])-self.s[0]),2)#outline
                pygame.draw.line(self.d,(0,0,0),(self.s[1]*x+self.s[2],self.s[0]+self.ws[1]-(self.s[0]*y+self.s[3]*y+self.s[4])-self.s[0]),(self.s[0]+self.s[1]*x+self.s[2],self.s[0]+self.ws[1]-(self.s[0]*y+self.s[3]*y+self.s[4])-self.s[0]),2)#outline
        for y in range(len(self.pm)):
            pygame.draw.rect(self.d,self.mcc[0],(self.ws[0]-((self.n+1)//2*self.s[6]+self.s[7])-self.s[2],self.ws[1]-(self.s[0]*y+self.s[3]*y+self.s[4])-self.s[0],((self.n+1)//2*self.s[6]+self.s[7]),self.s[0]))
            for i in range(len(self.pm[y])):
                if i&1:
                    pygame.draw.rect(self.d,self.mcc[self.pm[y][i]],(self.ws[0]-((self.n-i-1)//2*self.s[6]+self.s[7])-self.s[2]-self.s[5],self.ws[1]-(self.s[0]*y+self.s[3]*y+self.s[4])-self.s[0]+self.s[7]+self.s[6],self.s[5],self.s[5]))
                else:
                    pygame.draw.rect(self.d,self.mcc[self.pm[y][i]],(self.ws[0]-((self.n-i-1)//2*self.s[6]+self.s[7])-self.s[2]-self.s[5],self.ws[1]-(self.s[0]*y+self.s[3]*y+self.s[4])-self.s[0]+self.s[7],self.s[5],self.s[5]))
        pygame.draw.rect(self.d,(0,0,0),self.pc)
        pygame.draw.line(self.d,(255,255,255),(self.pc[0]+self.pc[2]//2+15,self.pc[1]+5),(self.pc[0]+self.pc[2]//2,self.pc[1]+35),3)
        pygame.draw.line(self.d,(255,255,255),(self.pc[0]+self.pc[2]//2-5,self.pc[1]+20),(self.pc[0]+self.pc[2]//2,self.pc[1]+35),3)
        pygame.display.update()

    def play(self):         
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    return
                if e.type == pygame.MOUSEBUTTONDOWN:
                    p = pygame.mouse.get_pos()
                    for r in range(len(self.pr)):
                        if self.pr[r].collidepoint(p):
                            self.p[-1][r]+=1
                            self.p[-1][r]%=len(self.cc)
                    if self.pc.collidepoint(p):
                        self.markingtime()
                if e.type==pygame.KEYDOWN:
                    if e.key==pygame.K_RETURN:
                        self.markingtime()
            self.display()
            self.clock.tick(60)

G=game()
G.play()
