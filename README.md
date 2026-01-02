# FIPE Crawler & Database Importer 🚗

Este projeto contém um conjunto de ferramentas para extrair a Tabela FIPE oficial atualizada (via API) e importá-la para um banco de dados ou planilha CSV.

Diferente de listas estáticas no GitHub que ficam desatualizadas rapidamente, este projeto busca os dados **em tempo real** da API oficial da FIPE.

## 🚀 Funcionalidades

- **Crawler Inteligente (`fetch_fipe_api.py`)**:
    - Consulta a API oficial da FIPE.
    - Baixa dados de Carros (configurável para Motos e Caminhões).
    - Gera um arquivo CSV (`fipe_completa.csv`) pronto para uso Excel/Data Analysis.
    - **Resiliente**: Possui lógica de "retry" e espera exponencial para evitar bloqueios da API (Erro 429).
    - Salva progresso incrementalmente (não perde dados se parar).

- **Importador de Banco de Dados (`import_fipe_data.py` e `create_tables.sql`)**:
    - Script SQL para criar tabelas otimizadas (`fipe_veiculos` e `fipe_historico_precos`).
    - Script Python que converte o CSV gerado em comandos `INSERT` SQL para importação em massa.

## 🛠️ Como Usar

### 1. Pré-requisitos
Certifique-se de ter o Python instalado.
Instale as dependências:

```bash
pip install requests
```

### 2. Baixar Dados da FIPE
Execute o crawler para obter a tabela mais recente:

```bash
python fetch_fipe_api.py
```
*O processo pode demorar alguns minutos a horas dependendo da quantidade de veículos, pois respeita os limites da API.*
O resultado será salvo em `fipe_completa.csv`.

### 3. Importar para Banco de Dados (SQL)
Se você deseja os dados em um banco SQL (PostgreSQL, MySQL, etc.):

1.  Crie as tabelas no seu banco:
    (Copie o conteúdo de `create_tables.sql` e execute no seu cliente SQL)

2.  Gere o script de inserção:
    ```bash
    python import_fipe_data.py
    ```
    Isso criará o arquivo `insert_data.sql`.

3.  Execute o script gerado no seu banco:
    ```sql
    -- Exemplo psql
    \i insert_data.sql
    ```

## 📋 Estrutura do CSV
O arquivo gerado contém as seguintes colunas:
`Tipo;Marca;Modelo;Ano;Valor;CodigoFipe;Combustivel`

Exemplo:
```csv
Carro;Acura;Integra GS 1.8;1992;R$ 10.942,00;038003-2;Gasolina
```

## ⚠️ Aviso Legal
Este projeto consulta dados públicos da Fundação Instituto de Pesquisas Econômicas (FIPE). Use com responsabilidade e respeite os limites de requisição da API.
