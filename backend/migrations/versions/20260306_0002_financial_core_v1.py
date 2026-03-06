"""financial core v1 modules

Revision ID: 20260306_0002
Revises: 20260305_0001
Create Date: 2026-03-06 09:20:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260306_0002"
down_revision = "20260305_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "financial_accounts",
        sa.Column("organization_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("account_type", sa.String(length=40), nullable=False),
        sa.Column("currency_code", sa.String(length=3), nullable=False),
        sa.Column("current_balance", sa.Numeric(14, 2), nullable=False, server_default=sa.text("0")),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "name", name="uq_financial_accounts_org_name"),
    )
    op.create_index(op.f("ix_financial_accounts_organization_id"), "financial_accounts", ["organization_id"], unique=False)
    op.create_index(op.f("ix_financial_accounts_account_type"), "financial_accounts", ["account_type"], unique=False)

    op.create_table(
        "income_records",
        sa.Column("organization_id", sa.String(length=36), nullable=False),
        sa.Column("account_id", sa.String(length=36), nullable=True),
        sa.Column("category", sa.String(length=80), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=False),
        sa.Column("amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("income_type", sa.String(length=30), nullable=False),
        sa.Column("frequency", sa.String(length=30), nullable=True),
        sa.Column("occurred_on", sa.Date(), nullable=False),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.ForeignKeyConstraint(["account_id"], ["financial_accounts.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_income_records_organization_id"), "income_records", ["organization_id"], unique=False)
    op.create_index(op.f("ix_income_records_account_id"), "income_records", ["account_id"], unique=False)
    op.create_index(op.f("ix_income_records_category"), "income_records", ["category"], unique=False)
    op.create_index(op.f("ix_income_records_income_type"), "income_records", ["income_type"], unique=False)
    op.create_index(op.f("ix_income_records_occurred_on"), "income_records", ["occurred_on"], unique=False)

    op.create_table(
        "expense_records",
        sa.Column("organization_id", sa.String(length=36), nullable=False),
        sa.Column("account_id", sa.String(length=36), nullable=True),
        sa.Column("category", sa.String(length=80), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=False),
        sa.Column("amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("expense_type", sa.String(length=30), nullable=False),
        sa.Column("due_on", sa.Date(), nullable=True),
        sa.Column("occurred_on", sa.Date(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="pending"),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.ForeignKeyConstraint(["account_id"], ["financial_accounts.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_expense_records_organization_id"), "expense_records", ["organization_id"], unique=False)
    op.create_index(op.f("ix_expense_records_account_id"), "expense_records", ["account_id"], unique=False)
    op.create_index(op.f("ix_expense_records_category"), "expense_records", ["category"], unique=False)
    op.create_index(op.f("ix_expense_records_expense_type"), "expense_records", ["expense_type"], unique=False)
    op.create_index(op.f("ix_expense_records_occurred_on"), "expense_records", ["occurred_on"], unique=False)
    op.create_index(op.f("ix_expense_records_status"), "expense_records", ["status"], unique=False)

    op.create_table(
        "debt_records",
        sa.Column("organization_id", sa.String(length=36), nullable=False),
        sa.Column("account_id", sa.String(length=36), nullable=True),
        sa.Column("creditor", sa.String(length=120), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=False),
        sa.Column("principal_amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("balance_amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("debt_type", sa.String(length=20), nullable=False),
        sa.Column("total_installments", sa.Integer(), nullable=True),
        sa.Column("paid_installments", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("opened_on", sa.Date(), nullable=False),
        sa.Column("due_on", sa.Date(), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="active"),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.ForeignKeyConstraint(["account_id"], ["financial_accounts.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_debt_records_organization_id"), "debt_records", ["organization_id"], unique=False)
    op.create_index(op.f("ix_debt_records_account_id"), "debt_records", ["account_id"], unique=False)
    op.create_index(op.f("ix_debt_records_creditor"), "debt_records", ["creditor"], unique=False)
    op.create_index(op.f("ix_debt_records_balance_amount"), "debt_records", ["balance_amount"], unique=False)
    op.create_index(op.f("ix_debt_records_debt_type"), "debt_records", ["debt_type"], unique=False)
    op.create_index(op.f("ix_debt_records_opened_on"), "debt_records", ["opened_on"], unique=False)
    op.create_index(op.f("ix_debt_records_status"), "debt_records", ["status"], unique=False)

    op.create_table(
        "payment_records",
        sa.Column("organization_id", sa.String(length=36), nullable=False),
        sa.Column("account_id", sa.String(length=36), nullable=False),
        sa.Column("payment_type", sa.String(length=20), nullable=False),
        sa.Column("amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("paid_on", sa.Date(), nullable=False),
        sa.Column("reference_type", sa.String(length=20), nullable=True),
        sa.Column("reference_id", sa.String(length=36), nullable=True),
        sa.Column("notes", sa.String(length=255), nullable=False),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.ForeignKeyConstraint(["account_id"], ["financial_accounts.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_payment_records_organization_id"), "payment_records", ["organization_id"], unique=False)
    op.create_index(op.f("ix_payment_records_account_id"), "payment_records", ["account_id"], unique=False)
    op.create_index(op.f("ix_payment_records_payment_type"), "payment_records", ["payment_type"], unique=False)
    op.create_index(op.f("ix_payment_records_paid_on"), "payment_records", ["paid_on"], unique=False)
    op.create_index(op.f("ix_payment_records_reference_type"), "payment_records", ["reference_type"], unique=False)
    op.create_index(op.f("ix_payment_records_reference_id"), "payment_records", ["reference_id"], unique=False)

    op.create_table(
        "budget_records",
        sa.Column("organization_id", sa.String(length=36), nullable=False),
        sa.Column("category", sa.String(length=80), nullable=False),
        sa.Column("period_start", sa.Date(), nullable=False),
        sa.Column("period_end", sa.Date(), nullable=False),
        sa.Column("planned_amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("alert_threshold_percent", sa.Numeric(5, 2), nullable=False, server_default="80"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_budget_records_organization_id"), "budget_records", ["organization_id"], unique=False)
    op.create_index(op.f("ix_budget_records_category"), "budget_records", ["category"], unique=False)
    op.create_index(op.f("ix_budget_records_period_start"), "budget_records", ["period_start"], unique=False)
    op.create_index(op.f("ix_budget_records_period_end"), "budget_records", ["period_end"], unique=False)
    op.create_index(op.f("ix_budget_records_is_active"), "budget_records", ["is_active"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_budget_records_is_active"), table_name="budget_records")
    op.drop_index(op.f("ix_budget_records_period_end"), table_name="budget_records")
    op.drop_index(op.f("ix_budget_records_period_start"), table_name="budget_records")
    op.drop_index(op.f("ix_budget_records_category"), table_name="budget_records")
    op.drop_index(op.f("ix_budget_records_organization_id"), table_name="budget_records")
    op.drop_table("budget_records")

    op.drop_index(op.f("ix_payment_records_reference_id"), table_name="payment_records")
    op.drop_index(op.f("ix_payment_records_reference_type"), table_name="payment_records")
    op.drop_index(op.f("ix_payment_records_paid_on"), table_name="payment_records")
    op.drop_index(op.f("ix_payment_records_payment_type"), table_name="payment_records")
    op.drop_index(op.f("ix_payment_records_account_id"), table_name="payment_records")
    op.drop_index(op.f("ix_payment_records_organization_id"), table_name="payment_records")
    op.drop_table("payment_records")

    op.drop_index(op.f("ix_debt_records_status"), table_name="debt_records")
    op.drop_index(op.f("ix_debt_records_opened_on"), table_name="debt_records")
    op.drop_index(op.f("ix_debt_records_debt_type"), table_name="debt_records")
    op.drop_index(op.f("ix_debt_records_balance_amount"), table_name="debt_records")
    op.drop_index(op.f("ix_debt_records_creditor"), table_name="debt_records")
    op.drop_index(op.f("ix_debt_records_account_id"), table_name="debt_records")
    op.drop_index(op.f("ix_debt_records_organization_id"), table_name="debt_records")
    op.drop_table("debt_records")

    op.drop_index(op.f("ix_expense_records_status"), table_name="expense_records")
    op.drop_index(op.f("ix_expense_records_occurred_on"), table_name="expense_records")
    op.drop_index(op.f("ix_expense_records_expense_type"), table_name="expense_records")
    op.drop_index(op.f("ix_expense_records_category"), table_name="expense_records")
    op.drop_index(op.f("ix_expense_records_account_id"), table_name="expense_records")
    op.drop_index(op.f("ix_expense_records_organization_id"), table_name="expense_records")
    op.drop_table("expense_records")

    op.drop_index(op.f("ix_income_records_occurred_on"), table_name="income_records")
    op.drop_index(op.f("ix_income_records_income_type"), table_name="income_records")
    op.drop_index(op.f("ix_income_records_category"), table_name="income_records")
    op.drop_index(op.f("ix_income_records_account_id"), table_name="income_records")
    op.drop_index(op.f("ix_income_records_organization_id"), table_name="income_records")
    op.drop_table("income_records")

    op.drop_index(op.f("ix_financial_accounts_account_type"), table_name="financial_accounts")
    op.drop_index(op.f("ix_financial_accounts_organization_id"), table_name="financial_accounts")
    op.drop_table("financial_accounts")
