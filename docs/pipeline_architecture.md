# Arquitetura do Pipeline

## Diagrama
```
[CSV Files] --> [S3 Raw Bucket] --> [Glue Crawler] --> [Glue Data Catalog]
                                                  |
                                              [Glue Job]
                                                  |
                                                  v
[S3 Processed Bucket (Parquet)] <--> [Athena Queries]
```

## Descrição
- **S3 Raw Bucket**: Armazena arquivos CSV de vendas.
- **Glue Crawler**: Cataloga os dados CSV no Glue Data Catalog.
- **Glue Job**: Executa o script PySpark para transformar os dados.
- **S3 Processed Bucket**: Armazena os dados processados em Parquet.
- **Athena**: Permite consultas SQL nos dados processados.