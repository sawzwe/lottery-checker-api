from fastapi import HTTPException, Query
from typing import List, Optional
from datetime import date

from ..services.lottery_service import LotteryService
from ..models.lottery import (
    LotteryDraw, 
    LotteryCheckRequest, 
    LotteryCheckResponse,
    LotteryCheckResult,
    APIResponse,
    PaginatedResponse
)

class LotteryController:
    """Controller for lottery-related endpoints"""
    
    def __init__(self):
        self.lottery_service = LotteryService()
    
    async def get_all_lottery_draws(
        self, 
        page: int = Query(1, ge=1, description="Page number"),
        size: int = Query(50, ge=1, le=100, description="Items per page")
    ) -> APIResponse:
        """Get all lottery draws with pagination"""
        try:
            result = await self.lottery_service.get_all_draws(page=page, size=size)
            
            return APIResponse(
                success=True,
                message=f"Retrieved {len(result.items)} lottery draws",
                data={
                    "draws": [draw.dict() for draw in result.items],
                    "pagination": {
                        "total": result.total,
                        "page": result.page,
                        "size": result.size,
                        "pages": result.pages
                    }
                }
            )
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving lottery draws: {str(e)}")
    
    async def get_lottery_draw_by_date(self, draw_date: date) -> APIResponse:
        """Get specific lottery draw by date"""
        try:
            draw = await self.lottery_service.get_draw_by_date(draw_date)
            
            if not draw:
                raise HTTPException(
                    status_code=404, 
                    detail=f"No lottery draw found for date {draw_date}"
                )
            
            return APIResponse(
                success=True,
                message=f"Lottery draw found for {draw_date}",
                data={"draw": draw.dict()}
            )
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving lottery draw: {str(e)}")
    
    async def get_latest_lottery_draw(self) -> APIResponse:
        """Get the most recent lottery draw"""
        try:
            draw = await self.lottery_service.get_latest_draw()
            
            if not draw:
                raise HTTPException(
                    status_code=404,
                    detail="No lottery draws found"
                )
            
            return APIResponse(
                success=True,
                message="Latest lottery draw retrieved",
                data={"draw": draw.dict()}
            )
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving latest lottery draw: {str(e)}")
    
    async def check_lottery_numbers(self, request: LotteryCheckRequest) -> APIResponse:
        """Check lottery numbers for winnings"""
        try:
            # Validate numbers format
            for number in request.numbers:
                if not number.isdigit() or len(number) < 2:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid lottery number format: {number}. Numbers must contain only digits and be at least 2 digits long."
                    )
            
            # Check the numbers
            results = await self.lottery_service.check_numbers(
                request.numbers, 
                request.date
            )
            
            # Calculate summary
            winning_results = [r for r in results if r.matched]
            total_winnings = sum(r.prize_amount or 0 for r in winning_results)
            
            response_data = LotteryCheckResponse(
                results=results,
                total_winnings=total_winnings,
                checked_count=len(request.numbers),
                winning_count=len(winning_results)
            )
            
            return APIResponse(
                success=True,
                message=f"Checked {len(request.numbers)} numbers. Found {len(winning_results)} winners.",
                data=response_data.dict()
            )
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error checking lottery numbers: {str(e)}")
    
    async def search_lottery_draws(
        self,
        start_date: Optional[date] = Query(None, description="Start date filter"),
        end_date: Optional[date] = Query(None, description="End date filter"),
        page: int = Query(1, ge=1, description="Page number"),
        size: int = Query(50, ge=1, le=100, description="Items per page")
    ) -> APIResponse:
        """Search lottery draws with date filters"""
        try:
            # This would need additional implementation in the service
            # For now, return all draws with basic filtering
            result = await self.lottery_service.get_all_draws(page=page, size=size)
            
            # Filter by date range if provided
            filtered_items = result.items
            if start_date or end_date:
                filtered_items = [
                    draw for draw in result.items
                    if (not start_date or draw.date >= start_date) and
                       (not end_date or draw.date <= end_date)
                ]
            
            return APIResponse(
                success=True,
                message=f"Found {len(filtered_items)} lottery draws",
                data={
                    "draws": [draw.dict() for draw in filtered_items],
                    "filters": {
                        "start_date": start_date.isoformat() if start_date else None,
                        "end_date": end_date.isoformat() if end_date else None
                    },
                    "pagination": {
                        "total": len(filtered_items),
                        "page": page,
                        "size": size
                    }
                }
            )
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error searching lottery draws: {str(e)}") 