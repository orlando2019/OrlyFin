import Link from "next/link";

export default function HomePage() {
  return (
    <section className="of-panel">
      <h1>Base arquitectonica lista</h1>
      <p>
        El proyecto esta preparado para crecer por modulos de negocio sin mezclar responsabilidades.
      </p>
      <div className="of-links">
        <Link href="/dashboard">Ir al dashboard base</Link>
        <Link href="/signin">Ir a autenticacion base</Link>
      </div>
    </section>
  );
}
