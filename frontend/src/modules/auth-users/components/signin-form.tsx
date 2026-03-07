"use client";

import { FormEvent, useState } from "react";

import { login, me, MeResponse } from "@/modules/auth-users/api/client";

export function SignInForm() {
  // Componente de autenticación inicial.
  // Responsabilidades:
  // - capturar credenciales y enviarlas al backend.
  // - manejar estados de carga/error.
  // - mostrar resumen de sesión activa (usuario, roles, permisos).
  const [email, setEmail] = useState("admin@orlyfin.local");
  const [password, setPassword] = useState("ChangeMe123!");
  const [error, setError] = useState<string | null>(null);
  const [session, setSession] = useState<MeResponse | null>(null);
  const [loading, setLoading] = useState(false);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    // Flujo de submit:
    // 1) previene refresh del navegador.
    // 2) ejecuta login para crear cookies de sesión.
    // 3) consulta /auth/me para sincronizar estado UI con backend.
    // 4) en error, limpia sesión local y muestra mensaje de fallo.
    event.preventDefault();
    setLoading(true);
    setError(null);

    try {
      await login({ email, password });
      const profile = await me();
      setSession(profile);
    } catch (err) {
      setSession(null);
      setError(err instanceof Error ? err.message : "Error inesperado al iniciar sesion.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="of-panel">
      <h1>Autenticacion</h1>
      <p>Base funcional de login para Fase 2.</p>
      <form onSubmit={onSubmit} className="of-form">
        <label>
          Email
          <input type="email" value={email} onChange={(event) => setEmail(event.target.value)} required />
        </label>
        <label>
          Password
          <input
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
            minLength={8}
          />
        </label>
        <button type="submit" disabled={loading}>
          {loading ? "Ingresando..." : "Iniciar sesion"}
        </button>
      </form>

      {error ? <p className="of-error">{error}</p> : null}

      {session ? (
        <article className="of-session">
          <h2>Sesion activa</h2>
          <p>
            {session.full_name} ({session.email})
          </p>
          <p>Roles: {session.roles.join(", ") || "sin roles"}</p>
          <p>Permisos: {session.permissions.length}</p>
        </article>
      ) : null}
    </section>
  );
}
