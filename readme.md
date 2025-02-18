# Autobid

## 简介

本项目旨在自动化生成投标文件，通过集成大模型（如Gemini FLash）来快速生成符合招标要求的技术文档和评分标准。项目使用Flask作为后端框架，提供简单的API接口来生成大纲和完整文档。

## 运行环境

- Python 3.x
- Flask
- 大模型API（推荐使用OpenRouter的API）

## 安装与配置

1. **克隆仓库**

   ```bash
   git clone [仓库地址]
   cd [仓库目录]
   ```

2. **安装依赖**

   ```bash
   pip install -r requirements.txt
   ```

3. **准备输入文件**

   在 `bidding/inputs/` 目录下准备以下文件：

   - `tech.md`：将招标文件的技术要求手动复制粘贴到这里。
   - `score.md`：将招标文件的评分标准手动复制粘贴到这里。

4. **配置大模型API**

   本项目推荐使用OpenRouter的API，因其支持Gemini FLash模型，生成速度快且内容信息密度高。请按照以下步骤配置：

   - 注册OpenRouter账户并获取API Key。
   - 将API Key填入 `config.py` 文件的相应位置。

## 运行程序

1. **启动Flask服务器**

   ```bash
   python app.py
   ```

   服务器默认运行在 `http://localhost:5000`。

2. **生成投标文件**

   生成投标文件分为两个步骤：生成大纲和生成完整文档。

   - **生成大纲**

     ```bash
     curl -X POST http://localhost:5000/generate_outline
     ```

     此操作会：
     - 读取 `tech.md` 和 `score.md` 文件。
     - 调用大模型生成大纲。
     - 将大纲保存到 `outputs/outline.json` 和 `outputs/outline.md`。

   - **生成完整文档**

     ```bash
     curl -X POST http://localhost:5000/generate_document
     ```

     此操作会：
     - 读取已生成的大纲。
     - 生成指定章节的内容。
     - 保存到 `outputs/content/` 目录。

## 实测

以下为作者实测数据：

a. 生成大纲一般在30s-1min以内；
b. 生成10万+文字的完整文档，用时约220s;
c. 以上单词任务完成，消费Gemini约0.09美元。

## 目录结构

```
bidding/
├── inputs/
│   ├── tech.md
│   └── score.md
├── outputs/
│   ├── outline.json
│   ├── outline.md
│   └── content/
├── config.py
└── app.py
```

## 贡献

欢迎提交Issue和Pull Request来改进本项目。


---

感谢使用本项目！希望它能帮助你高效生成投标文件。