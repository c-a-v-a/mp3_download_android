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

from Preflight import *
from Database import Database


BUTTON_BG = (98/255, 114/255, 164/255, 1) # #6272A4
DB = Database(DATABASE_PATH, MUSIC_LOCATIONS)


class ErrorPopup(Popup):
    """Class representing a popup taking care of showing what errors occured."""
    def __init__(self, **kwargs):
        super(ErrorPopup, self).__init__(**kwargs);
        self.title = 'Error'
        self.size_hint=(.8,.2)

        self.label = Label(text="Error")

        self.add_widget(self.label)

    def update_message(self, msg):
        """Updates popup with the new error message"""
        self.label.text = str(msg)


class AddOfflinePopup(Popup):
    """Popup window that allows user to add new offline song to the database."""
    def __init__(self, **kwargs):
        super(AddOfflinePopup, self).__init__(**kwargs)
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
        btn.bind(on_press=self.close)
        box.add_widget(btn)

        self.add_widget(box)

    def close(self, instance):
        url = self.url_input.text
        name = self.name_input.text
        path = self.path_input.text

        try:
            if not url == '':
                if 'youtube.com' in url or 'youtu.be' in url:
                    DB.add_offline_yt(url)
                else:
                    DB.add_offline(url,path,name)
        except Exception as e:
            p = ErrorPopup()
            p.update_message(e)
            p.open()

        self.dismiss()


class AddOnlinePopup(Popup):
    """Popup window that allows user to add new online song to the database."""
    def __init__(self, **kwargs):
        super(AddOnlinePopup, self).__init__(**kwargs)
        self.title = 'Add online'
        self.size_hint = (0.8, 0.2)

        box = BoxLayout(orientation='vertical', spacing=10, padding=[10,10])

        self.url_input = TextInput(hint_text="Url")
        box.add_widget(self.url_input)
        self.name_input = TextInput(hint_text="Name (optional)")
        box.add_widget(self.name_input)

        btn = Button(text='Submit', size_hint=(.5,1), pos_hint={'x': .25})
        btn.bind(on_press=self.close)
        box.add_widget(btn)

        self.add_widget(box)

    def close(self, instance):
        url = self.url_input.text
        name = self.name_input.text

        try:
            if not url == '':
                if 'youtube.com' in url or 'youtu.be' in url:
                    DB.add_online_yt(url)
                else:
                    DB.add_online(url,name)
        except Exception as e:
            p = ErrorPopup()
            p.update_message(e)
            p.open()

        self.dismiss()


class OfflineScreen(Screen):
    """Screen that shows all offline songs in the database."""
    def __init__(self, **kwargs):
        super(OfflineScreen, self).__init__(**kwargs)
        self.data = []
        self.count = 0
        self.refresh()

        self.layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=4, padding=[25,25])
        self.layout.bind(minimum_height=self.layout.setter('height'))
        

        self.btn = Button(text=f'---BACK---', size_hint_y=None,
                         height=60, background_color=BUTTON_BG)
        self.btn.bind(on_press=self.go_back)
        self.layout.add_widget(self.btn)        
        for item in self.data:
            self.btn = Button(text=f'{"(A) " if item.is_album else ""}{item.name}', size_hint_y=None,
                         height=60, background_color=BUTTON_BG)
            self.layout.add_widget(self.btn)

        self.sv = ScrollView()
        self.sv.add_widget(self.layout)
        self.add_widget(self.sv)

    def on_enter(self):
        self.refresh()

    def refresh(self):
        """Takes care of updating the layout if new song is added to the database."""
        try:
            if self.count == 0:
                self.count += 1
            else:
                self.sv.remove_widget(self.layout)

                self.layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=4, padding=[25,25])
                self.layout.bind(minimum_height=self.layout.setter('height'))
                

                self.btn = Button(text=f'---BACK---', size_hint_y=None,
                                 height=60, background_color=BUTTON_BG)
                self.btn.bind(on_press=self.go_back)
                self.layout.add_widget(self.btn)        
                for item in self.data:
                    self.btn = Button(text=f'{"(A) " if item.is_album else ""}{item.name}', size_hint_y=None,
                                 height=60, background_color=BUTTON_BG)
                    self.layout.add_widget(self.btn)

                self.sv.add_widget(self.layout)

            self.data = DB.offline_items
        except Exception as e:
            p = ErrorPopup()
            p.update_message(e)
            p.open()

    def go_back(self, instance):
        self.manager.current = 'select'


class OnlineScreen(Screen):
    """Screen that shows all online songs in the database."""
    def __init__(self, **kwargs):
        super(OnlineScreen, self).__init__(**kwargs)
        self.data = []
        self.count = 0
        self.refresh()

        self.layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=4, padding=[25,25])
        self.layout.bind(minimum_height=self.layout.setter('height'))
        
        self.btn = Button(text=f'---BACK---', size_hint_y=None,
                         height=60, background_color=BUTTON_BG)
        self.btn.bind(on_press=self.go_back)
        self.layout.add_widget(self.btn)        
        for item in self.data:
            self.btn = Button(text=f'{"(A) " if item.is_album else ""}{item.title}', size_hint_y=None,
                         height=60, background_color=BUTTON_BG)
            self.layout.add_widget(self.btn)
        
        self.sv = ScrollView()
        self.sv.add_widget(self.layout)
        self.add_widget(self.sv)

    def on_enter(self):
        self.refresh()


    def refresh(self):
        """Takes care of updating the layout if new song is added to the database."""
        try:
            if self.count == 0:
                self.count += 1
            else:
                self.sv.remove_widget(self.layout)
                self.layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=4, padding=[25,25])
                self.layout.bind(minimum_height=self.layout.setter('height'))
                
                self.btn = Button(text=f'---BACK---', size_hint_y=None,
                                 height=60, background_color=BUTTON_BG)
                self.btn.bind(on_press=self.go_back)
                self.layout.add_widget(self.btn)        
                for item in self.data:
                    self.btn = Button(text=f'{"(A) " if item.is_album else ""}{item.title}', size_hint_y=None,
                                 height=60, background_color=BUTTON_BG)
                    self.layout.add_widget(self.btn)

                self.sv.add_widget(self.layout)

            self.data = DB.online_items
        except Exception as e:
            p = ErrorPopup()
            p.update_message(e)
            p.open()


    def go_back(self, instance):
        self.manager.current = 'select'


class SelectScreen(Screen):
    """Main application screen. Allows user to pick what they want to do."""
    def __init__(self, **kwargs):
        super(SelectScreen, self).__init__(**kwargs)
        # layouts
        anchor = AnchorLayout(anchor_x='center', anchor_y='center', padding=[10,10])
        box = BoxLayout(orientation='vertical', size_hint=(.5,.15), spacing=4)
        grid = GridLayout(cols=2, rows=1, spacing=4)

        # grid buttons
        add_offline_btn = Button(text="Add offline", background_color=BUTTON_BG)
        add_offline_btn.bind(on_press=self.open_offline_popup)
        grid.add_widget(add_offline_btn)

        add_online_btn = Button(text="Add online", background_color=BUTTON_BG)
        add_online_btn.bind(on_press=self.open_online_popup)
        grid.add_widget(add_online_btn)

        box.add_widget(grid);

        # box buttons
        list_offline_btn = Button(text="List offline", background_color=BUTTON_BG)
        list_offline_btn.bind(on_press=self.goto_offline)
        box.add_widget(list_offline_btn);
        list_online_btn = Button(text="List online", background_color=BUTTON_BG)
        list_online_btn.bind(on_press=self.goto_online)
        box.add_widget(list_online_btn);

        anchor.add_widget(box)

        self.add_widget(anchor)

    def open_offline_popup(self, instance):
        """Opens a popup that allows user to add new offline song."""
        popup = AddOfflinePopup()
        popup.open()

    def open_online_popup(self, instance):
        """Opens a popup that allows user to add new online song."""
        popup = AddOnlinePopup()
        popup.open()

    def goto_offline(self, instance):
        self.manager.current = 'offline'

    def goto_online(self, instance):
        self.manager.current = 'online'


class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)
        self.add_widget(SelectScreen(name='select'))
        self.add_widget(OfflineScreen(name='offline'))
        self.add_widget(OnlineScreen(name='online'))


class MyApp(App):
    def build(self):
        sm = MyScreenManager()

        # Change the bg color
        with sm.canvas.before:
            Color(40/255, 42/255, 54/255, 1) # #282A36
            self.rect = Rectangle(size=Window.size, pos=sm.pos)

        sm.bind(size=self._update_rect, pos=self._update_rect)

        return sm

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

if __name__ == '__main__':
    validate_paths()
    MyApp().run()
