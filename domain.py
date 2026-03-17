from pydantic import BaseModel, Field, computed_field
from typing import Optional, List, Literal
from datetime import datetime
import uuid

class EvaluationRequest(BaseModel):
    """外部輸入的強型別介面合約 - 支援多模型選擇"""
    agent_id: str = Field(..., description="來源 Agent (例如: claude-3-opus, openclaw-v1)")
    prompt: str = Field(..., description="使用者的原始提示詞")
    response: str = Field(..., description="AI 產生的回覆內容")
    reference_context: Optional[str] = Field(None, description="可選：用於檢驗幻覺的 Ground Truth 或參考文件")
    # 新增模型供應商選項
    provider: Optional[Literal["openai", "anthropic", "google", "local"]] = Field(None, description="指定評估引擎")

class DiagnosticSignal(BaseModel):
    """三級信號階層"""
    level: Literal["Confirmed", "Potential", "Insufficient Data"] = Field(..., description="信號可靠度")
    score: float = Field(default=0.0, description="評估分數 (0-10)")
    reasoning: str = Field(..., description="評估理由與診斷資訊")
    missing_data: List[str] = Field(default_factory=list, description="缺失的依賴數據名")


class EvaluationResult(BaseModel):
    """最終數據合約"""
    evaluation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    agent_id: str
    provider_used: str # 記錄本次評估使用的模型
    quality: DiagnosticSignal
    hallucination_risk: DiagnosticSignal
    
    @computed_field
    def is_pass(self) -> bool:
        if self.quality.level == "Insufficient Data" or self.hallucination_risk.level == "Insufficient Data":
            return False
            
        # 品質及格且幻覺風險低
        return self.quality.score >= 7.0 and self.hallucination_risk.score <= 3.0