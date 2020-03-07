from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import StringProperty,ObjectProperty,ListProperty,NumericProperty
from kivy.lang.builder import Builder
from tools import distance
from kivy.animation import Animation
Builder.load_file("character.kv")
from functools import partial
import random

class Air:
    pass

class Block(RelativeLayout):
    sprite=StringProperty("images/base_brick_block.png")
    damage=1
    health=3
    tile=ObjectProperty(None)
    animpos=ListProperty([0,0])
    scale=NumericProperty(0.8)
    rang=NumericProperty(5)

    @property
    def gpos(self):
        return self.tile.gpos

    @property
    def blockheight(self):
        return self.height/2.125

    def activate(self):

        self.parent.highlighted=filter(
            lambda a:distance(a.gpos,self.tile.gpos)<=self.rang and a is not self.tile,
            self.parent.tiles)

    @property
    def ax(self):
        return self.animpos[0]

    @ax.setter
    def ax(self,value):
        self.animpos=value,self.animpos[1]

    @property
    def ay(self):
        return self.animpos[1]

    @ay.setter
    def ay(self,value):
        self.animpos=self.animpos[0],value

    def hop(self,tile):
        last=True
        d=distance(self.tile.pos,tile.pos)

        m=d/150
        t=.5+.1*m


        Animation(center_x=tile.center_x,center_y=tile.center_y+tile.blockheight,duration=t).start(self)
        a=Animation(ay=50+50*m,duration=t*.5,t="out_quad")


        b=Animation(ay=0,duration=t*.5,t="in_quad")

        i=0
        z=0
        t = "self"

        if not isinstance(tile.block,Air):
            l=lambda a: [self.hit(tile.block), self.hop(random.choice(tile.adjacenttiles)) ]
            b.on_complete=l
            last=False
            z=0
            tile.block.zefresh(z=z,i=1,t="target")

        a.on_complete=lambda a:self.zefresh(z=z,i=i,t=t)

        f=a+b
        f.start(self)
        self.parent.highlighted=[]
        self.tile.block = Air()

        if last:
            self.tile=tile

    def on_tile(self,_,tile):
        tile.block=self

    def hit(self,block):
        block.health-=self.damage

    def zefresh(self,i=0,z=0,t=""):
        g=self.parent
        if z!=0:
            index=z-i
        else:
            index=sum(self.gpos)-i
        print(f"BLOK zefresh {index} {t}")

        self.parent.remove_widget(self)
        g.add_widget(self,index=index)

class BrickBlock(Block):
    damage=2

class OldBrickBlock(BrickBlock):
    damage = 3
    health = 2

class MagicBlock(Block):
    def hop(self,tile):

        Animation(center_x=tile.center_x,center_y=tile.center_y).start(self)
        a=Animation(ay=100,duration=.5,t="out_cubic")+Animation(ay=0,duration=.5,t="in_quint")

        a.start(self)
        self.parent.highlighted=[]
        self.tile=tile

class Stack(Widget):
    stack=ListProperty([])

