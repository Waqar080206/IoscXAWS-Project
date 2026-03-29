import asyncio
import json
from app.core.database import SessionLocal
from app.services.authHelper import create_new_user, RoleEnum
from sqlalchemy import select
from app.model.models import DBUser

async def populate_test_users():
    with open("test.json", "r") as f:
        data = json.load(f)

    async with SessionLocal() as db:
        result = await db.execute(select(DBUser.username))
        existing_usernames = set(result.scalars().all())

        created = 0
        skipped = 0

        for entry in data:
            username = entry["username"]
            password = entry["password"]

            if username in existing_usernames:
                print(f"Skipping {username} — already exists")
                skipped += 1
                continue

            try:
                await create_new_user(db, username=username, plain_password=password, role=RoleEnum.student)
                print(f"Created test student: {username}")
                created += 1
            except Exception as e:
                print(f"Failed {username}: {e}")

        print(f"\nDone. Created: {created}, Skipped: {skipped}")

asyncio.run(populate_test_users())