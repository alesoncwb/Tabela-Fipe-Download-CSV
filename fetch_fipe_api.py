import requests
import csv
import time
import json
import os

# Constants
BASE_URL = "http://veiculos.fipe.org.br/api/veiculos"
HEADERS = {
    "Host": "veiculos.fipe.org.br",
    "Referer": "http://veiculos.fipe.org.br",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
OUTPUT_CSV = "fipe_completa.csv"

def make_request(url, payload=None):
    """
    Makes a request with retry logic for 429 (Too Many Requests) and other transient errors.
    """
    max_retries = 5
    base_delay = 2
    
    for attempt in range(max_retries):
        try:
            if payload:
                response = requests.post(url, headers=HEADERS, json=payload)
            else:
                response = requests.post(url, headers=HEADERS)
                
            if response.status_code == 429:
                wait_time = base_delay * (2 ** attempt)
                print(f"    [!] Rate limited (429). Waiting {wait_time}s...")
                time.sleep(wait_time)
                continue
                
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"    [!] Request error: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                return None
    return None

def get_tabela_referencia():
    url = f"{BASE_URL}/ConsultarTabelaDeReferencia"
    data = make_request(url)
    if data:
        return data[0]['Codigo']
    return None

def get_marcas(cod_tabela, tipo_veiculo):
    url = f"{BASE_URL}/ConsultarMarcas"
    payload = {
        "codigoTabelaReferencia": cod_tabela,
        "codigoTipoVeiculo": tipo_veiculo
    }
    return make_request(url, payload) or []

def get_modelos(cod_tabela, tipo_veiculo, cod_marca):
    url = f"{BASE_URL}/ConsultarModelos"
    payload = {
        "codigoTabelaReferencia": cod_tabela,
        "codigoTipoVeiculo": tipo_veiculo,
        "codigoMarca": cod_marca
    }
    data = make_request(url, payload)
    return data.get('Modelos', []) if data else []

def get_anos(cod_tabela, tipo_veiculo, cod_marca, cod_modelo):
    url = f"{BASE_URL}/ConsultarAnoModelo"
    payload = {
        "codigoTabelaReferencia": cod_tabela,
        "codigoTipoVeiculo": tipo_veiculo,
        "codigoMarca": cod_marca,
        "codigoModelo": cod_modelo
    }
    return make_request(url, payload) or []

def get_valor(cod_tabela, tipo_veiculo, cod_marca, cod_modelo, ano_modelo_str, codigo_tipo_combustivel, ano_modelo):
    url = f"{BASE_URL}/ConsultarValorComTodosParametros"
    payload = {
        "codigoTabelaReferencia": cod_tabela,
        "codigoTipoVeiculo": tipo_veiculo,
        "codigoMarca": cod_marca,
        "codigoModelo": cod_modelo,
        "ano": ano_modelo_str,
        "codigoTipoCombustivel": codigo_tipo_combustivel,
        "anoModelo": ano_modelo,
        "tipoConsulta": "tradicional"
    }
    return make_request(url, payload)

def main():
    print("Starting FIPE Crawler...")
    
    cod_tabela = get_tabela_referencia()
    if not cod_tabela:
        print("Failed to get reference table code. Exiting.")
        return
    print(f"Using Reference Table Code: {cod_tabela}")

    # 1: Carro, 2: Moto, 3: Caminhão
    # tipos_veiculo = {1: "Carro", 2: "Moto", 3: "Caminhao"}
    tipos_veiculo = {1: "Carro"} # Apenas Carros conforme solicitado
    
    # Initialize CSV
    file_exists = os.path.isfile(OUTPUT_CSV)
    with open(OUTPUT_CSV, mode='a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if not file_exists:
            writer.writerow(["Tipo", "Marca", "Modelo", "Ano", "Valor", "CodigoFipe", "Combustivel"])

    # Limit for testing purposes - REMOVE OR INCREASE FOR FULL RUN
    LIMIT_TEST = False 

    for cod_tipo, nome_tipo in tipos_veiculo.items():
        print(f"Processing Type: {nome_tipo}")
        marcas = get_marcas(cod_tabela, cod_tipo)
        
        for marca in marcas:
            cod_marca = marca['Value']
            nome_marca = marca['Label']
            print(f"  > Brand: {nome_marca}")
            
            modelos = get_modelos(cod_tabela, cod_tipo, cod_marca)
            
            # Shorten test: only process first 2 models of first brand if testing
            if LIMIT_TEST and modelos: modelos = modelos[:2]

            for modelo in modelos:
                cod_modelo = modelo['Value']
                nome_modelo = modelo['Label']
                # print(f"    - Model: {nome_modelo}")
                
                anos = get_anos(cod_tabela, cod_tipo, cod_marca, cod_modelo)
                
                for ano in anos:
                    # Parse "2013-1" into year and fuel type
                    # Protocol: year-fuelCode
                    ano_str = ano['Value']
                    
                    try:
                        parts = ano_str.split('-')
                        if len(parts) == 2:
                            ano_modelo = int(parts[0])
                            cod_combustivel = int(parts[1])
                        else:
                            # Sometimes it might be different, default to 1 if fails?
                            # Usually api returns "32000-1" for zero km
                            ano_modelo = int(parts[0])
                            cod_combustivel = 1
                    except:
                        continue

                    data_veiculo = get_valor(
                        cod_tabela, cod_tipo, cod_marca, cod_modelo, 
                        ano_str, cod_combustivel, ano_modelo
                    )
                    
                    if data_veiculo and 'Valor' in data_veiculo:
                        row = [
                            nome_tipo,
                            nome_marca,
                            nome_modelo,
                            data_veiculo.get('AnoModelo', ''),
                            data_veiculo.get('Valor', ''),
                            data_veiculo.get('CodigoFipe', ''),
                            data_veiculo.get('Combustivel', '')
                        ]
                        
                        # Append to CSV immediately
                        with open(OUTPUT_CSV, mode='a', encoding='utf-8', newline='') as f:
                            writer = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                            writer.writerow(row)
                            
                        # print(f"      Saved: {nome_modelo} - {data_veiculo.get('Valor', '')}")
                    else:
                        print(f"      Failed to get details for {nome_modelo} ({ano_str})")
                    
                    
                    # Be nice to the API - minimal delay as retry logic handles 429s
                    # time.sleep(0.1) 
                    print(f"      Processed: {nome_modelo} ({ano_str})") 

            if LIMIT_TEST: break # Stop after first brand for test
        if LIMIT_TEST: break # Stop after first type for test

    print(f"Crawler finished. Data saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
