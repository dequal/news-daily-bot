# 每日美国新闻邮件推送

自动抓取美国权威新闻源，每日定时推送邮件简报。

## 新闻源
- 纽约时报
- 华盛顿邮报
- 华尔街日报
- 美联社
- CNN
- 彭博

## 配置步骤

### 1. 获取 QQ 邮箱 SMTP 授权码

1. 登录 QQ 邮箱网页版
2. 设置 → 账户 → POP3/SMTP服务 → 开启
3. 生成**授权码**（不是QQ密码）

### 2. 在 GitHub 仓库添加 Secrets

进入仓库 Settings → Secrets and variables → Actions → New repository secret

添加以下三个：
- `SMTP_USER`: `806176940@qq.com`
- `SMTP_PASS`: 你的QQ邮箱授权码
- `TO_EMAIL`: `806176940@qq.com`

### 3. 推送到 GitHub

```bash
git add .
git commit -m "Initial setup"
git branch -M main
git remote add origin https://github.com/你的用户名/news-daily-bot.git
git push -u origin main
```

### 4. 启用 GitHub Actions

进入仓库 Actions 标签页，启用 workflow。

## 手动测试

在 Actions 页面点击 "Run workflow" 手动触发一次测试。

## 自动运行

每天北京时间 8:00 自动运行并发送邮件。
