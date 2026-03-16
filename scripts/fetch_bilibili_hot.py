#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B站热门视频抓取脚本
获取B站全站热门视频Top 100，输出CSV和Markdown表格格式
"""

import requests
import csv
import json
from typing import List, Dict


class BilibiliHotFetcher:
    """B站热门视频抓取器"""

    # B站热门视频API
    API_URL = "https://api.bilibili.com/x/web-interface/popular"

    # 请求头，模拟浏览器访问
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "*/*",
    }

    def __init__(self, num: int = 50):
        """
        初始化

        Args:
            num: 获取视频数量，默认50（B站API限制）
        """
        self.num = num
        self.videos = []

    def fetch(self) -> bool:
        """
        获取热门视频数据

        Returns:
            成功返回True，失败返回False
        """
        # 使用主API
        return self._fetch_from_api(self.API_URL)

    def _fetch_from_api(self, url: str) -> bool:
        """
        从指定API获取数据

        Args:
            url: API地址

        Returns:
            成功返回True，失败返回False
        """
        try:
            # 使用URL参数而不是params参数
            # B站API限制ps最大为50
            full_url = f"{url}?ps=50&pn=1"

            print(f"正在请求: {full_url}")
            response = requests.get(
                full_url,
                headers=self.HEADERS,
                timeout=10
            )
            response.raise_for_status()

            data = response.json()

            # 检查API返回状态
            if data.get("code") != 0:
                print(f"API错误信息: {data.get('message')}")
                return False

            # 提取视频列表
            video_list = data.get("data", {}).get("list", [])
            if not video_list:
                print("未获取到视频数据")
                return False

            self.videos = self._parse_videos(video_list)

            print(f"成功获取 {len(self.videos)} 个热门视频")
            return True

        except requests.exceptions.RequestException as e:
            print(f"网络请求失败: {str(e)}")
            return False
        except Exception as e:
            print(f"解析数据失败: {str(e)}")
            return False

    def _parse_videos(self, video_list: List[Dict]) -> List[Dict]:
        """
        解析视频数据

        Args:
            video_list: API返回的视频列表

        Returns:
            解析后的视频列表
        """
        videos = []

        for idx, item in enumerate(video_list, start=1):
            try:
                video = {
                    "rank": idx,
                    "title": item.get("title", "").strip(),
                    "url": f"https://www.bilibili.com/video/{item.get('bvid', '')}",
                    "view": self._format_view_count(item.get("stat", {}).get("view", 0)),
                    "uploader": item.get("owner", {}).get("name", ""),
                    "description": item.get("desc", "").strip()  # 视频简介
                }
                videos.append(video)
            except Exception as e:
                print(f"解析第 {idx} 个视频失败: {str(e)}")
                continue

        return videos

    @staticmethod
    def _format_view_count(count: int) -> str:
        """
        格式化播放量

        Args:
            count: 播放量数值

        Returns:
            格式化后的播放量字符串
        """
        if count >= 100000000:
            return f"{count / 100000000:.1f}亿"
        elif count >= 10000:
            return f"{count / 10000:.1f}万"
        else:
            return str(count)

    def save_csv(self, filename: str = "./bilibili_hot_videos.csv"):
        """
        保存为CSV文件

        Args:
            filename: 输出文件名
        """
        if not self.videos:
            print("没有视频数据可保存")
            return

        try:
            with open(filename, "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=["rank", "title", "url", "view", "uploader", "description"]
                )
                writer.writeheader()
                writer.writerows(self.videos)

            print(f"CSV文件已保存: {filename}")

        except Exception as e:
            print(f"保存CSV文件失败: {str(e)}")

    def save_markdown(self, filename: str = "./bilibili_hot_videos.md"):
        """
        保存为Markdown表格文件

        Args:
            filename: 输出文件名
        """
        if not self.videos:
            print("没有视频数据可保存")
            return

        try:
            with open(filename, "w", encoding="utf-8") as f:
                # 写入表格标题
                f.write("# B站热门视频排行榜\n\n")
                f.write(f"数据更新时间：{self._get_current_time()}\n\n")

                # 写入表头
                f.write("| 排名 | 标题 | 链接 | 播放量 | UP 主 | 简介 |\n")
                f.write("|------|------|------|--------|-------|------|\n")

                # 写入数据行
                for video in self.videos:
                    title = video["title"].replace("|", "\\|")  # 转义表格分隔符
                    # 处理简介中的换行符和表格分隔符
                    desc = video["description"].replace("|", "\\|").replace("\n", " ")
                    # 限制简介长度，避免表格过宽
                    desc = (desc[:100] + "...") if len(desc) > 100 else desc

                    f.write(
                        f"| {video['rank']} | {title} | [链接]({video['url']}) | "
                        f"{video['view']} | {video['uploader']} | {desc} |\n"
                    )

            print(f"Markdown文件已保存: {filename}")

        except Exception as e:
            print(f"保存Markdown文件失败: {str(e)}")

    @staticmethod
    def _get_current_time() -> str:
        """获取当前时间字符串"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def _get_current_date() -> str:
        """获取当前日期字符串"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")


def main():
    """主函数"""
    # 创建抓取器，获取Top 50热门视频（B站API限制）
    fetcher = BilibiliHotFetcher(num=50)

    # 获取数据
    if not fetcher.fetch():
        print("获取热门视频失败")
        return

    # 生成带日期的文件名
    date_str = fetcher._get_current_date()
    csv_filename = f"./bilibili_hot_videos-{date_str}.csv"
    md_filename = f"./bilibili_hot_videos-{date_str}.md"

    # 保存文件
    fetcher.save_csv(csv_filename)
    fetcher.save_markdown(md_filename)

    print("\n完成！生成的文件：")
    print(f"  - {csv_filename} (可用Excel打开)")
    print(f"  - {md_filename} (Markdown表格)")


if __name__ == "__main__":
    main()
