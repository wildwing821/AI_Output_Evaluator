Enterprise AI Output Evaluator

The last line of defense for automated AI Agents, transforming "black-box outputs" into "quantifiable reliability."

Scroll down for Traditional Chinese version / 向下捲動查看繁體中文版本

💡 Value Proposition (Why)

In enterprise environments, deploying outputs from Large Language Models (LLMs) or AI Agents (like OpenClaw, Codex) directly to production is fraught with risk. Hallucinations, logical breaks, and volatile output quality remain the biggest obstacles to AI adoption.

This project delivers a highly decoupled, strongly-typed, and fault-tolerant LLM-as-a-Judge evaluation gateway. We don't just return a score; we leverage a "Three-Tier Signal Hierarchy" to precisely diagnose missing dependency data. When facing unknown AI hallucinations, the system provides early warnings and graceful degradation rather than failing silently.

🛠 Skill Marketplace

This system provides multi-dimensional detection capabilities for AI outputs, supporting flexible integration patterns:

Skill / Pattern

Core Capability

Key Parameters

Automated Gateway (API Webhook)

Ingests callbacks from Agent workflows, executes static checks & dynamic LLM evaluations, and returns structured diagnostic reports.

agent_id, prompt, response, reference_context

Multi-Model Dynamic Routing

Avoids vendor lock-in by dynamically dispatching to the most suitable evaluation engine based on privacy needs or complexity.

provider (openai, anthropic, google, local)

Active Retrieval (Auto Context)

Automatically fetches Ground Truth via Vector DB (RAG) or Web Search when context is missing, enhancing evaluation accuracy.

Automatic fallback if reference_context is empty

Three-Tier Diagnostics

Abandons binary Pass/Fail logic. Introduces a Potential state to precisely indicate risks caused by a "missing baseline context."

quality.score, hallucination_risk.level, missing_data

Manual UI Console

Visual interface for development/debugging, supporting one-click model switching, JSON data contract previews, and status tagging.

None (Access via / in browser)

🚀 Getting Started (Defensive Setup)

This project strictly adheres to the principle of "Current Working Directory Independence." The system binds absolute paths via config.py at startup, thoroughly defending against "Path Dependency Traps."

1. Requirements

Python 3.10+

Isolated virtual environment (Recommended: venv or Docker containerization)

2. Installation

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt


3. Environment Variables (Sensitive Data Isolation)

Duplicate the example file and fill in the corresponding API Keys based on your model selection:

cp .env.example .env


Edit the .env file:

OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-...
GOOGLE_API_KEY=AIza...
EVALUATOR_PROVIDER=openai  # Default evaluation engine


4. Start Service

python main.py


Health Check: Once started, visit http://127.0.0.1:8000 to access the visual UI console, or send a POST request to http://127.0.0.1:8000/api/v1/evaluate.

📂 Project Structure

The project adopts a streamlined Domain-Driven Design (DDD) and layered architecture, strictly adhering to the Single Responsibility Principle (SRP).

enterprise-ai-evaluator/
├── main.py           # [Entrypoint] FastAPI routing, Dependency Injection (DI), HTML UI
├── evaluator.py      # [Service] Multi-model strategy, active retrieval, graceful degradation
├── domain.py         # [Domain] Pydantic contracts, fault-tolerant signals, logic centralization
├── config.py         # [Config] Absolute path bindings, env loading, Single Source of Truth
├── requirements.txt  # [Dependencies] Version-locked package list
└── .env              # [Security] Sensitive data (Excluded via .gitignore)


🧠 Design Philosophy

Logic Centralization
Strictly prohibits derivative logic like if score > 7 in API routes or UI layers. All state determinations (e.g., is_pass) must converge in the Model (@computed_field) within domain.py, treating the Model as the sole data contract.

Three-Tier Signal Hierarchy
The system does not use ambiguous booleans to judge hallucinations. Evaluation results are categorized into: Confirmed (clear signal), Potential (partial data missing, e.g., no reference context), and Insufficient Data (core data missing, evaluation halted), ensuring transparent and defensive diagnostics.

Vendor Decoupling
Isolates dependencies on single LLM providers via the Strategy Pattern. Callers can seamlessly switch between OpenAI, Claude, Google, or local open-source models simply by passing the provider parameter, ensuring enterprise data security and architectural elasticity.

Structured Observability
print() is globally disabled for core logic. We utilize structlog to record JSON logs containing the agent_id and execution context, ensuring no debugging clues are lost in Distributed Tracing.

🇹🇼 繁體中文版本 (Traditional Chinese Version)

Enterprise AI Output Evaluator (企業級 AI 輸出評估引擎)

為自動化 AI Agent 打造的最後一道防線，將「黑盒輸出」轉化為「可量化的信賴度」。

💡 價值主張 (Why)

在企業級環境中，將大語言模型 (LLM) 或 AI Agent（如 OpenClaw, Codex）的輸出直接應用於生產環境充滿風險。幻覺 (Hallucinations)、邏輯斷層與不穩定的輸出品質，是阻礙 AI 落地的最大挑戰。

本專案旨在提供一個高度解耦、強型別且具備容錯機制的 LLM-as-a-Judge 評估閘道。我們不只是給出一個分數，而是透過「三級信號階層 (Three-Tier Signal)」精確診斷缺失的依賴數據，讓系統在面對未知的 AI 幻覺時，能夠做到預警與優雅降級，而非無聲崩潰。

🛠 技能矩陣 (Skill Marketplace)

本系統提供針對 AI 輸出的多維度檢測能力，並支援靈活的介接模式：

技能模式

核心能力

關鍵參數

自動化閘道 (API Webhook)

接收 Agent 工作流的回傳，執行靜態檢查與動態 LLM 評估，並回傳結構化診斷報告。

agent_id, prompt, response, reference_context

多模型動態路由 (Multi-Model)

避免供應商鎖定，依據任務隱私需求或複雜度，動態調度最適合的評估引擎。

provider (openai, anthropic, google, local)

主動檢索 (Active Retrieval)

當缺乏參考依據時，自動觸發內部知識庫 (RAG) 或網路搜尋，補齊幻覺檢測的拼圖。

若 reference_context 為空自動觸發

容錯式階層診斷 (Three-Tier Diagnostics)

放棄二元對立的 Pass/Fail，引入 Potential 狀態，精確指出因「缺少基準上下文」造成的潛在風險。

quality.score, hallucination_risk.level, missing_data

手動審查中控台 (UI Console)

開發與除錯階段的視覺化介面，支援一鍵切換模型、預覽 JSON 數據合約與狀態標籤。

無 (透過瀏覽器訪問 / 即可)

🚀 防禦性起步 (Getting Started)

本專案嚴格遵守「執行目錄無關性」原則。系統啟動時已透過 config.py 綁定絕對路徑，徹底防禦「路徑依賴陷阱 (Path Dependency Traps)」，確保無論在哪個資料夾下執行，皆不會產生路徑偏移錯誤。

1. 環境要求

Python 3.10+

隔離的虛擬環境 (建議使用 venv 或 Docker 容器化)

2. 安裝依賴

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt


3. 環境變數配置 (敏感資訊隔離)

請複製範本檔案，並根據您的模型選擇填入對應的 API Keys：

cp .env.example .env


編輯 .env 檔案：

OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-...
GOOGLE_API_KEY=AIza...
EVALUATOR_PROVIDER=openai  # 預設評估引擎


4. 啟動服務

python main.py


Health Check: 服務啟動後，請訪問 http://127.0.0.1:8000 進入視覺化中控台，或向 http://127.0.0.1:8000/api/v1/evaluate 發送 POST 請求。

📂 物理結構 (Project Structure)

專案採用精簡版的領域驅動設計 (DDD) 與分層架構，嚴格遵守單一職責原則 (SRP)。

enterprise-ai-evaluator/
├── main.py           # [入口層] FastAPI 路由、依賴注入 (DI) 與 HTML UI 渲染
├── evaluator.py      # [服務層] 多模型策略路由、主動檢索擴充、優雅降級機制
├── domain.py         # [領域層] Pydantic 數據合約、容錯信號模型與邏輯收斂
├── config.py         # [配置層] 絕對路徑綁定、環境變數載入與單一來源原則
├── requirements.txt  # [依賴庫] 版本鎖定的套件清單
└── .env              # [安全層] 敏感資訊 (已被 .gitignore 排除)


🧠 設計哲學 (Philosophy)

邏輯收斂原則 (Logic Centralization)
嚴禁在 API 路由或 UI 層撰寫如 if score > 7 的衍生判斷。所有狀態判定（如 is_pass）必須收斂於 domain.py 中的 Model (@computed_field)，視 Model 為唯一的數據合約。

三級信號階層 (Three-Tier Signal Hierarchy)
系統不使用模糊的布林值判斷幻覺。評估結果分為：Confirmed (信號明確)、Potential (部分數據缺失，如無參考上下文) 以及 Insufficient Data (核心數據缺失，終止評估)，確保診斷回饋透明且具防禦性。

多模型策略解耦 (Vendor Decoupling)
透過策略模式 (Strategy Pattern) 隔離對單一 LLM 供應商的依賴。外部調用方只需透過 provider 參數，即可無縫切換 OpenAI、Claude、Google 或本地開源模型，保障企業數據安全與架構彈性。

結構化可觀察性 (Structured Observability)
核心邏輯全域禁用 print()，採用 structlog 記錄帶有 agent_id 與執行上下文的 JSON 日誌，確保在分散式追蹤 (Distributed Tracing) 中不會遺失任何除錯線索。