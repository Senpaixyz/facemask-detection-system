from configparser import ConfigParser
file = 'configuration/config.ini'
config = ConfigParser()
config.read(file)

# Default system global variables init
TITLE = config['DEFAULT']['title']
ICON = config['DEFAULT']['icon']
IS_RESIZABLE = config['DEFAULT']['windows_resizable']
SET_DIM = config['DEFAULT']['set_dimension']
DIM_WIDTH = config['DEFAULT']['dimension_width']
DIM_HEIGHT = config['DEFAULT']['dimension_height']
MIN_WIDTH = config['DEFAULT']['min_width']
MIN_HEIGHT = config['DEFAULT']['min_height']
LOADER_PTH = config['DEFAULT']['loader_path']
LOADER_DUR = config['DEFAULT']['loader_duration']
CONFIG_VER = config['DEFAULT']['config_version']
PALETTE = config['DEFAULT']['primary_palette']

# Opencv cameras var init
CAMERA_TYPE = config['VIDEOCAPTURE']['camera'] # 0 main camera
FPS = config['VIDEOCAPTURE']['fps']
LANDMARKS_ENABLED = config['VIDEOCAPTURE']['landmarks']

# DB Query
DB_MODEL = config['DB']['db_model']
DB_SYS = config['DB']['db_system']
DB_IMG = config['DB']['db_images']
MOD_Q = config['DB']['model_query']
SYS_Q = config['DB']['system_query']
IMG_Q = config['DB']['images_query']

# Model Parameter
INDEX = config['MODELPARAM']['index']
DEFAULT_PATH = config['MODELPARAM']['default_path']
MODEL_FILTERS = config['MODELPARAM']['model_filters']
LABEL_FILTERS = config['MODELPARAM']['label_filters']