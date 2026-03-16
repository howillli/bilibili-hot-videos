---
name: bilibili-hot-videos
description: 抓取 B 站热门视频信息（标题、链接、播放量、UP 主名称、简介），整理成 CSV 和 Markdown 表格格式
dependency:
  python:
    - requests==2.31.0
---

# B 站热门视频抓取 Skill

## 任务目标
- 本 Skill 用于：抓取 B 站热门视频榜单信息并整理成表格
- 能力包含：
  - 获取 B 站全站热门视频 Top 50（API限制）
  - 提取视频标题、链接、播放量、UP 主名称、简介
  - 输出 CSV 和 Markdown 表格两种格式
- 触发条件：用户需要获取 B 站热门视频排行榜

## 前置准备
无需额外准备

## 操作步骤

### 标准流程

1. **执行抓取**
   - 调用 `scripts/fetch_bilibili_hot.py` 脚本
   - 脚本会自动获取最新的热门视频数据
   - 默认获取 Top 50 热门视频（API限制）

2. **查看结果**
   - CSV 文件：`./bilibili_hot_videos-YYYY-MM-DD.csv`（适合 Excel 打开，YYYY-MM-DD 为日期）
   - Markdown 表格：`./bilibili_hot_videos-YYYY-MM-DD.md`（适合查看，YYYY-MM-DD 为日期）

3. **数据字段说明**
   - **排名**：视频在热门榜单中的位置
   - **标题**：视频标题
   - **链接**：视频完整 URL
   - **播放量**：已格式化（如"123.5万"）
   - **UP 主**：UP 主昵称
   - **简介**：视频简介（Markdown 表格中限制为 100 字符，CSV 中完整显示）

## 资源索引
- 必要脚本：见 [scripts/fetch_bilibili_hot.py](scripts/fetch_bilibili_hot.py)（用于抓取 B 站热门视频数据）

## 注意事项
- 脚本使用 B 站官方 API，无需处理复杂的 HTML 解析
- 已添加合理的请求头，避免被反爬限制
- 播放量已自动格式化为易读格式（万/亿）
- 文件名自动包含日期，便于区分不同时间的数据
- 如需获取更多视频数量，可修改脚本参数

## 使用示例

### 示例 1：获取当前热门视频
```
执行 scripts/fetch_bilibili_hot.py
结果：生成 bilibili_hot_videos-2026-01-23.csv 和 bilibili_hot_videos-2026-01-23.md（日期为执行当天）
```

### 示例 2：查看表格内容
```
cat bilibili_hot_videos-2026-01-23.md
输出：显示 Markdown 格式的热门视频表格（日期为执行当天）
```

### 示例 3：用 Excel 打开
```
打开 bilibili_hot_videos-2026-01-23.csv 文件
结果：在 Excel 中查看和编辑视频数据（日期为执行当天）
```
