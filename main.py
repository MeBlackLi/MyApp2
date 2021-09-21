'''
Application example using build() + return
==========================================

An application can be built if you return a widget on build(), or if you set
self.root.
'''

# from jnius import autoclass
# from sys import addaudithook
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
import kivy
from plyer import vibrator
from plyer import gps
kivy.require('2.0.0')


# # We need a reference to the Java activity running the current
# # application, this reference is stored automatically by
# # Kivy's PythonActivity bootstrap

# # This one works with SDL2
# PythonActivity = autoclass('org.kivy.android.PythonActivity')

# activity = PythonActivity.mActivity

# Context = autoclass('android.content.Context')
# vibrator = activity.getSystemService(Context.VIBRATOR_SERVICE)


class Tools(GridLayout):
    def __init__(self, **kwargs):
        super(Tools, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='Longitude'))
        self.longitude = TextInput(multiline=False)
        self.add_widget(self.longitude)
        self.add_widget(Label(text='Latitude'))
        self.latitude = TextInput(multiline=False)
        self.add_widget(self.latitude)
        self.curLon = Label(text='Cur Lon:')
        self.add_widget(self.curLon)
        self.curLonPos = Label(text='XX.XX')
        self.add_widget(self.curLonPos)
        self.curLat = Label(text='Cur Lat:')
        self.add_widget(self.curLat)
        self.curLatPos = Label(text='XX.XX')
        self.add_widget(self.curLatPos)
        self.haveVibrator = Label()
        self.add_widget(self.haveVibrator)
        self.startGps = Button(text='Gps Play')
        self.startGps.bind(on_press=self.playGps)
        self.add_widget(self.startGps)
        self.playGpsState = False
        self.haveVibrator.text = str(vibrator.exists())
        self.existVibrator = vibrator.exists()
        gps.configure(on_location=self.gps_update)

    def gps_update(self, **kwargs):
        self.startGps.text = '\n'.join(
            [f'{key}:{value}' for key, value in kwargs.items()])
        # self.startGps.text = str(kwargs).split(',').join('\n')
        self.curLatPos.text = "{lat}".format(**kwargs)
        self.curLonPos.text = "{lon}".format(**kwargs)

    def playGps(self, instance):
        if(self.existVibrator):
            vibrator.vibrate(0.1)
        # jnius function
        # vibrator.vibrate(10000)  # the argument is in milliseconds

        if(self.playGpsState):
            gps.stop()
            self.playGpsState = False
            self.startGps.text = 'Play Stop'
        else:
            gps.start()
            self.playGpsState = True
            self.startGps.text = 'Play Start'


class TestApp(App):

    def build(self):
        return Tools()


if __name__ == '__main__':
    TestApp().run()
