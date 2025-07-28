#!/usr/bin/env python3
"""
健康資料生成器 - Health Data Generator
用於生成模擬健康資料的工具，支援批量生成個人資料夾和健康資訊
"""

import os
import json
import csv
import random
import argparse
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import shutil

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('health_data_generator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class PersonalInfo:
    """個人基本資訊"""
    name: str
    age: int
    gender: str
    height: float  # cm
    weight: float  # kg
    blood_type: str
    phone: str
    email: str
    address: str
    emergency_contact: str
    id_number: str

@dataclass
class HealthMetrics:
    """健康指標"""
    bmi: float
    blood_pressure_systolic: int
    blood_pressure_diastolic: int
    heart_rate: int
    body_temperature: float
    blood_sugar: float
    cholesterol: float
    created_date: str

@dataclass
class MedicalHistory:
    """病史記錄"""
    allergies: List[str]
    chronic_diseases: List[str]
    medications: List[str]
    surgeries: List[str]
    family_history: List[str]

class HealthDataGenerator:
    """健康資料生成器主類"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config = self._load_config(config_file)
        self._init_data_sources()
    
    def _load_config(self, config_file: Optional[str]) -> Dict:
        """載入配置檔案"""
        default_config = {
            "output_directory": "./generated_health_data",
            "template_image": "1.png",
            "generate_csv": True,
            "generate_json": True,
            "create_folders": True,
            "copy_template": True
        }
        
        if config_file and Path(config_file).exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                default_config.update(user_config)
                logger.info(f"已載入配置檔案: {config_file}")
            except Exception as e:
                logger.warning(f"載入配置檔案失敗: {e}，使用預設配置")
        
        return default_config
    
    def _init_data_sources(self):
        """初始化資料來源"""
        # 中文姓氏
        self.surnames = [
            "趙", "錢", "孫", "李", "週", "吳", "鄭", "王", "馮", "陳", "褚", "衛", 
            "蔣", "沈", "韓", "楊", "朱", "秦", "尤", "許", "何", "呂", "施", "張", 
            "孔", "曹", "嚴", "華", "金", "魏", "陶", "姜", "戚", "謝", "鄒", "喻", 
            "柏", "水", "竇", "章", "雲", "蘇", "潘", "葛", "奚", "範", "彭", "郎", 
            "魯", "韋", "昌", "馬", "苗", "鳳", "花", "方", "俞", "任", "袁", "柳", 
            "酆", "鮑", "史", "唐", "費", "廉", "岑", "薛", "雷", "賀", "倪", "湯"
        ]
        
        # 中文名字
        self.given_names = [
            "家", "珈", "貝", "楠", "希", "辛", "潁", "英", "敬", "莫", "群", "海", 
            "渲", "兒", "與", "釣", "怡", "艾", "雪", "安", "愛", "書", "牛", "新", 
            "婷", "鐺", "妙", "晴", "葶", "歡", "羊", "娜", "瀟", "奧", "末", "城", 
            "圖", "星", "天", "敏", "銘", "君", "豪", "偉", "然", "軒", "萱", "涵", 
            "翔", "廷", "恩", "辰", "睿", "宇", "妍", "彤", "妤", "語", "綺", "俠", 
            "飛", "丁", "寧", "點", "彬", "傑", "美", "叮", "熊", "苗", "東", "奇", 
            "寶", "可", "智", "逸", "健", "筆", "七", "裕", "侃", "福", "嵐", "夕", 
            "博", "榮", "哲", "佛", "阿", "皓", "輝", "淼", "琦", "朗", "昂", "月", 
            "嚕", "賽", "紅", "餃", "岸", "拉", "斐", "保", "濛", "雅", "志", "浩", 
            "子", "梓", "詩", "宥", "承", "品", "宸", "柏", "詠", "羽", "禹", "芯", "思"
        ]
        
        # 血型
        self.blood_types = ["A", "B", "AB", "O"]
        
        # 性別
        self.genders = ["男", "女"]
        
        # 過敏原
        self.allergies = [
            "花粉", "塵蟎", "海鮮", "堅果", "牛奶", "雞蛋", "大豆", "小麥", 
            "藥物過敏", "動物毛髮", "化學物質", "無已知過敏"
        ]
        
        # 慢性疾病
        self.chronic_diseases = [
            "高血壓", "糖尿病", "高血脂", "心臟病", "氣喘", "關節炎", 
            "甲狀腺疾病", "腎臟病", "肝病", "無慢性疾病"
        ]
        
        # 常用藥物
        self.medications = [
            "降血壓藥", "降血糖藥", "降血脂藥", "心臟藥", "氣喘藥", 
            "止痛藥", "維生素", "鈣片", "魚油", "無服用藥物"
        ]
        
        # 手術史
        self.surgeries = [
            "闌尾切除", "膽囊切除", "白內障手術", "骨折手術", "心臟手術", 
            "腫瘤切除", "疝氣修補", "無手術史"
        ]
        
        # 家族病史
        self.family_history = [
            "高血壓", "糖尿病", "心臟病", "癌症", "中風", "腎臟病", 
            "精神疾病", "遺傳性疾病", "無家族病史"
        ]
        
        # 台灣地址
        self.addresses = [
            "台北市信義區", "台北市大安區", "台北市中山區", "台北市松山區",
            "新北市板橋區", "新北市新莊區", "新北市中和區", "新北市永和區",
            "桃園市桃園區", "桃園市中壢區", "台中市西屯區", "台中市北屯區",
            "台南市東區", "台南市北區", "高雄市左營區", "高雄市三民區"
        ]
    
    def generate_name(self) -> str:
        """生成隨機中文姓名"""
        surname = random.choice(self.surnames)
        # 生成1-2個字的名字
        name_length = random.choice([1, 2])
        given_name = ''.join(random.choices(self.given_names, k=name_length))
        return surname + given_name
    
    def generate_phone(self) -> str:
        """生成台灣手機號碼"""
        prefixes = ["09"]
        prefix = random.choice(prefixes)
        number = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        return f"{prefix}{number}"
    
    def generate_email(self, name: str) -> str:
        """生成電子郵件地址"""
        domains = ["gmail.com", "yahoo.com.tw", "hotmail.com", "outlook.com"]
        # 使用拼音或數字作為郵件前綴
        prefix = f"user{random.randint(1000, 9999)}"
        domain = random.choice(domains)
        return f"{prefix}@{domain}"
    
    def generate_id_number(self) -> str:
        """生成模擬身分證號碼（非真實）"""
        # 這是模擬的格式，不是真實的身分證號碼
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        first_letter = random.choice(letters)
        gender_digit = random.choice([1, 2])  # 1=男, 2=女
        numbers = ''.join([str(random.randint(0, 9)) for _ in range(7)])
        return f"{first_letter}{gender_digit}{numbers}"
    
    def calculate_bmi(self, height: float, weight: float) -> float:
        """計算BMI"""
        height_m = height / 100  # 轉換為公尺
        return round(weight / (height_m ** 2), 2)
    
    def generate_personal_info(self) -> PersonalInfo:
        """生成個人基本資訊"""
        name = self.generate_name()
        age = random.randint(18, 80)
        gender = random.choice(self.genders)
        
        # 根據性別和年齡生成合理的身高體重
        if gender == "男":
            height = random.uniform(160, 185)
            weight = random.uniform(55, 90)
        else:
            height = random.uniform(150, 175)
            weight = random.uniform(45, 75)
        
        return PersonalInfo(
            name=name,
            age=age,
            gender=gender,
            height=round(height, 1),
            weight=round(weight, 1),
            blood_type=random.choice(self.blood_types),
            phone=self.generate_phone(),
            email=self.generate_email(name),
            address=random.choice(self.addresses),
            emergency_contact=self.generate_phone(),
            id_number=self.generate_id_number()
        )
    
    def generate_health_metrics(self, person: PersonalInfo) -> HealthMetrics:
        """生成健康指標"""
        bmi = self.calculate_bmi(person.height, person.weight)
        
        # 根據年齡調整正常範圍
        age_factor = 1 + (person.age - 30) * 0.01
        
        return HealthMetrics(
            bmi=bmi,
            blood_pressure_systolic=random.randint(110, 140),
            blood_pressure_diastolic=random.randint(70, 90),
            heart_rate=random.randint(60, 100),
            body_temperature=round(random.uniform(36.0, 37.5), 1),
            blood_sugar=round(random.uniform(80, 120) * age_factor, 1),
            cholesterol=round(random.uniform(150, 250) * age_factor, 1),
            created_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    
    def generate_medical_history(self) -> MedicalHistory:
        """生成病史記錄"""
        return MedicalHistory(
            allergies=random.sample(self.allergies, random.randint(0, 3)),
            chronic_diseases=random.sample(self.chronic_diseases, random.randint(0, 2)),
            medications=random.sample(self.medications, random.randint(0, 3)),
            surgeries=random.sample(self.surgeries, random.randint(0, 2)),
            family_history=random.sample(self.family_history, random.randint(0, 3))
        )
    
    def create_person_folder(self, person: PersonalInfo, output_dir: Path) -> Path:
        """為個人建立資料夾"""
        person_dir = output_dir / person.name
        person_dir.mkdir(parents=True, exist_ok=True)
        
        # 複製範本圖片
        if self.config["copy_template"]:
            template_path = Path(self.config["template_image"])
            if template_path.exists():
                shutil.copy2(template_path, person_dir / template_path.name)
                logger.debug(f"已複製範本圖片到 {person_dir}")
        
        return person_dir
    
    def save_person_data(self, person: PersonalInfo, health: HealthMetrics, 
                        medical: MedicalHistory, person_dir: Path):
        """儲存個人資料"""
        # 合併所有資料
        person_data = {
            "personal_info": asdict(person),
            "health_metrics": asdict(health),
            "medical_history": asdict(medical)
        }
        
        # 儲存為JSON
        if self.config["generate_json"]:
            json_file = person_dir / "health_data.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(person_data, f, ensure_ascii=False, indent=2)
    
    def generate_batch_data(self, num_people: int, output_directory: str = None) -> List[Dict]:
        """批量生成健康資料"""
        if output_directory:
            self.config["output_directory"] = output_directory
        
        output_dir = Path(self.config["output_directory"])
        output_dir.mkdir(parents=True, exist_ok=True)
        
        all_data = []
        
        logger.info(f"開始生成 {num_people} 筆健康資料...")
        
        for i in range(num_people):
            try:
                # 生成個人資料
                person = self.generate_personal_info()
                health = self.generate_health_metrics(person)
                medical = self.generate_medical_history()
                
                # 建立個人資料夾
                if self.config["create_folders"]:
                    person_dir = self.create_person_folder(person, output_dir)
                    self.save_person_data(person, health, medical, person_dir)
                
                # 收集資料用於CSV匯出
                person_data = {
                    **asdict(person),
                    **asdict(health),
                    **asdict(medical)
                }
                all_data.append(person_data)
                
                if (i + 1) % 10 == 0:
                    logger.info(f"已生成 {i + 1}/{num_people} 筆資料")
                    
            except Exception as e:
                logger.error(f"生成第 {i + 1} 筆資料時發生錯誤: {e}")
                continue
        
        # 生成CSV檔案
        if self.config["generate_csv"] and all_data:
            self.save_csv_data(all_data, output_dir)
        
        logger.info(f"資料生成完成！共生成 {len(all_data)} 筆資料")
        logger.info(f"輸出目錄: {output_dir.absolute()}")
        
        return all_data
    
    def save_csv_data(self, data: List[Dict], output_dir: Path):
        """儲存CSV資料"""
        csv_file = output_dir / "health_data_summary.csv"
        
        if not data:
            return
        
        # 處理列表欄位
        processed_data = []
        for row in data:
            processed_row = {}
            for key, value in row.items():
                if isinstance(value, list):
                    processed_row[key] = '; '.join(value) if value else ''
                else:
                    processed_row[key] = value
            processed_data.append(processed_row)
        
        # 寫入CSV
        with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
            if processed_data:
                writer = csv.DictWriter(f, fieldnames=processed_data[0].keys())
                writer.writeheader()
                writer.writerows(processed_data)
        
        logger.info(f"CSV檔案已儲存: {csv_file}")

def create_sample_config():
    """建立範例配置檔案"""
    config = {
        "output_directory": "./generated_health_data",
        "template_image": "1.png",
        "generate_csv": True,
        "generate_json": True,
        "create_folders": True,
        "copy_template": True
    }
    
    with open("config.json", 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print("已建立範例配置檔案: config.json")

def main():
    """主函數"""
    parser = argparse.ArgumentParser(description="健康資料生成器")
    parser.add_argument("-n", "--number", type=int, required=True, 
                       help="要生成的人數")
    parser.add_argument("-o", "--output", type=str, 
                       help="輸出目錄路徑")
    parser.add_argument("-c", "--config", type=str, 
                       help="配置檔案路徑")
    parser.add_argument("--create-config", action="store_true", 
                       help="建立範例配置檔案")
    parser.add_argument("-v", "--verbose", action="store_true", 
                       help="詳細輸出")
    
    args = parser.parse_args()
    
    if args.create_config:
        create_sample_config()
        return
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        generator = HealthDataGenerator(args.config)
        generator.generate_batch_data(args.number, args.output)
    except KeyboardInterrupt:
        logger.info("使用者中斷操作")
    except Exception as e:
        logger.error(f"程式執行錯誤: {e}")
        raise

if __name__ == "__main__":
    main()