import feedparser
import smtplib
from email.mime.text import MIMEText
import os
from datetime import datetime

# 你要的新闻源
RSS_SOURCES = {
    "纽约时报": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "华盛顿邮报": "https://feeds.washingtonpost.com/rss/headlines",
    "华尔街日报": "https://feeds.a.dj.com/rss/RSSWorldNews.xml",
    "美联社": "https://apnews.com/rss/ap-top-news",
    "CNN": "https://rss.cnn.com/rss/cnn_topstories.rss",
    "彭博": "https://www.bloomberg.com/feed/rss",
}

def fetch_news():
    articles = []
    for name, url in RSS_SOURCES.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:  # 每个源取最新5条
                articles.append({
                    "source": name,
                    "title": entry.title,
                    "link": entry.link,
                    "summary": entry.get("summary", "")[:200] + "..."
                })
        except Exception as e:
            print(f"Error fetching {name}: {e}")
    return articles

def generate_html(articles):
    today = datetime.now().strftime("%Y-%m-%d")
    html = f"<h2>📰 每日美国权威新闻简报 {today}</h2>"
    html += "<p>由 阿尔法的1号机器人 自动生成 · 仅供参考</p><hr>"
    
    for art in articles:
        html += f"""
<p><strong>{art['source']}</strong>: <a href="{art['link']}">{art['title']}</a></p>
<p>{art['summary']}</p><hr>
"""
    return html

def send_email(html_content):
    msg = MIMEText(html_content, "html", "utf-8")
    msg["Subject"] = "📰 每日美国新闻简报"
    msg["From"] = os.environ["SMTP_USER"]
    msg["To"] = os.environ["TO_EMAIL"]

    with smtplib.SMTP_SSL(os.environ["SMTP_SERVER"], int(os.environ["SMTP_PORT"])) as server:
        server.login(os.environ["SMTP_USER"], os.environ["SMTP_PASS"])
        server.send_message(msg)

if __name__ == "__main__":
    news = fetch_news()
    html = generate_html(news)
    send_email(html)
    print(f"✅ 已发送 {len(news)} 条新闻到 {os.environ['TO_EMAIL']}")
