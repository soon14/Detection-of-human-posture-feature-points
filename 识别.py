import cv2
import mediapipe as mp
import numpy as np

class PoseDetector:
    def __init__(self):
        print("初始化姿态检测器...")
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
    def find_pose(self, img, draw=True):
        """检测并绘制人体姿态关键点"""
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(img_rgb)
        
        if self.results.pose_landmarks:
            if draw:
                # 绘制骨骼连接线
                self.mp_draw.draw_landmarks(
                    img, 
                    self.results.pose_landmarks,
                    self.mp_pose.POSE_CONNECTIONS,
                    self.mp_draw.DrawingSpec(color=(255,0,0), thickness=2, circle_radius=2),
                    self.mp_draw.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2)
                )
                
                # 添加关键点标注
                for id, lm in enumerate(self.results.pose_landmarks.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
                    cv2.putText(img, str(id), (cx-10, cy-10), 
                              cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
        
        return img
    
    def find_position(self, img):
        """获取所有关键点的位置"""
        lm_list = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])
        return lm_list

def main():
    print("正在启动人体姿态检测系统...")
    
    # 初始化摄像头
    cap = cv2.VideoCapture(0)
    detector = PoseDetector()
    
    try:
        while True:
            # 读取摄像头画面
            success, img = cap.read()
            if not success:
                print("无法获取摄像头画面")
                break
                
            # 检测姿态
            img = detector.find_pose(img)
            
            # 获取关键点位置
            lm_list = detector.find_position(img)
            if len(lm_list) > 0:
                # 示例：打印右手腕的位置 (关键点16)
                if len(lm_list) > 16:
                    print(f"右手腕坐标: x={lm_list[16][1]}, y={lm_list[16][2]}")
            
            # 显示FPS
            fps = cap.get(cv2.CAP_PROP_FPS)
            cv2.putText(img, f'FPS: {int(fps)}', (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # 显示画面
            cv2.imshow("人体姿态检测", img)
            
            # 按'q'退出
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("正在退出程序...")
                break
                
    except Exception as e:
        print(f"发生错误: {str(e)}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("程序已结束")

if __name__ == "__main__":
    main()