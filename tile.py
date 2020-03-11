from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.properties import ListProperty,StringProperty,ObjectProperty,BooleanProperty
import random
from Character import *
from tools import distance


class Square(Widget):

    active=BooleanProperty(False)
    bcol=ListProperty((0,0,0,.2))
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
            if self.highlight and touch.button=="right":
                return self.parent.active.block.hop(self)
            self.parent.active = self
            return True
        return super().on_touch_down(touch)

    def collide_point(self, x, y):
        if super().collide_point(x,y):
            x = abs(self.center_x - x)
            y = abs(self.center_y - y)
            if x+y<sum(self.size)/4:

                return True
        return False


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

