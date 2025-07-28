# 🏥 健康資料生成器 (Health Data Generator)

一個功能完整的 Python 工具，用於生成模擬健康資料，適用於機器學習訓練、系統測試和資料分析研究。

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)](#測試)

## 🌟 專案特色

### ✨ 核心功能
- **批量資料生成**: 支援大量健康資料的快速生成
- **真實性模擬**: 基於醫學常識的合理資料範圍
- **多格式輸出**: 支援 JSON、CSV 等多種格式
- **可配置參數**: 透過配置檔案自訂生成規則
- **跨平台相容**: 支援 Windows、macOS、Linux

### 📊 資料類型
- **個人基本資訊**: 姓名、年齡、性別、身高、體重、血型等
- **健康指標**: BMI、血壓、心率、體溫、血糖、膽固醇等
- **病史記錄**: 過敏史、慢性疾病、用藥記錄、手術史、家族病史
- **聯絡資訊**: 電話、電子郵件、地址、緊急聯絡人

### 🔧 進階功能
- **資料分析**: 內建統計分析工具
- **報告生成**: 自動產生分析報告
- **單元測試**: 完整的測試覆蓋
- **效能優化**: 支援大量資料快速生成
- **日誌記錄**: 詳細的操作日誌

## 🚀 快速開始

### 安裝需求
- Python 3.7 或更高版本
- 標準庫（無需額外安裝）

### 基本使用

1. **複製專案**
   ```bash
   git clone https://github.com/abandsdx/Health_GenData.git
   cd Health_GenData
   ```

2. **生成健康資料**
   ```bash
   # 生成 100 筆資料
   python health_data_generator.py -n 100
   
   # 指定輸出目錄
   python health_data_generator.py -n 50 -o ./my_health_data
   
   # 使用配置檔案
   python health_data_generator.py -n 200 -c config.json
   ```

3. **分析生成的資料**
   ```bash
   # 分析資料並生成報告
   python data_analyzer.py -d ./generated_health_data --print
   ```

## 📋 詳細使用說明

### 命令列參數

#### 資料生成器 (health_data_generator.py)
```bash
python health_data_generator.py [選項]

必要參數:
  -n, --number NUMBER     要生成的人數

可選參數:
  -o, --output PATH       輸出目錄路徑
  -c, --config PATH       配置檔案路徑
  --create-config         建立範例配置檔案
  -v, --verbose           詳細輸出
  -h, --help             顯示幫助訊息
```

#### 資料分析器 (data_analyzer.py)
```bash
python data_analyzer.py [選項]

必要參數:
  -d, --directory PATH    資料目錄路徑

可選參數:
  -o, --output PATH       輸出報告檔案路徑
  --print                在終端機顯示報告
  -h, --help             顯示幫助訊息
```

### 配置檔案

建立自訂配置檔案：
```bash
python health_data_generator.py --create-config
```

配置檔案範例 (config.json)：
```json
{
  "output_directory": "./generated_health_data",
  "template_image": "1.png",
  "generate_csv": true,
  "generate_json": true,
  "create_folders": true,
  "copy_template": true,
  "data_settings": {
    "age_range": [18, 80],
    "male_height_range": [160, 185],
    "male_weight_range": [55, 90],
    "female_height_range": [150, 175],
    "female_weight_range": [45, 75]
  },
  "health_ranges": {
    "blood_pressure_systolic": [110, 140],
    "blood_pressure_diastolic": [70, 90],
    "heart_rate": [60, 100],
    "body_temperature": [36.0, 37.5],
    "blood_sugar_base": [80, 120],
    "cholesterol_base": [150, 250]
  }
}
```

## 📁 輸出結構

生成的資料會按以下結構組織：

```
generated_health_data/
├── health_data_summary.csv          # 所有資料的CSV摘要
├── analysis_report.txt              # 分析報告（如果執行分析）
├── 張小明/                          # 個人資料夾
│   ├── health_data.json            # 個人健康資料
│   └── 1.png                       # 範本圖片（如果啟用）
├── 李美華/
│   ├── health_data.json
│   └── 1.png
└── ...
```

### 個人資料格式

每個人的 `health_data.json` 包含：

```json
{
  "personal_info": {
    "name": "張小明",
    "age": 35,
    "gender": "男",
    "height": 175.2,
    "weight": 72.5,
    "blood_type": "A",
    "phone": "0912345678",
    "email": "user1234@gmail.com",
    "address": "台北市信義區",
    "emergency_contact": "0987654321",
    "id_number": "A123456789"
  },
  "health_metrics": {
    "bmi": 23.6,
    "blood_pressure_systolic": 125,
    "blood_pressure_diastolic": 82,
    "heart_rate": 75,
    "body_temperature": 36.8,
    "blood_sugar": 95.2,
    "cholesterol": 185.7,
    "created_date": "2024-01-01 12:00:00"
  },
  "medical_history": {
    "allergies": ["花粉", "塵蟎"],
    "chronic_diseases": ["高血壓"],
    "medications": ["降血壓藥"],
    "surgeries": ["無手術史"],
    "family_history": ["糖尿病", "心臟病"]
  }
}
```

## 📊 資料分析功能

### 分析報告內容

資料分析器會生成包含以下內容的詳細報告：

#### 📈 人口統計分析
- 總人數統計
- 年齡分布（平均值、中位數、範圍）
- 性別分布
- 血型分布
- 年齡分組統計

#### 🏥 健康指標分析
- BMI 統計和分類
- 血壓統計和分類
- 心率、體溫、血糖、膽固醇統計
- 各項指標的平均值、範圍、標準差

#### 📋 病史分析
- 常見過敏原統計
- 慢性疾病分布
- 用藥情況統計
- 手術史和家族病史分析

### 範例分析報告

```
============================================================
健康資料分析報告
============================================================

📊 人口統計分析
------------------------------
總人數: 100
平均年齡: 49.2 歲
年齡範圍: 18 - 80 歲
性別分布:
  男: 52 人 (52.0%)
  女: 48 人 (48.0%)
年齡分組:
  18-30歲: 18 人 (18.0%)
  31-45歲: 25 人 (25.0%)
  46-60歲: 32 人 (32.0%)
  61-75歲: 20 人 (20.0%)
  76歲以上: 5 人 (5.0%)

🏥 健康指標分析
------------------------------
BMI:
  平均值: 23.4
  範圍: 18.2 - 29.8
BMI分類分布:
  正常體重 (18.5-24.9): 68 人 (68.0%)
  過重 (25-29.9): 25 人 (25.0%)
  體重過輕 (<18.5): 4 人 (4.0%)
  肥胖 (≥30): 3 人 (3.0%)

📋 病史分析
------------------------------
常見過敏原 (前5名):
  無已知過敏: 35 人
  花粉: 18 人
  塵蟎: 15 人
  海鮮: 12 人
  堅果: 8 人
```

## 🧪 測試

### 執行測試
```bash
# 執行所有測試
python test_generator.py

# 執行特定測試
python -m unittest test_generator.TestHealthDataGenerator.test_generate_name

# 執行效能測試
python test_generator.py
```

### 測試覆蓋範圍
- ✅ 姓名生成測試
- ✅ 聯絡資訊生成測試
- ✅ 健康指標計算測試
- ✅ 資料完整性測試
- ✅ 批量生成測試
- ✅ 檔案輸出測試
- ✅ 效能測試

## 🔧 開發和擴展

### 安裝開發相依套件
```bash
pip install -r requirements.txt
```

### 程式碼結構

```python
# 主要類別
class HealthDataGenerator:
    """健康資料生成器主類"""
    
    def generate_personal_info(self) -> PersonalInfo:
        """生成個人基本資訊"""
    
    def generate_health_metrics(self, person: PersonalInfo) -> HealthMetrics:
        """生成健康指標"""
    
    def generate_medical_history(self) -> MedicalHistory:
        """生成病史記錄"""
    
    def generate_batch_data(self, num_people: int) -> List[Dict]:
        """批量生成健康資料"""

# 資料模型
@dataclass
class PersonalInfo:
    """個人基本資訊"""
    name: str
    age: int
    gender: str
    # ... 其他欄位

@dataclass
class HealthMetrics:
    """健康指標"""
    bmi: float
    blood_pressure_systolic: int
    # ... 其他欄位

@dataclass
class MedicalHistory:
    """病史記錄"""
    allergies: List[str]
    chronic_diseases: List[str]
    # ... 其他欄位
```

### 自訂擴展

1. **新增資料欄位**
   ```python
   # 在相應的 dataclass 中新增欄位
   @dataclass
   class PersonalInfo:
       # 現有欄位...
       occupation: str  # 新增職業欄位
   ```

2. **自訂生成規則**
   ```python
   # 修改 _init_data_sources 方法
   def _init_data_sources(self):
       # 新增自訂資料來源
       self.occupations = ["醫生", "教師", "工程師", ...]
   ```

3. **新增分析功能**
   ```python
   # 在 HealthDataAnalyzer 中新增分析方法
   def analyze_occupations(self) -> Dict[str, Any]:
       """分析職業分布"""
       # 實作分析邏輯
   ```

## 📈 效能指標

### 生成效能
- **1,000 筆資料**: ~2-3 秒
- **10,000 筆資料**: ~20-30 秒
- **100,000 筆資料**: ~3-5 分鐘

### 記憶體使用
- **基本生成**: ~50MB
- **大量資料 (100k)**: ~500MB-1GB

### 檔案大小
- **個人 JSON 檔案**: ~1-2KB
- **CSV 摘要檔案**: ~100KB (1000 筆資料)

## 🔒 隱私和安全

### 資料隱私
- ✅ **模擬資料**: 所有生成的資料都是模擬的，非真實個人資訊
- ✅ **無個資外洩**: 不包含任何真實的個人識別資訊
- ✅ **安全使用**: 適合用於開發、測試和研究目的

### 使用建議
- 🔸 僅用於開發和測試環境
- 🔸 不要用於生產環境的真實資料處理
- 🔸 遵守當地的資料保護法規

## 🤝 貢獻指南

歡迎貢獻！請遵循以下步驟：

1. **Fork 專案**
2. **建立功能分支** (`git checkout -b feature/AmazingFeature`)
3. **提交變更** (`git commit -m 'Add some AmazingFeature'`)
4. **推送到分支** (`git push origin feature/AmazingFeature`)
5. **開啟 Pull Request**

### 程式碼規範
- 遵循 PEP 8 風格指南
- 新增適當的文件字串
- 包含單元測試
- 更新 README（如需要）

## 📝 更新日誌

### v2.0.0 (2024-01-01)
- ✨ 完全重寫，採用現代 Python 架構
- ✨ 新增資料分析功能
- ✨ 支援配置檔案
- ✨ 新增完整的單元測試
- ✨ 改善跨平台相容性
- ✨ 新增詳細的日誌記錄

### v1.0.0 (2020-10-16)
- 🎉 初始版本
- ✅ 基本的資料生成功能
- ✅ 支援中文姓名生成
- ✅ 基本的檔案輸出

## 🐛 已知問題

- 在某些 Windows 系統上，中文檔名可能會有編碼問題
- 大量資料生成時可能會消耗較多記憶體
- CSV 檔案在某些 Excel 版本中可能需要手動設定編碼

## 🔮 未來計劃

- [ ] 支援更多資料格式 (XML, YAML)
- [ ] 新增 GUI 介面
- [ ] 支援資料庫直接匯出
- [ ] 新增更多醫學指標
- [ ] 支援多語言姓名生成
- [ ] 新增資料視覺化功能
- [ ] 支援 Docker 部署

## 📞 支援和聯絡

如果您遇到問題或有建議，請：

1. 查看 [Issues](https://github.com/abandsdx/Health_GenData/issues) 頁面
2. 建立新的 Issue 描述問題
3. 提供詳細的錯誤訊息和重現步驟

## 📄 授權

本專案採用 MIT 授權 - 詳見 [LICENSE](LICENSE) 檔案。

## 🙏 致謝

- 感謝所有貢獻者的努力
- 感謝 Python 社群的支援
- 感謝醫學專業人士的建議

---

**⚠️ 免責聲明**: 本工具生成的資料僅供開發、測試和研究使用。請勿將生成的資料用於任何醫療診斷或治療決策。所有健康相關的決定都應該諮詢合格的醫療專業人士。