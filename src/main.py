import os
import datetime
import time
import pytz
import arxiv
import slackweb


SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL')

# 検索範囲: arXivの更新に遅延があるため，現在から1週間前の直近24時間に設定
dt_now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
dt_start = (dt_now - datetime.timedelta(days=8)).strftime('%Y%m%d')
dt_end = (dt_now - datetime.timedelta(days=7)).strftime('%Y%m%d')

# 取得する論文のカテゴリを限定し，検索範囲を指定
# カテゴリ一覧: https://arxiv.org/category_taxonomy
query = f'cat:(cs.AI OR cs.CL OR cs.CV) AND submittedDate:[{dt_start} TO {dt_end}]'

# 一度に取得する論文数の最大値
max_results = 10

# 条件に合う最新の論文を新しいものから順に取得
papers = arxiv.Search(query=query, max_results=max_results, sort_by=arxiv.SortCriterion.SubmittedDate, sort_order=arxiv.SortOrder.Descending)

slack = slackweb.Slack(url=SLACK_WEBHOOK_URL)

for paper in papers.results():
    title = paper.title
    pdf = paper.pdf_url
    summary = ''.join(paper.summary.splitlines())

    attachments = []
    content = {
        'title': title,
        'pretext': pdf,
        'text': summary
    }
    attachments.append(content)
    slack.notify(attachments=attachments)

    # 原則として，Incoming Webhookの呼び出しは1秒あたり1回まで
    time.sleep(1)