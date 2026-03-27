import asyncio
import json
from app.core.database import SessionLocal
from app.services.authHelper import create_new_user, RoleEnum, get_user_by_username


async def populate_users():
    with open("clean_data.json", "r") as f:
        data = json.load(f)

    async with SessionLocal() as db:
        created = 0
        skipped = 0
        for entry in data:
            username = entry["username"]
            password = entry["password"]

            existing = await get_user_by_username(db, username)
            if existing:
                print(f"Skipping {username} — already exists")
                skipped += 1
                continue

            await create_new_user(db, username=username, plain_password=password, role=RoleEnum.student)
            print(f"Created user: {username}")
            created += 1

        print(f"\nDone. Created: {created}, Skipped: {skipped}")


asyncio.run(populate_users())