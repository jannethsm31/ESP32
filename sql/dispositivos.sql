DROP TABLE IF EXISTS dispositivos;
CREATE TABLE dispositivos(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    dispositivo VARCHAR(10) NOT NULL,
    valor INTEGER NOT NULL DEFAULT 0
);

INSERT INTO dispositivos(dispositivo, valor) VALUES ('led', 0), ('potenciometro', 0);