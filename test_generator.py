#!/usr/bin/env python3
"""
健康資料生成器測試檔案
Test file for Health Data Generator
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import json
import csv

from health_data_generator import HealthDataGenerator, PersonalInfo, HealthMetrics, MedicalHistory

class TestHealthDataGenerator(unittest.TestCase):
    """健康資料生成器測試類"""
    
    def setUp(self):
        """測試前準備"""
        self.temp_dir = tempfile.mkdtemp()
        self.generator = HealthDataGenerator()
    
    def tearDown(self):
        """測試後清理"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_generate_name(self):
        """測試姓名生成"""
        name = self.generator.generate_name()
        self.assertIsInstance(name, str)
        self.assertGreater(len(name), 1)
        self.assertLess(len(name), 5)  # 中文姓名通常2-4個字
    
    def test_generate_phone(self):
        """測試電話號碼生成"""
        phone = self.generator.generate_phone()
        self.assertIsInstance(phone, str)
        self.assertTrue(phone.startswith('09'))
        self.assertEqual(len(phone), 10)
    
    def test_generate_email(self):
        """測試電子郵件生成"""
        email = self.generator.generate_email("測試")
        self.assertIsInstance(email, str)
        self.assertIn('@', email)
        self.assertTrue(email.endswith(('.com', '.tw')))
    
    def test_generate_id_number(self):
        """測試身分證號碼生成"""
        id_num = self.generator.generate_id_number()
        self.assertIsInstance(id_num, str)
        self.assertEqual(len(id_num), 10)
        self.assertTrue(id_num[0].isalpha())
        self.assertTrue(id_num[1].isdigit())
    
    def test_calculate_bmi(self):
        """測試BMI計算"""
        bmi = self.generator.calculate_bmi(170, 70)
        expected_bmi = 70 / (1.7 ** 2)
        self.assertAlmostEqual(bmi, expected_bmi, places=2)
    
    def test_generate_personal_info(self):
        """測試個人資訊生成"""
        person = self.generator.generate_personal_info()
        self.assertIsInstance(person, PersonalInfo)
        self.assertIsInstance(person.name, str)
        self.assertIsInstance(person.age, int)
        self.assertIn(person.gender, ['男', '女'])
        self.assertGreater(person.height, 0)
        self.assertGreater(person.weight, 0)
        self.assertIn(person.blood_type, ['A', 'B', 'AB', 'O'])
    
    def test_generate_health_metrics(self):
        """測試健康指標生成"""
        person = self.generator.generate_personal_info()
        health = self.generator.generate_health_metrics(person)
        self.assertIsInstance(health, HealthMetrics)
        self.assertGreater(health.bmi, 0)
        self.assertGreater(health.blood_pressure_systolic, 0)
        self.assertGreater(health.blood_pressure_diastolic, 0)
        self.assertGreater(health.heart_rate, 0)
        self.assertGreater(health.body_temperature, 35)
        self.assertLess(health.body_temperature, 40)
    
    def test_generate_medical_history(self):
        """測試病史記錄生成"""
        medical = self.generator.generate_medical_history()
        self.assertIsInstance(medical, MedicalHistory)
        self.assertIsInstance(medical.allergies, list)
        self.assertIsInstance(medical.chronic_diseases, list)
        self.assertIsInstance(medical.medications, list)
        self.assertIsInstance(medical.surgeries, list)
        self.assertIsInstance(medical.family_history, list)
    
    def test_generate_batch_data(self):
        """測試批量資料生成"""
        # 設定測試配置
        self.generator.config["output_directory"] = self.temp_dir
        self.generator.config["create_folders"] = True
        self.generator.config["generate_csv"] = True
        self.generator.config["copy_template"] = False  # 避免找不到範本圖片
        
        # 生成測試資料
        data = self.generator.generate_batch_data(5, self.temp_dir)
        
        # 驗證結果
        self.assertEqual(len(data), 5)
        
        # 檢查輸出目錄
        output_path = Path(self.temp_dir)
        self.assertTrue(output_path.exists())
        
        # 檢查CSV檔案
        csv_file = output_path / "health_data_summary.csv"
        self.assertTrue(csv_file.exists())
        
        # 檢查個人資料夾
        person_folders = [d for d in output_path.iterdir() if d.is_dir()]
        self.assertEqual(len(person_folders), 5)
        
        # 檢查個人資料檔案
        for folder in person_folders:
            json_file = folder / "health_data.json"
            self.assertTrue(json_file.exists())
            
            # 驗證JSON內容
            with open(json_file, 'r', encoding='utf-8') as f:
                person_data = json.load(f)
                self.assertIn('personal_info', person_data)
                self.assertIn('health_metrics', person_data)
                self.assertIn('medical_history', person_data)

class TestDataIntegrity(unittest.TestCase):
    """資料完整性測試"""
    
    def setUp(self):
        self.generator = HealthDataGenerator()
    
    def test_data_consistency(self):
        """測試資料一致性"""
        person = self.generator.generate_personal_info()
        health = self.generator.generate_health_metrics(person)
        
        # BMI應該與身高體重一致
        expected_bmi = self.generator.calculate_bmi(person.height, person.weight)
        self.assertEqual(health.bmi, expected_bmi)
    
    def test_age_appropriate_health_metrics(self):
        """測試年齡相關的健康指標"""
        # 生成多個不同年齡的人
        young_person = PersonalInfo(
            name="年輕人", age=25, gender="男", height=175, weight=70,
            blood_type="A", phone="0912345678", email="test@test.com",
            address="台北市", emergency_contact="0987654321", id_number="A123456789"
        )
        
        old_person = PersonalInfo(
            name="老年人", age=70, gender="男", height=175, weight=70,
            blood_type="A", phone="0912345678", email="test@test.com",
            address="台北市", emergency_contact="0987654321", id_number="A123456789"
        )
        
        young_health = self.generator.generate_health_metrics(young_person)
        old_health = self.generator.generate_health_metrics(old_person)
        
        # 老年人的某些指標通常會較高（這是統計趨勢，不是絕對）
        # 這裡只是確保程式能正常運行，不做嚴格的醫學驗證
        self.assertIsInstance(young_health.blood_sugar, float)
        self.assertIsInstance(old_health.blood_sugar, float)

def run_performance_test():
    """效能測試"""
    import time
    
    print("執行效能測試...")
    generator = HealthDataGenerator()
    
    # 測試生成1000筆資料的時間
    start_time = time.time()
    
    temp_dir = tempfile.mkdtemp()
    try:
        generator.config["output_directory"] = temp_dir
        generator.config["create_folders"] = False  # 只測試資料生成，不建立檔案
        generator.config["generate_csv"] = False
        generator.config["copy_template"] = False
        
        data = generator.generate_batch_data(1000, temp_dir)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print(f"生成1000筆資料耗時: {elapsed_time:.2f} 秒")
        print(f"平均每筆資料: {elapsed_time/1000*1000:.2f} 毫秒")
        print(f"實際生成資料筆數: {len(data)}")
        
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == '__main__':
    # 執行單元測試
    print("執行單元測試...")
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # 執行效能測試
    print("\n" + "="*50)
    run_performance_test()