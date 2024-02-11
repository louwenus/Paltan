from kivy.app import App
# from kivy.graphics import Color
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
# from kivy.uix.textinput import TextInput
# from kivy.uix.widget import Widget
# from kivy.uix.label import Label
from kivy.properties import (
    ObjectProperty, StringProperty, ColorProperty, NumericProperty)
from kivy.core.audio import SoundLoader
from random import shuffle

dRING = SoundLoader.load('assets/DRING.wav')
ding = SoundLoader.load('assets/ding.wav')


words = []
with open('assets/mots.txt', 'r') as file:
    for word in file:
        words.append(word[:-1])
shuffle(words)
party_count = 0


class MainScreen(FloatLayout):
    start = ObjectProperty(None)
    quitter = ObjectProperty(None)

    def __init__(self, appli, **kwargs):
        super().__init__(**kwargs)
        self.start.bind(on_press=appli.next_screen)
        self.quitter.bind(on_press=self.exitapp)

    def exitapp(self, *args):
        exit(0)


class Counter(ButtonBehavior, FloatLayout):
    counter = StringProperty("0")
    fgcolor = ColorProperty((1, 0.2, 0.2))
    r = NumericProperty(0)
    g = NumericProperty(0)
    b = NumericProperty(0)
    val = 0

    
    def reinit(self, fgcolor, bgcolor, value):
        self.fgcolor = fgcolor
        self.r, self.g, self.b = bgcolor
        self.counter = str(value)
        self.val = value

    def decrement(self):
        self.val -= 1
        self.counter = str(self.val)
        return self.val
    
    def terminate(self, *_):
        print("terminate called")
        self.val = 1
        self.counter = "1"


class Worddisplay(FloatLayout):
    word_cnt = 0
    word = StringProperty("")
    progress = NumericProperty(1000)

    def reinit(self):
        self.progress = 1000
        self.word = words[self.word_cnt]
        self.word_cnt += 1
        if self.word_cnt >= len(words):
            shuffle(words)
            self.word_cnt = 0

    def decrement(self, value):
        self.progress -= value
        return self.progress


class PaltanApp(App):
    phase = 0

    def build(self):
        self.main_layout = BoxLayout(orientation="vertical")
        self.screens = {
            "main": MainScreen(self),
            "counter": Counter(),
            "wo_di": Worddisplay()
        }
        self.screens["counter"].bind(
                on_press=self.screens["counter"].terminate)
        self.main_layout.add_widget(self.screens["main"])
        return self.main_layout

    def clock_callback_counter(self, dt):
        if (self.screens["counter"].decrement() == 0):
            Clock.schedule_once(self.next_screen)
            return False
        return True

    def clock_callback_word(self, dt):
        if (self.screens["wo_di"].decrement(dt*100) <= 0):
            Clock.schedule_once(self.next_screen)
            return False
        return True

    def next_screen(self, *args):
        self.phase += 1

        match self.phase:
            case 1:
                self.main_layout.remove_widget(self.screens["main"])
                self.main_layout.add_widget(self.screens["counter"])
                self.screens["counter"].reinit((.7, .3, .2), (.2, .2, 1), 3)
                Clock.schedule_interval(self.clock_callback_counter, 1)
            case 2:
                ding.play()
                self.main_layout.remove_widget(self.screens["counter"])
                self.main_layout.add_widget(self.screens["wo_di"])
                self.screens["wo_di"].reinit()
                Clock.schedule_interval(self.clock_callback_word, 0.01)
            case 3:
                ding.play()
                self.main_layout.remove_widget(self.screens["wo_di"])
                self.main_layout.add_widget(self.screens["counter"])
                self.screens["counter"].reinit((0, 0, 0), (1, .2, .2), 5)
                Clock.schedule_interval(self.clock_callback_counter, 1)
            case 4:
                dRING.play()
                self.screens["counter"].reinit((0, 0, 0), (0, 0.8, 0), 20)
                Clock.schedule_interval(self.clock_callback_counter, 1)
            case 5:
                ding.play()
                self.phase = 0
                self.main_layout.remove_widget(self.screens["counter"])
                self.main_layout.add_widget(self.screens["main"])


if __name__ == "__main__":
    app = PaltanApp()
    app.run()
