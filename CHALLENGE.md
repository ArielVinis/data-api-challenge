# Avaliação Técnica

## Objetivo

Avaliar competências em:

- extração de dados via API
- armazenamento em banco de dados
- acesso remoto (API REST)
- conteinerização com Docker
- boas práticas de código e organização no Git

---

## Instruções

### 1. Extração de dados via API

- Utilizar uma API pública com requisição **GET** (sugestão: [OpenWeather](https://openweathermap.org/api))
- Extrair dados de interesse (ex.: clima de uma cidade)
- Usar **parâmetros dinâmicos** na URL
- Autenticar com **chave de API**

### 2. Armazenamento em banco de dados

- Persistir os dados num banco **relacional** (MySQL ou PostgreSQL)
- **Uma tabela** é suficiente

### 3. Acesso remoto

- Criar uma API **RESTful** para consultar os dados armazenados
- Linguagem à escolha (neste projeto escolhi a preferencial: **Python + FastAPI**)
- Documentar com **Swagger** (OpenAPI em `/docs`) ou Postman

### 4. Conteinerização com Docker _(opcional, recomendado)_

- Ambiente Docker com **API + banco**
- Executável em qualquer máquina

### 5. Controlo de versão (Git)

- Subir código-fonte e ficheiros Docker no **GitHub**
- Incluir `README.md` com:
  - configuração e execução do ambiente
  - como aceder aos dados remotamente

---

## Entregáveis

- Repositório no GitHub com código-fonte completo (preferência: Python)
- Documentação clara de setup e uso

## Critérios de avaliação

- Qualidade e clareza do código
- Organização do repositório e documentação
- Estruturação correta das tabelas no banco
- Docker reprodutível e funcional

---

## Stack deste projeto

| Peça        | Escolha           |
| ----------- | ----------------- |
| API         | FastAPI           |
| ORM         | SQLModel          |
| Banco       | PostgreSQL        |
| HTTP client | httpx             |
| Config      | Pydantic Settings |
| Packaging   | uv                |
| Docs        | Swagger (`/docs`) |
| Runtime     | Docker Compose    |

---

## TODOs

### Fundação

- [x] Definir dependências no `pyproject.toml` (fastapi, uvicorn, sqlmodel, httpx, pydantic-settings, psycopg)
- [x] Criar `.env.example` e carregar settings (`DATABASE_URL`, `OPENWEATHER_API_KEY`)
- [x] Estruturar pastas: `api/`, `schemas/`, `models/`, `services/`, `db/`
- [x] App FastAPI em `src/main.py` com lifespan e router(s)

### Extração (OpenWeather)

- [x] Obter API key da OpenWeather e documentar no README
- [x] Service `httpx` com GET + parâmetros dinâmicos (ex.: `city`)
- [x] Mapear resposta da API externa para o modelo/schema interno

### Persistência

- [x] Modelo SQLModel (1 tabela) para os dados climáticos
- [x] Setup de engine/session (`db/`) e dependência `get_db`
- [x] Persistir dados após cada extração bem-sucedida

### API REST

- [x] Endpoint para **consultar** OpenWeather sem gravar (`GET /api/openweather?city=...`)
- [x] Endpoint para **extrair e gravar** via OpenWeather (`POST /api/openweather?city=...`)
- [x] Endpoints REST para registos gravados (`GET /api/weather`, `GET /api/weather/{id}`)
- [x] Schemas Pydantic de resposta (`response_model`)
- [ ] Verificar documentação em `/docs`

### Docker e entrega

- [x] `Dockerfile` da API
- [x] `docker-compose.yml` (API + PostgreSQL)
- [x] `README.md` (setup, `.env`, execução, exemplos de curl/Swagger)
- [ ] Push do repositório para o GitHub
