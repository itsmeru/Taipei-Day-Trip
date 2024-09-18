from sqlalchemy.future import select
async def getSignUp(db, name, email, password,Account):
    try:
        stmt = select(Account).filter(Account.email == email)
        result = await db.execute(stmt)
        existing_user = result.scalar_one_or_none()
        if existing_user:
            return "mailrepeat"

        new_user = Account(name=name, email=email, password=password)
        db.add(new_user)
        await db.commit()

        return {"ok": True}

    except Exception as e:
        print(f"signup Unhandled exception: {e}")
        return "error"
        