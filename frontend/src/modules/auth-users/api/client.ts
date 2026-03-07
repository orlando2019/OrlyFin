import { env } from "@/shared/config/env";

export interface LoginPayload {
  // Credenciales mínimas requeridas por /auth/login.
  email: string;
  password: string;
}

export interface MeResponse {
  // Contrato de sesión que devuelve backend para identificar usuario
  // y habilitar/ocultar funcionalidades por rol y permiso.
  id: string;
  organization_id: string;
  email: string;
  full_name: string;
  roles: string[];
  permissions: string[];
}

export async function login(payload: LoginPayload): Promise<MeResponse> {
  // Ejecuta login por cookies HttpOnly.
  // Entrada: credenciales del formulario.
  // Retorno: perfil autenticado con roles/permisos.
  // Efecto lateral: navegador almacena tokens en cookies (credentials: include).
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
  // Recupera sesión vigente del usuario actual leyendo cookies existentes.
  // Se utiliza después de login o al reconstruir estado tras recarga de página.
  const response = await fetch(`${env.apiBaseUrl}/auth/me`, {
    method: "GET",
    credentials: "include",
  });

  if (!response.ok) {
    throw new Error("No hay sesion activa.");
  }

  return response.json();
}
