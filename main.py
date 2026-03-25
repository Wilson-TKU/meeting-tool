import os
from src.module_whisper import process_audio_to_transcript
from src.module_llm import fix_domain_terms, generate_meeting_summary

def main():
    print("==============================================")
    print("      Meeting Tool Pipeline 啟動程序          ")
    print("==============================================\n")
    
    # 決定基礎資料夾路徑 (避免因執行路徑不同出錯)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    PROMPT_DIR = os.path.join(BASE_DIR, 'prompts')
    
    # 定義 I/O 操作路徑
    audio_input_path = os.path.join(DATA_DIR, 'input.mp3')
    raw_transcript_path = os.path.join(DATA_DIR, '1_raw_transcript.txt')
    corrected_transcript_path = os.path.join(DATA_DIR, '2_corrected_transcript.txt')
    summary_path = os.path.join(DATA_DIR, '3_final_summary.txt')
    
    correction_prompt_path = os.path.join(PROMPT_DIR, 'correction_prompt.txt')
    summary_prompt_path = os.path.join(PROMPT_DIR, 'summary_prompt.txt')

    # 防呆檢查：確認 prompt 檔案都在
    if not os.path.exists(correction_prompt_path) or not os.path.exists(summary_prompt_path):
        print("❌ 錯誤：找不到 Prompt 檔案！請確保 prompts/ 資料夾底下有準備好 txt 檔案。")
        return

    # [階段 1]
    print("\n--- [階段 1] 音檔轉原始逐字稿 (Whisper) ---")
    raw_transcript = process_audio_to_transcript(
        audio_path=audio_input_path, 
        output_path=raw_transcript_path
    )
    
    # [階段 2]
    print("\n--- [階段 2] 逐字稿專有名詞與錯字修正 (Ollama) ---")
    corrected_transcript = fix_domain_terms(
        raw_transcript=raw_transcript, 
        prompt_file=correction_prompt_path, 
        output_path=corrected_transcript_path
    )
    
    # [階段 3]
    print("\n--- [階段 3] 會議摘要分析與整理 (Ollama) ---")
    final_summary = generate_meeting_summary(
        corrected_transcript=corrected_transcript, 
        prompt_file=summary_prompt_path, 
        output_path=summary_path
    )
    
    # 終端輸出，方便觀看最終結果
    print("\n\n================ 最終會議摘要 ================\n")
    print(final_summary)
    print("\n==============================================")
    print("✅ Pipeline 全面執行完畢！")
    print("各階段的中間產物 txt 都已經儲存在 data/ 資料夾中供查詢與除錯。")

if __name__ == "__main__":
    main()
