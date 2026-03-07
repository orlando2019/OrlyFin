import { env } from "@/shared/config/env";

export interface ExecutiveDashboard {
  // Contrato alineado al endpoint /dashboard/executive.
  // Los montos viajan como string decimal para no perder precisión en transporte.
  period_start: string;
  period_end: string;
  total_income: string;
  total_expense: string;
  total_payments: string;
  outstanding_debt: string;
  total_account_balance: string;
  total_budget: string;
  budget_usage_percent: string;
  pending_expenses: number;
  active_debts: number;
}

export async function getExecutiveDashboard(): Promise<ExecutiveDashboard> {
  // Solicita resumen ejecutivo consolidado.
  // Usa `credentials: include` porque el backend resuelve sesión por cookies JWT.
  const response = await fetch(`${env.apiBaseUrl}/dashboard/executive`, {
    method: "GET",
    credentials: "include",
  });

  if (!response.ok) {
    throw new Error("No se pudo cargar el dashboard ejecutivo.");
  }

  return response.json();
}
