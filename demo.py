#!/usr/bin/env python3
"""
健康資料生成器示範腳本
Demo script for Health Data Generator
"""

import os
import sys
from pathlib import Path

# 新增當前目錄到 Python 路徑
sys.path.insert(0, str(Path(__file__).parent))

from health_data_generator import HealthDataGenerator
from data_analyzer import HealthDataAnalyzer

def run_demo():
    """執行示範"""
    print("🏥 健康資料生成器示範")
    print("=" * 50)
    
    # 建立生成器
    print("📝 初始化資料生成器...")
    generator = HealthDataGenerator()
    
    # 設定輸出目錄
    output_dir = "./demo_output"
    
    # 生成示範資料
    print("🔄 生成 20 筆示範資料...")
    try:
        data = generator.generate_batch_data(20, output_dir)
        print(f"✅ 成功生成 {len(data)} 筆資料")
        print(f"📁 輸出目錄: {Path(output_dir).absolute()}")
    except Exception as e:
        print(f"❌ 生成資料時發生錯誤: {e}")
        return
    
    # 分析資料
    print("\n📊 分析生成的資料...")
    try:
        analyzer = HealthDataAnalyzer(output_dir)
        report = analyzer.generate_report()
        
        # 顯示報告摘要
        lines = report.split('\n')
        summary_lines = []
        in_summary = False
        
        for line in lines:
            if "人口統計分析" in line:
                in_summary = True
            elif "健康指標分析" in line:
                break
            
            if in_summary and line.strip():
                summary_lines.append(line)
        
        print("📋 分析摘要:")
        for line in summary_lines[:10]:  # 顯示前10行
            print(line)
        
        # 儲存完整報告
        report_file = Path(output_dir) / "demo_analysis_report.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"📄 完整分析報告已儲存至: {report_file}")
        
    except Exception as e:
        print(f"❌ 分析資料時發生錯誤: {e}")
    
    print("\n🎉 示範完成！")
    print(f"📂 請查看 {output_dir} 目錄中的生成檔案")

def show_sample_data():
    """顯示範例資料"""
    print("\n📋 範例個人資料:")
    print("-" * 30)
    
    generator = HealthDataGenerator()
    
    # 生成一筆範例資料
    person = generator.generate_personal_info()
    health = generator.generate_health_metrics(person)
    medical = generator.generate_medical_history()
    
    print(f"姓名: {person.name}")
    print(f"年齡: {person.age} 歲")
    print(f"性別: {person.gender}")
    print(f"身高: {person.height} cm")
    print(f"體重: {person.weight} kg")
    print(f"BMI: {health.bmi}")
    print(f"血壓: {health.blood_pressure_systolic}/{health.blood_pressure_diastolic} mmHg")
    print(f"心率: {health.heart_rate} bpm")
    print(f"血型: {person.blood_type}")
    print(f"過敏史: {', '.join(medical.allergies) if medical.allergies else '無'}")
    print(f"慢性疾病: {', '.join(medical.chronic_diseases) if medical.chronic_diseases else '無'}")

def interactive_demo():
    """互動式示範"""
    print("\n🎮 互動式示範")
    print("=" * 30)
    
    while True:
        print("\n請選擇操作:")
        print("1. 生成示範資料")
        print("2. 顯示範例個人資料")
        print("3. 執行完整示範")
        print("4. 退出")
        
        choice = input("\n請輸入選項 (1-4): ").strip()
        
        if choice == '1':
            try:
                num = int(input("請輸入要生成的人數: "))
                if num <= 0:
                    print("❌ 人數必須大於 0")
                    continue
                
                generator = HealthDataGenerator()
                data = generator.generate_batch_data(num, "./interactive_output")
                print(f"✅ 成功生成 {len(data)} 筆資料")
                
            except ValueError:
                print("❌ 請輸入有效的數字")
            except Exception as e:
                print(f"❌ 發生錯誤: {e}")
        
        elif choice == '2':
            show_sample_data()
        
        elif choice == '3':
            run_demo()
        
        elif choice == '4':
            print("👋 再見！")
            break
        
        else:
            print("❌ 無效的選項，請重新選擇")

def main():
    """主函數"""
    print("🏥 健康資料生成器 - 示範程式")
    print("Health Data Generator - Demo")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--interactive':
            interactive_demo()
        elif sys.argv[1] == '--sample':
            show_sample_data()
        elif sys.argv[1] == '--help':
            print("使用方法:")
            print("  python demo.py              # 執行完整示範")
            print("  python demo.py --interactive # 互動式示範")
            print("  python demo.py --sample      # 顯示範例資料")
            print("  python demo.py --help        # 顯示幫助")
        else:
            print(f"❌ 未知參數: {sys.argv[1]}")
            print("使用 --help 查看可用選項")
    else:
        run_demo()

if __name__ == "__main__":
    main()