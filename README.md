

# メルカリスクレイピング

価格を分析したい

最新ぽい
[Pythonスクレイピングでメルカリの商品情報を自動取得する（2022年版）](https://python-work.com/scraping-mercari/)
環境構築
[https://qiita.com/Chanmoro/items/9a3c86bb465c1cce738a](https://qiita.com/Chanmoro/items/9a3c86bb465c1cce738a)
[10分で理解する Selenium - Qiita](https://qiita.com/Chanmoro/items/9a3c86bb465c1cce738a)

## selenium

seleniumは色々大変なのでコンテナを使う
```
$ docker run -d -p 4444:4444 -v /dev/shm:/dev/shm selenium/standalone-chrome:3.141.59-xenon
```
