"""Grant alert endpoints: create, list, update, delete."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.database import get_db
from app.models.user import User
from app.models.alert import GrantAlert
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/v1/alerts", tags=["Alerts"])


class AlertCreate(BaseModel):
    grant_id: Optional[str] = None
    alert_type: str = "all"  # new_grant, deadline, change, all
    channel: str = "email"   # email, push, both


class AlertUpdate(BaseModel):
    alert_type: Optional[str] = None
    channel: Optional[str] = None
    is_active: Optional[bool] = None


class AlertResponse(BaseModel):
    id: str
    grant_id: Optional[str] = None
    alert_type: str
    channel: str
    is_active: bool


@router.post("", response_model=AlertResponse, status_code=201)
def create_alert(
    body: AlertCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user.plan != "premium":
        raise HTTPException(403, "Grant alerts require a Premium subscription")

    alert = GrantAlert(
        user_id=user.id,
        grant_id=body.grant_id,
        alert_type=body.alert_type,
        channel=body.channel,
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)

    return AlertResponse(
        id=str(alert.id),
        grant_id=str(alert.grant_id) if alert.grant_id else None,
        alert_type=alert.alert_type,
        channel=alert.channel,
        is_active=alert.is_active,
    )


@router.get("", response_model=list[AlertResponse])
def list_alerts(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    alerts = db.query(GrantAlert).filter(GrantAlert.user_id == user.id).all()
    return [
        AlertResponse(
            id=str(a.id),
            grant_id=str(a.grant_id) if a.grant_id else None,
            alert_type=a.alert_type,
            channel=a.channel,
            is_active=a.is_active,
        )
        for a in alerts
    ]


@router.patch("/{alert_id}", response_model=AlertResponse)
def update_alert(
    alert_id: str,
    body: AlertUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    alert = (
        db.query(GrantAlert)
        .filter(GrantAlert.id == alert_id, GrantAlert.user_id == user.id)
        .first()
    )
    if not alert:
        raise HTTPException(404, "Alert not found")

    if body.alert_type is not None:
        alert.alert_type = body.alert_type
    if body.channel is not None:
        alert.channel = body.channel
    if body.is_active is not None:
        alert.is_active = body.is_active

    db.commit()
    db.refresh(alert)

    return AlertResponse(
        id=str(alert.id),
        grant_id=str(alert.grant_id) if alert.grant_id else None,
        alert_type=alert.alert_type,
        channel=alert.channel,
        is_active=alert.is_active,
    )


@router.delete("/{alert_id}", status_code=204)
def delete_alert(
    alert_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    alert = (
        db.query(GrantAlert)
        .filter(GrantAlert.id == alert_id, GrantAlert.user_id == user.id)
        .first()
    )
    if not alert:
        raise HTTPException(404, "Alert not found")
    db.delete(alert)
    db.commit()
