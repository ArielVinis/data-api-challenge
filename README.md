# Data API Challenge

Desafio técnico em que integro a [OpenWeather](https://openweathermap.org/api), persisto os dados em PostgreSQL e exponho uma API REST com FastAPI.

Documentação interativa: http://localhost:8000/docs

## O que a API faz

1. **Integração** — consulta a OpenWeather com parâmetro dinâmico (`city`) e API key
2. **Persistência** — grava o resultado na tabela `weather`
3. **REST** — consulta os registros já armazenados no banco

Separei as rotas de integração (`/api/openweather`) das rotas REST (`/api/weather`). A parte RESTful do desafio é consultar **os dados persistidos**: listar a coleção e buscar por `id`.

## Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) + Docker Compose, **ou** Python 3.14+ com [uv](https://docs.astral.sh/uv/)
- Conta na OpenWeather e uma API key — [home.openweathermap.org/api_keys](https://home.openweathermap.org/api_keys)  
  (cada pessoa usa a sua; não commitar a key)

## Configuração

```bash
cp .env.example .env
```

No `.env`, preencha pelo menos:

```env
OPENWEATHER_API_KEY=sua_chave_aqui
```

As credenciais Postgres de exemplo (`weather` / `weather`) são só para rodar localmente.

## Executar com Docker

```bash
docker compose up --build
```

- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- Health: http://localhost:8000/health
- Postgres: `localhost:5432`

Parar: `docker compose down`  
Resetar o banco: `docker compose down -v`

## Executar sem Docker (API local + Postgres no Docker)

1. Suba só o banco: `docker compose up db -d`
2. Mantenha `DATABASE_URL` com `localhost` no `.env`
3. Rode a API:

```bash
uv sync
uv run uvicorn main:app --app-dir src --reload
```

## Endpoints

### Integração OpenWeather

| Método | Caminho                               | Descrição                             |
| ------ | ------------------------------------- | ------------------------------------- |
| `GET`  | `/api/openweather?city=Florianopolis` | Clima ao vivo (não grava)             |
| `POST` | `/api/openweather?city=Florianopolis` | Busca na OpenWeather e grava no banco |

### REST — registros no PostgreSQL

| Método | Caminho             | Descrição                                     |
| ------ | ------------------- | --------------------------------------------- |
| `GET`  | `/api/weather`      | Lista a coleção (`limit` opcional, padrão 25) |
| `GET`  | `/api/weather/{id}` | Retorna um registro pelo id                   |

| Método | Caminho   | Descrição    |
| ------ | --------- | ------------ |
| `GET`  | `/health` | Health check |

### Exemplos

```bash
# Integração — consulta ao vivo
curl "http://localhost:8000/api/openweather?city=Florianopolis"

# Integração — buscar e salvar
curl -X POST "http://localhost:8000/api/openweather?city=Florianopolis"

# REST — listar registros salvos
curl "http://localhost:8000/api/weather"

# REST — registro por id
curl "http://localhost:8000/api/weather/1"
```

## Estrutura do projeto

```
src/
  main.py              # app FastAPI
  api/                 # routers (openweather + weather)
  services/            # chamada OpenWeather + regras de persistência
  models/              # SQLModel (tabela weather)
  schemas/             # Pydantic (request/response)
  db/                  # engine e sessão
  config.py            # variáveis de ambiente
Dockerfile
docker-compose.yml
```

Usei `create_all` no startup para criar a tabela — simples o suficiente para este desafio.

## Segurança

- `.env` no `.gitignore` — não enviar para o GitHub
- `.env.example` só com placeholders
- Keys novas da OpenWeather podem levar alguns minutos para ativar
