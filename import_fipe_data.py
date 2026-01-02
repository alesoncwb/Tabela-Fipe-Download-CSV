import csv
import os

def generate_insert_sql_from_csv(csv_file, output_file):
    """
    Reads fipe_completa.csv and writes SQL INSERT statements to output_file.
    CSV Columns: Tipo;Marca;Modelo;Ano;Valor;CodigoFipe;Combustivel
    """
    if not os.path.exists(csv_file):
        print(f"File not found: {csv_file}")
        return

    print(f"Processing {csv_file}...")
    
    # Use sets to avoid duplicate inserts for the main vehicle table
    processed_configs = set()
    
    with open(csv_file, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None) # Skip header
        
        for row in reader:
            if len(row) < 6: continue
            
            tipo = row[0].replace("'", "''")
            marca = row[1].replace("'", "''")
            modelo = row[2].replace("'", "''")
            ano_modelo = row[3].replace("'", "''")
            valor = row[4].replace("'", "''")
            codigo_fipe = row[5]
            # combustivel = row[6] if len(row) > 6 else ""
            
            # 1. Insert into fipe_veiculos (Avoid duplicates)
            if codigo_fipe not in processed_configs:
                sql_veiculo = f"INSERT INTO fipe_veiculos (codigo_fipe, marca, modelo, tipo_veiculo) VALUES ('{codigo_fipe}', '{marca}', '{modelo}', '{tipo}') ON CONFLICT (codigo_fipe) DO NOTHING;\n"
                output_file.write(sql_veiculo)
                processed_configs.add(codigo_fipe)
            
            # 2. Insert into fipe_historico_precos
            # We don't have mes_referencia explicitly in CSV line (unless we add it to crawler), 
            # but we can assume it's the current one or generic.
            sql_preco = f"INSERT INTO fipe_historico_precos (codigo_fipe, ano_modelo, valor, mes_referencia) VALUES ('{codigo_fipe}', '{ano_modelo}', '{valor}', 'Atual');\n"
            output_file.write(sql_preco)

def main():
    input_csv = 'fipe_completa.csv'
    output_sql_file = 'insert_data.sql'
    
    print(f"Generating {output_sql_file} from {input_csv}...")
    
    with open(output_sql_file, 'w', encoding='utf-8') as f:
        f.write("BEGIN;\n")
        generate_insert_sql_from_csv(input_csv, f)
        f.write("COMMIT;\n")
        
    print("Done! Executing the generated SQL file will populate the database.")

if __name__ == "__main__":
    main()
