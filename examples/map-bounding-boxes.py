#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
from py3dengine.objects.RectangleObject import RectangleObject
from py3dengine.utils.WavefrontOBJFormat.WavefrontOBJReader import WavefrontOBJReader
from py3dengine.scenes.SceneClient import SceneClient
from pyforms_gui.basewidget import BaseWidget
from pyforms_gui.controls.control_button import ControlButton
from pyforms_gui.controls.control_file import ControlFile
from pyforms_gui.controls.control_player.control_player import ControlPlayer
from pyforms_gui.controls.control_slider import ControlSlider


class MapBoundingBoxesApp(BaseWidget):

    SERVER_ADDRESS = ('127.0.0.1', 5005)

    COLORS = [
        (240, 163, 255), (0, 117, 220), (153, 63, 0), (76, 0, 92),
        (25, 25, 25), (0, 92, 49), (43, 206, 72), (255, 204, 153),
        (128, 128, 128), (148, 255, 181), (143, 124, 0), (157, 204, 0),
        (194, 0, 136), (0, 51, 128), (255, 164, 5), (255, 168, 187),
        (66, 102, 0), (255, 0, 16), (94, 241, 242), (0, 153, 143),
        (116, 10, 255), (153, 0, 0), (255, 255, 0), (255, 80, 5)
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.data1 = None #List of the bounding boxes for the camera1
        self.data2 = None #List of the bounding boxes for the camera1
        self.scene = None #Scene object
        self.cam1 = None #Camera1 object
        self.cam2 = None #Camera2 object
        self.floor = None #Floor object

        self._scene  = ControlFile('Scene')
        self._data1 = ControlFile('Data 1')
        self._data2 = ControlFile('Data 2')
        self._video1 = ControlFile('Video 1')
        self._video2 = ControlFile('Video 2')
        self._player1 = ControlPlayer('Player', process_frame_event=self.__process_player1_frame)
        self._player2 = ControlPlayer('Player', process_frame_event=self.__process_player2_frame)
        self._timeline = ControlSlider('Frame', changed_event=self.__timeline_changed_evt, enabled=False)
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

        self._video1.value = '/Users/ricardojvr/Downloads/tracking/385_cam_1.avi'
        self._video2.value = '/Users/ricardojvr/Downloads/tracking/385_cam_2.avi'
        self._data1.value = '/Users/ricardojvr/Downloads/tracking/385_cam_1_detection.csv'
        self._data2.value = '/Users/ricardojvr/Downloads/tracking/385_cam_2_detection.csv'



    def __process_player1_frame(self, frame):
        index = self._player1.video_index-1

        boxes = self.data1.get(index, [])
        for i, box in enumerate(boxes):
            color = self.COLORS[i]
            _, _, x, y, w, h = box
            cv2.rectangle(frame, (x,y), (x+w,y+h), color=color, thickness=3, lineType=cv2.LINE_AA)
        return frame

    def __process_player2_frame(self, frame):
        index = self._player2.video_index-1
        boxes = self.data2.get(index, [])
        for i, box in enumerate(boxes):
            color = self.COLORS[i]
            _, _, x, y, w, h = box
            cv2.rectangle(frame, (x, y), (x + w, y + h), color=color, thickness=3, lineType=cv2.LINE_AA)
        return frame


    def load_data(self, filepath):
        data = {}
        with open(filepath) as infile:
            for i, line in enumerate(infile):
                if i == 0: continue
                values = eval(line)
                frame = values[1]

                if frame not in data:
                    data[frame] = []

                data[frame].append(values)
        return data

    def trace_rays(self, cam, x, y, xx, yy, index=0):
        color = self.COLORS[index]
        b,g,r = color
        color = float(r)/255.0, float(g)/255.0, float(b)/255.0, 1.0

        rays = []
        rays.append(cam.addRay(x, y, color=color))
        rays.append(cam.addRay(x, yy, color=color))
        rays.append(cam.addRay(xx, yy, color=color))
        rays.append(cam.addRay(xx, y, color=color))

        points = []
        for ray in rays:
            points.append(
                ray.collidePlanZ(0)
            )

        obj = RectangleObject( f'plane-{len(self.scene.objects)}', *points )
        self.scene.add_object(obj)
        obj.color = color

    def __timeline_changed_evt(self):
        # Check if the data was already initialized
        if self.data1 and self.data2:
            index = int(self._timeline.value)

            boxes = self.data1.get(index, [])
            for i, box in enumerate(boxes):
                _, _, x, y, w, h = box
                self.trace_rays(self.cam1, x, y, x+w, y+h, index=i)

            boxes = self.data2.get(index, [])
            for i, box in enumerate(boxes):
                _, _, x, y, w, h = box
                self.trace_rays(self.cam2, x, y, x + w, y + h, index=i)

            self._player1.video_index = index
            self._player1.call_next_frame()
            self._player2.video_index = index
            self._player2.call_next_frame()

        self.scene.synchronize()
        self.cam1.cleanRays()
        self.cam2.cleanRays()
        self.scene.objects = [self.floor] if self.floor else []
        obj = RectangleObject(f'plane-{len(self.scene.objects)}',
            (-5, -5,1.8),
            (-5, 5, 1.8),
            (5, 5, 1.8),
            (5, -5, 1.8),
         )
        self.scene.add_object(obj)
        obj.color = (0.5,0,0,0.3)

    def init_scene(self):
        self.scene = SceneClient(self.SERVER_ADDRESS, describer=WavefrontOBJReader(self._scene.value))

        self.cam1 = self.scene.getCamera('Camera1')
        self.cam2 = self.scene.getCamera('Camera2')
        self.floor = self.scene.getObject('Floor')

        self.data1 = self.load_data(self._data1.value)
        self.data2 = self.load_data(self._data2.value)

        self._timeline.value = 0
        self._timeline.max = max(len(self.data1), len(self.data2))

        self._player1.value = self._video1.value
        self._player2.value = self._video2.value

        self.__timeline_changed_evt()

        self._timeline.enabled = True


if __name__ == '__main__':

    from pyforms import start_app
    start_app(MapBoundingBoxesApp)