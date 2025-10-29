#!/usr/bin/env python3
"""
测试功能完整的YouTube处理器工作流
"""

import requests
import json
import time
from datetime import datetime

def test_youtube_processor():
    """测试YouTube处理器工作流"""

    webhook_url = 'http://localhost:5679/webhook/youtube-processor-full'

    print("=" * 70)
    print("🎬 测试功能完整的YouTube处理器")
    print("=" * 70)
    print(f"Webhook URL: {webhook_url}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()

    # 测试用例
    test_cases = [
        {
            "name": "测试标准YouTube URL",
            "data": {
                "youtube_url": "https://www.youtube.com/watch?v=_ss8tOxWAuo",
                "language": "zh-CN"
            }
        },
        {
            "name": "测试Youtu.be短链接",
            "data": {
                "youtube_url": "https://youtu.be/_ss8tOxWAuo?si=e9DK79ZeTUoz3wg3",
                "language": "zh-CN"
            }
        },
        {
            "name": "测试YouTube Shorts",
            "data": {
                "youtube_url": "https://youtube.com/shorts/_ss8tOxWAuo",
                "language": "zh-CN"
            }
        },
        {
            "name": "测试无效URL",
            "data": {
                "youtube_url": "not-a-youtube-url",
                "language": "zh-CN"
            }
        },
        {
            "name": "测试缺少URL",
            "data": {
                "language": "zh-CN"
            }
        }
    ]

    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"测试 {i}: {test['name']}")
        print(f"{'='*70}")

        print(f"输入数据: {json.dumps(test['data'], ensure_ascii=False)}")

        try:
            start_time = time.time()
            response = requests.post(webhook_url, json=test['data'], timeout=30)
            elapsed = time.time() - start_time

            print(f"\n响应状态: {response.status_code}")
            print(f"响应时间: {elapsed:.2f}秒")

            if response.status_code == 200:
                result = response.json()

                print(f"\n✅ 成功!")

                # 分析响应
                print("\n📊 处理结果分析:")

                if result.get('success'):
                    print("  ✓ 处理成功")

                    # 视频ID
                    if 'videoId' in result:
                        print(f"  📹 视频ID: {result['videoId']}")

                    # 视频元数据
                    if 'videoMetadata' in result:
                        meta = result['videoMetadata']
                        print(f"  📝 标题: {meta.get('title', 'N/A')}")
                        print(f"  👥 频道: {meta.get('channelTitle', 'N/A')}")
                        print(f"  ⏱️ 时长: {meta.get('duration', 'N/A')}")
                        print(f"  👀 观看次数: {meta.get('viewCount', 'N/A'):,}")

                    # 文章内容
                    if 'article' in result:
                        article = result['article']
                        print(f"\n  📄 生成的文章:")
                        print(f"    标题: {article.get('title', 'N/A')}")
                        print(f"    章节数: {len(article.get('sections', []))}")
                        print(f"    预计阅读时间: {article['metadata'].get('estimatedReadTime', 'N/A')}")
                        print(f"    字数: {article['metadata'].get('wordCount', 'N/A')}")

                        # 显示第一部分内容
                        if article.get('sections'):
                            first_section = article['sections'][0]
                            print(f"\n    第一部分预览 ({first_section.get('type', 'N/A')}):")
                            content = first_section.get('content', 'N/A')[:200]
                            print(f"      {content}...")

                    # 社交媒体摘要
                    if 'socialSummary' in result:
                        social = result['socialSummary']
                        print(f"\n  📱 社交媒体摘要:")
                        print(f"    Twitter: {social.get('twitter', 'N/A')[:60]}...")
                        print(f"    Weibo: {social.get('weibo', 'N/A')[:60]}...")

                else:
                    print("  ❌ 处理失败")
                    if 'error' in result:
                        error = result['error']
                        print(f"    错误代码: {error.get('code', 'N/A')}")
                        print(f"    错误信息: {error.get('message', 'N/A')}")

                # 显示完整响应（可选）
                print(f"\n📦 完整响应数据:")
                print(json.dumps(result, indent=2, ensure_ascii=False)[:1500] + "..." if len(str(result)) > 1500 else json.dumps(result, indent=2, ensure_ascii=False))

            else:
                print(f"❌ HTTP错误: {response.status_code}")
                print(f"响应内容: {response.text[:300]}")

                # 检查是否是webhook未激活
                if "not registered" in response.text:
                    print("\n⚠️ Webhook未激活!")
                    print("请按以下步骤激活:")
                    print("1. 打开n8n UI: http://localhost:5679")
                    print("2. 找到工作流: 'YouTube Processor - Full Version'")
                    print("3. 按 Ctrl+S 保存工作流")
                    print("4. 重新运行此测试")

        except requests.exceptions.Timeout:
            print("\n⏱️ 请求超时（30秒）")
        except Exception as e:
            print(f"\n❌ 异常: {str(e)}")

        # 等待一下再进行下一个测试
        if i < len(test_cases):
            print("\n等待2秒...")
            time.sleep(2)

    print("\n" + "=" * 70)
    print("🎯 测试完成!")
    print("=" * 70)

if __name__ == "__main__":
    test_youtube_processor()