-- Create table for FIPE vehicles
CREATE TABLE IF NOT EXISTS fipe_veiculos (
    codigo_fipe VARCHAR(20) PRIMARY KEY,
    marca VARCHAR(100) NOT NULL,
    modelo VARCHAR(255) NOT NULL,
    tipo_veiculo VARCHAR(20) NOT NULL -- 'carro', 'moto', 'caminhao'
);

-- Optional: Create table for price history if needed later
CREATE TABLE IF NOT EXISTS fipe_historico_precos (
    id SERIAL PRIMARY KEY,
    codigo_fipe VARCHAR(20) REFERENCES fipe_veiculos(codigo_fipe),
    ano_modelo VARCHAR(50),
    valor VARCHAR(50),
    mes_referencia VARCHAR(50),
    CONSTRAINT fk_veiculo FOREIGN KEY (codigo_fipe) REFERENCES fipe_veiculos(codigo_fipe)
);

-- Index for faster searches
CREATE INDEX IF NOT EXISTS idx_fipe_veiculos_marca ON fipe_veiculos(marca);
CREATE INDEX IF NOT EXISTS idx_fipe_veiculos_modelo ON fipe_veiculos(modelo);
