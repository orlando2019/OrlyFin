"use client";

import { useEffect, useState } from "react";

import { ExecutiveDashboard, getExecutiveDashboard } from "@/modules/dashboard/api/client";

const currency = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  maximumFractionDigits: 2,
});

function money(value: string): string {
  // Formatea decimales de backend a moneda legible en UI.
  // Recibe string para mantener contrato API y convierte de forma defensiva.
  return currency.format(Number(value || 0));
}

export function ExecutiveDashboardPanel() {
  // Panel ejecutivo principal del frontend.
  // Se encarga de cargar métricas agregadas y representar estados de la consulta:
  // loading -> error -> sin datos -> vista de métricas.
  const [data, setData] = useState<ExecutiveDashboard | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;

    async function load() {
      // Carga datos una sola vez al montar.
      // `active` evita actualizar estado si el componente se desmonta antes
      // de que termine la promesa (previene warnings por setState tardío).
      try {
        const payload = await getExecutiveDashboard();
        if (active) setData(payload);
      } catch (err) {
        if (active) setError(err instanceof Error ? err.message : "Error cargando dashboard.");
      } finally {
        if (active) setLoading(false);
      }
    }

    load();
    return () => {
      active = false;
    };
  }, []);

  if (loading) {
    return <section className="of-panel">Cargando dashboard ejecutivo...</section>;
  }

  if (error) {
    return <section className="of-panel of-error">{error}</section>;
  }

  if (!data) {
    return <section className="of-panel">Sin datos disponibles.</section>;
  }

  return (
    <section className="of-panel">
      <h1>Dashboard Ejecutivo</h1>
      <p>
        Periodo: {data.period_start} a {data.period_end}
      </p>
      <div className="of-grid-metrics">
        <article>
          <h2>Ingresos</h2>
          <strong>{money(data.total_income)}</strong>
        </article>
        <article>
          <h2>Gastos</h2>
          <strong>{money(data.total_expense)}</strong>
        </article>
        <article>
          <h2>Pagos</h2>
          <strong>{money(data.total_payments)}</strong>
        </article>
        <article>
          <h2>Deuda Pendiente</h2>
          <strong>{money(data.outstanding_debt)}</strong>
        </article>
        <article>
          <h2>Saldo en Cuentas</h2>
          <strong>{money(data.total_account_balance)}</strong>
        </article>
        <article>
          <h2>Uso Presupuesto</h2>
          <strong>{Number(data.budget_usage_percent).toFixed(2)}%</strong>
        </article>
      </div>
      <p>
        Presupuesto total: {money(data.total_budget)} | Gastos pendientes: {data.pending_expenses} | Deudas activas: {data.active_debts}
      </p>
    </section>
  );
}
