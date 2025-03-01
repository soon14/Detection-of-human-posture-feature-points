import cv2
import mediapipe as mp
import time

# 初始化Mediapipe Face模块
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

# 初始化摄像头
cap = cv2.VideoCapture(0)

# 初始化Face Detection和Face Mesh模型
with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection, \
     mp_face_mesh.FaceMesh(min_detection_confidence=0.1, min_tracking_confidence=0.1) as face_mesh:

    # 初始化FPS计算
    start_time = time.time()
    frame_count = 0

    while cap.isOpened():
        # 读取视频帧
        ret, frame = cap.read()
        if not ret:
            break

        # 将图像转换为RGB格式
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 进行Face Detection
        results_detection = face_detection.process(rgb_frame)

        # 进行Face Mesh
        results_mesh = face_mesh.process(rgb_frame)

        # 如果检测到面部
        if results_detection and results_detection.detections:
            for detection in results_detection.detections:
                mp_drawing.draw_detection(frame, detection)

        # 如果检测到面部并提取到了面部特征点
        if results_mesh and results_mesh.multi_face_landmarks:
            for face_landmarks in results_mesh.multi_face_landmarks:
                mp_drawing.draw_landmarks(frame, face_landmarks)

                # 简单的面部表情识别（如微笑检测）
                left_lip = face_landmarks.landmark[61]
                right_lip = face_landmarks.landmark[291]
                upper_lip = face_landmarks.landmark[13]
                lower_lip = face_landmarks.landmark[14]

                lip_distance = abs(upper_lip.y - lower_lip.y)
                lip_width = abs(left_lip.x - right_lip.x)

                # 设定一个简单的阈值来判断微笑
                if lip_distance / lip_width > 0.05:
                    expression = "Smiling"
                else:
                    expression = "Neutral"

                # 在帧上显示面部表情
                cv2.putText(frame, f'Expression: {expression}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # 计算FPS
        frame_count += 1
        elapsed_time = time.time() - start_time
        fps = frame_count / elapsed_time

        # 在帧上显示FPS
        cv2.putText(frame, f'FPS: {fps:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # 显示结果
        cv2.imshow('Facial Expression Analysis', frame)

        # 检测按键，按 'q' 键退出循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放资源
    cap.release()
    cv2.destroyAllWindows()