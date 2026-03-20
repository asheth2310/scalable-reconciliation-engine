import typing
import strawberry
from sqlalchemy.future import select
from app.models import Invoice as InvoiceModel, ReconciliationLog as LogModel

@strawberry.type
class Invoice:
    id: int
    vendor_name: str
    amount: float
    reference_number: str
    status: str
    created_at: str

@strawberry.type
class ReconciliationLog:
    id: int
    invoice_id: int
    action_taken: str
    system_confidence: float
    timestamp: str

@strawberry.type
class Query:
    @strawberry.field
    async def get_invoice(self, info: strawberry.Info, id: int) -> typing.Optional[Invoice]:
        db = info.context["db"]
        result = await db.execute(select(InvoiceModel).where(InvoiceModel.id == id))
        invoice = result.scalars().first()
        if invoice:
            return Invoice(
                id=invoice.id, vendor_name=invoice.vendor_name, amount=invoice.amount,
                reference_number=invoice.reference_number, status=invoice.status, 
                created_at=str(invoice.created_at)
            )
        return None

    @strawberry.field
    async def list_invoices(self, info: strawberry.Info, limit: int = 100) -> typing.List[Invoice]:
        db = info.context["db"]
        result = await db.execute(select(InvoiceModel).limit(limit))
        return [
            Invoice(
                id=i.id, vendor_name=i.vendor_name, amount=i.amount,
                reference_number=i.reference_number, status=i.status, 
                created_at=str(i.created_at)
            ) for i in result.scalars().all()
        ]

    @strawberry.field
    async def list_logs(self, info: strawberry.Info, limit: int = 100) -> typing.List[ReconciliationLog]:
        db = info.context["db"]
        result = await db.execute(select(LogModel).limit(limit))
        return [
            ReconciliationLog(
                id=log.id, invoice_id=log.invoice_id, action_taken=log.action_taken,
                system_confidence=log.system_confidence, timestamp=str(log.timestamp)
            ) for log in result.scalars().all()
        ]

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_invoice(self, info: strawberry.Info, vendor_name: str, amount: float, reference_number: str) -> Invoice:
        db = info.context["db"]
        new_invoice = InvoiceModel(vendor_name=vendor_name, amount=amount, reference_number=reference_number)
        db.add(new_invoice)
        await db.commit()
        await db.refresh(new_invoice)
        return Invoice(
            id=new_invoice.id, vendor_name=new_invoice.vendor_name, amount=new_invoice.amount,
            reference_number=new_invoice.reference_number, status=new_invoice.status, 
            created_at=str(new_invoice.created_at)
        )

schema = strawberry.Schema(query=Query, mutation=Mutation)
