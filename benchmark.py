import asyncio
import time
import os
import sys
from sqlalchemy.future import select

# Ensure we can import app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models import Invoice, ReconciliationLog
from app.database import engine, Base, SessionLocal
from app.engine import ReconciliationEngine

async def run_benchmark():
    records_count = 3200

    print("Initializing Database...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    print(f"Seeding {records_count} pending invoices...")
    async with SessionLocal() as session:
        invoices = [
            Invoice(
                vendor_name=f"Vendor-{i}",
                amount=100.0 + i,
                reference_number=f"BNCH-{time.time()}-{i}",
                status="PENDING"
            ) for i in range(records_count)
        ]
        session.add_all(invoices)
        await session.commit()
    
    print(f"Starting reconciliation engine benchmark on {records_count} records...")
    start_time = time.perf_counter()
    
    async with SessionLocal() as session:
        recon_engine = ReconciliationEngine(session)
        # Process the entire batch at once for the benchmark
        processed = await recon_engine.process_batch(records_count)
    
    end_time = time.perf_counter()
    latency_ms = (end_time - start_time) * 1000
    
    print("-" * 40)
    print(f"Processed count: {processed}")
    print(f"Execution Latency: {latency_ms:.2f} ms")
    
    if latency_ms < 600:
        print("✅ SUCCESS: Distributed Reconciliation Engine verified at sub-600ms latency!")
    else:
        print("❌ FAILED: Latency exceeded 600ms limit.")
    print("-" * 40)

if __name__ == "__main__":
    asyncio.run(run_benchmark())
