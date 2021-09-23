'''
Application example using build() + return
==========================================

An application can be built if you return a widget on build(), or if you set
self.root.
'''

import time
from os import times
from enum import Flag
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
import kivy
from plyer import flash
from plyer import brightness
from plyer import temperature
from plyer import storagepath
from plyer import spatialorientation
from plyer import proximity
from plyer import processors
from plyer import irblaster
from plyer import light
from plyer import gyroscope
from plyer import gravity
from plyer import compass
from plyer import bluetooth
from plyer import barometer
from plyer import accelerometer
from plyer import vibrator, gps


# from jnius import autoclass
# from sys import addaudithook
kivy.require('2.0.0')


# # We need a reference to the Java activity running the current
# # application, this reference is stored automatically by
# # Kivy's PythonActivity bootstrap

# # This one works with SDL2
# PythonActivity = autoclass('org.kivy.android.PythonActivity')

# activity = PythonActivity.mActivity

# Context = autoclass('android.content.Context')
# vibrator = activity.getSystemService(Context.VIBRATOR_SERVICE)

# from android.permissions import request_permissions, Permission
# request_permissions([Permission.WRITE_EXTERNAL_STORAGE])

class MainWidget(GridLayout):
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.existVibrator = vibrator.exists()
        self.cols = 2
        self.playState = False
        self.flashState = False
        gps.configure(on_location=self.gps_update)

    def gps_update(self, **kwargs):
        self.ids['lat_set'].text = '\n'.join(
            [f'{key}:{value}' for key, value in kwargs.items()])
        # self.startGps.text = str(kwargs).split(',').join('\n')
        self.ids['lat_value'].text = "{lat}".format(**kwargs)
        self.ids['lon_value'].text = "{lon}".format(**kwargs)

    def flash_switch(self, instance):
        if(self.flashState):
            self.flashState = False
            self.ids['flash'].text = 'Flash Off'
            flash.off()
        else:
            self.flashState = True
            self.ids['flash'].text = "Flash On"
            flash.on()

    def play_callback(self, instance):
        if(self.existVibrator):
            vibrator.vibrate(0.1)
        # jnius function
        # vibrator.vibrate(10000)  # the argument is in milliseconds

        if(self.playState):
            self.ids['btn_getGps'].text = 'Play Stop'
            accelerometer.disable()
            barometer.disable()
            compass.disable()
            gravity.disable()
            gyroscope.disable()
            light.disable()
            # proximity.disable()
            temperature.disable()
            spatialorientation.disable_listener()
            gps.stop()
            self.playState = False
        else:
            accelerometer.enable()
            barometer.enable()
            compass.enable()
            gravity.enable()
            gyroscope.enable()
            light.enable()
            # proximity.enable()
            temperature.enable()
            spatialorientation.enable_listener()
            gps.start()
            time.sleep(0.5)
            self.playState = True
            self.ids['btn_getGps'].text = 'Play Start'
            self.ids['accelerometer'].text = '\n'.join(
                map(str, accelerometer.acceleration))
            self.ids['barometer'].text = str(barometer.pressure)+' hPa'
            self.ids['compass'].text = '\n'.join(map(str, compass.field))
            self.ids['gravity'].text = '\n'.join(map(str, gravity.gravity))
            self.ids['infrared'].text = str(irblaster.exists())
            self.ids['light'].text = str(light.illumination)+' lx'
            # self.ids['proximity'].text = str(proximity.proximity)
            self.ids['flash'].text = 'ON'
            self.ids['temperature'].text = str(temperature.temperature)
            self.ids['spatial'].text = '\n'.join(
                map(str, spatialorientation.orientation))
            self.ids['brightness'].text = str(brightness.current_level())
            # self.ids['proc'].text = str(processors.status)
            self.ids['Dp'].text = str(storagepath.get_sdcard_dir())
            # self.ids['Dp'].text = f"app_dir: {StoragePath.get_application_dir()} \
            #                         doc_dir: {StoragePath.get_documents_dir_dir()}
            #                         dow_dir: {StoragePath.get_downloads_dir()}
            #                         ext_dir: {StoragePath.get_external_storage_dir()}
            #                         home_dir: {StoragePath.get_home_dir()}
            #                         pic_dir: {StoragePath.get_pictures_dir()}
            #                         music_dir: {StoragePath.get_music_dir()}
            #                         root_dir: {StoragePath.get_root_dir()}
            #                         sd_dir: {StoragePath.get_sdcard_dir()}"
        self.ids['bluetooth'].text = str(bluetooth.info)


class BlackApp(App):

    def build(self):
        AmainWidget = MainWidget()
        # request_permissions([Permission.WRITE_SETTINGS])
        return AmainWidget


if __name__ == '__main__':
    BlackApp().run()
