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
    """Load grants from seed JSON. Adds new grants that don't exist yet (by slug). Returns count of newly imported grants."""

    if not os.path.exists(SEED_FILE):
        print(f"Seed file not found: {SEED_FILE}")
        return 0

    with open(SEED_FILE, "r") as f:
        grants_data = json.load(f)

    # Build a set of existing slugs to avoid duplicates
    existing_slugs = set(row[0] for row in db.query(Grant.slug).all())

    count = 0
    for g_data in grants_data:
        slug = g_data.get("slug", slugify(g_data["name"]))
        if slug in existing_slugs:
            continue  # Already exists, skip

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

    # Update existing grants with changed rules (migration-style)
    _update_existing_rules(db, grants_data)

    print(f"Seeded {count} new grants into database.")
    return count


def _update_existing_rules(db: Session, grants_data: list) -> None:
    """Update eligibility rules for existing grants when seed data changes."""
    for g_data in grants_data:
        slug = g_data.get("slug", slugify(g_data["name"]))
        grant = db.query(Grant).filter(Grant.slug == slug).first()
        if not grant:
            continue

        # Compare rule count - if different, replace rules
        seed_rules = g_data.get("eligibility_rules", [])
        existing_rules = db.query(EligibilityRule).filter(EligibilityRule.grant_id == grant.id).all()

        # Simple check: if rule count or content changed, replace
        if len(seed_rules) != len(existing_rules):
            # Delete old rules and re-add
            db.query(EligibilityRule).filter(EligibilityRule.grant_id == grant.id).delete()
            for rule_data in seed_rules:
                db.add(EligibilityRule(
                    grant_id=grant.id,
                    rule_group=rule_data.get("rule_group", 0),
                    field=rule_data["field"],
                    operator=rule_data["operator"],
                    value=rule_data["value"],
                    description=rule_data.get("description"),
                    is_mandatory=rule_data.get("is_mandatory", True),
                ))

    db.commit()
