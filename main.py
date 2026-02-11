import time
import json
import requests
import easyocr
import sys
import os
import warnings
from PIL import ImageGrab
from datetime import datetime
from colorama import Fore, Style, init


# --- 設定ファイルの読み込み（ここを修正しました） ---
def load_config():
    # 実行中のmain.pyがあるフォルダのパスを取得
    base_path = os.path.dirname(os.path.abspath(__file__))
    # そのフォルダの中にあるconfig.jsonのパスを作成
    config_path = os.path.join(base_path, 'config.json')

    if not os.path.exists(config_path):
        print(f"{Fore.RED}[ERROR] {config_path} が見つかりません。{Style.RESET_ALL}")
        # デバッグ用に現在の探している場所を表示
        input("エンターキーを押して終了してください...")
        sys.exit()
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# --- Webhook送信 ---
def send_webhook(url, message):
    data = {"content": message}
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {Fore.GREEN}[INFO] Webhookを送信しました{Style.RESET_ALL}")
    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {Fore.RED}[ERROR] Webhookを送信できませんでした: {e}{Style.RESET_ALL}")

# --- メイン処理 ---
def main():
    print("--- スクリーンOCR監視ツールを起動します ---")
    
    # 設定読み込み
    config = load_config()
    warnings.simplefilter('ignore', UserWarning)
    reader = easyocr.Reader(['en'], gpu=False, verbose=False)
    
    # 設定値の取得
    bbox = (
        config['scan_area']['left'],
        config['scan_area']['top'],
        config['scan_area']['right'],
        config['scan_area']['bottom']
    )
    target_text = config['target_text']
    target_text2 = config['target_text2']
    interval = config['check_interval_seconds']
    webhook_url = config['webhook_url']
    mention = config['mention']

    print(f"{interval}秒ごとに監視します。")
    print(f"ターゲット文字列: {target_text},{target_text2}")
    print(f"監視エリア: {bbox}")
    print("------------------------------------------")

    try:
        while True:
            current_time = datetime.now().strftime('%H:%M:%S')
            
            # 1. 画面キャプチャ
            try:
                # 指定範囲をキャプチャ
                screenshot = ImageGrab.grab(bbox=bbox)
                screenshot.save("screenshot.png")
            except Exception as e:
                print(f"[{current_time}] {Fore.RED}[ERROR] {e}{Style.RESET_ALL}")
                time.sleep(interval)
                continue

            # 2. OCR実行
            try:
                # 画像から文字を抽出
                detected_text = reader.readtext('screenshot.png', detail=0)
                
                # # ログ表示
                display_text = "".join(detected_text)
                print(f"[{current_time}] [INFO] 検出: {display_text}")

                # 3. 文字列判定
                if target_text in display_text:
                    print(f"[{current_time}] {Fore.GREEN}[INFO] {target_text} が来ました Webhookを送信します。{Style.RESET_ALL}")
                    send_webhook(webhook_url, f"<@{mention}> {target_text} が来ました")
                    print(f"[{current_time}] [INFO] 重複を防ぐため、100秒待機します。")
                    time.sleep(100)

                if target_text2 in display_text:
                    print(f"[{current_time}] {Fore.GREEN}[INFO] {target_text2} が来ました Webhookを送信します。{Style.RESET_ALL}")
                    send_webhook(webhook_url, f"<@{mention}> {target_text2} が来ました")
                    print(f"[{current_time}] [INFO] 重複を防ぐため、100秒待機します。")
                    time.sleep(100)
                
            except Exception as e:
                print(f"{Fore.RED}OCRエラー: {e}{Style.RESET_ALL}")

            # 待機
            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n終了します。")

if __name__ == "__main__":
    main()