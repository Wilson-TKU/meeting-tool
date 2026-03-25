import requests
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="Prompt 測試小工具：用來測試不同 Prompt 對於文本生成的影響")
    parser.add_argument("--host", default="http://localhost:11434", help="Ollama 伺服器網址 (預設為 http://localhost:11434，若是遠端請填入 http://<IP>:11434)")
    parser.add_argument("--prompt", required=True, help="你的 prompt 文字檔路徑 (例如: prompts/summary_prompt.txt)")
    parser.add_argument("--text", required=True, help="你要測試的逐字稿路徑 (例如: data/1_raw_transcript.txt)")
    parser.add_argument("--output", required=False, help="如果加上此參數，將會把結果存入指定檔案 (例如: result.txt)")
    args = parser.parse_args()

    # 讀取檔案
    try:
        with open(args.prompt, 'r', encoding='utf-8') as f:
            prompt_content = f.read()
        with open(args.text, 'r', encoding='utf-8') as f:
            text_content = f.read()
    except FileNotFoundError as e:
        print(f"❌ 發生錯誤，找不到檔案: {e}")
        sys.exit(1)

    url = f"{args.host}/api/generate"
    # 將 Prompt 與文本組合
    full_prompt = f"{prompt_content}\n\n{text_content}"
    
    data = {
        "model": "llama3.2", # 如果你們平台有改用其它模型請在這裡改
        "prompt": full_prompt,
        "stream": False
    }

    print(f"▶ 正在將你的 Prompt 送往 {args.host} (llama3.2) 進行測試中...\n")
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        result = response.json().get("response", "")
        
        print("================ 🤖 模型測試產出結果 ================\n")
        if args.output:
            import os
            output_dir = os.path.dirname(args.output)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"✅ 成功！測試結果已儲存至檔案: {args.output}")
        else:
            print(result)
        print("\n=====================================================")
    except Exception as e:
        print(f"❌ 連線失敗，請確認網址正確與主機端的 Ollama 是否已經開放外部連線: {e}")

if __name__ == "__main__":
    main()
