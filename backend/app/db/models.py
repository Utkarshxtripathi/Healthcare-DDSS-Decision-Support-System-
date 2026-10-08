"""
SQLAlchemy ORM Data Models
CSIR Healthcare Clinical Decision Support System (CDSS/DDSS)
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    DateTime,
    ForeignKey,
    JSON,
    Enum as SQLEnum,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class UserProfile(Base):
    __tablename__ = "profiles"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(String, default="clinician", nullable=False)
    department = Column(String, default="Clinical Research")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    assessments = relationship("AssessmentRecord", back_populates="user")


class PatientRecord(Base):
    __tablename__ = "patients"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    synthetic_patient_id = Column(String, unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    sex = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    assessments = relationship("AssessmentRecord", back_populates="patient")


class AssessmentRecord(Base):
    __tablename__ = "assessments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String, ForeignKey("profiles.id", ondelete="SET NULL"), nullable=True)
    vitals = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    patient = relationship("PatientRecord", back_populates="assessments")
    user = relationship("UserProfile", back_populates="assessments")
    prediction = relationship("PredictionRecord", back_populates="assessment", uselist=False)


class PredictionRecord(Base):
    __tablename__ = "predictions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    assessment_id = Column(String, ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False)
    risk_score = Column(Float, nullable=False)
    risk_category = Column(String, nullable=False)
    risk_label = Column(Integer, nullable=False)
    model_version = Column(String, nullable=False)
    model_family = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    assessment = relationship("AssessmentRecord", back_populates="prediction")
    attributions = relationship("FeatureAttributionRecord", back_populates="prediction")


class FeatureAttributionRecord(Base):
    __tablename__ = "feature_attributions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    prediction_id = Column(String, ForeignKey("predictions.id", ondelete="CASCADE"), nullable=False)
    feature_name = Column(String, nullable=False)
    feature_value = Column(Float, nullable=False)
    shap_value = Column(Float, nullable=False)
    direction = Column(String, nullable=False)
    clinical_impact = Column(String, nullable=False)

    prediction = relationship("PredictionRecord", back_populates="attributions")


class AuditLogRecord(Base):
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=True)
    action = Column(String, nullable=False)
    resource_type = Column(String, nullable=False)
    resource_id = Column(String, nullable=True)
    metadata_json = Column(JSON, default=dict)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
