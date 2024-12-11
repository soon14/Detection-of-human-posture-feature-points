import sqlite3
from geopy.geocoders import Nominatim

class EmergencyContactManager:
    def __init__(self):
        self.db_connection = sqlite3.connect('fall_detection.db')
        self.geolocator = Nominatim(user_agent="fall_detection_app")
        
    def add_contact(self, name, phone, relationship):
        cursor = self.db_connection.cursor()
        cursor.execute('''
            INSERT INTO emergency_contacts (name, phone, relationship)
            VALUES (?, ?, ?)
        ''', (name, phone, relationship))
        self.db_connection.commit()
        
    def send_emergency_alert(self, location):
        # 获取地理位置信息
        location_info = self.geolocator.reverse(f"{location[0]}, {location[1]}")
        
        # 获取所有紧急联系人
        cursor = self.db_connection.cursor()
        contacts = cursor.execute('SELECT phone FROM emergency_contacts').fetchall()
        
        # 发送紧急短信
        message = f"紧急提醒：检测到跌倒事件！\n位置：{location_info.address}"
        for contact in contacts:
            self.send_sms(contact[0], message) 