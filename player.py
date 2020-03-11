from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.properties import ListProperty,StringProperty,ObjectProperty,BooleanProperty
import random
from tile import Square
from tools import distance
from kivy.config import Config
from copy import copy


class Player(Widget):
    pass