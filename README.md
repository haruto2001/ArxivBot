[![Run](https://github.com/haruto2001/ArxivBot/actions/workflows/python_app.yaml/badge.svg)](https://github.com/haruto2001/ArxivBot/actions/workflows/python_app.yaml)
![](https://img.shields.io/github/languages/code-size/haruto2001/ArxivBot?color=success)

# ArxivBot

## 概要
このプログラムは，arXivにある論文をSlackに定時投稿します．論文の検索条件，投稿するワークスペース・チャンネル・時間は自由に設定可能です．また，定期実行にはGitHub Actionsを使用しています．

## 導入方法
### Step1. リポジトリをフォークする
まずはこのリポジトリを自分のリポジトリにフォークしてください．

>**Note**
>フォークした直後はGitHub Actionsが無効になっています．そのため，自分のリポジトリ内のSettings > Actions > General > Actions permissionsからAllow all actions and reusable workflowsにチェックを付けて保存してください．

### Step2. SlackのワークスペースにIncoming Webhookを追加
Slackに論文を投稿するために，ワークスペースにIncoming Webhookを追加する必要があります．Slackのアプリ検索から追加してください．追加すると，連携するチャンネルを選ぶことができます．ここでは論文を投稿したいチャンネルを選択してください．それが終わるとWebhook URLが発行されるので，それをコピーするなどして控えておいてください．

>**Note**
>Webhook URLを控えるのを忘れてしまった場合は，SlackからIncomig Webhookの設定に飛ぶことで確認することができます．

### Step3. Webhook URLをGitHub Actions Secretsに登録
Step2で発行したWebhook URLをリポジトリ内で環境変数として使用するために，GitHub Actions Secretsから登録します．自分のリポジトリ内のSettings > Secrets and variables > ActionsからNew repository secretボタンを押して追加してください．

## 設定の変更
論文の検索条件，投稿時間は自由に設定することができます．論文の検索条件を変更したい場合は`src/main.py`を変更してください．投稿時間を変更したい場合は`.github/workflows/python_app.yaml`の`schedule`の部分を変更してください．