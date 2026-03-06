import { env } from "@/shared/config/env";

export interface LoginPayload {
  email: string;
  password: string;
}

export interface MeResponse {
  id: string;
  organization_id: string;
  email: string;
  full_name: string;
  roles: string[];
  permissions: string[];
}

export async function login(payload: LoginPayload): Promise<MeResponse> {
  const response = await fetch(`${env.apiBaseUrl}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
    credentials: "include",
  });

  if (!response.ok) {
    throw new Error("Credenciales invalidas o sesion no disponible.");
  }

  return response.json();
}

export async function me(): Promise<MeResponse> {
  const response = await fetch(`${env.apiBaseUrl}/auth/me`, {
    method: "GET",
    credentials: "include",
  });

  if (!response.ok) {
    throw new Error("No hay sesion activa.");
  }

  return response.json();
}
