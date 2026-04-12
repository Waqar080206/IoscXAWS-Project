import asyncio
import json
from app.core.database import SessionLocal
from app.model.models import DBStudent
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

async def populate_basic():
    with open("basic3.json", "r") as f:
        data = json.load(f)

    async with SessionLocal() as db:
        created = 0
        updated = 0
        skipped = 0
        failed = 0

        for i, entry in enumerate(data):
            roll_number = entry["roll_number"]
            try:
                result = await db.execute(select(DBStudent).filter(DBStudent.roll_number == roll_number))
                student = result.scalars().first()

                if student:
                    student.name = entry["name"]
                    student.branch = entry["branch"]
                    student.year = entry["year"]
                    await db.commit()
                    updated += 1
                    print(f"[{i+1}/{len(data)}] Updated: {roll_number}")
                else:
                    new_student = DBStudent(
                        roll_number=roll_number,
                        name=entry["name"],
                        branch=entry["branch"],
                        year=entry["year"],
                        email=f"{roll_number}@estudentcell.local",
                        mobile="0000000000",
                    )
                    db.add(new_student)
                    await db.commit()
                    created += 1
                    print(f"[{i+1}/{len(data)}] Created: {roll_number}")

            except Exception as e:
                print(f"[{i+1}/{len(data)}] Failed: {roll_number} — {e}")
                await db.rollback()
                failed += 1

        print(f"\nDone. Created: {created}, Updated: {updated}, Skipped: {skipped}, Failed: {failed}")

asyncio.run(populate_basic())