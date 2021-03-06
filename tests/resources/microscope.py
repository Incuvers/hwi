"""
Microscope Resources
==================== 
"""
DARKFIELD_PATTERN = [
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
]


DPC_PATTERN = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
TCAM_VIDEO_FORMAT = "video/x-raw"
TCAM_PIXEL_FORMAT = "GRAY8"
GST_NAME = "test-pipeline"
CAPS = "ultra"
STREAM_MODE = True

CMOS_CONFIG = {
    'name': "Test",
    'width': 100,
    'height': 100,
    'framerate': '1/2'
}

# gst properties
TCAM_PROPERTIES = {
    'model': "DMK 27AUP031",
    'identifier': "test_identifier",
    'serial': "2120898",
    'backend': "v4l2",
    'exposure_range': (50, 30000000),
    'brightness_range': (0, 4095),
    'gain_range': (4, 63),
    'initialized': True
}
TCAM_PROBE = {
    'Exposure Time (us)': {
        'min': 50,
        'max': 30000000,
        'value': 4000
    },
    'Gain': {
        'min': 4,
        'max': 63,
        'value': 32
    },
    'Brightness': {
        'min': 0,
        'max': 4095,
        'value': 4095
    }
}
TCAM_CAPS = {
    TCAM_VIDEO_FORMAT: {
        TCAM_PIXEL_FORMAT: {
            (2592, 1944): ['15/1', '12/1', '10/1', '8/1', '5/1', '3/1'],
            (2560, 1920): ['15/1', '12/1', '10/1', '8/1', '5/1', '3/1'],
            (1920, 1080): ['30/1', '25/1', '20/1', '10/1', '7/1', '5/1'],
            (1280, 960): ['50/1', '40/1', '30/1', '20/1', '15/1', '10/1'],
            (1280, 720): ['60/1', '50/1', '40/1', '30/1', '20/1', '10/1'],
            (1024, 768): ['70/1', '60/1', '40/1', '30/1', '20/1', '10/1'],
            (640, 480): ['120/1', '90/1', '60/1', '30/1', '15/1', '10/1'],
        },
        "GRAY16_LE": {
            (2592, 1944): ['15/1', '12/1', '10/1', '8/1', '5/1', '3/1'],
            (2560, 1920): ['15/1', '12/1', '10/1', '8/1', '5/1', '3/1'],
            (1920, 1080): ['30/1', '25/1', '20/1', '10/1', '7/1', '5/1'],
            (1280, 960): ['50/1', '40/1', '30/1', '20/1', '15/1', '10/1'],
            (1280, 720): ['60/1', '50/1', '40/1', '30/1', '20/1', '10/1'],
            (1024, 768): ['70/1', '60/1', '40/1', '30/1', '20/1', '10/1'],
            (640, 480): ['120/1', '90/1', '60/1', '30/1', '15/1', '10/1'],
        }}
}
RES_KEYS = list(TCAM_CAPS[TCAM_VIDEO_FORMAT][TCAM_PIXEL_FORMAT].keys())
RESOLUTIONS = {
    'max': {
        'resolution': RES_KEYS[0],
        'framerate': TCAM_CAPS[TCAM_VIDEO_FORMAT][TCAM_PIXEL_FORMAT][RES_KEYS[0]][0]
    },
    'ultra': {
        'resolution': RES_KEYS[1],
        'framerate': TCAM_CAPS[TCAM_VIDEO_FORMAT][TCAM_PIXEL_FORMAT][RES_KEYS[1]][0]
    },
    'high': {
        'resolution': RES_KEYS[3],
        'framerate': TCAM_CAPS[TCAM_VIDEO_FORMAT][TCAM_PIXEL_FORMAT][RES_KEYS[3]][0]
    },
    'med': {
        'resolution': RES_KEYS[4],
        'framerate': TCAM_CAPS[TCAM_VIDEO_FORMAT][TCAM_PIXEL_FORMAT][RES_KEYS[4]][0]
    },
    'low': {
        'resolution': RES_KEYS[6],
        'framerate': TCAM_CAPS[TCAM_VIDEO_FORMAT][TCAM_PIXEL_FORMAT][RES_KEYS[6]][0]
    }
}
