from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.properties import ListProperty,StringProperty,ObjectProperty,BooleanProperty
import random

from Character import Block,Air
from tools import distance

class UiBox(BoxLayout):
    bcol=ListProperty((1,1,1,1))

class Battle(RelativeLayout):

    state=StringProperty("ready")
    turn=StringProperty("player")


    def load(self):
        pass

class Square(Widget):

    active=BooleanProperty(False)
    bcol=ListProperty((0,0,0,.2))
    pressed=ListProperty([0,0])
    gpos=ListProperty((0,0))
    highlight=BooleanProperty(False)
    block=ObjectProperty(Air())

    @property
    def blockheight(self):
        if not isinstance(self.block,Air):
            return self.block.blockheight
        else:
            return 0

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self.pressed=touch.pos
            return True
        return super().on_touch_down(touch)

    def collide_point(self, x, y):
        if super().collide_point(x,y):
            x = abs(self.center_x - x)
            y = abs(self.center_y - y)
            if x+y<sum(self.size)/4:

                return True
        return False

    def on_pressed(self,instance,pos):
        if self.highlight:
            return self.parent.active.block.hop(self)
        self.parent.active=self

    def on_active(self,_,b):
        if b is True and\
                self.battle.turn=="player" and\
                self.block is not None and\
                not isinstance(self.block,Air) and\
                self.battle.state=="ready":
            self.block.activate()


    def on_highlight(self,*_):
        pass

    @property
    def adjacenttiles(self):
        return list(filter(lambda a: distance(a.gpos,self.gpos)<=1.5 and a is not self ,self.parent.tiles))



class Grid(RelativeLayout):
    _active=ObjectProperty(None)
    _highlighted=ListProperty([])
    def __init__(self,**kw):

        super().__init__(**kw)
        self.tiles=[]
        self.blocks=[]
        h=50
        for x in range(10):
            ax = x * 50
            for y in range(10):
                ay=y*h
                fy=ay/2+ax/2
                fx=ax-ay-50
                square=Square(size=(100,h),
                              pos=(fx,fy),
                              bcol=[.2+(random.random()/4) for _ in range(3)]+[1],
                              gpos=(x,y))
                self.tiles.append(square)
                self.add_widget(square,index=fy)

        self.add_block(Block(),self.tiles[10])
        self.add_block(Block(),self.tiles[11])

    def add_block(self,block,tile):
        block.tile=tile
        block.center=tile.center
        self.add_widget(block)
        self.blocks.append(block)
        block.zefresh()

    @property
    def state(self):
        return self.battle.state

    @state.setter
    def state(self,value):
        if value=="ready":
            print()
            for pos,i in enumerate(reversed(self.tiles)):
                x="x" if isinstance(i.block,Block) else " "
                print(x,end=f"|"+(str("\n" if i.gpos[1]==0 else "")))
        self.battle.state=value

    @property
    def highlighted(self):
        return self._highlighted

    @highlighted.setter
    def highlighted(self,tiles):
        tiles=list(tiles)
        for i in self._highlighted:
            i.highlight=False
        for i in tiles:
            i.highlight=True
        self._highlighted=tiles

    @property
    def active(self):
        return self._active
    @active.setter
    def active(self,value):

        if self._active is not None:
            self._active.active=False
        self.highlighted=[]
        value.active=True
        self._active=value


class Game(App):
    pass

if __name__=="__main__":
    Game().run()