from interfaces import SnakeUI, SnakeWorld
from constants import Command

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
import sys
from kivy.config import Config
from kivy.core.window import Window
from kivy.clock import Clock


class Head(Widget):
    def __init__(self, grid_pos, direction=None, **kwargs):
        super(Head, self).__init__(**kwargs)
        self.grid_pos = grid_pos


class Body(Widget):
    def __init__(self, grid_pos, **kwargs):
        super(Body, self).__init__(**kwargs)
        self.grid_pos = grid_pos


class Fruit(Widget):
    def __init__(self, grid_pos, **kwargs):
        super(Fruit, self).__init__(**kwargs)
        self.grid_pos = grid_pos


# creating the root widget used in .kv file
class PlayField(BoxLayout):
    game_view = ObjectProperty()
    score_label = ObjectProperty()

    def __init__(self, world, **kwargs):
        super().__init__(**kwargs)
        self.world = world
        self.command = Command.RIGHT

        self.rows = self.world.height
        self.cols = self.world.width

        #    print("WS",Window.size)
        #    print("GV",self.game_view.size)
        self.widget_size = Window.size[0] / self.cols
        #    print("WidgetSize",self.widget_size)

        self.widgets = []

        Window.bind(on_key_down=self.key_action)
        self.show_world()

    def show_world(self):
        for widget in self.widgets:
            self.game_view.remove_widget(widget)
        self.widgets = []
        self.score_label.text = str(self.world.score)
        fruit = Fruit(self.world.food)
        self.add_my_widget(fruit)
        head = Head(self.world.snake[0])
        self.add_my_widget(head)
        for body_part in self.world.snake[1:]:
            body = Body(body_part)
            self.add_my_widget(body)

    def add_my_widget(self, widget):
        """add a new widget on the grid"""
        # print("WindowSize", Window.size)
        #    print("GridPos",widget.grid_pos)

        widget.x = widget.grid_pos[0] * self.widget_size
        widget.y = (
            Window.size[1] - self.widget_size - widget.grid_pos[1] * self.widget_size
        )
        #    print("WidgetPos",widget.x,widget.top)
        widget.size_hint = (None, None)
        widget.size = (self.widget_size, self.widget_size)
        self.game_view.add_widget(widget)
        self.widgets.append(widget)

    def key_action(self, *args):
        # print("Key", args)
        if args[1] == 273:
            self.move_snake("up")
        elif args[1] == 274:
            self.move_snake("down")
        elif args[1] == 275:
            self.move_snake("right")
        elif args[1] == 276:
            self.move_snake("left")

    def move_snake(self, direction):
        # score = int(self.score_label.text) + 1
        # self.score_label.text = str(score)
        self.score_label.text = str(self.world.score)
        direction2command = {
            "up": Command.UP,
            "down": Command.DOWN,
            "right": Command.RIGHT,
            "left": Command.LEFT,
        }
        self.command = direction2command[direction]

    def update(self, dt):
        still_running = self.world.update(self.command)
        if not still_running:
            print("Game Over")
            App.get_running_app().stop()
        self.show_world()


# creating the App class in which name
# .kv file is to be named snakeapp.kv
class SnakeApp(App):
    def __init__(self, world, **kwargs):
        super().__init__(**kwargs)
        self.world = world
        Clock.schedule_interval(self.update, 1.0 / 6.0)

    # defining build()
    def build(self):
        # returning the instance of root class
        return PlayField(self.world)

    def command(self):
        return self.root.command

    def update(self, dt):
        self.root.update(dt)

    def on_stop(self):
        # print("SnakeApp stoppt")
        self.world.last_command = Command.EXIT
        self.world.game_over = True


# Klasse orientiert sich an TextUI, aber mit pygame statt curses
class KivyUI(SnakeUI):
    def __init__(self, world: SnakeWorld) -> None:
        self.world = world
        # siehe https://github.com/kivy/kivy/issues/8257
        # https://support.microsoft.com/en-us/windows/change-your-screen-resolution-in-windows-5effefe3-2eac-e306-0b5d-2073b765876b
        SCREEN_SCALE = (Window.dpi / 96.0) if sys.platform in ["win32"] else 1.0
        Config.set("graphics", "width", int(1200 / SCREEN_SCALE))
        Config.set("graphics", "height", int(1800 / SCREEN_SCALE))
        Config.set("graphics", "resizable", "0")
        Config.set("kivy", "log_level", "error")
        Config.write()
        # print("Platform", sys.platform)

        self.app = SnakeApp(world)
        self.app.run()
        # print("KivyUI stoppt")

    def draw(self, world: SnakeWorld) -> None:
        pass

    def get_command(self) -> Command:
        # print("Command", self.app.command())
        return self.app.command()

    def timeout(self, new_timeout: int) -> None:
        pass

    def game_aborted(self) -> bool:
        return self.get_command() == Command.EXIT

    def close(self) -> None:
        pass
