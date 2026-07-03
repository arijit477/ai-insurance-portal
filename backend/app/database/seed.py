import logging
from sqlalchemy.orm import Session
from app.models.insurance_plan import InsurancePlan, InsuranceCategory

logger = logging.getLogger(__name__)

INITIAL_PLANS = [
    {
        "id": 1,
        "plan_name": "SecureHealth Plus",
        "category": "HEALTH",
        "premium": 8999.0,
        "coverage_amount": 500000.0,
        "duration_months": 12,
        "description": "Comprehensive health coverage including hospitalization, surgery, critical illness, and pre/post hospitalization expenses for individuals and families."
    },
    {
        "id": 2,
        "plan_name": "MediCare Gold",
        "category": "HEALTH",
        "premium": 14999.0,
        "coverage_amount": 1000000.0,
        "duration_months": 12,
        "description": "Premium health plan with zero co-pay, maternity benefits, day-care procedures, and worldwide emergency cover for complete peace of mind."
    },
    {
        "id": 3,
        "plan_name": "AutoShield Basic",
        "category": "VEHICLE",
        "premium": 3499.0,
        "coverage_amount": 200000.0,
        "duration_months": 12,
        "description": "Essential motor insurance covering third-party liability, own damage from accidents, fire, natural calamities, and theft for your vehicle."
    },
    {
        "id": 4,
        "plan_name": "AutoShield Comprehensive",
        "category": "VEHICLE",
        "premium": 6999.0,
        "coverage_amount": 500000.0,
        "duration_months": 12,
        "description": "Full coverage motor plan with zero depreciation, engine protection, roadside assistance, and personal accident cover for driver and passengers."
    },
    {
        "id": 5,
        "plan_name": "HomeGuard Essential",
        "category": "HOME",
        "premium": 4999.0,
        "coverage_amount": 1500000.0,
        "duration_months": 12,
        "description": "Protect your home from fire, flood, earthquake, burglary, and natural disasters. Covers structure and contents with quick claim settlement."
    },
    {
        "id": 6,
        "plan_name": "HomeGuard Premium",
        "category": "HOME",
        "premium": 9999.0,
        "coverage_amount": 5000000.0,
        "duration_months": 24,
        "description": "Premium home insurance with worldwide content cover, alternative accommodation, domestic helper liability, and personal liability protection."
    },
    {
        "id": 7,
        "plan_name": "JetSafe Travel",
        "category": "TRAVEL",
        "premium": 1299.0,
        "coverage_amount": 100000.0,
        "duration_months": 12,
        "description": "Single and multi-trip travel insurance covering medical emergencies, trip cancellation, lost baggage, flight delays, and passport loss globally."
    },
    {
        "id": 8,
        "plan_name": "LifeSecure Term Plan",
        "category": "LIFE",
        "premium": 12999.0,
        "coverage_amount": 10000000.0,
        "duration_months": 240,
        "description": "Pure term life insurance providing high coverage at affordable premiums. Financial security for your family in case of untimely demise."
    }
]


def seed_db(db: Session):
    existing = db.query(InsurancePlan).first()
    if existing is not None:
        logger.info("Database already seeded with insurance plans.")
        return

    logger.info("Seeding initial insurance plans...")
    for plan_data in INITIAL_PLANS:
        plan = InsurancePlan(
            id=plan_data["id"],
            plan_name=plan_data["plan_name"],
            category=InsuranceCategory[plan_data["category"]],
            premium=plan_data["premium"],
            coverage_amount=plan_data["coverage_amount"],
            duration_months=plan_data["duration_months"],
            description=plan_data["description"],
            is_active=True
        )
        db.add(plan)
    db.commit()
    logger.info("Seeding completed successfully!")
