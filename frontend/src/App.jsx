import { useEffect, useState } from "react";

// VITE_API_URL queda incrustada en el JavaScript público: es solo una ruta,
// nunca un secreto.
const API_URL = import.meta.env.VITE_API_URL ?? "/api";

export default function App() {
  const [tiendas, setTiendas] = useState([]);
  const [carrito, setCarrito] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`${API_URL}/tiendas`)
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then(setTiendas)
      .catch((e) => setError(e.message));
  }, []);

  const agregar = (tienda) => setCarrito((c) => [...c, tienda]);

  return (
    <main>
      <h1>Mercado Vecino</h1>
      <p className="sub">Tiendas de barrio de Bogotá a domicilio</p>

      {error && <p className="error">No se pudo cargar el catálogo: {error}</p>}

      <ul className="tiendas">
        {tiendas.map((t) => (
          <li key={t.id}>
            <div>
              <strong>{t.nombre}</strong>
              <span>{t.barrio}</span>
            </div>
            <button onClick={() => agregar(t)}>Agregar</button>
          </li>
        ))}
      </ul>

      <section className="carrito">
        <h2>Carrito ({carrito.length})</h2>
        {carrito.map((t, i) => (
          <p key={i}>{t.nombre}</p>
        ))}
      </section>
    </main>
  );
}
