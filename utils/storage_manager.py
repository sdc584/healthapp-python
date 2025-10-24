# -*- coding: utf-8 -*-
"""
数据存储管理器
管理本地数据存储和读取
"""

import os
import json
from datetime import datetime, timedelta

class StorageManager:
    """数据存储管理器"""
    
    def __init__(self):
        # 数据存储路径
        self.data_dir = 'data'
        self.ensure_data_dir()
        
        # 文件路径
        self.user_file = os.path.join(self.data_dir, 'user_data.json')
        self.runs_dir = os.path.join(self.data_dir, 'runs')
        self.foods_dir = os.path.join(self.data_dir, 'foods')
        
        # 确保子目录存在
        os.makedirs(self.runs_dir, exist_ok=True)
        os.makedirs(self.foods_dir, exist_ok=True)
    
    def ensure_data_dir(self):
        """确保数据目录存在"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def load_user_data(self):
        """加载用户数据"""
        try:
            if os.path.exists(self.user_file):
                with open(self.user_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # 返回默认数据
                return {
                    'name': '用户',
                    'height': 170,
                    'weight': 60,
                    'age': 25,
                    'gender': 'male',
                    'daily_calorie_goal': 2000,
                    'created_at': datetime.now().isoformat()
                }
        except Exception as e:
            print(f"加载用户数据失败: {e}")
            return {}
    
    def save_user_data(self, user_data):
        """保存用户数据"""
        try:
            user_data['updated_at'] = datetime.now().isoformat()
            
            with open(self.user_file, 'w', encoding='utf-8') as f:
                json.dump(user_data, f, ensure_ascii=False, indent=2)
                
            return True
        except Exception as e:
            print(f"保存用户数据失败: {e}")
            return False
    
    def save_run_record(self, run_record):
        """保存跑步记录"""
        try:
            date = run_record['date']
            runs_file = os.path.join(self.runs_dir, f'runs_{date}.json')
            
            # 加载现有数据
            if os.path.exists(runs_file):
                with open(runs_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {'date': date, 'runs': []}
            
            # 添加新记录
            data['runs'].append(run_record)
            
            # 保存数据
            with open(runs_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"保存跑步记录失败: {e}")
            return False
    
    def load_daily_run_data(self, date):
        """加载指定日期的跑步数据"""
        try:
            runs_file = os.path.join(self.runs_dir, f'runs_{date}.json')
            
            if os.path.exists(runs_file):
                with open(runs_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {'date': date, 'runs': []}
                
        except Exception as e:
            print(f"加载跑步数据失败: {e}")
            return {'date': date, 'runs': []}
    
    def save_daily_food_data(self, date, food_data):
        """保存指定日期的食物数据"""
        try:
            foods_file = os.path.join(self.foods_dir, f'foods_{date}.json')
            
            # 确保数据格式正确
            if 'date' not in food_data:
                food_data['date'] = date
            
            food_data['updated_at'] = datetime.now().isoformat()
            
            with open(foods_file, 'w', encoding='utf-8') as f:
                json.dump(food_data, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"保存食物数据失败: {e}")
            return False
    
    def load_daily_food_data(self, date):
        """加载指定日期的食物数据"""
        try:
            foods_file = os.path.join(self.foods_dir, f'foods_{date}.json')
            
            if os.path.exists(foods_file):
                with open(foods_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {
                    'date': date,
                    'foods': [],
                    'nutrition': {
                        'calories': 0,
                        'protein': 0,
                        'carbs': 0,
                        'fat': 0
                    }
                }
                
        except Exception as e:
            print(f"加载食物数据失败: {e}")
            return {'date': date, 'foods': [], 'nutrition': {}}
    
    def load_daily_nutrition(self):
        """加载今日营养数据"""
        today = datetime.now().strftime('%Y-%m-%d')
        data = self.load_daily_food_data(today)
        return data.get('nutrition', {
            'calories': 0,
            'protein': 0,
            'carbs': 0,
            'fat': 0
        })
    
    def save_daily_nutrition(self, nutrition_data):
        """保存今日营养数据"""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            # 获取现有食物数据
            food_data = self.load_daily_food_data(today)
            
            # 更新营养数据
            food_data['nutrition'] = nutrition_data
            food_data['updated_at'] = datetime.now().isoformat()
            
            # 保存到文件
            return self.save_daily_food_data(today, food_data)
            
        except Exception as e:
            print(f"保存营养数据失败: {e}")
            return False
    
    def get_user_statistics(self):
        """获取用户统计数据"""
        try:
            stats = {
                'total_runs': 0,
                'total_distance': 0,
                'total_duration': 0,
                'total_calories_burned': 0,
                'total_foods': 0,
                'total_calories_consumed': 0
            }
            
            # 统计跑步数据
            for filename in os.listdir(self.runs_dir):
                if filename.startswith('runs_') and filename.endswith('.json'):
                    filepath = os.path.join(self.runs_dir, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            runs = data.get('runs', [])
                            
                            for run in runs:
                                stats['total_runs'] += 1
                                stats['total_distance'] += run.get('distance', 0)
                                stats['total_duration'] += run.get('duration', 0)
                                stats['total_calories_burned'] += run.get('calories', 0)
                    except:
                        continue
            
            # 统计食物数据
            for filename in os.listdir(self.foods_dir):
                if filename.startswith('foods_') and filename.endswith('.json'):
                    filepath = os.path.join(self.foods_dir, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            foods = data.get('foods', [])
                            nutrition = data.get('nutrition', {})
                            
                            stats['total_foods'] += len(foods)
                            stats['total_calories_consumed'] += nutrition.get('calories', 0)
                    except:
                        continue
            
            return stats
            
        except Exception as e:
            print(f"获取统计数据失败: {e}")
            return {}
    
    def get_date_range_data(self, start_date, end_date, data_type='both'):
        """获取日期范围内的数据"""
        try:
            results = {
                'runs': [],
                'foods': [],
                'dates': []
            }
            
            # 生成日期列表
            current = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            
            while current <= end:
                date_str = current.strftime('%Y-%m-%d')
                results['dates'].append(date_str)
                
                if data_type in ['both', 'runs']:
                    run_data = self.load_daily_run_data(date_str)
                    results['runs'].extend(run_data.get('runs', []))
                
                if data_type in ['both', 'foods']:
                    food_data = self.load_daily_food_data(date_str)
                    results['foods'].extend(food_data.get('foods', []))
                
                current += timedelta(days=1)
            
            return results
            
        except Exception as e:
            print(f"获取范围数据失败: {e}")
            return {'runs': [], 'foods': [], 'dates': []}
    
    def delete_run_record(self, date, run_index):
        """删除跑步记录"""
        try:
            runs_file = os.path.join(self.runs_dir, f'runs_{date}.json')
            
            if not os.path.exists(runs_file):
                return False
            
            with open(runs_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            runs = data.get('runs', [])
            if 0 <= run_index < len(runs):
                runs.pop(run_index)
                
                # 保存更新后的数据
                with open(runs_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                return True
            
            return False
            
        except Exception as e:
            print(f"删除跑步记录失败: {e}")
            return False
    
    def backup_data(self, backup_path):
        """备份数据"""
        try:
            import shutil
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_dir = f"{backup_path}/health_app_backup_{timestamp}"
            
            shutil.copytree(self.data_dir, backup_dir)
            
            return backup_dir
            
        except Exception as e:
            print(f"数据备份失败: {e}")
            return None
    
    def restore_data(self, backup_path):
        """恢复数据"""
        try:
            import shutil
            
            # 备份当前数据
            current_backup = self.backup_data('.')
            
            # 清除当前数据
            shutil.rmtree(self.data_dir)
            
            # 恢复备份数据
            shutil.copytree(backup_path, self.data_dir)
            
            return True
            
        except Exception as e:
            print(f"数据恢复失败: {e}")
            return False
    
    def clear_all_data(self):
        """清除所有数据"""
        try:
            import shutil
            
            if os.path.exists(self.data_dir):
                shutil.rmtree(self.data_dir)
            
            self.ensure_data_dir()
            os.makedirs(self.runs_dir, exist_ok=True)
            os.makedirs(self.foods_dir, exist_ok=True)
            
            return True
            
        except Exception as e:
            print(f"清除数据失败: {e}")
            return False
