export const env = {
  // URL base única para todos los clientes API del frontend.
  // Prioriza NEXT_PUBLIC_API_BASE_URL para entornos (dev/qa/prod) y
  // usa localhost como fallback local para evitar romper ejecución inicial.
  apiBaseUrl: process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api/v1",
};
