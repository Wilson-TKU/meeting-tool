import requests
import os

def _call_ollama(prompt_text: str, content_text: str, output_path: str) -> str:
    """
    由外部讀取 prompt 指令與內文字串，組合成單一訊息送給 Ollama API 的底層方法。
    """
    url = "http://localhost:11434/api/generate"
    full_prompt = f"{prompt_text}\n\n{content_text}"

    data = {
        "model": "llama3.2",  # 我們使用的 3B 語言模型
        "prompt": full_prompt,
        "stream": False       # 關閉串流，一次拿到完整字串
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        result_text = response.json().get("response", "")
        
        # 將最終生成的文本備份至 data/ 目錄
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result_text.strip())
            
        return result_text.strip()
    except requests.exceptions.RequestException as e:
        error_msg = f"呼叫 Ollama 時發生網路錯誤 (請確認 localhost:11434 有啟動): {e}"
        print(f"❌ {error_msg}")
        return error_msg

def fix_domain_terms(raw_transcript: str, prompt_file: str, output_path: str) -> str:
    """階段二：修正專有名詞與錯字"""
    print(f"▶ 讀取外部 Prompt 檔案: {prompt_file}")
    with open(prompt_file, 'r', encoding='utf-8') as f:
        prompt_text = f.read()
        
    print(f"▶ 呼叫 Ollama (llama3.2) 進行專有名詞修潤中...")
    corrected_text = _call_ollama(prompt_text, raw_transcript, output_path)
    print(f"▶ 修潤完成，已備份修正版逐字稿至: {output_path}")
    
    return corrected_text

def generate_meeting_summary(corrected_transcript: str, prompt_file: str, output_path: str) -> str:
    """階段三：依據整理好的逐字稿生成會議摘要"""
    print(f"▶ 讀取外部 Prompt 檔案: {prompt_file}")
    with open(prompt_file, 'r', encoding='utf-8') as f:
        prompt_text = f.read()
        
    print(f"▶ 呼叫 Ollama (llama3.2) 生成結構化摘要中...")
    summary_text = _call_ollama(prompt_text, corrected_transcript, output_path)
    print(f"▶ 摘要生成完成，已備份摘要至: {output_path}")
    
    return summary_text
