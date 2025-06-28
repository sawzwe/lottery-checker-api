from pydantic import BaseModel, Field
from typing import List, Optional, Union
from datetime import date

class LotteryDrawBase(BaseModel):
    """Base lottery draw model"""
    date: date
    prize_1st: str
    prize_pre_3digit: List[str] = Field(default_factory=list)
    prize_sub_3digits: List[str] = Field(default_factory=list)
    prize_2digits: Optional[int] = None
    nearby_1st: List[str] = Field(default_factory=list)
    prize_2nd: List[str] = Field(default_factory=list)
    prize_3rd: List[str] = Field(default_factory=list)
    prize_4th: List[str] = Field(default_factory=list)
    prize_5th: List[str] = Field(default_factory=list)

class LotteryDraw(LotteryDrawBase):
    """Complete lottery draw model with ID"""
    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True

class LotteryCheckRequest(BaseModel):
    """Request model for checking lottery numbers"""
    numbers: List[str] = Field(..., min_items=1, max_items=10, description="List of lottery numbers to check")
    date: Union[str, None] = None

class LotteryCheckResult(BaseModel):
    """Result of lottery number checking"""
    number: str
    date: date
    prize_type: Optional[str] = None
    prize_amount: Optional[int] = None
    matched: bool = False

class LotteryCheckResponse(BaseModel):
    """Response for lottery checking"""
    results: List[LotteryCheckResult]
    total_winnings: int = 0
    checked_count: int = 0
    winning_count: int = 0

class APIResponse(BaseModel):
    """Standard API response wrapper"""
    success: bool = True
    message: str = "OK"
    data: Optional[dict] = None
    error: Optional[str] = None

class PaginatedResponse(BaseModel):
    """Paginated response model"""
    items: List[LotteryDraw]
    total: int
    page: int
    size: int
    pages: int 