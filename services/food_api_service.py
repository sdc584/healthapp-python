# -*- coding: utf-8 -*-
"""
食物API服务
集成Open Food Facts等免费食物数据库API
"""

import requests
import json
import time
from datetime import datetime

class FoodAPIService:
    """食物API服务类"""
    
    def __init__(self):
        # Open Food Facts API配置
        self.base_url = "https://world.openfoodfacts.org"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'HealthApp-Python/1.0'
        })
        
        # 缓存
        self.cache = {}
        self.cache_timeout = 3600  # 1小时缓存
    
    def search_by_barcode(self, barcode):
        """根据条形码搜索食物"""
        try:
            # 检查缓存
            cache_key = f"barcode_{barcode}"
            if cache_key in self.cache:
                cached_data, cache_time = self.cache[cache_key]
                if time.time() - cache_time < self.cache_timeout:
                    return cached_data
            
            # API请求
            url = f"{self.base_url}/api/v0/product/{barcode}.json"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('status') == 1:  # 找到产品
                    product = data.get('product', {})
                    food_data = self.parse_product_data(product)
                    
                    # 缓存结果
                    self.cache[cache_key] = (food_data, time.time())
                    
                    return food_data
                else:
                    return None
            else:
                print(f"API请求失败: {response.status_code}")
                return None
                
        except requests.RequestException as e:
            print(f"网络请求失败: {e}")
            return None
        except Exception as e:
            print(f"条形码搜索失败: {e}")
            return None
    
    def search_by_name(self, query, limit=10):
        """根据食物名称搜索"""
        try:
            # 检查缓存
            cache_key = f"search_{query}_{limit}"
            if cache_key in self.cache:
                cached_data, cache_time = self.cache[cache_key]
                if time.time() - cache_time < self.cache_timeout:
                    return cached_data
            
            # API请求
            url = f"{self.base_url}/cgi/search.pl"
            params = {
                'search_terms': query,
                'json': 1,
                'page_size': limit,
                'fields': 'product_name,brands,nutriments,image_front_url'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                products = data.get('products', [])
                
                results = []
                for product in products[:limit]:
                    food_data = self.parse_product_data(product)
                    if food_data:
                        results.append(food_data)
                
                # 缓存结果
                self.cache[cache_key] = (results, time.time())
                
                return results
            else:
                print(f"搜索API请求失败: {response.status_code}")
                return []
                
        except requests.RequestException as e:
            print(f"搜索网络请求失败: {e}")
            return []
        except Exception as e:
            print(f"名称搜索失败: {e}")
            return []
    
    def parse_product_data(self, product):
        """解析产品数据"""
        try:
            # 基本信息
            name = product.get('product_name', '').strip()
            if not name:
                name = product.get('generic_name', '未知食物')
            
            brands = product.get('brands', '')
            
            # 营养信息（每100g）
            nutriments = product.get('nutriments', {})
            
            # 获取营养数据（优先使用每100g数据）
            calories = self.get_nutrient_value(nutriments, 'energy-kcal_100g', 'energy-kcal')
            protein = self.get_nutrient_value(nutriments, 'proteins_100g', 'proteins')
            carbs = self.get_nutrient_value(nutriments, 'carbohydrates_100g', 'carbohydrates')
            fat = self.get_nutrient_value(nutriments, 'fat_100g', 'fat')
            fiber = self.get_nutrient_value(nutriments, 'fiber_100g', 'fiber')
            sugar = self.get_nutrient_value(nutriments, 'sugars_100g', 'sugars')
            sodium = self.get_nutrient_value(nutriments, 'sodium_100g', 'sodium')
            
            # 其他信息
            image_url = product.get('image_front_url', '')
            ingredients = product.get('ingredients_text', '')
            
            food_data = {
                'name': name,
                'brand': brands,
                'calories': calories,
                'protein': protein,
                'carbs': carbs,
                'fat': fat,
                'fiber': fiber,
                'sugar': sugar,
                'sodium': sodium,
                'image_url': image_url,
                'ingredients': ingredients,
                'source': 'openfoodfacts',
                'serving_size': 100,  # 默认100g
                'servings': 1
            }
            
            return food_data
            
        except Exception as e:
            print(f"解析产品数据失败: {e}")
            return None
    
    def get_nutrient_value(self, nutriments, primary_key, fallback_key):
        """获取营养数据值"""
        # 优先使用每100g的数据
        value = nutriments.get(primary_key)
        if value is not None:
            return float(value)
        
        # 回退到总量数据
        value = nutriments.get(fallback_key)
        if value is not None:
            return float(value)
        
        return 0.0
    
    def get_nutrition_grade(self, food_data):
        """计算营养等级（简化版）"""
        try:
            calories = food_data.get('calories', 0)
            fat = food_data.get('fat', 0)
            sugar = food_data.get('sugar', 0)
            sodium = food_data.get('sodium', 0)
            
            # 简单的评分系统
            score = 0
            
            # 热量评分
            if calories > 400:
                score += 3
            elif calories > 200:
                score += 2
            elif calories > 100:
                score += 1
            
            # 脂肪评分
            if fat > 20:
                score += 3
            elif fat > 10:
                score += 2
            elif fat > 5:
                score += 1
            
            # 糖分评分
            if sugar > 20:
                score += 3
            elif sugar > 10:
                score += 2
            elif sugar > 5:
                score += 1
            
            # 钠含量评分
            if sodium > 600:
                score += 3
            elif sodium > 300:
                score += 2
            elif sodium > 120:
                score += 1
            
            # 转换为等级
            if score <= 2:
                return 'A'  # 优秀
            elif score <= 5:
                return 'B'  # 良好
            elif score <= 8:
                return 'C'  # 一般
            elif score <= 11:
                return 'D'  # 较差
            else:
                return 'E'  # 很差
                
        except Exception as e:
            print(f"计算营养等级失败: {e}")
            return 'C'
    
    def calculate_nutrition(self, base_nutrition, serving_size, servings):
        """根据份量计算营养信息"""
        try:
            multiplier = (serving_size / 100) * servings
            
            calculated = {}
            for key, value in base_nutrition.items():
                if key in ['calories', 'protein', 'carbs', 'fat', 'fiber', 'sugar', 'sodium']:
                    calculated[key] = value * multiplier
                else:
                    calculated[key] = value
            
            return calculated
            
        except Exception as e:
            print(f"计算营养信息失败: {e}")
            return base_nutrition
    
    def get_common_foods(self):
        """获取常见食物列表"""
        common_foods = [
            {
                'name': '白米饭',
                'calories': 130,
                'protein': 2.7,
                'carbs': 28,
                'fat': 0.3
            },
            {
                'name': '苹果',
                'calories': 52,
                'protein': 0.3,
                'carbs': 14,
                'fat': 0.2
            },
            {
                'name': '鸡胸肉',
                'calories': 165,
                'protein': 31,
                'carbs': 0,
                'fat': 3.6
            },
            {
                'name': '牛奶',
                'calories': 42,
                'protein': 3.4,
                'carbs': 5,
                'fat': 1
            },
            {
                'name': '鸡蛋',
                'calories': 155,
                'protein': 13,
                'carbs': 1.1,
                'fat': 11
            }
        ]
        
        # 添加默认字段
        for food in common_foods:
            food.update({
                'brand': '',
                'fiber': 0,
                'sugar': 0,
                'sodium': 0,
                'serving_size': 100,
                'servings': 1,
                'source': 'builtin'
            })
        
        return common_foods
    
    def clear_cache(self):
        """清除缓存"""
        self.cache = {}



