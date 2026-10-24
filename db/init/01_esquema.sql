-- Se ejecuta UNA sola vez, cuando el volumen pgdata está vacío.
-- Corre como el superusuario (mercado_admin) sobre la base "mercado".

CREATE TABLE tiendas (
    id      SERIAL PRIMARY KEY,
    nombre  VARCHAR(120) NOT NULL,
    barrio  VARCHAR(80)  NOT NULL
);

CREATE TABLE productos (
    id         SERIAL PRIMARY KEY,
    tienda_id  INT NOT NULL REFERENCES tiendas(id),
    nombre     VARCHAR(120) NOT NULL,
    precio     NUMERIC(12, 2) NOT NULL CHECK (precio > 0)
);

CREATE TABLE pedidos (
    id         SERIAL PRIMARY KEY,
    tienda_id  INT NOT NULL REFERENCES tiendas(id),
    cliente    VARCHAR(120) NOT NULL,
    total      NUMERIC(12, 2) NOT NULL CHECK (total > 0),
    creado_en  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Datos semilla
INSERT INTO tiendas (nombre, barrio) VALUES
    ('Tienda Doña Rosa',      'Chapinero'),
    ('Fruver El Campesino',   'Teusaquillo'),
    ('Panadería La Espiga',   'Suba'),
    ('Minimercado San Luis',  'Kennedy');

INSERT INTO productos (tienda_id, nombre, precio) VALUES
    (1, 'Leche entera 1 L',     4800),
    (1, 'Huevos AA x 30',      17500),
    (2, 'Aguacate Hass (kg)',   9000),
    (2, 'Banano (kg)',          3200),
    (3, 'Pan aliñado',          1500),
    (3, 'Almojábana',           2000),
    (4, 'Arroz 1 kg',           4300),
    (4, 'Café molido 500 g',   15900);
