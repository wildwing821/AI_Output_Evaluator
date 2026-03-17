from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
import structlog

from config import settings
from domain import EvaluationRequest, EvaluationResult
from evaluator import LlmEvaluatorService

# 結構化日誌初始化
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ]
)
logger = structlog.get_logger(__name__)

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

# --- 依賴注入 (DI) ---
def get_evaluator() -> LlmEvaluatorService:
    return LlmEvaluatorService()

# --- API 端點 (支援 Agent 自動化串接) ---
@app.post("/api/v1/evaluate", response_model=EvaluationResult)
async def evaluate_agent_output(
    request: EvaluationRequest,
    evaluator: LlmEvaluatorService = Depends(get_evaluator)
):
    """
    接收來自 AI Agent (如 OpenClaw, Codex) 的輸出並進行自動化評估。
    """
    try:
        result = evaluator.evaluate(request)
        return result
    except Exception as e:
        logger.error("api_evaluation_failed", error=str(e), exc_info=True)
        # 優雅降級：回傳清晰錯誤而非崩潰
        raise HTTPException(status_code=500, detail="評估引擎內部錯誤，請聯繫管理員。")

# --- UI 端點 (支援手動操作與切換) ---
@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    """
    提供輕量級的 HTML UI，實作「手動輸入」與「自動化 API 指南」的切換。
    （在實際企業專案中，這裡通常會分離為獨立的 React/Vue 專案或 Streamlit）
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <title>AI 輸出評估控制台 v1.1</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f7fa; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; }
            .tabs { margin-bottom: 20px; border-bottom: 2px solid #e2e8f0; }
            .tab-btn { padding: 10px 20px; border: none; background: none; cursor: pointer; font-size: 16px; color: #718096; }
            .tab-btn.active { color: #3182ce; border-bottom: 2px solid #3182ce; margin-bottom: -2px; font-weight: bold; }
            .panel { display: none; }
            .panel.active { display: block; }
            label { display: block; margin-top: 15px; font-weight: bold; color: #4a5568; }
            input, textarea, select { width: 100%; padding: 10px; margin-top: 5px; border: 1px solid #cbd5e0; border-radius: 4px; box-sizing: border-box; }
            button.submit { margin-top: 20px; background-color: #3182ce; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
            button.submit:hover { background-color: #2b6cb0; }
            pre { background: #edf2f7; padding: 15px; border-radius: 4px; overflow-x: auto; }
            .tag { display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
            .tag.pass { background-color: #c6f6d5; color: #22543d; }
            .tag.fail { background-color: #fed7d7; color: #822727; }
            .tag.potential { background-color: #feebc8; color: #7b341e; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🛡️ AI 輸出品質與幻覺評估引擎 (多模型版)</h1>
            
            <div class="tabs">
                <button class="tab-btn active" onclick="switchTab('manual')">手動評估 (Manual Mode)</button>
                <button class="tab-btn" onclick="switchTab('api')">Agent 自動化串接 (API Mode)</button>
            </div>

            <!-- 手動評估面板 -->
            <div id="manual" class="panel active">
                <p>手動貼上 AI 模型的輸出以進行品質與幻覺度檢驗。</p>
                
                <label>選擇評估引擎 (Evaluator Provider)</label>
                <select id="provider">
                    <option value="openai">OpenAI (GPT-4o)</option>
                    <option value="anthropic">Anthropic (Claude 3.5)</option>
                    <option value="google">Google (Gemini 1.5)</option>
                    <option value="local">Local (Llama 3 / Ollama)</option>
                </select>

                <label>Agent 名稱 (Model)</label>
                <input type="text" id="agentId" value="manual-test-agent">
                
                <label>原始提示詞 (Prompt)</label>
                <textarea id="prompt" rows="3">請解釋量子力學的基本原理。</textarea>
                
                <label>AI 回覆 (Response)</label>
                <textarea id="response" rows="5">量子力學是描述微觀物體運動規律的物理學分支，其核心包含波粒二象性與測不準原理。</textarea>
                
                <label>參考依據 (Ground Truth / Context - 可留空)</label>
                <textarea id="context" rows="3" placeholder="若留空，幻覺檢驗將處於 'Potential' 潛在信號狀態..."></textarea>
                
                <button class="submit" onclick="runEvaluation()">執行多模型評估 (Run Eval)</button>
                
                <div id="result" style="margin-top: 30px; display: none;">
                    <h3>📊 評估結果</h3>
                    <div id="resultStatus" style="margin-bottom: 10px;"></div>
                    <pre id="resultJson"></pre>
                </div>
            </div>

            <!-- API 串接面板 -->
            <div id="api" class="panel">
                <h3>🚀 如何讓 OpenClaw / Codex 自動串接？</h3>
                <p>在你的 Agent 工作流中，配置以下 Webhook URL：</p>
                <pre>POST http://localhost:8000/api/v1/evaluate</pre>
                <label>Payload (JSON)</label>
                <pre>{
  "agent_id": "openclaw-agent-v2",
  "provider": "openai",
  "prompt": "生成一段 Python 爬蟲",
  "response": "import requests...",
  "reference_context": "需使用 requests 與 BeautifulSoup"
}</pre>
                <p>系統將自動返回評估分數與缺失數據報告。</p>
            </div>
        </div>

        <script>
            function switchTab(tabId) {
                document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
                document.querySelectorAll('.panel').forEach(panel => panel.classList.remove('active'));
                event.target.classList.add('active');
                document.getElementById(tabId).classList.add('active');
            }

            async function runEvaluation() {
                const btn = document.querySelector('.submit');
                btn.textContent = "評估中...";
                btn.disabled = true;

                const payload = {
                    agent_id: document.getElementById('agentId').value,
                    prompt: document.getElementById('prompt').value,
                    response: document.getElementById('response').value,
                    reference_context: document.getElementById('context').value,
                    provider: document.getElementById('provider').value
                };

                try {
                    const response = await fetch('/api/v1/evaluate', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(payload)
                    });
                    
                    const data = await response.json();
                    
                    document.getElementById('result').style.display = 'block';
                    document.getElementById('resultJson').textContent = JSON.stringify(data, null, 2);
                    
                    const statusDiv = document.getElementById('resultStatus');
                    if (data.is_pass) {
                        statusDiv.innerHTML = '<span class="tag pass">✅ 評估通過 (Pass)</span>';
                    } else if (data.hallucination_risk && data.hallucination_risk.level === 'Potential') {
                        statusDiv.innerHTML = '<span class="tag potential">⚠️ 潛在風險 (Missing Context)</span>';
                    } else {
                        statusDiv.innerHTML = '<span class="tag fail">❌ 評估不通過 (Fail)</span>';
                    }
                } catch (error) {
                    alert("請求失敗: " + error);
                } finally {
                    btn.textContent = "執行多模型評估 (Run Eval)";
                    btn.disabled = false;
                }
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    # 開發環境下啟動：python main.py
    print("\n" + "="*50)
    print("💡 開發者專用 UI 介面：http://127.0.0.1:8000")
    print("="*50 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)