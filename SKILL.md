---
name: Meeting Tool Pipeline
description: Instructions and architectural context for standard development and modification of the Meeting Tool pipeline.
---

# Meeting Tool 專案開發指南 (Agent 專用技能)

本專案將「會議音檔」自動循序漸進轉換為「會議摘要」。專案設計非常重視**模組化**與**Prompt分離**，讓非工程背景人員也能輕鬆調整 AI 行為。
當未來的 AI (Agent) 被喚醒來修改此專案時，請務必遵循以下的架構原則。

## 系統核心架構 (Pipeline)

所有流程都由 `main.py` 負責指揮串接，分為三個階段：

1. **階段一：音檔轉原始逐字稿 (Whisper)**
   - **負責模組**: `src/module_whisper.py`
   - **工作邏輯**: 讀取 `data/input.mp3`，辨識出語音後，產出字串並儲存到 `data/1_raw_transcript.txt`。
   - **目前狀態**: 此模組尚未實作真正的語音辨識指令，目前透過 `dummy_transcript` 模擬假資料回傳。

2. **階段二：逐字稿專有名詞與錯字修正 (LLM)**
   - **負責模組**: `src/module_llm.py` (`fix_domain_terms`)
   - **工作邏輯**: 讀取階段一的字串，並載入外部指令檔案 `prompts/correction_prompt.txt`。將兩者合併發送給本機端背景執行的 Ollama，並將修正好錯字與名詞的結果儲存至 `data/2_corrected_transcript.txt`。

3. **階段三：會議摘要與待辦事項生成 (LLM)**
   - **負責模組**: `src/module_llm.py` (`generate_meeting_summary`)
   - **工作邏輯**: 讀取階段二乾淨的字串，並載入外部指令檔案 `prompts/summary_prompt.txt`。藉由 Ollama 生成最終整理，儲存至 `data/3_final_summary.txt`。

## Agent 維護與修改原則

1. **調整 AI 的行為與輸出格式 (非寫扣)**：
   如果是使用者希望「摘要的格式長得不一樣」或是「AI 常常改錯某個專有名詞」，請**直接去修改 `prompts/` 裡面的 `txt` 檔案**。切記，絕大部分的邏輯微調都不該去動 Python 程式碼。

2. **如何接入真實的語音辨識**：
   未來當你要實作 Whisper 的程式時，請只改動 `src/module_whisper.py`。你可以呼叫外部 CLI，或是在背景跑其他的 Python inference，但最終必須回傳跟原本一模一樣的 `string` 介面字串。

3. **如何更改使用的 LLM**：
   目前預設使用包含 3B 參數的 `llama3.2` 模型 (Google 的 Gemma 3B 我們找用 Meta Llama 3.2 3B 替代品)。若要改為其他模型，請至 `src/module_llm.py` 中的 `_call_ollama()` 函式去修改 `data["model"]` 參數。

4. **除錯指南 (Debugging)**：
   本架構規定每經過一個階段，都必須實體輸出一個備查的 `txt` 到 `data/` 目錄。若生成結果不好，請先去查看：
   * `data/1_raw_transcript.txt`：看是不是聲音本來就沒錄清楚。
   * `data/2_corrected_transcript.txt`：看是不是第二階段錯字沒修好，或把對的字修成了錯字。

## 環境準備

- 需要在背景啟動 Ollama (`http://localhost:11434`)。
- 若 `requests` 套件找不到，請執行 `pip install -r requirements.txt`。
