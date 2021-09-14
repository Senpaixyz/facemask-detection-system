from kivy import Config
# Command: pyinstaller main.py -w <- Not this
# COmmand: pyinstaller main.spec -y
# Command: pyinstaller --icon=main.ico --additional-hooks-dir=hooks --hidden-import=win32file --hidden-import=win32timezone --hidden-import=win32con --hidden-import=pwintypes main.py
# Config.set('graphics', 'width', '1200')
# Config.set('graphics', 'height', '800')
# Config.set('graphics', 'minimum_width', '800')
# Config.set('graphics', 'minimum_height', '600')
Config.set('graphics', 'window_state', 'maximized')
# Config.set('graphics', 'resizable', False)

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.image import Image, Widget
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton
from kivy.graphics.texture import Texture
from kivy.graphics import Rectangle
from kivy.clock import Clock
from mtcnn.mtcnn import MTCNN
from tensorflow.keras.models import load_model
import time
import pickle
import numpy as np
import cv2
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.animation import Animation

# Window.size = (300,500)
# navigation_helper = """
# ScreenManager:
#     NavScreen:
# <NavScreen>:
#     name: 'navscreen'
#     NavigationLayout:
#         ScreenManager:
#             Screen:
#                 BoxLayout:
#                     orientation: 'vertical'
#                     MDToolbar:
#                         title: 'Facemask Wearing Condition System'
#                         left_action_items: [['menu',lambda x: nav_drawer.toggle_nav_drawer()]]
#                         elevation: 10
#                     Widget:
#                 MDBoxLayout:
#                     orientation: 'vertical'
#         MDNavigationDrawer:
#             id: nav_drawer
#     MDBoxLayout:
#         orientation: 'vertical'
#
#
# """

# helperString = '''
# ScreenManager:
#     MainScreen:
# <c>:
#     name: 'mainscreen'
#     MDLabel:
#         text: 'Welcome Screen'
#         font_style: 'H2'
#         halign: 'center'
#         pos_hint: {'center_y':0.65}
#     MDBoxLayout:
#         orientation: 'vertical'
# '''
Builder.load_string('''

<MainScreen>:
    name: 'mainscreen'
    MDNavigationLayout:
        ScreenManager:
            Screen:
                id: mainScreenID
                BoxLayout:
                    orientation: 'vertical'
                    MDToolbar:
                        title: 'Facemask Wearing Condition System'
                        left_action_items: [['menu',lambda x: nav_drawer.set_state('open')]]
                        elevation: 10
                    # MDLabel:
                    #     text: 'Hello World'
                    #     halign: 'center'
                    #     font_size: '30sp'
                    GridLayout:
                        cols: 2
                        size: (root.width, root.height)
                        BoxLayout:  
                            orientation: 'vertical'
                            GridLayout:
                                id: grid_ID
                                cols: 1
                                rows: 3
                                GridLayout:
                                    cols:4
                                    size_hint: None,None
                                    width: 930
                                    height: 350
                                    padding: 55
                                    FloatLayout:
                                        spacing: 70
                                        Image:
                                            source: 'images/nw.png'
                                            pos_hint: {'center_x':0.3,'center_y':0.6}
                                            size_hint: None,None
                                            size: 200,200
                                            allow_stretch: False
                                            keep_ratio: True
                                        MDLabel:
                                            id: nw_label_id
                                            text: '50'
                                            font_size: '78'
                                            color :(0,150,136,0.8)
                                            pos_hint: {'center_x':0.88,'center_y':0.43}
                                        MDRectangleFlatButton:
                                            text: 'View Chart'
                                            pos_hint: {'center_x':0.3,'center_y':0.02}
                                    FloatLayout:
                                        spacing: 10
                                        Image:
                                            source: 'images/cw.png'
                                            pos_hint: {'center_x':0.3,'center_y':0.6}
                                            size_hint: None,None
                                            size: 200,200
                                            allow_stretch: False
                                            keep_ratio: True
                                        MDLabel:
                                            id: icw_label_id
                                            text: '50'
                                            font_size: '78'
                                            color :(0,150,136,0.8)
                                            pos_hint: {'center_x':0.865,'center_y':0.43}
                                        MDRectangleFlatButton:
                                            text: 'View Chart'
                                            pos_hint: {'center_x':0.3,'center_y':0.02}
                                    FloatLayout:
                                        spacing: 10
                                        Image:
                                            source: 'images/cw.png'
                                            pos_hint: {'center_x':0.3,'center_y':0.6}
                                            size_hint: None,None
                                            size: 200,200
                                            allow_stretch: False
                                            keep_ratio: True
                                        MDLabel:
                                            id: cw_label_id
                                            text: '50'
                                            font_size: '78'
                                            color :(0,150,136,0.8)
                                            pos_hint: {'center_x':0.895,'center_y':0.43}
                                        MDRectangleFlatButton:
                                            text: 'View Chart'
                                            pos_hint: {'center_x':0.3,'center_y':0.02}
                                    FloatLayout:
                                        spacing: 10
                                        id: cameraViewID
                                        # MDRectangleFlatButton:
                                        #     text: 'View Chart'
                                        #     pos_hint: {'center_x':0.35,'center_y':0.02}
                                        # 
                                BoxLayout:
                                    orientation: 'vertical'
                                    size_hint:None,None       
                                    width: 630             
                                    MDToolbar:
                                        height:(root.height-root.height)+5
                                GridLayout:
                                    rows: 4
                                    size_hint: None,None
                                    width: 630 
                                    padding: 5
                                    GridLayout:
                                        cols: 1
                                        MDLabel:
                                            text: 'IMPORT RESNET-50 MODEL AND PKL FILE'
                                            bold: True
                                            font_size: 12 
                                            halign: 'left' 
                                    GridLayout:
                                        cols: 3
                                        MDLabel:
                                            text: 'Model Path:'
                                            font_size: 12 
                                            halign: 'left'
                                            width: 70
                                            size_hint_x:None 
                                        MDLabel:
                                            id: model_id_path
                                            text: ""
                                            font_size: 12   
                                            halign: 'left'
                                        Button: 
                                            text: 'Import Model'
                                            font_size: 12   
                                            width: 120
                                            size_hint_x:None 
                                            on_release: root.show_ModelDialog()
                                            #background_color: 0,0,0,0  
                                    GridLayout:
                                        cols: 3
                                        MDLabel:
                                            text: 'Label Path:'
                                            font_size: 12 
                                            halign: 'left'
                                            width: 70
                                            size_hint_x:None 
                                        MDLabel:
                                            id: label_id_path
                                            text: ""
                                            font_size: 12   
                                            halign: 'left'
                                        Button: 
                                            text: 'Import Label'
                                            size_hint: 0.5,0.01
                                            font_size: 12   
                                            width: 120
                                            size_hint_x:None 
                                            on_release: root.show_LabelDialog()
                                            #background_color: 0,0,0,0 
                                    GridLayout:
                                        cols: 1
                                        halign: 'right' 
                                        Button:
                                            text: 'Saved Changes' 
                                            size_hint: 0.5,0.01
                                            font_size: 12   
                                            width: 120
                                            size_hint_x:None
                                            on_release: root.saved_changes()


                    MDToolbar:
                        height:(root.height-root.height)+15
        MDNavigationDrawer:
            id: nav_drawer

<LoadModelDialog>:
    BoxLayout:
        size: root.size
        pos: root.pos
        orientation: "vertical"
        FileChooserListView:
            id: model_filechooser
            path: "./"
            filters: ['*.h5','*.pth','*.pt']
        BoxLayout:
            size_hint_y: None
            height: 30
            Button:
                text: "Cancel"
                on_release: root.cancel()

            Button:
                text: "Import Model"
                on_release: root.load_model_path(model_filechooser.path, model_filechooser.selection)
<LoadLabelDialog>:
    BoxLayout:
        size: root.size
        pos: root.pos
        orientation: "vertical"
        FileChooserListView:
            id: label_filechooser
            path: "./"
            filters: ['*.pkl']
        BoxLayout:
            size_hint_y: None
            height: 30
            Button:
                text: "Cancel"
                on_release: root.cancel()

            Button:
                text: "Import Label"
                on_release: root.load_label_path(label_filechooser.path, label_filechooser.selection)
''')

class LoadModelDialog(FloatLayout):
    load_model_path = ObjectProperty(None)
    cancel = ObjectProperty(None)


class LoadLabelDialog(FloatLayout):
    load_label_path = ObjectProperty(None)
    cancel = ObjectProperty(None)


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.loadmodel_path = ObjectProperty(None)
        self.loadlabel_path = ObjectProperty(None)
        self.model_id_path = ObjectProperty(None)
        self.label_id_path = ObjectProperty(None)
        self.capture = ObjectProperty(None)
        self.cameraScreen = ObjectProperty(None)
        self.dialog = ObjectProperty(None)
        self.widget_list = {
            "NW": self.ids.nw_label_id,
            "ICW": self.ids.icw_label_id,
            "CW": self.ids.cw_label_id
        }
        self.model_path = ""  # "C:/Users/admin/PycharmProjects/app/model/facemask-inceptionV3-model.h5"
        self.label_path = ""  # "C:/Users/admin/PycharmProjects/app/model/labels8k.pkl"
        self.start_videoCapture()

    def animation(self):
        def animation_complete(animation, widget):
            self.ids.cameraViewID.remove_widget(widget)

        bullet1 = Image(
            source='images/loader.gif',
            center=(self.width / 2, self.height / 2),
            size_hint=(None, None)
        )
        self.ids.cameraViewID.add_widget(bullet1)
        animation1 = Animation(duration=10)
        animation1.start(bullet1)
        animation1.bind(on_complete=animation_complete)

    def start_videoCapture(self):
        self.capture = cv2.VideoCapture(0)
        self.cameraScreen = CameraScreen(
            capture=self.capture,
            fps=30,
            model_path=self.model_path,
            label_path=self.label_path,
            size_hint=(None, None),
            size=(950, 950),
            allow_stretch=False,
            keep_ratio=True,
            pos_hint={'center_x': 1.7, 'center_y': 0.04},
            widget_lst=self.widget_list

        )
        self.ids.cameraViewID.add_widget(self.cameraScreen, len(self.ids.cameraViewID.children))

    def stop_videoCapture(self):
        self.ids.cameraViewID.remove_widget(self.cameraScreen)
        self.animation()
        self.cameraScreen.stop_video()

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_ModelDialog(self):
        content = LoadModelDialog(load_model_path=self.load_model_path, cancel=self.dismiss_popup)
        self._popup = Popup(title="Import Model File", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def show_LabelDialog(self):
        content = LoadLabelDialog(load_label_path=self.load_label_path, cancel=self.dismiss_popup)
        self._popup = Popup(title="Import PKL File", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load_model_path(self, path, filename):
        self.ids.model_id_path.text = filename[0]
        self.model_path = filename[0]
        self.dismiss_popup()

    def load_label_path(self, path, filename):
        self.ids.label_id_path.text = filename[0]
        self.label_path = filename[0]
        self.dismiss_popup()

    def saved_changes(self):
        self.dialog = None
        if len(self.model_path) == 0 or len(self.label_path) == 0:
            if not self.dialog:
                self.dialog = MDDialog(
                    title="Invalid Action",
                    text="Model or Label path is empty please import those necessary files!",
                    buttons=[
                        MDFlatButton(
                            text="Ok",
                            on_release=self.close_dialog
                        ),
                    ]
                )
                self.dialog.open()
        else:
            self.stop_videoCapture()
            self.start_videoCapture()
            print("REMOVING KEME")

    def close_dialog(self):
        self.dialog.dismiss()
        # self.ids.cameraViewID.add_widget(self.cameraScreen)

        # self.BodyCol = FloatLayout(
        #     size=(self.width, self.height)
        # )
        # self.buttonClick = MDRaisedButton(
        #     text="Click Me!!!!!",
        #     size_hint=(None, None),
        #     pos_hint={'x':0,'top':1}
        # )
        # self.BodyCol.add_widget(self.buttonClick)
        # self.cameraScreen = CameraScreen(
        #         capture=self.capture,
        #         fps=30,
        #         #pos_hint={'x': 0.02, 'top': 0.35},
        #
        # )
        # self.BodyCol.add_widget(self.cameraScreen)
        # self.buttonClick2 = MDRaisedButton(
        #     text="Click Meeeeee!!!!!",
        #     size_hint=(None, None)
        # )
        # self.BodyCol.add_widget(self.buttonClick2)


class CameraScreen(Image):
    def __init__(self, capture, fps, model_path, label_path, widget_lst, **kwargs):
        super(CameraScreen, self).__init__(**kwargs)
        self.capture = capture
        self.texture = None
        self.model_path = model_path  # self.load_model_event()
        self.label_path = label_path
        self.detector = MTCNN(scale_factor=0.1)
        self.img_size = (150, 150)
        self.colors = {0: (0, 0, 255), 1: (0, 255, 0), 2: (0, 255, 255)}
        self.yellow = (0, 155, 255)
        self.model = self.load_model_event(self.model_path)
        self.labels = self.load_label_event(self.label_path)
        self.target = 0
        self.not_wearing_cnt = 0
        self.wearing_cnt = 0
        self.inc_wearing_cnt = 0
        self.widget_list = widget_lst
        Clock.schedule_interval(self.load_video, 1.0 / fps)

    def load_model_event(self, model_path):
        if len(model_path) == 0:
            return None
        else:
            return load_model(model_path)

    def load_label_event(self, label_path):
        labels_tmp = None
        if len(label_path) == 0:
            return None
        else:
            with open(label_path, 'rb') as pf:
                labels_tmp = pickle.load(pf)
            return labels_tmp

    def stop_video(self, *args):
        self.capture.release()

    def set_label_count(self):
        if self.target == 0:
            self.not_wearing_cnt += 1
            self.widget_list["NW"].text = str(self.not_wearing_cnt)
        elif self.target == 1:
            self.wearing_cnt += 1
            self.widget_list["CW"].text = str(self.wearing_cnt)
        elif self.target == 2:
            self.inc_wearing_cnt += 1
            self.widget_list["ICW"].text = str(self.inc_wearing_cnt)

    def reset_label_count(self):
        self.not_wearing_cnt = 0
        self.wearing_cnt = 0
        self.inc_wearing_cnt = 0
        self.widget_list["NW"].text = str(self.not_wearing_cnt)
        self.widget_list["CW"].text = str(self.wearing_cnt)
        self.widget_list["ICW"].text = str(self.inc_wearing_cnt)

    def load_video(self, *args):
        ret, frame = self.capture.read()
        self.reset_label_count()
        if ret:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            faces = self.detector.detect_faces(rgb)
            print(faces)
            for face in faces:
                try:
                    x, y, w, h = face['box']
                    keypoints = face['keypoints']
                    roi = rgb[y: y + h, x: x + w]  # get region of intrest.
                    data = cv2.resize(roi, self.img_size) / 255.  # resize imge and flatten
                    data = data.reshape((1,) + data.shape)  # reshape the data to fit model
                    if (len(self.model_path) != 0) and (len(self.label_path) != 0):
                        scores = self.model.predict(data)  # predict
                        self.target = np.argmax(scores, axis=1)[0]
                        # Draw bounding boxes
                        self.set_label_count()
                        cv2.rectangle(img=frame, pt1=(x, y), pt2=(x + w, y + h), color=self.colors[self.target],
                                      thickness=2)  #
                        text = "{}: {:.2f}".format(self.labels[self.target], scores[0][self.target])
                        cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                    cv2.circle(frame, (keypoints['left_eye']), 2, self.yellow, 2)
                    cv2.circle(frame, (keypoints['right_eye']), 2, self.yellow, 2)
                    cv2.circle(frame, (keypoints['nose']), 2, self.yellow, 2)
                    cv2.circle(frame, (keypoints['mouth_left']), 2, self.yellow, 2)
                    cv2.circle(frame, (keypoints['mouth_right']), 2, self.yellow, 2)
                except Exception as e:
                    print("THeres some error regarading to importing file")
                    print(e)
                    # print(roi.shape)
            # Frame
            # self.image_frame = frame
            buffer = cv2.flip(frame, 0).tostring()
            self.texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            self.texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
            self.texture = self.texture

            # with self.canvas:
            #   Rectangle(texture=self.texture, size=(900, 200))


#
# class MainScreen(MDBoxLayout):
#     def __init__(self, **kwargs):
#         super(MainScreen, self).__init__(**kwargs)
#         self.HeaderCol = GridLayout(cols=1)
#         self.navScreen = NavScreen();
#         self.HeaderCol.add_widget(self.navScreen)
#         self.add_widget(self.HeaderCol,index=1)
#         #
#         # self.BodyCol = GridLayout(cols=2)
#         # self.buttonClick = MDRaisedButton(
#         #     text="Click Me",
#         #     pos_hint={'center_x': .5, 'center_y': 63},
#         #     size_hint=(None, None)
#         # )
#         # self.BodyCol.add_widget(self.buttonClick)
#         # self.cameraScreen = CameraScreen(capture=self.capture, fps=30)
#         # self.BodyCol.add_widget(self.cameraScreen)
#         # self.add_widget(self.BodyCol,index=0)


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.helperStr = ""
        self.cameraCap = None
        self.mainscreen = None

    def build(self):
        # self.theme_cls.primary_pallete = "BlueGray"
        self.theme_cls.primary_palette = "Teal"
        self.mainscreen = MainScreen()

        # self.helperStr = Builder.load_string(helperString)
        # self.helperStr.get_screen('mainscreen').cameraCapture(self.capture)
        # layout = MDBoxLayout(orientation="vertical")
        # self.cameraScreen = CameraScreen(capture=self.capture, fps=30)
        # layout.add_widget(self.cameraScreen)
        # layout.add_widget(
        #      MDRaisedButton(
        #          text="Click Me",
        #          pos_hint={'center_x': .5, 'center_y': 63},
        #          size_hint=(None, None)
        #      )
        # )
        # screen = Builder.load_string(navigation_helper)
        # layout = MDBoxLayout(orientation='vertical')

        return self.mainscreen  # screen


# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# # Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    MainApp().run()
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/
