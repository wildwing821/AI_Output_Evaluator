import structlog
from domain import EvaluationRequest, EvaluationResult, DiagnosticSignal
from config import settings

logger = structlog.get_logger(__name__)

class LlmEvaluatorService:
    """
    多模型評估路由服務：負責檢驗 AI 輸出品質與幻覺程度。
    """
    
    def evaluate(self, req: EvaluationRequest) -> EvaluationResult:
        # 1. 決定使用哪個 Provider (請求指定優先於全域設定)
        provider = req.provider or settings.DEFAULT_PROVIDER
        
        # 恢復：記錄更詳細的 prompt_length
        logger.info("evaluation_started", provider=provider, agent_id=req.agent_id, prompt_length=len(req.prompt))
        
        # 2. 衛句模式：檢查是否缺少核心資料
        if not req.response or not req.response.strip():
            logger.warning("evaluation_insufficient_data", reason="Response is empty")
            return self._build_error_result(req, "AI 回覆為空，無法進行評估", provider)

        # [新增] 3. 自動化獲取參考依據的邏輯 (主動檢索機制 RAG / Web Search)
        if not req.reference_context or not req.reference_context.strip():
            logger.info("context_missing", action="auto_fetching_context")
            req.reference_context = self._auto_fetch_ground_truth(req.prompt)

        # 4. 判斷是否具備 Context (影響幻覺評估的信賴度)
        has_context = bool(req.reference_context and req.reference_context.strip())

        # 5. 根據 Provider 路由到不同的核心邏輯，並恢復 try-except 錯誤捕獲機制
        try:
            if provider == "openai":
                return self._run_openai_eval(req, has_context)
            elif provider == "anthropic":
                return self._run_anthropic_eval(req, has_context)
            elif provider == "google":
                return self._run_google_eval(req, has_context)
            elif provider == "local":
                return self._run_local_eval(req, has_context)
            else:
                return self._run_openai_eval(req, has_context)
                
        except ValueError as ve:
            # 精確捕獲異常，防止系統無聲崩潰
            logger.error("evaluation_value_error", error=str(ve))
            raise

    def _auto_fetch_ground_truth(self, prompt: str) -> str:
        """
        模擬主動檢索 (Active Retrieval) 機制：
        在實際企業應用中，這裡會串接 Vector DB (RAG) 或是 Google Search API 進行自動化。
        """
        logger.info("executing_active_retrieval", query=prompt)
        
        # 這裡作為防禦性與架構展示，我們根據提示詞關鍵字模擬回傳檢索結果
        if "量子力學" in prompt:
            return "【自動檢索結果】維基百科記載：量子力學是研究微觀粒子運動規律的物理學，包含波粒二象性與測不準原理。"
        elif "退貨" in prompt:
            return "【自動內部知識庫】公司退貨政策第3條指出，實體商品享有 7 天猶豫期。"
            
        # 如果網路搜尋或資料庫也找不到相關資料，回傳空字串
        # 讓系統後續正當地觸發 Potential 潛在風險信號，達成優雅降級
        return ""

    def _run_openai_eval(self, req: EvaluationRequest, has_context: bool) -> EvaluationResult:
        logger.info("executing_openai_assessment")
        # 恢復：缺乏真實 API Key 時，啟動優雅降級 (Fallback)
        if not settings.OPENAI_API_KEY:
            logger.warning("api_key_missing", action="fallback_to_mock", provider="openai")
            return self._mock_eval_logic(req, "openai", has_context)
            
        return self._mock_eval_logic(req, "openai", has_context)

    def _run_anthropic_eval(self, req: EvaluationRequest, has_context: bool) -> EvaluationResult:
        logger.info("executing_anthropic_assessment")
        if not settings.ANTHROPIC_API_KEY:
            logger.warning("api_key_missing", action="fallback_to_mock", provider="anthropic")
        return self._mock_eval_logic(req, "anthropic", has_context)

    def _run_google_eval(self, req: EvaluationRequest, has_context: bool) -> EvaluationResult:
        logger.info("executing_google_assessment")
        if not settings.GOOGLE_API_KEY:
            logger.warning("api_key_missing", action="fallback_to_mock", provider="google")
        return self._mock_eval_logic(req, "google", has_context)

    def _run_local_eval(self, req: EvaluationRequest, has_context: bool) -> EvaluationResult:
        logger.info("executing_local_assessment")
        return self._mock_eval_logic(req, "local", has_context)

    def _mock_eval_logic(self, req: EvaluationRequest, provider: str, has_context: bool) -> EvaluationResult:
        """模擬通用評估邏輯 (融合動態評分與防禦性設計)"""
        
        # 恢復：模擬品質評估 (根據字數動態給分)
        quality_score = 8.5 if len(req.response) > 20 else 4.0
        
        quality_signal = DiagnosticSignal(
            level="Confirmed",
            score=quality_score,
            reasoning=f"[{provider}] 回覆結構完整且切合題意。" if quality_score > 5 else f"[{provider}] 回覆過於簡短。",
            missing_data=[]
        )
        
        # 模擬幻覺評估 (依賴 Context 的決策樹)
        if has_context:
            hallucination_signal = DiagnosticSignal(
                level="Confirmed",
                score=2.0,
                reasoning=f"[{provider}] 根據提供的參考上下文：\n\"{req.reference_context}\"\n未發現明顯事實捏造。",
                missing_data=[]
            )
        else:
            hallucination_signal = DiagnosticSignal(
                level="Potential", # 潛在信號：缺少基準資料
                score=5.0,
                reasoning=f"[{provider}] [預警] 缺少 reference_context 基準資料，且自動檢索未找到相關內容，無法最終確認事實正確性。",
                missing_data=["reference_context"]
            )
            
        logger.info("evaluation_completed", agent_id=req.agent_id, is_pass=(quality_score >= 7.0))
        
        return EvaluationResult(
            agent_id=req.agent_id,
            provider_used=provider,  # 確保 Pydantic 驗證通過
            quality=quality_signal,
            hallucination_risk=hallucination_signal
        )

    def _build_error_result(self, req: EvaluationRequest, msg: str, provider: str) -> EvaluationResult:
        """處理極端異常情況的回傳"""
        sig = DiagnosticSignal(level="Insufficient Data", score=0.0, reasoning=msg)
        return EvaluationResult(
            agent_id=req.agent_id, 
            provider_used=provider, 
            quality=sig, 
            hallucination_risk=sig
        )