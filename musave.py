from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window

from Database import Database


BUTTON_BG = (98/255, 114/255, 164/255, 1) # Button background color (#6272A4)
DB = Database() # Database


class ErrorPopup(Popup):
    """
    A class responsible for error popup window. Most of the methods and 
    attributes are derived from the kivy Popup class

    Attributes
    ----------
    label
        label for error messages

    Methods
    -------
    update_message(msg)
        Updates error popup with the new error message.
    """
    def __init__(self, **kwargs):
        """
        Creates the error popup and its layout.
        """
        super(ErrorPopup, self).__init__(**kwargs);
        self.title = 'Error'
        self.size_hint=(.8,.2)

        self._label = Label(text="Error")

        self.add_widget(self._label)

    def update_message(self, msg: str):
        """
        Updates error popup with the new error message.

        Parameters
        ----------
        msg : str
            new error message that sould be displayed
        """
        self._label.text = str(msg)


class AddPopup(Popup):
    """
    A class responsible for providing a popup window, in which user can input
    the parameters of a song that needs to be downloaded.
    """
    def __init__(self, **kwargs):
        """
        Creates the popup and its layout.
        """
        super(AddPopup, self).__init__(**kwargs)
        self.title = 'Add offline'
        self.size_hint = (0.8, 0.25)

        box = BoxLayout(orientation='vertical', spacing=10, padding=[10,10])

        self.url_input = TextInput(hint_text="Url")
        box.add_widget(self.url_input)
        self.name_input = TextInput(hint_text="Name (optional)")
        box.add_widget(self.name_input)
        self.path_input = TextInput(hint_text="Path (optional)")
        box.add_widget(self.path_input)

        btn = Button(text='Submit', size_hint=(.5,1), pos_hint={'x': .25})
        btn.bind(on_press=self._close)
        box.add_widget(btn)

        self.add_widget(box)

    def _close(self, instance):
        """
        Closes the popup and tries to add the song, with params taken from
        text inputs, to the database.
        """
        url = self.url_input.text
        name = self.name_input.text
        path = self.path_input.text

        try:
            if url == '':
                raise Exception('Error. Cannot download from empty url.')
            DB.add(url, path=path, name=name)
        except Exception as e:
            p = ErrorPopup()
            p.update_message(str(e))
            p.open()

        self.dismiss()


class ListScreen(Screen):
    """
    A class that represents the screen that displays all the music items added 
    to the database (all the items that are saved in the database location).
    """
    def __init__(self, **kwargs):
        """
        Creates the screen and its layout.

        The screen uses kivy ScrollView to prevent the layout from overflowing
        when there are many saved items.
        """
        super(ListScreen, self).__init__(**kwargs)
        data = DB.items
        print(data)

        self._layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10, padding=[25,25])
        self._layout.bind(minimum_height=self._layout.setter('height'))

        for item in data:
            btn = Button(text=f'{"(A) " if item.is_album else ""}{item.name}', 
                         size_hint_y=None, height=100, background_color=BUTTON_BG)
            self._layout.add_widget(btn)

        back_btn = Button(text=f'---BACK---', size_hint_y=None,
                         height=100, background_color=BUTTON_BG)
        back_btn.bind(on_press=self._go_back)

        self._scroll = ScrollView()
        self._scroll.add_widget(self._layout)
        self.add_widget(self._scroll)
        self.add_widget(back_btn)

    def on_enter(self):
        """Handles the kivy on_enter screen event."""
        self._refresh()

    def _refresh(self):
        """Obtains information about saved items and updates the ScrollVew."""
        try:
            data = DB.items

            self._scroll.remove_widget(self._layout)

            self._layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10, padding=[25,25])
            self._layout.bind(minimum_height=self._layout.setter('height'))
            
            for item in data:
                btn = Button(text=f'{"(A) " if item.is_album else ""}{item.name}', size_hint_y=None,
                             height=100, background_color=BUTTON_BG)
                self._layout.add_widget(btn)

            self._scroll.add_widget(self._layout)
        except Exception as e:
            p = ErrorPopup()
            p.update_message(e)
            p.open()

    def _go_back(self, instance):
        """Changes the currently displayed screen to the MainScreen."""
        self.manager.current = 'main'


class MainScreen(Screen):
    """A class that represents main application screen."""
    def __init__(self, **kwargs):
        """Creates main screen and its layout."""
        super(MainScreen, self).__init__(**kwargs)
        # layouts
        anchor = AnchorLayout(anchor_x='center', anchor_y='center', padding=[10,10])
        box = BoxLayout(orientation='vertical', size_hint=(.5,.15), spacing=10)

        add_btn = Button(text="Add music", background_color=BUTTON_BG)
        add_btn.bind(on_press=self._open_add_popup)
        box.add_widget(add_btn)

        list_btn = Button(text="Music list", background_color=BUTTON_BG)
        list_btn.bind(on_press=self._goto_list)
        box.add_widget(list_btn);

        anchor.add_widget(box)

        self.add_widget(anchor)

    def _open_add_popup(self, instance):
        """Open popup for adding songs."""
        popup = AddPopup()
        popup.open()

    def _goto_list(self, instance):
        """Changes the currently displayed screen to the ListScreen."""
        self.manager.current = 'list'


class MyScreenManager(ScreenManager):
    """A class manages which screen is displayed by the application."""
    def __init__(self, **kwargs):
        """Creates scrreen manages with two screens (MainScreen and ListScreen)."""
        super(MyScreenManager, self).__init__(**kwargs)
        self.add_widget(MainScreen(name='main'))
        self.add_widget(ListScreen(name='list'))


class MyApp(App):
    """A class representing the whole application interface."""
    def build(self):
        """Builds the application with the screen manager."""
        sm = MyScreenManager()

        # Change the bg color
        with sm.canvas.before:
            Color(40/255, 42/255, 54/255, 1) # #282A36
            self.rect = Rectangle(size=Window.size, pos=sm.pos)

        sm.bind(size=self._update_rect, pos=self._update_rect)

        return sm

    def _update_rect(self, instance, value):
        """Updates the application size and position (used for coloring background."""
        self.rect.pos = instance.pos
        self.rect.size = instance.size

if __name__ == '__main__':
    MyApp().run()
