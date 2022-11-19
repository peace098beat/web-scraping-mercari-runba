import sys
import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

 # https://jp.mercari.com/search?keyword=%E3%83%AB%E3%83%B3%E3%83%90
 #&brand_id=3271&status=on_sale
 #&price_min=2000&gclid=Cj0KCQjwqc6aBhC4ARIsAN06NmMiGWhQwRrVNyocu-ms30y4XsnZP1-lYX6nxqa6r-tquO4TBLN6hgoaArF4EALw_wcB&price_max=100000
 #&category_id=875

# メインプログラム
def main():
 
    # PRG2:クロール設定
    BASE_URL = 'https://jp.mercari.com'
    CUR_DIR = os.getcwd()
    args = sys.argv
    KEYWORD = args[1]
    for i in range(2,len(args)):
        KEYWORD += '+' + args[i]
 
    # 検索用URL生成
    options = "&status=on_sale"
    options += "&price_max=100000&price_min=1000"
    options += "&brand_id=3271&category_id=875"

    URL_INI = BASE_URL + '/search/?keyword=' + KEYWORD + options
    url = URL_INI
    page_num = 1
 
    # 検索結果格納リスト・画像保存フォルダ作成
    result = [["label", "price", "url"]]

    # PRG3:スクレイピング実行
    while True:
        try:
            print("page ", page_num)
            print('connectiong to remote browser...')
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')

            browser = webdriver.Remote(
                command_executor='http://localhost:4444/wd/hub',
                desired_capabilities=options.to_capabilities(),
                options=options,
            )

            # browser = webdriver.Chrome(executable_path='C:\chromedriver.exe', options=options)
            browser.get(url)

            print("wait.. ", url)
            time.sleep(5)

            html = browser.page_source.encode('utf-8')
            soup = BeautifulSoup(html, "html.parser")

            items_list = soup.find_all("li", attrs={'data-testid':'item-cell'})
 
            for i, item in enumerate(items_list):
                result.append([item.find("mer-item-thumbnail").get('label'),
                                int(item.find("mer-item-thumbnail").get('price')),
                                BASE_URL + item.find('a').get('href')]
                                )
            
            print("result: ", len(result))
                
            # 次ページボタン処理
            next_button = soup.find('mer-button',attrs={'data-testid':"pagination-next-button"})
            if next_button:
                page_num += 1
                param = '&page_token=v1%3A' + str(page_num)
                next_url = URL_INI + param
                url = next_url
                next_url = ''
            else:
                break
 
        # エラー発生時の例外処理
        except Exception as e:
            message = "[エラー]"+"type:{0}".format(type(e))+"\n"+"args:{0}".format(e.args)
            print(message)
 
        # Chrome終了処理
        finally:
            browser.close()
            browser.quit() 
 

    # csvファイルへ書き込み
    from datetime import datetime as dt
    now = str(dt.now())[:16].replace(":", "").replace(" ", "").replace("-", "")
    import csv
    with open(f'mercari_{KEYWORD}_{now}.csv', 'w') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerows(result)
 
    print('--- END ---')
 
# PRG5:アスペクト比固定して画像リサイズ
def scale_to_width(img, width):  
    height = round(img.height * width / img.width)
    return img.resize((width, height))
 
# スクリプトとして実行された場合の処理
if __name__ == '__main__':
    main()