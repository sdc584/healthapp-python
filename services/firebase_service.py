# -*- coding: utf-8 -*-
"""
Firebase服务
处理数据同步和云端存储
"""

import json
import requests
import threading
from datetime import datetime

class FirebaseService:
    """Firebase服务类"""
    
    def __init__(self):
        # Firebase配置（需要实际的Firebase项目配置）
        self.config = {
            'apiKey': 'your_api_key',
            'authDomain': 'your_project.firebaseapp.com',
            'databaseURL': 'https://your_project-default-rtdb.firebaseio.com',
            'projectId': 'your_project',
            'storageBucket': 'your_project.appspot.com',
            'messagingSenderId': '123456789012',
            'appId': '1:123456789012:android:abcdef123456'
        }
        
        self.session = requests.Session()
        self.user_token = None
        self.user_id = None
        
        # 本地缓存
        self.offline_queue = []
        self.is_online = True
        
        self.init_firebase()
    
    def init_firebase(self):
        """初始化Firebase"""
        try:
            # 这里可以初始化Firebase SDK
            # 由于是Python版本，使用REST API方式
            self.base_url = self.config.get('databaseURL', '')
            
            # 检查网络连接
            self.check_connection()
            
        except Exception as e:
            print(f"Firebase初始化失败: {e}")
            self.is_online = False
    
    def check_connection(self):
        """检查网络连接"""
        try:
            response = self.session.get(f"{self.base_url}/.json", timeout=5)
            self.is_online = response.status_code == 200
        except:
            self.is_online = False
        
        return self.is_online
    
    def authenticate_user(self, email, password):
        """用户认证"""
        try:
            if not self.is_online:
                return {'success': False, 'error': '网络连接失败'}
            
            # Firebase Auth REST API
            auth_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
            
            payload = {
                'email': email,
                'password': password,
                'returnSecureToken': True
            }
            
            params = {'key': self.config['apiKey']}
            
            response = self.session.post(auth_url, json=payload, params=params)
            
            if response.status_code == 200:
                data = response.json()
                self.user_token = data.get('idToken')
                self.user_id = data.get('localId')
                
                return {
                    'success': True,
                    'user_id': self.user_id,
                    'token': self.user_token
                }
            else:
                return {'success': False, 'error': '登录失败'}
                
        except Exception as e:
            return {'success': False, 'error': f'认证失败: {e}'}
    
    def register_user(self, email, password):
        """用户注册"""
        try:
            if not self.is_online:
                return {'success': False, 'error': '网络连接失败'}
            
            # Firebase Auth REST API
            auth_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp"
            
            payload = {
                'email': email,
                'password': password,
                'returnSecureToken': True
            }
            
            params = {'key': self.config['apiKey']}
            
            response = self.session.post(auth_url, json=payload, params=params)
            
            if response.status_code == 200:
                data = response.json()
                self.user_token = data.get('idToken')
                self.user_id = data.get('localId')
                
                return {
                    'success': True,
                    'user_id': self.user_id,
                    'token': self.user_token
                }
            else:
                return {'success': False, 'error': '注册失败'}
                
        except Exception as e:
            return {'success': False, 'error': f'注册失败: {e}'}
    
    def sync_user_data(self, user_data):
        """同步用户数据"""
        try:
            if not self.is_online or not self.user_id:
                # 添加到离线队列
                self.offline_queue.append({
                    'type': 'user_data',
                    'data': user_data,
                    'timestamp': datetime.now().isoformat()
                })
                return False
            
            url = f"{self.base_url}/users/{self.user_id}.json"
            params = {'auth': self.user_token}
            
            response = self.session.put(url, json=user_data, params=params)
            
            return response.status_code == 200
            
        except Exception as e:
            print(f"同步用户数据失败: {e}")
            return False
    
    def sync_run_data(self, run_record):
        """同步跑步数据"""
        try:
            if not self.is_online or not self.user_id:
                # 添加到离线队列
                self.offline_queue.append({
                    'type': 'run_data',
                    'data': run_record,
                    'timestamp': datetime.now().isoformat()
                })
                return False
            
            # 按日期组织数据
            date = run_record.get('date', datetime.now().strftime('%Y-%m-%d'))
            url = f"{self.base_url}/runs/{self.user_id}/{date}.json"
            params = {'auth': self.user_token}
            
            # 获取现有数据
            response = self.session.get(url, params=params)
            
            if response.status_code == 200:
                existing_data = response.json() or {'runs': []}
            else:
                existing_data = {'runs': []}
            
            # 添加新记录
            existing_data['runs'].append(run_record)
            
            # 保存更新后的数据
            response = self.session.put(url, json=existing_data, params=params)
            
            return response.status_code == 200
            
        except Exception as e:
            print(f"同步跑步数据失败: {e}")
            return False
    
    def sync_food_data(self, food_data, date):
        """同步饮食数据"""
        try:
            if not self.is_online or not self.user_id:
                # 添加到离线队列
                self.offline_queue.append({
                    'type': 'food_data',
                    'data': food_data,
                    'date': date,
                    'timestamp': datetime.now().isoformat()
                })
                return False
            
            url = f"{self.base_url}/foods/{self.user_id}/{date}.json"
            params = {'auth': self.user_token}
            
            response = self.session.put(url, json=food_data, params=params)
            
            return response.status_code == 200
            
        except Exception as e:
            print(f"同步饮食数据失败: {e}")
            return False
    
    def load_user_data_from_cloud(self):
        """从云端加载用户数据"""
        try:
            if not self.is_online or not self.user_id:
                return None
            
            url = f"{self.base_url}/users/{self.user_id}.json"
            params = {'auth': self.user_token}
            
            response = self.session.get(url, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
                
        except Exception as e:
            print(f"从云端加载用户数据失败: {e}")
            return None
    
    def load_run_data_from_cloud(self, date):
        """从云端加载跑步数据"""
        try:
            if not self.is_online or not self.user_id:
                return None
            
            url = f"{self.base_url}/runs/{self.user_id}/{date}.json"
            params = {'auth': self.user_token}
            
            response = self.session.get(url, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
                
        except Exception as e:
            print(f"从云端加载跑步数据失败: {e}")
            return None
    
    def load_food_data_from_cloud(self, date):
        """从云端加载饮食数据"""
        try:
            if not self.is_online or not self.user_id:
                return None
            
            url = f"{self.base_url}/foods/{self.user_id}/{date}.json"
            params = {'auth': self.user_token}
            
            response = self.session.get(url, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
                
        except Exception as e:
            print(f"从云端加载饮食数据失败: {e}")
            return None
    
    def sync_offline_data(self):
        """同步离线数据"""
        if not self.is_online or not self.offline_queue:
            return
        
        def sync_thread():
            success_count = 0
            
            for item in self.offline_queue[:]:  # 复制列表进行迭代
                try:
                    if item['type'] == 'user_data':
                        if self.sync_user_data(item['data']):
                            self.offline_queue.remove(item)
                            success_count += 1
                    
                    elif item['type'] == 'run_data':
                        if self.sync_run_data(item['data']):
                            self.offline_queue.remove(item)
                            success_count += 1
                    
                    elif item['type'] == 'food_data':
                        if self.sync_food_data(item['data'], item['date']):
                            self.offline_queue.remove(item)
                            success_count += 1
                
                except Exception as e:
                    print(f"同步离线数据项失败: {e}")
                    continue
            
            print(f"成功同步 {success_count} 条离线数据")
        
        # 在后台线程中同步
        threading.Thread(target=sync_thread, daemon=True).start()
    
    def get_sync_status(self):
        """获取同步状态"""
        return {
            'is_online': self.is_online,
            'is_authenticated': self.user_token is not None,
            'offline_queue_count': len(self.offline_queue),
            'user_id': self.user_id
        }
    
    def logout(self):
        """登出"""
        self.user_token = None
        self.user_id = None
        self.offline_queue = []
    
    def start_auto_sync(self, interval=30):
        """启动自动同步"""
        def auto_sync():
            import time
            
            while True:
                try:
                    # 检查连接状态
                    was_online = self.is_online
                    self.check_connection()
                    
                    # 如果刚恢复在线状态，同步离线数据
                    if not was_online and self.is_online:
                        self.sync_offline_data()
                    
                    time.sleep(interval)
                    
                except Exception as e:
                    print(f"自动同步错误: {e}")
                    time.sleep(interval)
        
        sync_thread = threading.Thread(target=auto_sync, daemon=True)
        sync_thread.start()
        
        return sync_thread



