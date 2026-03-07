import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "OrlyFin",
  description: "Plataforma financiera multiusuario",
};

// Implementa la lógica de 'root layout' y retorna la estructura esperada por el módulo.
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body>
        <div className="of-shell">
          <header className="of-header">
            <div>
              <p className="of-brand">OrlyFin</p>
              <p className="of-subtitle">Financial Control Platform</p>
            </div>
            <span className="of-badge">Fase 5</span>
          </header>
          <main className="of-main">{children}</main>
        </div>
      </body>
    </html>
  );
}
