import feedparser
import smtplib
from email.mime.text import MIMEText
from deep_translator import GoogleTranslator
import os
import re
from datetime import datetime

# 你要的新闻源
RSS_SOURCES = {
    # 主流新闻
    "纽约时报": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "华盛顿邮报": "https://feeds.washingtonpost.com/rss/headlines",
    "美联社": "https://apnews.com/rss/ap-top-news",
    "CNN": "https://rss.cnn.com/rss/cnn_topstories.rss",
    # 金融财经
    "经济学人": "https://www.economist.com/rss/economics_finance.xml",
    "金融时报": "https://www.ft.com/rss?format=xml",
    "彭博社": "https://www.bloomberg.com/feed/rss",
    "路透社财经": "https://feeds.reuters.com/reuters/businessNews",
    "华尔街日报财经": "https://feeds.a.dj.com/rss/RSSMoneyInvesting.xml",
    "MarketWatch": "https://feeds.marketwatch.com/marketwatch/topstories/",
    "CNBC": "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    "Seeking Alpha": "https://seekingalpha.com/feed",
}

MAX_PER_SOURCE = 5  # 每个源取最新5条

# 清理 HTML 标签
def strip_html(text):
    return re.sub(r'<[^>]+>', '', text).strip()

def translate_text(text):
    """将英文翻译为中文"""
    if not text:
        return ""
    try:
        result = GoogleTranslator(source='en', target='zh-CN').translate(text[:500])
        return result if result else text
    except Exception:
        return text

def fetch_news():
    articles = []
    for name, url in RSS_SOURCES.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:MAX_PER_SOURCE]:
                articles.append({
                    "source": name,
                    "title": entry.title,
                    "link": entry.link,
                    "summary": strip_html(entry.get("summary", ""))[:300],
                })
        except Exception as e:
            print(f"Error fetching {name}: {e}")
    return articles

def translate_articles(articles):
    """批量翻译标题和摘要"""
    for art in articles:
        print(f"  翻译: {art['title'][:40]}...")
        art['title_cn'] = translate_text(art['title'])
        art['summary_cn'] = translate_text(art['summary'])
    return articles

def generate_html(articles):
    today = datetime.now().strftime("%Y-%m-%d")
    html = f"<h2>📰 每日新闻+金融简报 {today}</h2>"
    html += "<p>由 阿尔法的1号机器人 自动生成 · 仅供参考</p><hr>"
    
    # 分类：新闻 vs 金融
    news_sources = ["纽约时报", "华盛顿邮报", "美联社", "CNN"]
    finance_sources = ["经济学人", "金融时报", "彭博社", "路透社财经", "华尔街日报财经", "MarketWatch", "CNBC", "Seeking Alpha"]
    
    html += "<h3>📰 综合新闻</h3>"
    for art in articles:
        if art['source'] in news_sources:
            html += f'''<p><strong>【{art['source']}】</strong><br>
<a href="{art['link']}" style="color:#1a73e8;">{art['title_cn']}</a><br>
<span style="color:#666;font-size:13px;">{art['summary_cn']}</span></p><hr style="border:none;border-top:1px solid #eee;">'''
    
    html += "<h3>💰 金融财经</h3>"
    for art in articles:
        if art['source'] in finance_sources:
            html += f'''<p><strong>【{art['source']}】</strong><br>
<a href="{art['link']}" style="color:#1a73e8;">{art['title_cn']}</a><br>
<span style="color:#666;font-size:13px;">{art['summary_cn']}</span></p><hr style="border:none;border-top:1px solid #eee;">'''

    for art in articles:
        html += f"""
<p><strong>【{art['source']}】</strong><br>
<a href="{art['link']}" style="color:#1a73e8;">{art['title_cn']}</a><br>
<span style="color:#666;font-size:13px;">{art['summary_cn']}</span></p><hr style="border:none;border-top:1px solid #eee;">
"""
    return html

def send_email(html_content):
    msg = MIMEText(html_content, "html", "utf-8")
    msg["Subject"] = "📰 每日新闻+金融简报"
    msg["From"] = os.environ["SMTP_USER"]
    msg["To"] = os.environ["TO_EMAIL"]

    with smtplib.SMTP_SSL(os.environ["SMTP_SERVER"], int(os.environ["SMTP_PORT"])) as server:
        server.login(os.environ["SMTP_USER"], os.environ["SMTP_PASS"])
        server.send_message(msg)

if __name__ == "__main__":
    print("📡 正在抓取新闻...")
    news = fetch_news()
    print(f"📰 共获取 {len(news)} 条新闻")

    print("🔄 正在翻译为中文...")
    news = translate_articles(news)

    html = generate_html(news)
    send_email(html)
    print(f"✅ 已发送 {len(news)} 条新闻到 {os.environ['TO_EMAIL']}")
