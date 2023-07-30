import os
import datetime
import time
import argparse
import pytz
import arxiv
import slackweb


def format_summary(summary):
    formatted_summary = ''
    for line in summary.splitlines():
        formatted_summary += line
        if not line.endswith('-'):
            formatted_summary += ' '
    formatted_summary = formatted_summary.rstrip()
    return formatted_summary


def notify_slack(title, pretext, text):
    attachments = []
    content = {
        'title': title,
        'pretext': pretext,
        'text': text
    }
    attachments.append(content)
    slack.notify(attachments=attachments)


SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL')

# コマンドライン引数のパース
parser = argparse.ArgumentParser()
parser.add_argument('--max_results', default=30, help='取得する論文の最大件数を指定してください', type=int)
args = parser.parse_args()

# 検索範囲: arXivの更新に遅延があるため，現在から1週間前の直近24時間に設定
dt_now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
dt_start = (dt_now - datetime.timedelta(days=8)).strftime('%Y%m%d')
dt_end = (dt_now - datetime.timedelta(days=7)).strftime('%Y%m%d')

# 取得する論文のカテゴリを限定し，検索範囲を指定
# カテゴリ一覧: https://arxiv.org/category_taxonomy
query = f'abs:((diagram AND generation) OR text-to-diagram OR (figure AND generation) OR text-to-figure OR (code AND generation) OR text-to-code) AND cat:(cs.CL OR cs.CV OR cs.PL) AND submittedDate:[{dt_start} TO {dt_end}]'

# 条件に合う最新の論文を新しいものから順に取得
papers = arxiv.Search(
    query=query,
    max_results=args.max_results,
    sort_by=arxiv.SortCriterion.SubmittedDate,
    sort_order=arxiv.SortOrder.Descending
)

slack = slackweb.Slack(url=SLACK_WEBHOOK_URL)

for paper in papers.results():
    title = paper.title
    pdf_url = paper.pdf_url
    summary = format_summary(paper.summary)

    notify_slack(title=title, pretext=pdf_url, text=summary)

    # 原則として，Incoming Webhookの呼び出しは1秒あたり1回まで
    time.sleep(1)
