# Enterprise AI Output Evaluator

The last line of defense for automated AI Agents, transforming "black-box outputs" into "quantifiable reliability."

Scroll down for Traditional Chinese version / 向下捲動查看繁體中文版本

## 💡 Value Proposition (Why)

In enterprise environments, deploying outputs from Large Language Models (LLMs) or AI Agents directly to production is fraught with risk. Hallucinations, logical breaks, and volatile output quality remain the biggest obstacles to AI adoption.

This project delivers a **highly decoupled, strongly-typed, and fault-tolerant** LLM-as-a-Judge evaluation gateway. We don't just return a score; we leverage a **"Three-Tier Signal Hierarchy"** to precisely diagnose missing dependency data. When facing unknown AI hallucinations, the system provides early warnings and graceful degradation rather than failing silently.

## 🛠 Skill Marketplace

| Skill / Pattern | Core Capability | Key Parameters |
| :--- | :--- | :--- |
| **Automated Gateway** | Ingests callbacks from Agent workflows, executes static checks & dynamic LLM evaluations. | `agent_id`, `prompt`, `response`, `reference_context` |
| **Multi-Model Routing** | Avoids vendor lock-in by dynamically dispatching to the most suitable engine. | `provider` (openai, anthropic, google, local) |
| **Active Retrieval** | Automatically fetches Ground Truth via Vector DB or Web Search when context is missing. | Automatic fallback if `reference_context` is empty |
| **Three-Tier Diagnostics** | Abandons binary Pass/Fail logic. Introduces `Potential` state for risk indication. | `quality.score`, `hallucination_risk.level` |
| **Manual UI Console** | Visual interface for development, supporting one-click model switching and JSON previews. | Access via `/` in browser |



## 🚀 Getting Started (Defensive Setup)

This project strictly adheres to the principle of **"Current Working Directory Independence."** The system binds absolute paths via `config.py` at startup, thoroughly defending against **"Path Dependency Traps"**.

### 1. Requirements
* Python 3.10+
* Isolated virtual environment (Recommended: `venv` or Docker)

### 2. Installation
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```


### 3. Environment Variables (Sensitive Data Isolation)
Duplicate the example file and fill in your API Keys:
```bash
cp .env.example .env
```


### 4. Start Service
```bash
python main.py
```
**Health Check**: Once started, visit `http://127.0.0.1:8000` to access the visual UI console.

## 📂 Project Structure

```text
enterprise-ai-evaluator/
├── main.py           # [Entrypoint] FastAPI routing, Dependency Injection (DI), HTML UI
├── evaluator.py      # [Service] Multi-model strategy, active retrieval, graceful degradation
├── domain.py         # [Domain] Pydantic contracts, fault-tolerant signals, logic centralization
├── config.py         # [Config] Absolute path bindings, env loading, Single Source of Truth
├── requirements.txt  # [Dependencies] Version-locked package list
└── .env              # [Security] Sensitive data (Excluded via .gitignore)
```


---

## 🇹🇼 繁體中文版本 (Traditional Chinese Version)

### 💡 價值主張 (Why)
本專案旨在提供一個高度解耦、強型別且具備容錯機制的 LLM-as-a-Judge 評估閘道。我們透過「三級信號階層 (Three-Tier Signal)」精確診斷缺失的依賴數據，讓系統在面對未知的 AI 幻覺時，能夠做到預警與優雅降級。

### 🚀 防禦性起步 (Getting Started)
本專案嚴格遵守「執行目錄無關性」原則。系統啟動時已透過 `config.py` 綁定絕對路徑，徹底防禦「路徑依賴陷阱 (Path Dependency Traps)」。

### 📂 物理結構 (Project Structure)
```text
enterprise-ai-evaluator/
├── main.py           # [入口層] FastAPI 路由、依賴注入 (DI) 與 HTML UI 渲染
├── evaluator.py      # [服務層] 多模型策略路由、主動檢索擴充、優雅降級機制
├── domain.py         # [領域層] Pydantic 數據合約、容錯信號模型與邏輯收斂
├── config.py         # [配置層] 絕對路徑綁定、環境變數載入與單一來源原則
├── requirements.txt  # [依賴庫] 版本鎖定的套件清單
└── .env              # [安全層] 敏感資訊 (已被 .gitignore 排除)
```


### 🧠 設計哲學 (Philosophy)
* **邏輯收斂原則**：嚴禁在 API 路由或 UI 層撰寫判斷邏輯。所有狀態判定必須收斂於 `domain.py` 中的 Model。
* **三級信號階層**：評估結果分為 `Confirmed`、`Potential` 與 `Insufficient Data`，確保診斷回饋透明。
* **多模型策略解耦**：透過 Strategy Pattern 隔離對單一 LLM 供應商的依賴。
* **結構化可觀察性**：核心邏輯全域禁用 `print()`，採用 `structlog` 紀錄 JSON 日誌。
