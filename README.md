# pipeline-de-dados-do-campeonato-brasileiro

### Problema:
dados do campeonato brasileiro 2025 não estão disponíveis em formato analítico (tabelas) para consultas SQL.

### Arquitetura:
<img width="1191" height="340" alt="Captura de tela 2025-12-22 192233" src="https://github.com/user-attachments/assets/6822d365-6df9-4c0b-882a-7d8fd7fba494" />

### Tecnologias:
python, docker, airflow, AWS S3, AWS Glue, AWS Athena e Football-Data.org API.

### Fluxo do Dado:
API → ETL (Airflow) → S3 → Glue (catálogo) → Athena (SQL)

### Pré-requisitos:
Docker Desktop, conta AWS com acesso a um bucket no S3, Glue e Athena, além do uso de AWS CLI, chave da API do Football Data Org.
O usuário AWS precisa de uma policy com permissões do S3 e do GLue:  
- S3: `s3:ListBucket`, `s3:GetObject`, `s3:PutObject`.
- Glue: `glue:CreateDatabase`, `glue:GetDatabase`, `glue:GetDatabases`,  
    `glue:CreateTable`, `glue:UpdateTable`, `glue:GetTable`, `glue:GetTables`.

### Como rodar:
1º Clonar o projeto:
```Bash
git clone https://github.com/viniciusnnr/pipeline-de-dados-do-campeonato-brasileiro.git
cd pipeline-de-dados-do-campeonato-brasileiro
```

2º Configuração das variáveis de ambiente
```bash
nano .env
```
Preencha no .env:
- FOOTBALL_DATA_URL=
- FOOTBALL_DATA_API_KEY=
- S3_BUCKET= 

3º Build, Inicialização do airflow e Subir o container:
```bash
docker compose build
```

```bash
docker compose up airflow-init
```

```bash
docker compose up -d
```

4º Acesso ao airflow e execução do pipeline
Acesse `http://localhost:8080` e execute a DAG

### Resultados:
ao final, os dados ficam no S3, são catalogados no Glue e podem ser consultados com SQL via Athena.




