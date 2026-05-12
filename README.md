# AI智能教室 - 教师需求调研系统

一个用于收集和分析教师对AI智能教室需求的调研系统。

## 功能特点

- **问卷填写页面** - 美观的移动端友好问卷界面
- **数据收集** - 自动保存问卷数据到JSON文件
- **管理后台** - 完整的数据查看和统计分析界面
- **可视化图表** - 学科、教龄、年级等分布图表
- **详细查看** - 可查看每份问卷的完整内容

## 项目结构

```
AI自习室建设/
├── app.py                  # Flask后端应用
├── requirements.txt        # Python依赖包
├── survey_data.json        # 数据存储文件（自动生成）
├── templates/
│   ├── ai_classroom_survey.html  # 问卷页面
│   └── admin.html          # 管理后台页面
└── README.md               # 项目说明文档
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动服务

```bash
python app.py
```

### 3. 访问页面

- **问卷页面**: http://localhost:5000/
- **管理后台**: http://localhost:5000/admin

## API接口

### 提交问卷
- `POST /api/submit` - 提交问卷数据

### 获取数据
- `GET /api/data` - 获取所有问卷数据
- `GET /api/stats` - 获取统计数据
- `DELETE /api/data/<id>` - 删除指定问卷

## 数据存储

所有问卷数据保存在 `survey_data.json` 文件中，采用JSON格式存储，便于后续处理和分析。
