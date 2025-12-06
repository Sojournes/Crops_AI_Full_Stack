from pydantic import BaseModel
from typing import List, Optional, Any

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[dict]] = [] # List of {"role": "user"|"model", "parts": [...]}

class ChatResponse(BaseModel):
    response: str
    history: List[dict]

class PlotDataPoint(BaseModel):
    name: str # e.g., product name or crop type
    value: float # e.g., price or demand index
    category: Optional[str] = None

class VisualDataResponse(BaseModel):
    title: str
    data: List[PlotDataPoint]
    xLabel: str
    yLabel: str
