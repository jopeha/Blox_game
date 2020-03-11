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
    name="Some air"
    damage=1
    health=1
    rang=1
    sprite="images/air.png"

class Block(RelativeLayout):

    name="Basic Block"
    sprite=StringProperty("images/base_brick_block.png")
    damage=1
    health=3
    tile=ObjectProperty(None,allownone=True)
    animpos=ListProperty([0,0])
    animpos2=ListProperty([0,0])

    scale=NumericProperty(0.8)
    rang=NumericProperty(5)
    dead=False
    player=None

    @property
    def my_turn(self):
        return self.parent.player_turn is self.player

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
        self.parent.active=None

        self.parent.state="anim"
        self.tile.block = Air()
        self.parent.highlighted = []

        d=distance(self.tile.pos,tile.pos)
        m=d/150
        t=.5+.1*m

        i=0
        z=None

        Animation(center_x=tile.center_x,center_y=tile.center_y+tile.blockheight,duration=t).start(self)
        a=Animation(ay=50+50*m,duration=t*.5,t="out_quad")
        b=Animation(ay=0,duration=t*.5,t="in_quad")

        t = "self"
        if not isinstance(tile.block,Air):
            l=lambda a: [self.hit(tile.block,self.damage), self.hop(random.choice(tile.adjacenttiles)) ]
            b.on_complete=l
            last=False
            z=-sum(tile.block.gpos)
            i=1

        a.on_complete=lambda a:self.zefresh(z=z,i=i,t=t)

        f=a+b

        def dolast(_):


            self.parent.state="ready"

        if last:
            self.tile=tile
            self.tile.block=self

            f.on_complete=dolast

        f.start(self)


    def on_tile(self,_,tile):
        tile.block=self

    def hit(self,block,damage):
        block.get_hit(damage)
        block.health-=damage

    def get_hit(self,damage):

        if damage>0:
            a=Animation(bcol=(1,.5,.5,1),ay=-2,duration=.2)+Animation(bcol=self.bcol,duration=.2,ay=0)
            a.start(self)

    def zefresh(self,i=0,z=None,t=""):
        g=self.parent
        if z is not None:
            index=z-i
        else:
            index=-sum(self.gpos)

        self.parent.remove_widget(self)
        g.add_widget(self,index=max(0,index))
        self._index=index

    def die(self):
        if self.dead:
            return
        self.dead=True
        a=Animation(opacity=0,ay=50,duration=.5,t="out_quad")
        a.on_complete=lambda a:[self.parent.kill(self),setattr(self.tile,"block",Air())]
        a.start(self)

    def spawn_anim(self,wait):

        self.opacity=0
        self.ay=300

        a=Animation(duration=wait)+Animation(opacity=1,ay=0,duration=.5,t="out_quad")
        return a.start(self)

class BrickBlock(Block):
    damage=2

class OldBrickBlock(BrickBlock):
    damage = 3
    health = 2
    rang = 1.5
    sprite = "images/old_brick_block.png"
    name = "Old Brick Block"
class MagicBlock(Block):
    def hop(self,tile):

        Animation(center_x=tile.center_x,center_y=tile.center_y).start(self)
        a=Animation(ay=100,duration=.5,t="in_sine")+Animation(ay=0,duration=.5,t="in_quint")

        a.start(self)
        self.parent.highlighted=[]
        self.tile=tile

class Stack(Widget):
    stack=ListProperty([])

"""icons"""

