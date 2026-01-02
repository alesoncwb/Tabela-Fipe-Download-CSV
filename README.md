FIPE Crawler & Database Importer
Este projeto oferece ferramentas para extrair dados atualizados diretamente da Tabela FIPE oficial e organizá-los em bancos de dados SQL ou arquivos CSV.

Ao contrário de repositórios que disponibilizam listas estáticas (que perdem a validade em pouco tempo), este script consulta a API da FIPE em tempo real, garantindo que você tenha sempre as informações mais recentes.

O que o projeto faz
Extração de Dados (fetch_fipe_api.py)
O crawler principal é responsável por navegar na API da FIPE e consolidar as informações.

Abrangência: Focado em carros, mas facilmente ajustável para motos e caminhões.
Saída: Gera um arquivo fipe_completa.csv compatível com Excel e ferramentas de análise de dados.
Estabilidade: Inclui um sistema de tentativas automáticas e espera progressiva para evitar bloqueios por excesso de requisições (Erro 429).
Persistência: O progresso é salvo durante a execução, permitindo retomar de onde parou caso a conexão caia.
Integração com Banco de Dados (import_fipe_data.py e create_tables.sql)
Ferramentas para quem precisa estruturar os dados de forma profissional:

Modelagem: Scripts SQL prontos para criar tabelas de veículos e histórico de preços.
Conversão: Transforma o arquivo CSV em comandos INSERT para facilitar a importação em massa para bancos como PostgreSQL ou MySQL.
Como utilizar
1. Preparação
Com o Python instalado no seu sistema, instale a biblioteca necessária para as requisições:

bash
copiar
baixar
pip install requests
2. Coleta de dados
Para iniciar a extração da tabela atual, execute:

bash
copiar
baixar
python fetch_fipe_api.py
Atenção: O processo pode levar de alguns minutos a algumas horas. O script respeita os limites da API para garantir que a coleta seja concluída sem interrupções.

3. Importação para SQL
Caso prefira trabalhar com um banco de dados relacional:

Execute as instruções contidas em create_tables.sql no seu console de banco de dados para criar a estrutura necessária.
Gere o arquivo de importação executando:
bash
copiar
baixar
python import_fipe_data.py
O script criará um arquivo insert_data.sql. Basta rodar esse arquivo no seu banco de dados para popular as tabelas.
Formato dos dados
O CSV final utiliza o ponto e vírgula (;) como separador e segue esta estrutura:
Tipo;Marca;Modelo;Ano;Valor;CodigoFipe;Combustivel

Exemplo:
Carro;Acura;Integra GS 1.8;1992;R$ 10.942,00;038003-2;Gasolina

Observações importantes
Este software é uma ferramenta de automação para consulta de dados públicos fornecidos pela Fundação Instituto de Pesquisas Econômicas (FIPE). Ao utilizá-lo, certifique-se de respeitar os termos de uso da instituição e evite sobrecarregar os servidores com requisições desnecessárias.