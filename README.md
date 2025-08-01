<!-- @format -->

# Pipeline de Dados de Vendas com AWS Glue e PySpark

Este projeto implementa um pipeline de dados serverless na AWS para processar
arquivos CSV de vendas, utilizando **AWS Glue**, **PySpark**, **S3** e
**Athena**. O pipeline ingere dados brutos do S3, realiza transformações com
PySpark (ex.: calcular o total de vendas por região) e armazena os resultados em
formato Parquet, prontos para análise no Athena.

## Tecnologias Utilizadas

- **Python**: Desenvolvimento do script ETL.
- **PySpark**: Processamento de dados no AWS Glue.
- **AWS Glue**: Orquestração do pipeline e catalogação de dados.
- **Amazon S3**: Armazenamento de dados brutos e processados.
- **Amazon Athena**: Consultas SQL nos dados processados.
- **Git**: Versionamento do código.

## Arquitetura

![Arquitetura do Pipeline](docs/pipeline_architecture.md)

1. Dados CSV de vendas são carregados no bucket S3 `raw-sales-data-<seu-nome>`.
2. Um crawler do AWS Glue catalogará os dados no Glue Data Catalog.
3. Um job Glue executa o script PySpark (`scripts/sales_etl_job.py`) para
   transformar os dados.
4. Os dados processados são salvos em Parquet no bucket
   `processed-sales-data-<seu-nome>`.
5. O Amazon Athena é usado para consultar os dados processados.

## Pré-requisitos

- Conta AWS com permissões para S3, Glue, Athena e IAM.
- Python 3.x e bibliotecas listadas em `requirements.txt`.
- Git instalado.

## Configuração

1. **Crie buckets S3**:
   - `raw-sales-data-<seu-nome>`: Para dados brutos.
   - `processed-sales-data-<seu-nome>`: Para dados processados.
2. **Faça upload do CSV**:
   - Copie `data/sample_sales_data.csv` para o bucket
     `raw-sales-data-<seu-nome>`.
3. **Configure o AWS Glue**:
   - Crie um banco de dados `sales_db` no Glue Data Catalog.
   - Crie um crawler para catalogar os dados CSV no bucket
     `raw-sales-data-<seu-nome>`.
   - Crie um job Glue chamado `sales-etl-job`, associando o script
     `scripts/sales_etl_job.py` e a role IAM com permissões para Glue, S3 e
     CloudWatch.
4. **Configure o Athena**:
   - Crie uma tabela externa apontando para o bucket
     `processed-sales-data-<seu-nome>/sales_parquet/`.
   - Exemplo de query:
     ```sql
     CREATE EXTERNAL TABLE sales_processed (
         region STRING,
         sum_total_sale DOUBLE
     )
     STORED AS PARQUET
     LOCATION 's3://processed-sales-data-<seu-nome>/sales_parquet/';
     ```

## Executando o Pipeline

1. Execute o crawler Glue para criar a tabela `sales_data` no `sales_db`.
2. Execute o job Glue `sales-etl-job` no console AWS Glue.
3. Verifique os arquivos Parquet gerados no bucket
   `processed-sales-data-<seu-nome>`.
4. Consulte os dados no Athena com: `SELECT * FROM sales_processed;`.

## Estrutura do Repositório

```
aws-glue-sales-pipeline/
├── scripts/
│   ├── sales_etl_job.py          # Script PySpark para o job Glue
├── data/
│   ├── sample_sales_data.csv     # Dados de exemplo
├── docs/
│   ├── pipeline_architecture.md  # Diagrama da arquitetura
├── README.md                     # Documentação principal
├── requirements.txt              # Dependências
└── .gitignore                    # Arquivos ignorados pelo Git
```

## Possíveis Melhorias

- Adicionar uma função Lambda para disparar o job Glue automaticamente.
- Integrar notificações via SNS para monitoramento.
- Implementar streaming com Amazon MSK (Kafka).
- Adicionar testes unitários com pytest.

## Contato

- LinkedIn:
  https://www.linkedin.com/in/ot%C3%A1vio-c%C3%A9sar-machado-silva-46a02024a/
- Email: otavioc366@gmail.com

---

Desenvolvido por Otávio para demonstrar habilidades em engenharia de dados com
AWS e PySpark.
