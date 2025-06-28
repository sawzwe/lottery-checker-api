from typing import List, Optional, Dict, Any
from datetime import date
import math

from supabase import Client
from ..models.lottery import LotteryDraw, LotteryCheckResult, PaginatedResponse
from ..core.database import get_supabase_client

class LotteryService:
    """Service class for lottery-related business logic"""
    
    def __init__(self):
        self.supabase: Client = get_supabase_client()
        
        # Prize amounts mapping
        self.prize_amounts = {
            "1st_prize": 6000000,
            "nearby_1st": 100000,
            "2nd_prize": 200000,
            "3rd_prize": 80000,
            "4th_prize": 40000,
            "5th_prize": 20000,
            "pre_3digit": 4000,
            "sub_3digits": 4000,
            "2digits": 2000
        }
    
    async def get_all_draws(self, page: int = 1, size: int = 50) -> PaginatedResponse:
        """Get all lottery draws with pagination"""
        try:
            # Calculate offset
            offset = (page - 1) * size
            
            # Get total count
            count_result = self.supabase.table('lottery_draws').select('count').execute()
            total = len(count_result.data)
            
            # Get paginated data
            result = self.supabase.table('lottery_draws')\
                .select('*')\
                .order('date', desc=True)\
                .range(offset, offset + size - 1)\
                .execute()
            
            # Convert to models
            draws = [LotteryDraw(**draw) for draw in result.data]
            
            # Calculate pagination info
            pages = math.ceil(total / size)
            
            return PaginatedResponse(
                items=draws,
                total=total,
                page=page,
                size=size,
                pages=pages
            )
            
        except Exception as e:
            raise Exception(f"Error fetching lottery draws: {str(e)}")
    
    async def get_draw_by_date(self, draw_date: date) -> Optional[LotteryDraw]:
        """Get specific lottery draw by date"""
        try:
            result = self.supabase.table('lottery_draws')\
                .select('*')\
                .eq('date', draw_date.isoformat())\
                .execute()
            
            if result.data:
                return LotteryDraw(**result.data[0])
            return None
            
        except Exception as e:
            raise Exception(f"Error fetching lottery draw for {draw_date}: {str(e)}")
    
    async def get_latest_draw(self) -> Optional[LotteryDraw]:
        """Get the most recent lottery draw"""
        try:
            result = self.supabase.table('lottery_draws')\
                .select('*')\
                .order('date', desc=True)\
                .limit(1)\
                .execute()
            
            if result.data:
                return LotteryDraw(**result.data[0])
            return None
            
        except Exception as e:
            raise Exception(f"Error fetching latest lottery draw: {str(e)}")
    
    async def check_numbers(self, numbers: List[str], check_date: Optional[date] = None) -> List[LotteryCheckResult]:
        """Check lottery numbers against draws"""
        try:
            results = []
            
            if check_date:
                # Check against specific date
                draw = await self.get_draw_by_date(check_date)
                if draw:
                    for number in numbers:
                        result = self._check_number_against_draw(number, draw)
                        results.append(result)
            else:
                # Check against all draws
                all_draws_result = self.supabase.table('lottery_draws')\
                    .select('*')\
                    .order('date', desc=True)\
                    .execute()
                
                for number in numbers:
                    best_result = None
                    for draw_data in all_draws_result.data:
                        draw = LotteryDraw(**draw_data)
                        result = self._check_number_against_draw(number, draw)
                        
                        # Keep the best result (highest prize)
                        if result.matched and (not best_result or 
                                             (result.prize_amount or 0) > (best_result.prize_amount or 0)):
                            best_result = result
                    
                    if best_result:
                        results.append(best_result)
                    else:
                        # No match found
                        results.append(LotteryCheckResult(
                            number=number,
                            date=date.today(),
                            matched=False
                        ))
            
            return results
            
        except Exception as e:
            raise Exception(f"Error checking lottery numbers: {str(e)}")
    
    def _check_number_against_draw(self, number: str, draw: LotteryDraw) -> LotteryCheckResult:
        """Check a single number against a single draw"""
        number = number.strip()
        
        # Check 1st prize
        if number == draw.prize_1st:
            return LotteryCheckResult(
                number=number,
                date=draw.date,
                prize_type="1st Prize",
                prize_amount=self.prize_amounts["1st_prize"],
                matched=True
            )
        
        # Check nearby 1st prize
        if number in draw.nearby_1st:
            return LotteryCheckResult(
                number=number,
                date=draw.date,
                prize_type="Around 1st Prize",
                prize_amount=self.prize_amounts["nearby_1st"],
                matched=True
            )
        
        # Check 2nd prize
        if number in draw.prize_2nd:
            return LotteryCheckResult(
                number=number,
                date=draw.date,
                prize_type="2nd Prize",
                prize_amount=self.prize_amounts["2nd_prize"],
                matched=True
            )
        
        # Check 3rd prize
        if number in draw.prize_3rd:
            return LotteryCheckResult(
                number=number,
                date=draw.date,
                prize_type="3rd Prize",
                prize_amount=self.prize_amounts["3rd_prize"],
                matched=True
            )
        
        # Check 4th prize
        if number in draw.prize_4th:
            return LotteryCheckResult(
                number=number,
                date=draw.date,
                prize_type="4th Prize",
                prize_amount=self.prize_amounts["4th_prize"],
                matched=True
            )
        
        # Check 5th prize
        if number in draw.prize_5th:
            return LotteryCheckResult(
                number=number,
                date=draw.date,
                prize_type="5th Prize",
                prize_amount=self.prize_amounts["5th_prize"],
                matched=True
            )
        
        # Check first/last 3 digits
        if len(number) >= 3:
            first_3 = number[:3]
            last_3 = number[-3:]
            
            if first_3 in draw.prize_pre_3digit or last_3 in draw.prize_pre_3digit:
                return LotteryCheckResult(
                    number=number,
                    date=draw.date,
                    prize_type="First/Last 3 Digits",
                    prize_amount=self.prize_amounts["pre_3digit"],
                    matched=True
                )
        
        # Check sub 3 digits
        if len(number) >= 3:
            for i in range(len(number) - 2):
                sub_3 = number[i:i+3]
                if sub_3 in draw.prize_sub_3digits:
                    return LotteryCheckResult(
                        number=number,
                        date=draw.date,
                        prize_type="Sub 3 Digits",
                        prize_amount=self.prize_amounts["sub_3digits"],
                        matched=True
                    )
        
        # Check last 2 digits
        if len(number) >= 2 and draw.prize_2digits:
            last_2 = number[-2:]
            if last_2 == str(draw.prize_2digits).zfill(2):
                return LotteryCheckResult(
                    number=number,
                    date=draw.date,
                    prize_type="Last 2 Digits",
                    prize_amount=self.prize_amounts["2digits"],
                    matched=True
                )
        
        # No match
        return LotteryCheckResult(
            number=number,
            date=draw.date,
            matched=False
        ) 