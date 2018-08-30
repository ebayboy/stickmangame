from tkinter import *
import random
import time

#坐标类
class Coords:
    #左上(x1,y1)  右下：(x2,y2)
    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

#X重叠
def with_x(co1, co2):
    if (co1.x1 > co2.x1 and co1.x1 < co2.x1) \
        or (co1.x2 > co2.x1 and co1.x2 < co2.x2) \
        or (co2.x1 > co1.x1 and co2.x2 < co1.x1) \
        or (co2.x2 > co1.x1 and co2.x2 < co1.x2) :
        return True
    else:
        return False

#Y重叠
def with_y(co1, co2):
    if (co1.y1 > co2.y1 and co1.y1 < co2.y2) \
        or (co1.y2 > co2.y1 and co1.y2 < co2.y2) \
        or (co2.y1 >  co1.y1 and co2.y1 < co1.y2) \
        or (co2.y2 > co1.y1 and co2.y2 < co1.y2) :
        return True
    else:
        return False

def collied_left(co1, co2):
    if with_y(co1, co2):
        if co1.x1 <= co2.x2 and co1.x1 >= co2.x1:
            return True
    return False

#右侧冲突
def collied_right(co1, co2):
    if with_y(co1, co2):
        if co1.x2 <= co2.x2 and co1.x2 >= co2.x1:
            return True
    return False

#上面冲突
def collied_top(co1, co2):
    if with_x(co1, co2):
        if co1.y1 <= co2.y1 and co1.y1 >= co2.y2:
            return True
    return False

#预判断底部冲突
def collied_bottom(y, co1, co2):
    if with_x(co1, co2):
        y_calc = co1.y2 + y
        if y_calc  >= co2.y1 and y_calc <= co2.y2:
            return True
    return False

#game类
class Game:
    def __init__(self):
        #Tkinter 模块(Tk 接口)是 Python 的标准 Tk GUI 工具包
        self.tk = Tk()
        self.tk.title("Mr. Stick Man Races for the Exit")
        self.tk.resizable(0,0)
        self.tk.wm_attributes("-topmost", 1)

        #创建画布
        self.canvas = Canvas(self.tk, width=500, height=500, highlightthickness=0)
        self.canvas.pack()
        self.tk.update()
        self.canvas_height = 500
        self.canvas_width = 500

        #将小背景铺满屏幕
        self.bg = PhotoImage(file="image/backgroud.gif")
        w = self.bg.width()
        h = self.bg.height()
        for x in range(0, 5):
            for y in range(0, 5):
                self.canvas.create_image(x*w, y*h, image=self.bg, anchor = 'nw')

        self.sprites = []
        self.running = True

    #主循环
    def mainloop(self):
        while 1:
            if self.running == True:
                for sprite in self.sprites:
                    sprite.move()
            #mainhold GUI
            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.01)

#sprite类， 所有元素看成是精灵， 通用方法move && coords
class Sprite:
    def __init__(self, game):
        self.game  =game
        self.endgame = False
        #coordinates 是Coords类的实例
        self.coordinates = None

    def move(self):
        pass

    def coords(self):
        return self.coordinates

#平台类
class PlatformSprte(Sprite):
    def __init__(self, game, photo_image, x, y, width, height):
        Sprite.__init__(self,game)
        #平台图片
        self.photo_image = photo_image
        #创建的图片对象
        self.image = game.canvas.create_image(x, y, image=self.photo_image, anchor='nw')
        #坐标
        self.coordinates = Coords(x,y, x+width, y + height)

#火柴人类
class StickFigureSprite(Sprite):
    def __init__(self, game):
        Sprite.__init__(self,game)
        #向左跑图片列表
        self.images_left = [
            PhotoImage(file="image/stick-L1.gif"),
            PhotoImage(file="image/stick-L2.gif"),
            PhotoImage(file="image/stick-L3.gif")
            ]
        #向右跑图片列表
        self.images_right = [
            PhotoImage(file="image/stick-R1.gif"),
            PhotoImage(file="image/stick-R2.gif"),
            PhotoImage(file="image/stick-R3.gif")
        ]

        #创建图片对象
        self.image = game.canvas.create_image(200, 470, \
                image=self.images_left[0], anchor='nw')

        #初始化其他参数
        #x, y代表向左右或者上下移动
        self.x = -2
        self.y = 0

        self.current_image = 0
        self.current_image_add = 1
        self.jump_count = 0
        self.last_time = time.time()
        self.coordinates = Coords()

        #绑定按键
        game.canvas.bind_all('<KeyPress-Left>',self.turn_left)
        game.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        game.canvas.bind_all('<space>', self.jump)

    def turn_left(self,evt):
        if self.y == 0:
            self.x = -2

    def turn_right(self,evt):
        if self.y == 0:
            self.x = 2

    def jump(self, evt):
        if self.y == 0:
            self.y = -4
            self.jump_count = 0

    #实现动画效果
    def animate(self):
        if self.x != 0 and self.y == 0:
            if time.time() - self.last_time > 0.1:
                self.last_time = time.time()
                self.current_image += self.current_image_add
                if self.current_image >= 2:
                    self.current_image_add = -1
                if self.current_image <= 0:
                    self.current_image_add = 1
        if self.x < 0:
            #jump
            if self.y != 0:
                self.game.canvas.itemconfig(self.image, image=self.images_left[2])
            else:
            #move
                self.game.canvas.itemconfig(self.image, image=self.images_left[self.current_image])
        elif self.x > 0:
            if self.y != 0:
                self.game.canvas.itemconfig(self.image, image=self.images_right[2])
            else:
                self.game.canvas.itemconfig(self.image, image=self.images_right[self.current_image])

    def coords(self):
        #获取图片对象的位置信息
        xy = self.game.canvas.coords(self.image)
        self.coordinates.x1 = xy[0]
        self.coordinates.y1 = xy[1]
        self.coordinates.x2 = xy[0] + 27
        self.coordinates.y2 = xy[1] + 30
        return self.coordinates

    def move(self):
        self.animate()
        #跳起状态
        if self.y < 0:
            self.jump_count += 1
            if self.jump_count > 20:
                self.y = 4
        if self.y > 0:
            self.jump_count -= 1

        #获取图片对象位置信息
        co = self.coords()

        #是否撞到上下左右， 默认True代表没撞到
        left = True
        right = True
        top = True
        bottom = True
        falling = True

        if self.y > 0 and co.y2 >= self.game.canvas_height:
            self.y = 0
            bottom = False #到达底部
        elif self.y < 0 and co.y1 <= 0:
            self.y = 0
            top = False  #到达顶部
        elif  self.x > 0 and co.x2 >= self.game.canvas_width:
            self.x = 0
            right = False  #超过右边界
        elif self.x < 0 and co.x1 <= 0:
            self.x = 0
            left = False  #到达左边界

        #查看是否与其他精灵（物体）有碰撞
        for sprite in self.game.sprites:
            #跳过和自己的碰撞的检测
            if sprite == self:
                continue

            sprite_co = sprite.coords()
            #没有撞到画布顶部 and 跳跃状态 and 顶部撞到其他精灵
            if top and self.y < 0 and collied_top(co, sprite_co):
                self.y = -self.y #希望火柴人下落
                top = False #不再对火柴人进行检测

            #火柴人没有到底底部 and 火柴人下落状态  and 火柴人底部撞到其他精灵（物品)
            if bottom and self.y > 0 and collied_bottom(self.y, co, sprite_co):
                #如果预判断底部冲突， 则下次下落的距离设置为到地板的距离， 这样火柴人就不会撞到底部再弹起来
                self.y = sprite_co.y1 - co.y2
                if self.y < 0:
                    self.y = 0
                bottom = False
                top = False

            #没有到达底部  & 没有下落 &
            if bottom and falling and self.y == 0 and co.y2 < self.game.canvas_height and collied_bottom(1, co, sprite_co):
                falling = False

            #左侧冲突检测 & 向左移动 & 左侧与精灵发生冲突
            if left and self.x < 0 and collied_left(co, sprite_co):
                self.x = 0
                #设置左侧冲突（这样就不会再次检测左侧冲突）
                left = False
                if sprite.endgame:
                    self.game.running = False

            #右侧冲突检测
            if right and self.x > 0 and collied_right(co, sprite_co):
                self.x = 0
                right = False
                if sprite.endgame:
                    self.game.running = False

            #没有处于下落状态 & 没有撞到底部 & 没有处于跳起状态
            if falling and bottom and self.y == 0 and co.y2 < self.game.canvas_height:
                self.y = 4
        #移动图片对象
        self.game.canvas.move(self.image, self.x, self.y)

class DoorSprite(Sprite):
    def __init__(self, game, photo_image, x, y, width, height):
        Sprite.__init__(self, game)
        self.photo_image = photo_image
        self.image = game.canvas.create_image(x, y, image=self.photo_image, anchor = 'nw')
        self.coordinates = Coords(x, y, x + (width/2), y + height)
        self.endgame = True


co1 = Coords(40,40,100,100)
co2 = Coords(50, 50, 150, 150)
print(with_x(co1,co2))
print(with_y(co1,co2))

g = Game()

platform1 = PlatformSprte(g, PhotoImage(file="image\platform1.gif"), 0, 480, 100, 10)
platform2 = PlatformSprte(g, PhotoImage(file="image\platform1.gif"), 150, 440, 100, 10)
platform3 = PlatformSprte(g, PhotoImage(file="image\platform1.gif"), 300, 400, 100, 10)
platform4 = PlatformSprte(g, PhotoImage(file="image\platform1.gif"), 300, 160, 100, 10)

platform5 = PlatformSprte(g, PhotoImage(file="image\platform2.gif"), 175, 350, 66, 10)
platform6 = PlatformSprte(g, PhotoImage(file="image\platform2.gif"), 50, 300, 66, 10)
platform7 = PlatformSprte(g, PhotoImage(file="image\platform2.gif"), 170, 120, 66, 10)
platform8 = PlatformSprte(g, PhotoImage(file="image\platform2.gif"), 45, 60, 66, 10)

platform9 = PlatformSprte(g, PhotoImage(file="image\platform3.gif"), 170, 250, 32, 10)
platform10 = PlatformSprte(g, PhotoImage(file="image\platform3.gif"), 230, 200, 32, 10)

g.sprites.append(platform1)
g.sprites.append(platform2)
g.sprites.append(platform3)
g.sprites.append(platform4)
g.sprites.append(platform5)
g.sprites.append(platform6)
g.sprites.append(platform7)
g.sprites.append(platform8)
g.sprites.append(platform9)
g.sprites.append(platform10)

door = DoorSprite(g, PhotoImage(file="image/door1.gif"), 45, 30, 40, 35)
g.sprites.append(door)

sf = StickFigureSprite(g)
g.sprites.append(sf)
g.mainloop()







