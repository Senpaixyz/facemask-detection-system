from kivy import Config
import config as sys_config
Config.set('graphics', 'resizable', sys_config.IS_RESIZABLE)
if sys_config.SET_DIM == True:
    Config.set('graphics', 'width', sys_config.DIM_WIDTH)
    Config.set('graphics', 'height', sys_config.DIM_HEIGHT)
    Config.set('graphics', 'minimum_width', sys_config.MIN_WIDTH)
    Config.set('graphics', 'minimum_height', sys_config.MIN_HEIGHT)
else:
    Config.set('graphics', 'window_state', 'maximized')

from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.image import Image, Widget
from kivy.lang import Builder
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton
from mtcnn.mtcnn import MTCNN
from tensorflow.keras.models import load_model
from modules.systemDB import DB
import time
import pickle
import numpy as np
import cv2
from kivymd.uix.list import TwoLineIconListItem


# COmmand: pyinstaller main.spec -y
# Command for With Folders: pyinstaller --icon=main.ico --additional-hooks-dir=hooks --hidden-import=configparser --hidden-import=win32file --hidden-import=win32timezone --hidden-import=win32con --hidden-import=pwintypes main.py
# Command Onefile: pyinstaller --onefile --icon=main.ico --additional-hooks-dir=hooks --hidden-import=configparser main.py
try:
    DBMODEL = DB(sys_config.DB_MODEL)
    DBMODEL.open_db()
    DBMODEL.create_tb(sys_config.MOD_Q)
    DBMODEL.close_db()
except Exception as e:
    print("THeres some error regarading to importing file")

helperString = '''
ScreenManager:
    OpeningScreen:
    MainScreen:
    WaitingScreen:
<OpeningScreen>:
    name: 'openingscreen'
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: "images/banner.jpg"
    MDRaisedButton:
        text: "START MONITORING"
        md_bg_color: app.theme_cls.primary_color
        font_size: '20sp'
        pos_hint: {'center_x':0.125,'center_y':0.2}
        on_press:
            root.manager.current = 'waitingscreen'
            root.manager.transition.direction = 'left'
    
            app.initialized_mainscreen()
<WaitingScreen>:
    name: 'waitingscreen'
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: "images/loader_banner.jpg"  
    MDProgressBar:
        id: progress_bar_id
        value:30
        pos_hint: {'center_y':0.02}
        color: app.theme_cls.accent_color
<MainScreen>:
    name: 'mainscreen'
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: "images/mainscreen_bg.jpg"
    MDNavigationLayout:
        ScreenManager:
            Screen:
                id: mainScreenID
                BoxLayout:
                    orientation: 'vertical'
                    MDToolbar:
                        id : title_id
                        title: ''
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
                                    cols:5
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
                                            text: '5'
                                            font_size: '78'
                                            color :(0,150,136,0.8)
                                            pos_hint: {'center_x':0.88,'center_y':0.43}
                                        MDRaisedButton:
                                            id: nw_btn_id
                                            text: 'NOT DETECTED'
                                            md_bg_color : 0.098,0.64,0.80,1
                                            pos_hint: {'center_x':0.3,'center_y':0.02}
                                    FloatLayout:
                                        spacing: 50
                                        Image:
                                            source: 'images/icw.png'
                                            pos_hint: {'center_x':0.65,'center_y':0.6}
                                            size_hint: None,None
                                            size: 200,200
                                            allow_stretch: False
                                            keep_ratio: True
                                        MDLabel:
                                            id: icw_label_id
                                            text: '5'
                                            font_size: '78'
                                            color :(0,150,136,0.8)
                                            pos_hint: {'center_x':1.25,'center_y':0.43}
                                        MDRaisedButton:
                                            id: icw_btn_id
                                            text: 'NOT DETECTED'
                                            md_bg_color : 0.098,0.64,0.80,1
                                            pos_hint: {'center_x':0.65,'center_y':0.02}
                                    FloatLayout:
                                        spacing: 50
                                        Image:
                                            source: 'images/cw.png'
                                            pos_hint: {'center_x':1,'center_y':0.6}
                                            size_hint: None,None
                                            size: 200,200
                                            allow_stretch: False
                                            keep_ratio: True
                                        MDLabel:
                                            id: cw_label_id
                                            text: '5'
                                            font_size: '78'
                                            color :(0,150,136,0.8)
                                            pos_hint: {'center_x':1.6,'center_y':0.43}
                                        MDRaisedButton:
                                            id: cw_btn_id
                                            text: 'NOT DETECTED'
                                            md_bg_color : 0.098,0.64,0.80,1
                                            pos_hint: {'center_x':1,'center_y':0.02}
                                    FloatLayout:
                                        MDLabel:
                                            text: 'FPS: '
                                            font_size: '25'
                                            color :(0,150,136,0.8)
                                            pos_hint: {'center_x':4.4,'center_y':1.1}
                                        MDLabel:
                                            id: fps_id
                                            text: '20'
                                            font_size: '25'
                                            color :(0,150,136,0.8)
                                            pos_hint: {'center_x':4.8,'center_y':1.1}
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
                                    size_hint_x: None
                                    size_hint_y: 0.01
                                    width: 640 
                                    padding: 10
                                    GridLayout:
                                        cols: 1                 
                                        MDLabel:
                                            text: 'IMPORT RESNET-50 MODEL AND PKL FILE'
                                            bold: True
                                            font_size: 12 
                                            halign: 'left' 
                                    GridLayout:
                                        cols: 3
                                        height: 500
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
                                        MDRaisedButton: 
                                            text: 'IMPORT'
                                            font_size: 10   
                                            width: 120
                                            size_hint: None,None
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
                                        MDRaisedButton: 
                                            text: 'IMPORT'
                                            font_size: 10 
                                            width: 120
                                            size_hint: None,None
                                            on_release: root.show_LabelDialog()
                                            #background_color: 0,0,0,0 
                                    GridLayout:
                                        cols: 1
                                        halign: 'right' 
                                        MDRaisedButton:
                                            text: 'APPLY CHANGES' 
                                            font_size: 11  
                                            width: 120
                                            size_hint: None,None
                                            on_press:
                                                root.manager.current = 'waitingscreen'
                                                root.manager.transition.direction = 'right'
                                                app.savedChanges()


                    MDToolbar:
                        height:(root.height-root.height)+15
        MDNavigationDrawer:
            id: nav_drawer
            ContentNavigationDrawer:
<ContentNavigationDrawer>:
    orientation: "vertical"
    size_hint_y: 0.93
    padding: 5
    GridLayout:
        rows:3
        spacing: 110
        AnchorLayout:
            size_hint_y:None
            spacing: 100
            Image:
                size_hint:None,None
                id: avatar
                size: "266dp", "266dp"
                source: "images/SMCL_Emblem.png"
        AnchorLayout:
            size_hint_y:None
            MDLabel:
                text: "DEVELOPERS"
                color: (0,150,136,0.8)
                font_style: "Button"
                font_size: 15
        AnchorLayout:
            size_hint_y:None
            MDList:
                TwoLineIconListItem:
                    text: "[size=15]ANNA LIZA RAMOS[/size]"
                    secondary_text: "[size=13]Thesis Advisor[/size]"
                    IconLeftWidget:
                        icon: "account-circle" 
                TwoLineIconListItem:
                    text: "[size=15]JHENO S. CERBITO[/size]"
                    secondary_text: "[size=13]Programmer/Group Leader[/size]"
                    IconLeftWidget:
                        icon: "account-circle"  
                TwoLineIconListItem:
                    text: "[size=15]SOPHIA MIGUELA HADI[/size]"
                    secondary_text: "[size=13]UI Designer/Researcher[/size]"
                    IconLeftWidget:
                        icon: "account-circle"  
                TwoLineIconListItem:
                    text: "[size=15]KIER MIGUEL DELORIA[/size]"
                    secondary_text: "[size=13]Programmer/Researcher[/size]"
                    IconLeftWidget:
                        icon: "account-circle"  
                TwoLineIconListItem:
                    text: "[size=15]TRICIA ELIS BLANCA[/size]"
                    secondary_text: "[size=13]Researchers[/size]"
                    IconLeftWidget:
                        icon: "account-circle" 
                TwoLineIconListItem:
                    text: "[size=15]KYLE SPENCER GO[/size]"
                    secondary_text: "[size=13]Researchers[/size]"
                    IconLeftWidget:
                        icon: "account-circle" 

<ItemDrawer>:
    theme_text_color: "Custom"
    on_release: self.parent.set_color_item(self)
    IconLeftWidget:
        id: icon
        icon: root.icon
        theme_text_color: "Custom"
        text_color: root.text_color
<LoadModelDialog>:
    BoxLayout:
        size: root.size
        pos: root.pos
        orientation: "vertical"
        FileChooserListView:
            id: model_filechooser
            path:
            filters: 
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
            path: 
            filters: 
        BoxLayout:
            size_hint_y: None
            height: 30
            Button:
                text: "Cancel"
                on_release: root.cancel()

            Button:
                text: "Import Label"
                on_release: root.load_label_path(label_filechooser.path, label_filechooser.selection)
'''

class ContentNavigationDrawer(BoxLayout):
    pass

class OpeningScreen(Screen):
    pass

class WaitingScreen(Screen):
    def __init__(self, **kwargs):
        super(WaitingScreen, self).__init__(**kwargs)
        self.nextScreen =ObjectProperty(None)

    def call_once(self,*args):
        Clock.schedule_once(self.load, int(sys_config.LOADER_DUR))

    def increased_prog(self,*args):
        self.ids.progress_bar_id.value += 10

    def reset_progress(self):
        self.ids.progress_bar_id.value = 5

    def load(self,*args):
        self.manager.current = 'mainscreen'
        self.manager.transition.direction = 'left'

class LoadModelDialog(FloatLayout):
    def __init__(self,load_model_path,cancel ,**kwargs):
        super(LoadModelDialog, self).__init__(**kwargs)
        self.load_model_path =load_model_path
        self.cancel = cancel

        Mfilters = list(sys_config.MODEL_FILTERS.split(','))
        self.ids.model_filechooser.filters = Mfilters
        self.ids.model_filechooser.path = sys_config.DEFAULT_PATH

class LoadLabelDialog(FloatLayout):
    def __init__(self,load_label_path,cancel, **kwargs):
        super(LoadLabelDialog, self).__init__(**kwargs)
        self.load_label_path = load_label_path
        self.cancel = cancel
        Lfilters = list(sys_config.LABEL_FILTERS.split(','))
        self.ids.label_filechooser.filters = Lfilters
        self.ids.label_filechooser.path = sys_config.DEFAULT_PATH

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
        self.widget_list = ObjectProperty(None)
        self.model_path = ""#"C:/Users/admin/PycharmProjects/model tmp storage/facemask-inceptionV3-model.h5"
        self.label_path = ""#"C:/Users/admin/PycharmProjects/model tmp storage/labels8k.pkl"

    def check_fps(self,*args):
        self.ids.fps_id.text = str(round(Clock.get_fps(), 2))
    def start_videoCapture(self,*args):
        self.capture = cv2.VideoCapture(int(sys_config.CAMERA_TYPE))
        self.cameraScreen = CameraScreen(
            capture=self.capture,
            fps=float(sys_config.FPS),
            model_path=self.model_path,
            label_path=self.label_path,
            size_hint=(None, None),
            size=(950, 950),
            allow_stretch=False,
            keep_ratio=True,
            pos_hint={'center_x': 1.7, 'center_y': 0.008},
            widget_lst=self.widget_list

        )
        self.ids.cameraViewID.add_widget(self.cameraScreen, len(self.ids.cameraViewID.children))

    def stop_videoCapture(self):
        self.ids.cameraViewID.remove_widget(self.cameraScreen)
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
    def restore_data_path(self):
        DBMODEL.open_db()
        Modelquery = "SELECT * FROM MODEL_CONFIG"
        if DBMODEL.has_values(Modelquery):
            data = DBMODEL.fetch_data(Modelquery)
            model_path_db = data[0][1]
            label_path_db = data[0][2]
            self.ids.model_id_path.text = model_path_db
            self.ids.label_id_path.text = label_path_db
            self.model_path = model_path_db
            self.label_path = label_path_db
        DBMODEL.close_db()
    def saved_changes(self,*args):
        self.dialog = None
        DBMODEL.open_db()
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
            if DBMODEL.has_values("SELECT * FROM MODEL_CONFIG"):
                values = """UPDATE MODEL_CONFIG SET model_path= ?,label_path= ? WHERE id= ? """
                DBMODEL.update_data(values,(self.model_path, self.label_path, int(sys_config.INDEX)))
            else:
                DBMODEL.insert_data("INSERT INTO MODEL_CONFIG VALUES (?,?,?)", (int(sys_config.INDEX), self.model_path, self.label_path))
            DBMODEL.print_data("SELECT * FROM MODEL_CONFIG")
            self.stop_videoCapture()
            self.start_videoCapture()
        DBMODEL.close_db()

    def close_dialog(self,*args):
        self.dialog.dismiss()

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
        print(self.colors[0])

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
            self.widget_list["NW"]["LABEL"].text = str(self.not_wearing_cnt)
            self.widget_list["NW"]["BUTTON"].text = "DETECTED"
            self.widget_list["NW"]["BUTTON"].md_bg_color = 0,0.59,0.53,1
        if self.target == 1:
            self.wearing_cnt += 1
            self.widget_list["CW"]["LABEL"].text = str(self.wearing_cnt)
            self.widget_list["CW"]["BUTTON"].text = "DETECTED"
            self.widget_list["CW"]["BUTTON"].md_bg_color = 0,0.59,0.53,1
        if self.target == 2:
            self.inc_wearing_cnt += 1
            self.widget_list["ICW"]["LABEL"].text = str(self.inc_wearing_cnt)
            self.widget_list["ICW"]["BUTTON"].text = "DETECTED"
            self.widget_list["ICW"]["BUTTON"].md_bg_color = 0,0.59,0.53,1

    def reset_label_count(self):
        self.not_wearing_cnt = 0
        self.wearing_cnt = 0
        self.inc_wearing_cnt = 0
        self.widget_list["NW"]["LABEL"].text = str(self.not_wearing_cnt)
        self.widget_list["NW"]["BUTTON"].text = "NOT DETECTED"
        self.widget_list["NW"]["BUTTON"].md_bg_color = 0.098, 0.64, 0.80, 1
        self.widget_list["CW"]["LABEL"].text = str(self.wearing_cnt)
        self.widget_list["CW"]["BUTTON"].text = "NOT DETECTED"
        self.widget_list["CW"]["BUTTON"].md_bg_color = 0.098, 0.64, 0.80, 1
        self.widget_list["ICW"]["LABEL"].text = str(self.inc_wearing_cnt)
        self.widget_list["ICW"]["BUTTON"].text = "NOT DETECTED"
        self.widget_list["ICW"]["BUTTON"].md_bg_color = 0.098, 0.64, 0.80, 1
    def load_video(self, *args):
        ret, frame = self.capture.read()
        self.reset_label_count()
        if ret:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            faces = self.detector.detect_faces(rgb)
            #print(faces)
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
                    print(e)            #
            buffer = cv2.flip(frame, 0).tostring()
            self.texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            self.texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
            self.texture = self.texture


sm = ScreenManager()
sm.add_widget(OpeningScreen(name='openingscreen'))
sm.add_widget(WaitingScreen(name='waitingscreen'))
sm.add_widget(MainScreen(name='mainscreen'))

class MainApp(MDApp):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.helperStr = ""
        self.cameraCap = None
        self.mainscreen = None
        self.db = None
        self.icon = 'images/tensorflow-logo.png'
        self.title = sys_config.TITLE
    def build(self):
        # self.theme_cls.primary_pallete = "BlueGray"
        self.theme_cls.primary_palette = sys_config.PALETTE

       # self.mainscreen = MainScreen()
        self.helperStr = Builder.load_string(helperString)
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

        return self.helperStr#self.mainscreen  # screen
    def load_waitingscreen(self):
        self.helperStr.get_screen('waitingscreen').call_once()
    def savedChanges(self):
        Clock.schedule_once(self.helperStr.get_screen('mainscreen').saved_changes, 1)
        self.progress()
        self.load_waitingscreen()
        self.resetProgress()
    def resetProgress(self):
        self.helperStr.get_screen('waitingscreen').reset_progress()
    def progress(self):
        Clock.schedule_once(self.helperStr.get_screen('waitingscreen').increased_prog, 1)
        Clock.schedule_once(self.helperStr.get_screen('waitingscreen').increased_prog, 1)
        Clock.schedule_once(self.helperStr.get_screen('waitingscreen').increased_prog, 1)
        Clock.schedule_once(self.helperStr.get_screen('waitingscreen').increased_prog, 0.5)
        Clock.schedule_once(self.helperStr.get_screen('waitingscreen').increased_prog, 1)
        Clock.schedule_once(self.helperStr.get_screen('waitingscreen').increased_prog, 1)
        Clock.schedule_once(self.helperStr.get_screen('waitingscreen').increased_prog, 1)

    def initialized_mainscreen(self):
        self.helperStr.get_screen('mainscreen').ids.title_id.title = sys_config.TITLE
        self.helperStr.get_screen('mainscreen').widget_list = {
            "NW": {
                    "LABEL":   self.helperStr.get_screen('mainscreen').ids.nw_label_id,
                    "BUTTON":  self.helperStr.get_screen('mainscreen').ids.nw_btn_id
            },
            "ICW": {
                    "LABEL":  self.helperStr.get_screen('mainscreen').ids.icw_label_id,
                    "BUTTON": self.helperStr.get_screen('mainscreen').ids.icw_btn_id
            },
            "CW": {
                    "LABEL":  self.helperStr.get_screen('mainscreen').ids.cw_label_id,
                    "BUTTON": self.helperStr.get_screen('mainscreen').ids.cw_btn_id
            }
        }
        Clock.schedule_interval(self.helperStr.get_screen('mainscreen').check_fps, 0.5)
        self.helperStr.get_screen('mainscreen').restore_data_path()
        self.progress()
        self.load_waitingscreen()
        #.init duration load time = 20
        Clock.schedule_once(self.helperStr.get_screen('mainscreen').start_videoCapture,1.5)
        self.resetProgress()


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
