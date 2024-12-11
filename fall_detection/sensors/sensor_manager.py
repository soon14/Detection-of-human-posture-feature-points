from kivy.clock import Clock
from plyer import accelerometer, gyroscope

class SensorManager:
    def __init__(self):
        self.acc_threshold = 15.0
        self.gyro_threshold = 45.0
        
    def start_monitoring(self):
        # 暂时禁用传感器监测
        pass
        
    def check_sensor_data(self, dt):
        # 返回模拟数据
        return False 