from fastapi import APIRouter, Depends, Query
from typing import Optional
from datetime import date

from ..controllers.lottery_controller import LotteryController
from ..models.lottery import LotteryCheckRequest, APIResponse

# import the validor validate api key
from app.core import validate_api_key
from fastapi import Depends
from fastapi_limiter.depends import RateLimiter  # <-- import rate limiter

# Create router
# router = APIRouter(prefix="/th/v1/lottery", tags=["Thailand Lottery"])

# lucas -- to secure protect all route
router = APIRouter(
    prefix="/th/v1/lottery",
    tags=["Thailand Lottery"],
    # Remove global dependencies to inject client_name explicitly per route
    # dependencies=[Depends(validate_api_key)]
)


# Dependency to get controller
def get_lottery_controller() -> LotteryController:
    return LotteryController()


def format_response(data, client_name, success=True, message=None):
    response = {
        "success": success,
        "client": client_name,
        "data": data,
    }
    if message:
        response["message"] = message
    return response


@router.get("/draws", response_model=APIResponse, summary="Get All Lottery Draws", dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_all_lottery_draws(
    page: int = Query(1, ge=1, description="Page number", example=1),
    size: int = Query(50, ge=1, le=100,
                      description="Items per page (max 100)", example=10),
    # <--- explicitly add this to determine who the client request is
    client_name: str = Depends(validate_api_key),
    controller: LotteryController = Depends(get_lottery_controller)
):
    """Get all lottery draws with pagination support."""
    return await controller.get_all_lottery_draws(page=page, size=size, client_name=client_name)

@router.get("/draws/latest", response_model=APIResponse, summary="Get Latest Lottery Draw", dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_latest_lottery_draw(
    client_name: str = Depends(validate_api_key),
    controller: LotteryController = Depends(get_lottery_controller)
):
    """Get the most recent lottery draw results."""
    return await controller.get_latest_lottery_draw(client_name=client_name)


@router.get("/draws/{draw_date}", response_model=APIResponse, summary="Get Lottery Draw by Date", dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_lottery_draw_by_date(
    draw_date: date,
    client_name: str = Depends(validate_api_key),
    controller: LotteryController = Depends(get_lottery_controller)
):
    """Get lottery draw results for a specific date (YYYY-MM-DD format)."""
    return await controller.get_lottery_draw_by_date(draw_date, client_name=client_name)


@router.post("/check", response_model=APIResponse, summary="Check Lottery Numbers", dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def check_lottery_numbers(
    request: LotteryCheckRequest,
    client_name: str = Depends(validate_api_key),
    controller: LotteryController = Depends(get_lottery_controller)
):
    """
    Check lottery numbers for winnings.

    Submit 1-10 lottery numbers to check against historical draws.
    Optionally specify a date to check against a specific draw only.
    """
    return await controller.check_lottery_numbers(request, client_name=client_name)


@router.get("/search", response_model=APIResponse, summary="Search Lottery Draws", dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def search_lottery_draws(
    start_date: Optional[date] = Query(
        None, description="Start date (YYYY-MM-DD)", example="2024-01-01"),
    end_date: Optional[date] = Query(
        None, description="End date (YYYY-MM-DD)", example="2024-12-31"),
    page: int = Query(1, ge=1, description="Page number", example=1),
    size: int = Query(50, ge=1, le=100,
                      description="Items per page (max 100)", example=20),
    client_name: str = Depends(validate_api_key),
    controller: LotteryController = Depends(get_lottery_controller)
):
    """Search lottery draws with optional date range filters."""
    return await controller.search_lottery_draws(
        start_date=start_date,
        end_date=end_date,
        page=page,
        size=size,
        client_name=client_name
    )
