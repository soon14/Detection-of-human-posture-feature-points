from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.lang import Builder
from core.detector import FallDetector
from sensors.sensor_manager import SensorManager
from contacts.emergency_contact import EmergencyContactManager

# 加载 KV 文件
Builder.load_file('fall_detection/ui/main.kv')

class MainLayout(BoxLayout):
    pass

class FallDetectionApp(App):
    def build(self):
        # 初始化各个模块
        self.detector = FallDetector()
        self.sensor_manager = SensorManager()
        self.contact_manager = EmergencyContactManager()
        
        # 创建主布局
        self.main_layout = MainLayout()
        
        # 启动视频检测
        Clock.schedule_interval(self.update, 1.0/30.0)  # 30 FPS
        
        return self.main_layout

    def update(self, dt):
        try:
            # 获取摄像头画面
            if not hasattr(self.main_layout, 'ids'):
                print("错误：主布局没有 ids 属性")
                return
            
            if not hasattr(self.main_layout.ids, 'camera'):
                print("错误：找不到摄像头组件")
                return
            
            camera = self.main_layout.ids.camera
            if not camera:
                print("错误：摄像头对象为空")
                return
            
            if not camera.texture:
                print("错误：摄像头纹理为空")
                return
            
            # 检测跌倒
            if self.detector.detect_fall(camera.texture):
                self.handle_fall_detection()
            
        except Exception as e:
            print(f"更新过程中出错: {e}")

    def handle_fall_detection(self):
        # 获取当前位置
        location = self.get_current_location()
        # 发送紧急警报
        self.contact_manager.send_emergency_alert(location)

    def emergency_call(self):
        # 处理紧急求助按钮点击事件
        self.handle_fall_detection()

    def get_current_location(self):
        # 返回固定位置用于测试
        return (0.0, 0.0)

if __name__ == '__main__':
    FallDetectionApp().run() 