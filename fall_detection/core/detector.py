import cv2
import numpy as np
from kivy.graphics.texture import Texture

class FallDetector:
    def __init__(self):
        # 初始化人体检测器
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        
    def detect_fall(self, texture):
        if not isinstance(texture, Texture):
            return False
            
        # 将 Kivy 纹理转换为 OpenCV 图像
        pixels = texture.pixels
        size = texture.size
        frame = np.frombuffer(pixels, np.uint8)
        frame = frame.reshape(size[1], size[0], 4)  # RGBA 格式
        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
        
        # 使用简单的图像处理方法
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        boxes, weights = self.hog.detectMultiScale(gray, 
                                                 winStride=(4, 4),
                                                 padding=(8, 8),
                                                 scale=1.05)
                                                 
        if len(boxes) == 0:
            return False
            
        # 使用简单的规则检测跌倒
        for (x, y, w, h) in boxes:
            aspect_ratio = float(w)/h
            # 如果人体区域的宽高比异常，可能表示跌倒
            if aspect_ratio > 1.5:  
                return True
        return False 