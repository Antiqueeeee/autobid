这个程序的运行方式如下：
首先需要准备输入文件：
bidding/inputs/
    ├── tech.md    # 技术要求文件
    └── score.md   # 评分标准文件

    运行程序：python bidding/bidding_workflow.py

这会启动Flask服务器，默认在 http://localhost:5000
使用API接口：
a. 生成大纲
curl -X POST http://localhost:5000/generate_outline

这会：
读取tech.md和score.md
调用LLM生成大纲
将大纲保存到 outputs/outline.json 和 outputs/outline.md

b. 生成特定章节内容：

curl -X POST http://localhost:5000/generate_content \
  -H "Content-Type: application/json" \
  -d '{"section_title": "第一章 总则"}'

  这会：
读取已生成的大纲
生成指定章节的内容
保存到 outputs/content/ 目录

c. 生成完整文档：

curl -X POST http://localhost:5000/generate_document