"""ops modules v1: reconciliation, alerts, audit, attachments, settings

Revision ID: 20260306_0003
Revises: 20260306_0002
Create Date: 2026-03-06 11:15:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260306_0003"
down_revision = "20260306_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "audit_events",
        sa.Column("organization_id", sa.String(length=36), nullable=True),
        sa.Column("user_id", sa.String(length=36), nullable=True),
        sa.Column("module", sa.String(length=80), nullable=False),
        sa.Column("action", sa.String(length=40), nullable=False),
        sa.Column("entity_type", sa.String(length=80), nullable=True),
        sa.Column("entity_id", sa.String(length=36), nullable=True),
        sa.Column("trace_id", sa.String(length=36), nullable=True),
        sa.Column("details_json", sa.Text(), nullable=False, server_default="{}"),
        sa.Column("occurred_on", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_audit_events_organization_id"), "audit_events", ["organization_id"], unique=False)
    op.create_index(op.f("ix_audit_events_user_id"), "audit_events", ["user_id"], unique=False)
    op.create_index(op.f("ix_audit_events_module"), "audit_events", ["module"], unique=False)
    op.create_index(op.f("ix_audit_events_action"), "audit_events", ["action"], unique=False)
    op.create_index(op.f("ix_audit_events_entity_id"), "audit_events", ["entity_id"], unique=False)
    op.create_index(op.f("ix_audit_events_trace_id"), "audit_events", ["trace_id"], unique=False)
    op.create_index(op.f("ix_audit_events_occurred_on"), "audit_events", ["occurred_on"], unique=False)

    op.create_table(
        "system_settings",
        sa.Column("organization_id", sa.String(length=36), nullable=False),
        sa.Column("key", sa.String(length=120), nullable=False),
        sa.Column("value", sa.Text(), nullable=False),
        sa.Column("value_type", sa.String(length=20), nullable=False, server_default="string"),
        sa.Column("is_sensitive", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "key", name="uq_system_settings_org_key"),
    )
    op.create_index(op.f("ix_system_settings_organization_id"), "system_settings", ["organization_id"], unique=False)
    op.create_index(op.f("ix_system_settings_key"), "system_settings", ["key"], unique=False)

    op.create_table(
        "attachment_records",
        sa.Column("organization_id", sa.String(length=36), nullable=False),
        sa.Column("uploaded_by_user_id", sa.String(length=36), nullable=False),
        sa.Column("module", sa.String(length=80), nullable=False),
        sa.Column("entity_id", sa.String(length=36), nullable=False),
        sa.Column("file_name", sa.String(length=255), nullable=False),
        sa.Column("mime_type", sa.String(length=120), nullable=False),
        sa.Column("size_bytes", sa.Integer(), nullable=False),
        sa.Column("storage_path", sa.String(length=500), nullable=False),
        sa.Column("checksum_sha256", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="uploaded"),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.ForeignKeyConstraint(["uploaded_by_user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("storage_path"),
    )
    op.create_index(op.f("ix_attachment_records_organization_id"), "attachment_records", ["organization_id"], unique=False)
    op.create_index(op.f("ix_attachment_records_uploaded_by_user_id"), "attachment_records", ["uploaded_by_user_id"], unique=False)
    op.create_index(op.f("ix_attachment_records_module"), "attachment_records", ["module"], unique=False)
    op.create_index(op.f("ix_attachment_records_entity_id"), "attachment_records", ["entity_id"], unique=False)
    op.create_index(op.f("ix_attachment_records_mime_type"), "attachment_records", ["mime_type"], unique=False)
    op.create_index(op.f("ix_attachment_records_checksum_sha256"), "attachment_records", ["checksum_sha256"], unique=False)
    op.create_index(op.f("ix_attachment_records_status"), "attachment_records", ["status"], unique=False)

    op.create_table(
        "alert_records",
        sa.Column("organization_id", sa.String(length=36), nullable=False),
        sa.Column("created_by_user_id", sa.String(length=36), nullable=True),
        sa.Column("module", sa.String(length=80), nullable=False),
        sa.Column("severity", sa.String(length=20), nullable=False),
        sa.Column("channel", sa.String(length=20), nullable=False),
        sa.Column("title", sa.String(length=180), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("reference_type", sa.String(length=80), nullable=True),
        sa.Column("reference_id", sa.String(length=36), nullable=True),
        sa.Column("fingerprint", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="unread"),
        sa.Column("triggered_on", sa.DateTime(timezone=True), nullable=False),
        sa.Column("read_on", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_alert_records_organization_id"), "alert_records", ["organization_id"], unique=False)
    op.create_index(op.f("ix_alert_records_created_by_user_id"), "alert_records", ["created_by_user_id"], unique=False)
    op.create_index(op.f("ix_alert_records_module"), "alert_records", ["module"], unique=False)
    op.create_index(op.f("ix_alert_records_severity"), "alert_records", ["severity"], unique=False)
    op.create_index(op.f("ix_alert_records_channel"), "alert_records", ["channel"], unique=False)
    op.create_index(op.f("ix_alert_records_reference_id"), "alert_records", ["reference_id"], unique=False)
    op.create_index(op.f("ix_alert_records_fingerprint"), "alert_records", ["fingerprint"], unique=False)
    op.create_index(op.f("ix_alert_records_status"), "alert_records", ["status"], unique=False)
    op.create_index(op.f("ix_alert_records_triggered_on"), "alert_records", ["triggered_on"], unique=False)

    op.create_table(
        "reconciliation_records",
        sa.Column("organization_id", sa.String(length=36), nullable=False),
        sa.Column("account_id", sa.String(length=36), nullable=False),
        sa.Column("period_start", sa.Date(), nullable=False),
        sa.Column("period_end", sa.Date(), nullable=False),
        sa.Column("book_balance", sa.Numeric(14, 2), nullable=False),
        sa.Column("statement_balance", sa.Numeric(14, 2), nullable=False),
        sa.Column("difference_amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="unbalanced"),
        sa.Column("notes", sa.String(length=255), nullable=False, server_default=""),
        sa.Column("resolved_on", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.ForeignKeyConstraint(["account_id"], ["financial_accounts.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_reconciliation_records_organization_id"), "reconciliation_records", ["organization_id"], unique=False)
    op.create_index(op.f("ix_reconciliation_records_account_id"), "reconciliation_records", ["account_id"], unique=False)
    op.create_index(op.f("ix_reconciliation_records_period_start"), "reconciliation_records", ["period_start"], unique=False)
    op.create_index(op.f("ix_reconciliation_records_period_end"), "reconciliation_records", ["period_end"], unique=False)
    op.create_index(op.f("ix_reconciliation_records_status"), "reconciliation_records", ["status"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_reconciliation_records_status"), table_name="reconciliation_records")
    op.drop_index(op.f("ix_reconciliation_records_period_end"), table_name="reconciliation_records")
    op.drop_index(op.f("ix_reconciliation_records_period_start"), table_name="reconciliation_records")
    op.drop_index(op.f("ix_reconciliation_records_account_id"), table_name="reconciliation_records")
    op.drop_index(op.f("ix_reconciliation_records_organization_id"), table_name="reconciliation_records")
    op.drop_table("reconciliation_records")

    op.drop_index(op.f("ix_alert_records_triggered_on"), table_name="alert_records")
    op.drop_index(op.f("ix_alert_records_status"), table_name="alert_records")
    op.drop_index(op.f("ix_alert_records_fingerprint"), table_name="alert_records")
    op.drop_index(op.f("ix_alert_records_reference_id"), table_name="alert_records")
    op.drop_index(op.f("ix_alert_records_channel"), table_name="alert_records")
    op.drop_index(op.f("ix_alert_records_severity"), table_name="alert_records")
    op.drop_index(op.f("ix_alert_records_module"), table_name="alert_records")
    op.drop_index(op.f("ix_alert_records_created_by_user_id"), table_name="alert_records")
    op.drop_index(op.f("ix_alert_records_organization_id"), table_name="alert_records")
    op.drop_table("alert_records")

    op.drop_index(op.f("ix_attachment_records_status"), table_name="attachment_records")
    op.drop_index(op.f("ix_attachment_records_checksum_sha256"), table_name="attachment_records")
    op.drop_index(op.f("ix_attachment_records_mime_type"), table_name="attachment_records")
    op.drop_index(op.f("ix_attachment_records_entity_id"), table_name="attachment_records")
    op.drop_index(op.f("ix_attachment_records_module"), table_name="attachment_records")
    op.drop_index(op.f("ix_attachment_records_uploaded_by_user_id"), table_name="attachment_records")
    op.drop_index(op.f("ix_attachment_records_organization_id"), table_name="attachment_records")
    op.drop_table("attachment_records")

    op.drop_index(op.f("ix_system_settings_key"), table_name="system_settings")
    op.drop_index(op.f("ix_system_settings_organization_id"), table_name="system_settings")
    op.drop_table("system_settings")

    op.drop_index(op.f("ix_audit_events_occurred_on"), table_name="audit_events")
    op.drop_index(op.f("ix_audit_events_trace_id"), table_name="audit_events")
    op.drop_index(op.f("ix_audit_events_entity_id"), table_name="audit_events")
    op.drop_index(op.f("ix_audit_events_action"), table_name="audit_events")
    op.drop_index(op.f("ix_audit_events_module"), table_name="audit_events")
    op.drop_index(op.f("ix_audit_events_user_id"), table_name="audit_events")
    op.drop_index(op.f("ix_audit_events_organization_id"), table_name="audit_events")
    op.drop_table("audit_events")
