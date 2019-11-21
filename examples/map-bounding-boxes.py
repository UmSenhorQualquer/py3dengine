#!/usr/bin/env python
# -*- coding: utf-8 -*-
from py3dengine.utils.WavefrontOBJFormat.WavefrontOBJReader import WavefrontOBJReader
from py3dengine.scenes.SceneClient import SceneClient
from pyforms_gui.basewidget import BaseWidget
from pyforms_gui.controls.control_button import ControlButton
from pyforms_gui.controls.control_file import ControlFile
from pyforms_gui.controls.control_player.control_player import ControlPlayer
from pyforms_gui.controls.control_slider import ControlSlider


class MapBoundingBoxesApp(BaseWidget):

    SERVER_ADDRESS = ('127.0.0.1', 5005)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.data1 = None #List of the bounding boxes for the camera1
        self.data2 = None #List of the bounding boxes for the camera1
        self.scene = None #Scene object
        self.cam1 = None #Camera1 object
        self.cam2 = None #Camera2 object

        self._scene  = ControlFile('Scene')
        self._data1 = ControlFile('Data 1')
        self._data2 = ControlFile('Data 2')
        self._video1 = ControlFile('Video 1')
        self._video2 = ControlFile('Video 2')
        self._player1 = ControlPlayer('Player')
        self._player2 = ControlPlayer('Player')
        self._timeline = ControlSlider('Frame', changed_event=self.__timeline_changed_evt)
        self._loadbtn = ControlButton('Load data', default=self.init_scene)

        self.formset = [
            ('_video1', '_video2'),
            ('_data1', '_data2'),
            ('_scene','_loadbtn'),
            ('_player1','_player2'),
            '_timeline'
        ]


        self._scene.value = 'data/scene-example.obj'
        self._data1.value = '/Users/ricardojvr/Downloads/376_cam_1_detection.csv'
        self._data2.value = '/Users/ricardojvr/Downloads/376_cam_2_detection.csv'
        self._video1.value = '/Users/ricardojvr/Downloads/376_cam_1.avi'
        self._video2.value = '/Users/ricardojvr/Downloads/376_cam_2.avi'

    def load_data(self, filepath):
        data = []
        with open(filepath) as infile:
            for i, line in enumerate(infile):
                if i == 0: continue

                values = eval(line)
                index, frame, x, y, xx, yy = values

                if frame > len(data):
                    while len(data) < frame:  data.append(None)
                data.append(values)
        return data

    def trace_rays(self, cam, x, y, xx, yy):
        cam.addRay(x, y)
        cam.addRay(x, yy)
        cam.addRay(xx, yy)
        cam.addRay(xx, y)
        for ray in cam.rays:
            ray.collidePlanZ(0)

    def __timeline_changed_evt(self):
        # Check if the data was already initialized
        if not (self.data1 and self.data2): return

        index = int(self._timeline.value)
        v1 = self.data1[index] if len(self.data1)>index else None

        if v1 is not None:
            index, frame, x, y, xx, yy = v1
            self.trace_rays(self.cam1, x, y, xx, yy)

        v2 = self.data2[index] if len(self.data2)>index else None
        if v2 is not None:
            index, frame, x, y, xx, yy = v2
            self.trace_rays(self.cam2, x, y, xx, yy)

        self._player1.video_index = index
        self._player1.call_next_frame()
        self._player2.video_index = index
        self._player2.call_next_frame()

        self.scene.synchronize()
        self.cam1.cleanRays()
        self.cam2.cleanRays()

    def init_scene(self):
        self.scene = SceneClient(self.SERVER_ADDRESS, describer=WavefrontOBJReader(self._scene.value))

        self.cam1 = self.scene.getCamera('Camera1')
        self.cam2 = self.scene.getCamera('Camera2')

        self.data1 = self.load_data(self._data1.value)
        self.data2 = self.load_data(self._data2.value)

        self._timeline.value = 0
        self._timeline.max = max(len(self.data1), len(self.data2))

        self._player1.value = self._video1.value
        self._player2.value = self._video2.value

        self.__timeline_changed_evt()


if __name__ == '__main__':

    from pyforms import start_app
    start_app(MapBoundingBoxesApp)