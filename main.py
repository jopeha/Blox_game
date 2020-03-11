from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.properties import ListProperty,StringProperty,ObjectProperty,BooleanProperty
from kivy.clock import Clock
import random
from Character import *
from tile import Square
from player import *
from tools import distance
from kivy.config import Config
from copy import copy
from functools import partial



Config.set('input', 'mouse', 'mouse,disable_multitouch')

class UiBox(BoxLayout):
    bcol=ListProperty((1,1,1,1))

class Battle(RelativeLayout):

    state=StringProperty("ready")
    turn=StringProperty("player")

    def load(self):
        pass



class Grid(RelativeLayout):
    _active=ObjectProperty(None,allownone=True)
    _highlighted=ListProperty([])

    active_name=StringProperty("Some Air")
    active_icon=StringProperty("1")
    active_damage=StringProperty("1")
    active_range=StringProperty("1")
    active_health=StringProperty("1")
    active_sprite=StringProperty("images/air.png")
    _state="not ready"
    player_turn=ObjectProperty(None)
    teams=[]
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

        self.add_block(Block(),self.tiles[3])
        self.add_block(OldBrickBlock(),self.tiles[1])
        self.add_block(BrickBlock(),self.tiles[2])
        for i in range(40):
            self.add_block(OldBrickBlock(),self.tiles[4+i])

        self.ready()

        for pos,i in enumerate(sorted(self.blocks,key=lambda a:sum(a.gpos))):
            i.spawn_anim(6*(.4-(3/(pos+1))))

    def add_block(self,block,tile):
        block.tile=tile
        block.center=tile.center
        self.add_widget(block)
        self.blocks.append(block)
        block.zefresh()


    def ready(self):
        self.state="ready"

    def kill(self,block):
        self.blocks.remove(block)
        self.remove_widget(block)
        self.ready()

    @property
    def state(self):
        return self.battle.state

    @state.setter
    def state(self,value):
        if value=="ready" and self._state!="ready":
            DEAD=[*filter(lambda a:a.health<=0,self.blocks)]
            for i in DEAD:
                i.die()

            for i in sorted(self.blocks,key= lambda a:-sum(a.gpos)):
                self.remove_widget(i)
                self.add_widget(i)
            print("did thing")
        self._state=value

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
        if value is not None:
            value.active=True
            self._active=value
            self.active_stats(value.block)

    def active_stats(self,block):

        self.active_name=block.name
        self.active_damage=str(block.damage)
        self.active_range= str(block.rang)
        self.active_health=str(block.health)
        self.active_sprite = block.sprite


class Game(App):
    pass

if __name__=="__main__":
    Game().run()