#!/usr/bin/env python3
"""
健康資料分析器 - Health Data Analyzer
用於分析生成的健康資料並產生統計報告
"""

import json
import csv
import argparse
from pathlib import Path
from typing import Dict, List, Any
import statistics
from collections import Counter, defaultdict

class HealthDataAnalyzer:
    """健康資料分析器"""
    
    def __init__(self, data_directory: str):
        self.data_dir = Path(data_directory)
        self.data = []
        self.load_data()
    
    def load_data(self):
        """載入資料"""
        # 嘗試載入CSV檔案
        csv_file = self.data_dir / "health_data_summary.csv"
        if csv_file.exists():
            self.load_from_csv(csv_file)
        else:
            # 從個別JSON檔案載入
            self.load_from_json_files()
    
    def load_from_csv(self, csv_file: Path):
        """從CSV檔案載入資料"""
        with open(csv_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # 轉換數值欄位
                processed_row = {}
                for key, value in row.items():
                    if key in ['age', 'blood_pressure_systolic', 'blood_pressure_diastolic', 'heart_rate']:
                        processed_row[key] = int(value) if value else 0
                    elif key in ['height', 'weight', 'bmi', 'body_temperature', 'blood_sugar', 'cholesterol']:
                        processed_row[key] = float(value) if value else 0.0
                    else:
                        processed_row[key] = value
                self.data.append(processed_row)
        print(f"從CSV載入了 {len(self.data)} 筆資料")
    
    def load_from_json_files(self):
        """從JSON檔案載入資料"""
        json_files = list(self.data_dir.glob("*/health_data.json"))
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 扁平化資料結構
                    flat_data = {}
                    flat_data.update(data['personal_info'])
                    flat_data.update(data['health_metrics'])
                    flat_data.update(data['medical_history'])
                    self.data.append(flat_data)
            except Exception as e:
                print(f"載入 {json_file} 時發生錯誤: {e}")
        print(f"從JSON檔案載入了 {len(self.data)} 筆資料")
    
    def analyze_demographics(self) -> Dict[str, Any]:
        """分析人口統計資料"""
        if not self.data:
            return {}
        
        ages = [row['age'] for row in self.data if 'age' in row]
        genders = [row['gender'] for row in self.data if 'gender' in row]
        blood_types = [row['blood_type'] for row in self.data if 'blood_type' in row]
        
        analysis = {
            "總人數": len(self.data),
            "年齡統計": {
                "平均年齡": round(statistics.mean(ages), 1) if ages else 0,
                "年齡中位數": round(statistics.median(ages), 1) if ages else 0,
                "最小年齡": min(ages) if ages else 0,
                "最大年齡": max(ages) if ages else 0,
                "標準差": round(statistics.stdev(ages), 1) if len(ages) > 1 else 0
            },
            "性別分布": dict(Counter(genders)),
            "血型分布": dict(Counter(blood_types)),
            "年齡分組": self.analyze_age_groups(ages)
        }
        
        return analysis
    
    def analyze_age_groups(self, ages: List[int]) -> Dict[str, int]:
        """分析年齡分組"""
        age_groups = {
            "18-30歲": 0,
            "31-45歲": 0,
            "46-60歲": 0,
            "61-75歲": 0,
            "76歲以上": 0
        }
        
        for age in ages:
            if 18 <= age <= 30:
                age_groups["18-30歲"] += 1
            elif 31 <= age <= 45:
                age_groups["31-45歲"] += 1
            elif 46 <= age <= 60:
                age_groups["46-60歲"] += 1
            elif 61 <= age <= 75:
                age_groups["61-75歲"] += 1
            else:
                age_groups["76歲以上"] += 1
        
        return age_groups
    
    def analyze_health_metrics(self) -> Dict[str, Any]:
        """分析健康指標"""
        if not self.data:
            return {}
        
        metrics = ['bmi', 'blood_pressure_systolic', 'blood_pressure_diastolic', 
                  'heart_rate', 'body_temperature', 'blood_sugar', 'cholesterol']
        
        analysis = {}
        
        for metric in metrics:
            values = [row[metric] for row in self.data if metric in row and row[metric]]
            if values:
                analysis[metric] = {
                    "平均值": round(statistics.mean(values), 2),
                    "中位數": round(statistics.median(values), 2),
                    "最小值": round(min(values), 2),
                    "最大值": round(max(values), 2),
                    "標準差": round(statistics.stdev(values), 2) if len(values) > 1 else 0
                }
        
        # BMI分類分析
        bmi_values = [row['bmi'] for row in self.data if 'bmi' in row and row['bmi']]
        analysis['bmi_categories'] = self.analyze_bmi_categories(bmi_values)
        
        # 血壓分類分析
        bp_data = [(row['blood_pressure_systolic'], row['blood_pressure_diastolic']) 
                   for row in self.data 
                   if 'blood_pressure_systolic' in row and 'blood_pressure_diastolic' in row]
        analysis['blood_pressure_categories'] = self.analyze_bp_categories(bp_data)
        
        return analysis
    
    def analyze_bmi_categories(self, bmi_values: List[float]) -> Dict[str, int]:
        """分析BMI分類"""
        categories = {
            "體重過輕 (<18.5)": 0,
            "正常體重 (18.5-24.9)": 0,
            "過重 (25-29.9)": 0,
            "肥胖 (≥30)": 0
        }
        
        for bmi in bmi_values:
            if bmi < 18.5:
                categories["體重過輕 (<18.5)"] += 1
            elif 18.5 <= bmi < 25:
                categories["正常體重 (18.5-24.9)"] += 1
            elif 25 <= bmi < 30:
                categories["過重 (25-29.9)"] += 1
            else:
                categories["肥胖 (≥30)"] += 1
        
        return categories
    
    def analyze_bp_categories(self, bp_data: List[tuple]) -> Dict[str, int]:
        """分析血壓分類"""
        categories = {
            "正常 (<120/80)": 0,
            "血壓偏高 (120-129/<80)": 0,
            "高血壓第一期 (130-139/80-89)": 0,
            "高血壓第二期 (≥140/90)": 0
        }
        
        for systolic, diastolic in bp_data:
            if systolic < 120 and diastolic < 80:
                categories["正常 (<120/80)"] += 1
            elif 120 <= systolic < 130 and diastolic < 80:
                categories["血壓偏高 (120-129/<80)"] += 1
            elif (130 <= systolic < 140) or (80 <= diastolic < 90):
                categories["高血壓第一期 (130-139/80-89)"] += 1
            else:
                categories["高血壓第二期 (≥140/90)"] += 1
        
        return categories
    
    def analyze_medical_history(self) -> Dict[str, Any]:
        """分析病史資料"""
        if not self.data:
            return {}
        
        # 分析過敏原
        all_allergies = []
        for row in self.data:
            if 'allergies' in row and row['allergies']:
                if isinstance(row['allergies'], str):
                    allergies = [a.strip() for a in row['allergies'].split(';') if a.strip()]
                else:
                    allergies = row['allergies']
                all_allergies.extend(allergies)
        
        # 分析慢性疾病
        all_diseases = []
        for row in self.data:
            if 'chronic_diseases' in row and row['chronic_diseases']:
                if isinstance(row['chronic_diseases'], str):
                    diseases = [d.strip() for d in row['chronic_diseases'].split(';') if d.strip()]
                else:
                    diseases = row['chronic_diseases']
                all_diseases.extend(diseases)
        
        # 分析用藥情況
        all_medications = []
        for row in self.data:
            if 'medications' in row and row['medications']:
                if isinstance(row['medications'], str):
                    medications = [m.strip() for m in row['medications'].split(';') if m.strip()]
                else:
                    medications = row['medications']
                all_medications.extend(medications)
        
        analysis = {
            "過敏原統計": dict(Counter(all_allergies)),
            "慢性疾病統計": dict(Counter(all_diseases)),
            "用藥統計": dict(Counter(all_medications)),
            "過敏原總數": len(all_allergies),
            "慢性疾病總數": len(all_diseases),
            "用藥總數": len(all_medications)
        }
        
        return analysis
    
    def generate_report(self) -> str:
        """生成分析報告"""
        if not self.data:
            return "無資料可分析"
        
        demographics = self.analyze_demographics()
        health_metrics = self.analyze_health_metrics()
        medical_history = self.analyze_medical_history()
        
        report = []
        report.append("=" * 60)
        report.append("健康資料分析報告")
        report.append("=" * 60)
        report.append("")
        
        # 人口統計分析
        report.append("📊 人口統計分析")
        report.append("-" * 30)
        report.append(f"總人數: {demographics.get('總人數', 0)}")
        
        if '年齡統計' in demographics:
            age_stats = demographics['年齡統計']
            report.append(f"平均年齡: {age_stats.get('平均年齡', 0)} 歲")
            report.append(f"年齡範圍: {age_stats.get('最小年齡', 0)} - {age_stats.get('最大年齡', 0)} 歲")
        
        if '性別分布' in demographics:
            report.append("性別分布:")
            for gender, count in demographics['性別分布'].items():
                percentage = (count / demographics['總人數']) * 100
                report.append(f"  {gender}: {count} 人 ({percentage:.1f}%)")
        
        if '年齡分組' in demographics:
            report.append("年齡分組:")
            for group, count in demographics['年齡分組'].items():
                percentage = (count / demographics['總人數']) * 100
                report.append(f"  {group}: {count} 人 ({percentage:.1f}%)")
        
        report.append("")
        
        # 健康指標分析
        report.append("🏥 健康指標分析")
        report.append("-" * 30)
        
        metric_names = {
            'bmi': 'BMI',
            'blood_pressure_systolic': '收縮壓',
            'blood_pressure_diastolic': '舒張壓',
            'heart_rate': '心率',
            'body_temperature': '體溫',
            'blood_sugar': '血糖',
            'cholesterol': '膽固醇'
        }
        
        for metric, chinese_name in metric_names.items():
            if metric in health_metrics:
                stats = health_metrics[metric]
                report.append(f"{chinese_name}:")
                report.append(f"  平均值: {stats['平均值']}")
                report.append(f"  範圍: {stats['最小值']} - {stats['最大值']}")
        
        # BMI分類
        if 'bmi_categories' in health_metrics:
            report.append("BMI分類分布:")
            for category, count in health_metrics['bmi_categories'].items():
                percentage = (count / demographics['總人數']) * 100
                report.append(f"  {category}: {count} 人 ({percentage:.1f}%)")
        
        # 血壓分類
        if 'blood_pressure_categories' in health_metrics:
            report.append("血壓分類分布:")
            for category, count in health_metrics['blood_pressure_categories'].items():
                percentage = (count / demographics['總人數']) * 100
                report.append(f"  {category}: {count} 人 ({percentage:.1f}%)")
        
        report.append("")
        
        # 病史分析
        report.append("📋 病史分析")
        report.append("-" * 30)
        
        if '過敏原統計' in medical_history:
            report.append("常見過敏原 (前5名):")
            allergies = medical_history['過敏原統計']
            for allergy, count in sorted(allergies.items(), key=lambda x: x[1], reverse=True)[:5]:
                report.append(f"  {allergy}: {count} 人")
        
        if '慢性疾病統計' in medical_history:
            report.append("常見慢性疾病 (前5名):")
            diseases = medical_history['慢性疾病統計']
            for disease, count in sorted(diseases.items(), key=lambda x: x[1], reverse=True)[:5]:
                report.append(f"  {disease}: {count} 人")
        
        report.append("")
        report.append("=" * 60)
        report.append("報告生成完成")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def save_report(self, output_file: str = None):
        """儲存分析報告"""
        report = self.generate_report()
        
        if output_file is None:
            output_file = self.data_dir / "analysis_report.txt"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"分析報告已儲存至: {output_file}")
        return report

def main():
    """主函數"""
    parser = argparse.ArgumentParser(description="健康資料分析器")
    parser.add_argument("-d", "--directory", type=str, required=True,
                       help="資料目錄路徑")
    parser.add_argument("-o", "--output", type=str,
                       help="輸出報告檔案路徑")
    parser.add_argument("--print", action="store_true",
                       help="在終端機顯示報告")
    
    args = parser.parse_args()
    
    try:
        analyzer = HealthDataAnalyzer(args.directory)
        report = analyzer.save_report(args.output)
        
        if args.print:
            print(report)
            
    except Exception as e:
        print(f"分析過程中發生錯誤: {e}")
        raise

if __name__ == "__main__":
    main()