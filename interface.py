'''Widgets for the full app interface.'''

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.actionbar import ActionBar
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import ListProperty, ObjectProperty, StringProperty

from os.path import exists
from glob import glob
import random

class NavBar(ActionBar):
    pass

class PhutballInterface(BoxLayout):
    manager = ObjectProperty()
    actionbar = ObjectProperty()

class PhutballManager(ScreenManager):
    def new_board(self, ai=False, from_file=None, force_switch=False,
                  touch_mode='play_man', mode='normal'):
        '''Creates and moves to a new board screen.'''
        if not self.has_screen('board'):
            new_screen = GameScreen(name='board')
            self.add_widget(new_screen)
        elif force_switch and not self.has_screen('board2'):
            new_screen = GameScreen(name='board2')
            self.add_widget(new_screen)
        next = 'board'
        if self.current in ('board', 'board2'):
            if force_switch:
                next = {'board': 'board2', 'board2': 'board'}[self.current]
            else:
                next = self.current
        board = self.get_screen(next).children[0].board
        board.reset(touch_mode=touch_mode, game_mode=mode)
        if from_file is not None:
            board.load_position(from_file)
        board.use_ai = ai
        self.go_to(next)

    def tutorial(self):
        self.new_board(from_file='puzzles/dir01_tutorials/tutorial1.phut',
                       mode='tutorial1')

    def puzzles_index(self):
        if not self.has_screen('puzzles_index'):
            new_screen = ProblemChooserScreen()
            new_screen.populate()
            self.add_widget(new_screen)
        self.go_to('puzzles_index')

    def rules(self):
        if not self.has_screen('rules'):
            new_screen = RulesScreen(name='rules')
            self.add_widget(new_screen)
        self.go_to('rules')

    def go_to(self, name, forward=True):
        if self.transition.is_active:
            return
        self.transition = SlideTransition(direction='left')
        if not forward:
            self.transition = SlideTransition(direction='right')
        self.current = name
        self.transition = SlideTransition(direction='left')

    def on_current(self, *args):
        super(PhutballManager, self).on_current(*args)

    def go_back(self, *args):
        popup = App.get_running_app().popup
        if popup:
            popup.dismiss()
        target = 'home'
        if self.current in ('board', 'board2'):
            target = 'home'
        self.go_to(target, forward=False)

    def go_home(self, *args):
        self.go_to('home', forward=False)

    def try_save(self):
        '''Tries to save the current board in a new filename, automatically generated.

        This method is not intended for general use, only for
        development.

        '''
        filen = 'board'
        i = 0
        while exists(filen + '{}.phut'.format(i)):
            i += 1
        filen = filen + '{}.phut'.format(i)
        if self.has_screen('board'):
            screen = self.get_screen('board')
            board = screen.children[0].board
            board.save_position(filen)

    def try_load(self):
        '''Tries to load a random game.'''
        filens = glob('board*.phut')
        if not filens:
            return
        filen = random.choice(filens)
        self.new_board()
        screen = self.get_screen('board')
        board = screen.children[0].board
        board.load_position(filen)

        
class GameScreen(Screen):
    '''Screen containing a BoardInterface'''
    

class HomeScreen(Screen):
    pass


class RulesScreen(Screen):
    pass


class ProblemChooserScreen(Screen):
    chooser_container = ObjectProperty()
    def populate(self):
        filens = glob('puzzles/dir*')
        numbers = [int(name.split('_')[0]) for name in filens]
        argsort = [i for i, x in sorted(enumerate(numbers),
                                        key=lambda j: j[1])]

    def new_problem_set(self, filen):
        pass
        


class ProblemRow(BoxLayout):
    title = StringProperty('')
    identifier = StringProperty('')
    buttons = ObjectProperty()

class ProblemButton(Button):
    pass


class ProblemLabel(Label):
    pass


class ProblemChooser(GridLayout):
    pass
