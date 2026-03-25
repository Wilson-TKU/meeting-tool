import requests
import json

def generate_summary(transcript: str) -> str:
    """
    呼叫本機端運行的 Ollama API 服務來生成會議摘要
    """
    url = "http://localhost:11434/api/generate"
    
    # 這裡可以修改成你的會議摘要 Prompt，請 Ollama 幫忙整理！
    # 如果未來需要加上「專有名詞修正」，也可以在這邊再串一層 prompt 或拆分 API 呼叫。
    prompt = f"""請幫我將以下的會議逐字稿整理成一份專業的會議摘要。
包含：
1. 會議重點 (Bullet points)
2. 待辦事項 (Action Items) 與負責部門

會議逐字稿：
{transcript}
"""

    data = {
        "model": "llama3.2",  # 我們選用 3B 參數模型 (Llama 3.2 3B)
        "prompt": prompt,
        "stream": False # 設定 False 表示等待全部生成完才回傳；設成 True 則會像打字機一樣逐步回傳
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status() # 檢查是否有 HTTP Error
        result = response.json()
        return result.get("response", "沒有取得任何內容。")
    except requests.exceptions.RequestException as e:
        return f"連線 Ollama 時發生錯誤，請確認 Ollama (http://localhost:11434) 是否已啟動：{e}"

if __name__ == "__main__":
    # 這裡的假資料代表步驟 1 (音檔 + Whisper) 處理後輸出的逐字稿
    dummy_transcript = """
    A: 大家好，我們今天開會主要是討論接下來 App 首頁改版的計畫。
    B: 沒問題，我覺得首頁的載入速度需要優化，目前大概要等 3 秒。
    A: 好的，那我們把「首頁載入速度優化」列為第一優先，目標是縮短到 1 秒以內。這部分請工程部下週五前評估。
    C: UI 部門這週會先出新的設計稿，預計週三可以給工程部。
    A: 了解，所以週三看設計稿，下週五前工程評估。那今天先這樣，謝謝大家。
    """
    
    print("正在呼叫 Ollama (3B模型) 生成會議摘要中...\n")
    summary = generate_summary(dummy_transcript)
    
    print("================ 會議摘要 ================")
    print(summary)
    print("==========================================")
