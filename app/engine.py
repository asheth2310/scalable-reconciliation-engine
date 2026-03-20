import asyncio
import random
from sqlalchemy.future import select
from app.models import Invoice, ReconciliationLog
from app.database import SessionLocal

class ReconciliationEngine:
    def __init__(self, db_session):
        self.db = db_session

    async def process_batch(self, batch_size=500):
        # Fetch pending invoices
        result = await self.db.execute(
            select(Invoice).where(Invoice.status == "PENDING").limit(batch_size)
        )
        invoices = result.scalars().all()

        if not invoices:
            return 0

        # Simulate fast sub-600ms latency processing
        await asyncio.sleep(0.01)

        processed_count = 0
        for invoice in invoices:
            # Multi-turn logic simulation
            feature_match = random.uniform(0.7, 1.0)
            anomaly_score = random.uniform(0.0, 0.3)
            confidence = feature_match - anomaly_score
            
            if confidence > 0.8:
                invoice.status = "RECONCILED"
                action = "AUTO_MATCH"
            elif confidence > 0.5:
                invoice.status = "FLAGGED"
                action = "HUMAN_REVIEW_REQUIRED"
            else:
                invoice.status = "DISCREPANCY"
                action = "REJECTED_ANOMALY"
            
            # Log action
            log = ReconciliationLog(
                invoice_id=invoice.id,
                action_taken=action,
                system_confidence=confidence
            )
            self.db.add(log)
            processed_count += 1

        await self.db.commit()
        return processed_count

async def background_recon_task(websocket_manager=None):
    """
    Runs periodically to process pending invoices.
    """
    while True:
        try:
            async with SessionLocal() as session:
                engine = ReconciliationEngine(session)
                count = await engine.process_batch(500)
                if count > 0 and websocket_manager:
                    await websocket_manager.broadcast_json({"type": "reconciliation_batch", "count": count})
        except Exception as e:
            print(f"Engine error: {e}")
        
        await asyncio.sleep(0.5)
