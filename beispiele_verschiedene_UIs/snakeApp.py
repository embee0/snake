from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
import sys
from kivy.config import Config
from kivy.core.window import Window

# siehe https://github.com/kivy/kivy/issues/8257
# https://support.microsoft.com/en-us/windows/change-your-screen-resolution-in-windows-5effefe3-2eac-e306-0b5d-2073b765876b
print("Platform", sys.platform)
SCREEN_SCALE = (Window.dpi / 96.0) if sys.platform in ["win32"] else 1.0
Config.set("graphics", "width", int(600 / SCREEN_SCALE))
Config.set("graphics", "height", int(900 / SCREEN_SCALE))
Config.set("graphics", "resizable", "0")
Config.write()


class Head(Widget):
    def __init__(self, grid_pos=None, direction=None, **kwargs):
        super(Head, self).__init__(**kwargs)

        # position head in middle of the screen
        if grid_pos is None:
            grid_pos = [10, 10]
        self.grid_pos = grid_pos


class Body(Widget):
    def __init__(self, grid_pos=None, **kwargs):
        super(Body, self).__init__(**kwargs)

        if grid_pos is None:
            grid_pos = [10, 11]
        self.grid_pos = grid_pos


class Fruit(Widget):
    def __init__(self, grid_pos=None, **kwargs):
        super(Fruit, self).__init__(**kwargs)

        if grid_pos is None:
            grid_pos = [2, 3]
        self.grid_pos = grid_pos


# creating the root widget used in .kv file
class PlayField(BoxLayout):
    game_view = ObjectProperty()
    score_label = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # create chess board pattern on float layout
        self.rows = 20
        self.cols = 20

        #    print("WS",Window.size)
        #    print("GV",self.game_view.size)
        self.widget_size = Window.size[0] / self.cols
        #    print("WidgetSize",self.widget_size)

        Window.bind(on_key_down=self.key_action)

        # add first fruit
        # self.fruit = Fruit([19,19])
        self.fruit = Fruit()
        print("Fruit")
        self.add_my_widget(self.fruit)

        # add head
        self.head_pos = [0, 0]
        self.head = Head(self.head_pos)
        # self.head = Head()
        print("Head")
        self.add_my_widget(self.head)
        # add body
        self.body = Body()
        print("Body")
        self.add_my_widget(self.body)

    def key_action(self, *args):
        print("Key", args)
        if args[1] == 273:
            self.move_snake("up")
        elif args[1] == 274:
            self.move_snake("down")
        elif args[1] == 275:
            self.move_snake("right")
        elif args[1] == 276:
            self.move_snake("left")

    def add_my_widget(self, widget):
        """add a new widget on the grid"""
        print("WindowSize", Window.size)
        #    print("GridPos",widget.grid_pos)

        widget.x = widget.grid_pos[0] * self.widget_size
        widget.y = (
            Window.size[1] - self.widget_size - widget.grid_pos[1] * self.widget_size
        )
        #    print("WidgetPos",widget.x,widget.top)
        widget.size_hint = (None, None)
        widget.size = (self.widget_size, self.widget_size)
        self.game_view.add_widget(widget)

    def move_snake(self, direction):
        score = int(self.score_label.text) + 1
        self.score_label.text = str(score)
        # Score ändern und anzeigen
        if direction == "up":
            self.head_pos[1] -= 1
        elif direction == "down":
            self.head_pos[1] += 1
        elif direction == "right":
            self.head_pos[0] += 1
        elif direction == "left":
            self.head_pos[0] -= 1
        self.head_pos[0] = (self.head_pos[0] + self.cols) % self.cols
        self.head_pos[1] = (self.head_pos[1] + self.rows) % self.rows
        self.game_view.remove_widget(self.head)
        self.head = Head(self.head_pos)
        self.add_my_widget(self.head)
        print(direction)


# creating the App class in which name
# .kv file is to be named snakeapp.kv
class SnakeApp(App):
    # defining build()
    def build(self):
        # returning the instance of root class
        return PlayField()


# run the app
if __name__ == "__main__":
    SnakeApp().run()
