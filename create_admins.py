import asyncio
import json
from app.core.database import SessionLocal
from app.services.authHelper import create_new_user, RoleEnum, get_user_by_username
from sqlalchemy import select
from app.model.models import DBUser

async def create_admins():
    with open("admins.json", "r") as f:
        admins = json.load(f)

    async with SessionLocal() as db:
        result = await db.execute(select(DBUser.username))
        existing_usernames = set(result.scalars().all())
        print(f"Found {len(existing_usernames)} existing users in DB")

        created = 0
        skipped = 0
        for admin in admins:
            if admin["username"] in existing_usernames:
                print(f"Skipping {admin['username']} — already exists")
                skipped += 1
                continue
            await create_new_user(db, username=admin["username"], plain_password=admin["password"], role=RoleEnum.admin)
            print(f"Created admin: {admin['username']}")
            created += 1

        print(f"\nDone. Created: {created}, Skipped: {skipped}")

asyncio.run(create_admins())