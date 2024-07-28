from http.client import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from models import Schedule
from sqlalchemy import select,update
async def getBookInfo(db,cart,tokenData,schedule_redis):
    try:
        token = tokenData["data"]
        if token is None:
            return "forbidden"
        
        user_id = token["id"]

        stmt = select(Schedule).filter(Schedule.user_id == user_id)
        result = await db.execute(stmt)
        existing_schedule = result.scalar_one_or_none()

        if existing_schedule:
            stmt = update(Schedule).where(Schedule.user_id == user_id).values(
                attraction_id=cart["attraction_id"],
                date=cart["date"],
                time=cart["time"],
                price=cart["price"]
            )
            await db.execute(stmt)
        else:
            new_schedule = Schedule(
                user_id=user_id,
                attraction_id=cart["attraction_id"],
                date=cart["date"],
                time=cart["time"],
                price=cart["price"]
            )
            db.add(new_schedule)
           

        await db.commit()
        
        cache_key = f"member:{user_id}"
        schedule_redis.delete(cache_key)
        
        data = {"ok": True}
        return data
    
    except HTTPException as http_exc:
        return http_exc
    except SQLAlchemyError as e:
        print(e)
        await db.rollback()
        return "error"
    except Exception as e:
        print(e)
        return "error"
        