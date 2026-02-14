"""Seed the database with initial grant data from grants_seed.json."""

import json
import os
from datetime import datetime

from slugify import slugify
from sqlalchemy.orm import Session

from app.models.grant import Grant, GrantDocument, GrantStep
from app.models.eligibility_rule import EligibilityRule


SEED_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "grants_seed.json")


def seed_grants(db: Session) -> int:
    """Load grants from seed JSON if the grants table is empty. Returns count of imported grants."""
    existing = db.query(Grant).count()
    if existing > 0:
        return 0  # Already seeded

    if not os.path.exists(SEED_FILE):
        print(f"Seed file not found: {SEED_FILE}")
        return 0

    with open(SEED_FILE, "r") as f:
        grants_data = json.load(f)

    count = 0
    for g_data in grants_data:
        grant = Grant(
            name=g_data["name"],
            slug=g_data.get("slug", slugify(g_data["name"])),
            short_description=g_data["short_description"],
            long_description=g_data.get("long_description"),
            category=g_data["category"],
            subcategory=g_data.get("subcategory"),
            max_amount=g_data.get("max_amount"),
            amount_description=g_data.get("amount_description"),
            amount_type=g_data.get("amount_type", "variable"),
            is_means_tested=g_data.get("is_means_tested", False),
            source_organisation=g_data["source_organisation"],
            source_url=g_data["source_url"],
            application_url=g_data.get("application_url"),
            application_method=g_data.get("application_method"),
            is_always_open=g_data.get("is_always_open", True),
            typical_processing=g_data.get("typical_processing"),
            last_verified_at=datetime.utcnow(),
        )
        db.add(grant)
        db.flush()

        for rule_data in g_data.get("eligibility_rules", []):
            db.add(EligibilityRule(
                grant_id=grant.id,
                rule_group=rule_data.get("rule_group", 0),
                field=rule_data["field"],
                operator=rule_data["operator"],
                value=rule_data["value"],
                description=rule_data.get("description"),
                is_mandatory=rule_data.get("is_mandatory", True),
            ))

        for step_data in g_data.get("steps", []):
            db.add(GrantStep(
                grant_id=grant.id,
                step_number=step_data["step_number"],
                title=step_data["title"],
                description=step_data["description"],
                url=step_data.get("url"),
            ))

        for doc_data in g_data.get("documents", []):
            db.add(GrantDocument(
                grant_id=grant.id,
                document_name=doc_data["document_name"],
                description=doc_data.get("description"),
                is_required=doc_data.get("is_required", True),
            ))

        count += 1

    db.commit()
    print(f"Seeded {count} grants into database.")
    return count
