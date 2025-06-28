from fastapi import APIRouter, Depends, Query
from typing import Optional
from datetime import date

from ..controllers.lottery_controller import LotteryController
from ..models.lottery import LotteryCheckRequest, APIResponse

# Create router
router = APIRouter(prefix="/th/v1/lottery", tags=["Thailand Lottery"])

# Dependency to get controller
def get_lottery_controller() -> LotteryController:
    return LotteryController()

@router.get("/draws", response_model=APIResponse, summary="Get All Lottery Draws")
async def get_all_lottery_draws(
    page: int = Query(1, ge=1, description="Page number", example=1),
    size: int = Query(50, ge=1, le=100, description="Items per page (max 100)", example=10),
    controller: LotteryController = Depends(get_lottery_controller)
):
    """Get all lottery draws with pagination support."""
    return await controller.get_all_lottery_draws(page=page, size=size)

@router.get("/draws/latest", response_model=APIResponse, summary="Get Latest Lottery Draw")
async def get_latest_lottery_draw(
    controller: LotteryController = Depends(get_lottery_controller)
):
    """Get the most recent lottery draw results."""
    return await controller.get_latest_lottery_draw()

@router.get("/draws/{draw_date}", response_model=APIResponse, summary="Get Lottery Draw by Date")
async def get_lottery_draw_by_date(
    draw_date: date,
    controller: LotteryController = Depends(get_lottery_controller)
):
    """Get lottery draw results for a specific date (YYYY-MM-DD format)."""
    return await controller.get_lottery_draw_by_date(draw_date)

@router.post("/check", response_model=APIResponse, summary="Check Lottery Numbers")
async def check_lottery_numbers(
    request: LotteryCheckRequest,
    controller: LotteryController = Depends(get_lottery_controller)
):
    """
    Check lottery numbers for winnings.
    
    Submit 1-10 lottery numbers to check against historical draws.
    Optionally specify a date to check against a specific draw only.
    """
    return await controller.check_lottery_numbers(request)

@router.get("/search", response_model=APIResponse, summary="Search Lottery Draws")
async def search_lottery_draws(
    start_date: Optional[date] = Query(None, description="Start date (YYYY-MM-DD)", example="2024-01-01"),
    end_date: Optional[date] = Query(None, description="End date (YYYY-MM-DD)", example="2024-12-31"),
    page: int = Query(1, ge=1, description="Page number", example=1),
    size: int = Query(50, ge=1, le=100, description="Items per page (max 100)", example=20),
    controller: LotteryController = Depends(get_lottery_controller)
):
    """Search lottery draws with optional date range filters."""
    return await controller.search_lottery_draws(
        start_date=start_date,
        end_date=end_date,
        page=page,
        size=size
    ) 