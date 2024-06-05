import zwoasi as asi # pip install zwoasi
import numpy as np
import cv2           # pip install opencv-python

# 
# SDK 
# скачивается здесь https://www.zwoastro.com/software/ в разделе For Developers
# распаковывается надо взять путь к SDK DLL (Для Windows берется ASICamera2.dll)
dll = "C:/Users/447/Desktop/ZWOASI/ASI_Camera_SDK/ASI_Windows_SDK_V1.35/ASI SDK/lib/x64/ASICamera2.dll"
asi.init(dll)

# Ожидается наличие камер ASI
num_cameras = asi.get_num_cameras()
if num_cameras == 0 :
    raise Exception("Не найдено ASI камер")

# ----------------------------------------

# Выводит список подключенных камер
if False :
    cameras_found = asi.list_cameras()
    print(cameras_found)

# ----------------------------------------
camera_id = 0   # используем первую камеру. Номер меняется если камер несколько и нужна определённая
camera = asi.Camera(camera_id)
# Считываем характеристики камеры
camera_info = camera.get_camera_property()

"""
Здесь примеры camera_info для разных камер
[ZWO ASI183MC Pro]
{'Name': 'ZWO ASI183MC Pro', 'CameraID': 0, 'MaxHeight': 3672, 'MaxWidth': 5496, 'IsColorCam': True, 'BayerPatte
rn': 0, 'SupportedBins': [1, 2, 3, 4], 'SupportedVideoFormat': [0, 1, 3, 2], 'PixelSize': 2.4, 'MechanicalShutte
r': False, 'ST4Port': 0, 'IsCoolerCam': True, 'IsUSB3Host': True, 'IsUSB3Camera': True, 'ElecPerADU': 1.75270402
43148804, 'BitDepth': 12, 'IsTriggerCam': 0}

['ZWO ASI533MM Pro']
{'Name': 'ZWO ASI533MM Pro', 'CameraID': 0, 'MaxHeight': 3008, 'MaxWidth': 3008, 'IsColorCam': False, 'BayerPatt
ern': 0, 'SupportedBins': [1, 2, 3, 4], 'SupportedVideoFormat': [0, 2], 'PixelSize': 3.76, 'MechanicalShutter':
False, 'ST4Port': 0, 'IsCoolerCam': True, 'IsUSB3Host': True, 'IsUSB3Camera': True, 'ElecPerADU': 2.834177970886
2305, 'BitDepth': 14, 'IsTriggerCam': 0}

"""
# ----------------------------------------
if False :
    # Показать возможности настроек
    print('')
    print('Camera controls:')
    controls = camera.get_controls()
    for cn in sorted(controls.keys()):
        print('    %s:' % cn)
        for k in sorted(controls[cn].keys()):
            print('        %s: %s' % (k, repr(controls[cn][k])))

# ----------------------------------------        

# Автоматическая настройка 
expisureAuto = True 

if not expisureAuto : # ручная установка
    camera.set_control_value(asi.ASI_EXPOSURE, 1000) # экспозиция в микросекундах
    camera.set_control_value(asi.ASI_GAIN, 100)       # усиление
    camera.set_control_value(asi.ASI_WB_B, 99)
    camera.set_control_value(asi.ASI_WB_R, 75)
    camera.set_control_value(asi.ASI_GAMMA, 50)
    camera.set_control_value(asi.ASI_BRIGHTNESS, 50)
    camera.set_control_value(asi.ASI_FLIP, 0)
else :                 # автоматическая
    camera.set_control_value(asi.ASI_AUTO_MAX_GAIN, 10)  
    camera.set_control_value(asi.ASI_AUTO_MAX_EXP, 1000000)  
    camera.set_control_value(asi.ASI_GAIN, 0, True)  
    camera.set_control_value(asi.ASI_EXPOSURE, 1000, True) 

# при необходимости ставим свой размер. 
# Иначе будет выводится с размерами camera_info['MaxWidth'] camera_info['MaxHeight'] 
custom_width = 1280
custom_height = 720

# заданные размеры не должны превышать максимальные характеристики 
if custom_width > camera_info['MaxWidth'] or custom_height > camera_info['MaxHeight'] :
    raise ValueError("Некорректные размеры")

cv2.namedWindow('Video')
# указываем камере в каком формете выдавать кадры
camera.set_roi_format(custom_width, custom_height, 1, asi.ASI_IMG_RAW8)

# захват изображения
camera.start_video_capture()

try :
    while True :
        # захват одного кадра
        frame = camera.capture_video_frame()
        # преобразование кадра в формат OpenCV
        image = np.frombuffer(frame, dtype=np.uint8).reshape(custom_height, custom_width, -1)
        # отображение с помощью OpenCV2
        cv2.imshow('Video', image)
        # следим за нажатием ESC
        if cv2.waitKey(1) & 0xFF == 27 :
            break
        # следим за закрытием окна
        if cv2.getWindowProperty('Video', cv2.WND_PROP_VISIBLE) < 1 :
            break
finally :
    # останавливаем видеозахват
    camera.stop_video_capture
    cv2.destroyAllWindows()
