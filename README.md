# AI Telegram Task Manager

A smart Telegram bot task manager built to solve task-management problems for the Almaty Hub office as part of an internship project.

The bot understands natural language (text and voice), turns it into structured tasks via an LLM, and syncs everything with Notion. No rigid command syntax — just type or say what needs to be done, and the bot figures out the date, priority, duration, and details on its own.

![Working process demo](assets/working_process.gif)

---

## Features

### Natural language understanding

The bot doesn't require any special command syntax. Every message (text or voice) is sent to an LLM with a detailed system prompt that extracts one or more tasks from it and determines the required action:

- **Creation** — "remind me to call mom tomorrow at 18:00", "team meeting on Friday at 10:00, high priority"
- **Editing** — "move the team meeting to 12:00", "change the priority of the report task to high"
- **Completion** — "I bought the bread, mark the task as done"
- **Deletion** — "delete the task about calling mom"
- **Search** — "what do I have planned for tomorrow?", "show all urgent tasks"
- **Notion actions directly from chat** — "create a task and add it to Notion", "move task 3 to in progress", "add a comment to the meeting: bring laptop"

For every task, the AI automatically determines (unless explicitly stated):

- **Date and time** — calculated relative to the current moment, accounting for time zone
- **Duration** — a logical estimate based on the nature of the task (a meeting ≈ 60 min, a quick errand ≈ 5 min, etc.)
- **Priority** (`low` / `medium` / `high`) — only if the user explicitly mentioned it
- **Details** — word translation, event context, a list of items, etc.

### Voice messages

Voice messages are downloaded from Telegram's servers and transcribed via Groq Whisper (`whisper-large-v3-turbo`), then processed through the same pipeline as regular text.

### Smart schedule conflict resolution

If a new task overlaps in time with an existing one, the bot:

- automatically looks for the nearest free slot of the required duration, if the user didn't explicitly specify a time
- if the time was explicitly specified and conflicts with another task, sends an interactive warning with buttons: keep both tasks in parallel, reschedule the old one, or reschedule the new one

### Two-way Notion integration

- **Export** — tasks created in the bot can be sent to Notion with a single request; fields (title, date, description, priority, status, multi-select/sprint, author) are automatically mapped to your database properties based on their type.
- **Import** (`/fetch_notion_tasks`) — pulls all incomplete tasks assigned to the user from Notion and adds them locally, so they'll also generate reminders.
- **Status sync** — the "Sync completed tasks from Notion" button marks all tasks whose Notion status starts with `Done` as completed in the bot.
- **Comments** — you can ask the bot to leave a comment on a specific task directly in Notion.
- Configurable "on creation" and "on completion" statuses, plus support for multiple data sources within a single database.

### Administrator approval

Linking a user's Notion account goes through moderation: after the workspace member is selected, all administrators (`ADMIN_IDS`) receive a request with "Approve" / "Reject" buttons, and the integration is only activated once approved.

### Reminders and digests

- Individual notification sent exactly when a task is due (with "Complete" / "Snooze 15 minutes" buttons right in the notification).
- Daily task digests at 9:00 and 21:00.
- On bot restart, all active tasks are reloaded into the scheduler from the database — no reminders are lost.

### Task database hygiene

A dedicated "Overdue tasks" section shows all tasks past their deadline and lets you bulk-complete them or clean them up via Notion sync — this helps keep the database from growing unbounded (with 2000+ tasks in context, the AI starts getting confused).

### Multi-language support

Russian and English interface, switchable with the `/change_language` command.

### Pagination

Task lists (active, completed, today's tasks, search results) are displayed page by page with inline navigation.

---

## Architecture

The project is built on aiogram 3.x with a clean layered structure and dependency injection: repositories are created in handlers and passed into services; services don't know about each other directly except through explicitly passed dependencies.

```
┌─────────────┐     ┌──────────────┐     ┌───────────────┐
│  handlers/  │ ──▶ │  services/   │ ──▶ │ repositories/ │ ──▶ PostgreSQL
│ (aiogram)   │     │ (business    │     │  (asyncpg)    │
│             │     │  logic)      │     │               │
└─────────────┘     └──────────────┘     └───────────────┘
       │                    │
       │                    ├──▶ services/ai        (LLM: command parsing)
       │                    ├──▶ services/notion     (Notion API)
       │                    └──▶ services/scheduler  (APScheduler)
       │
       └──▶ middlewares/ (DB session per Update + user fetch/creation)
```

### Key layers

| Layer | Purpose |
|---|---|
| `handlers/` | aiogram entry points: commands, text buttons, callback queries. No SQL knowledge — they only call repositories/services. |
| `services/ai/` | Builds the system prompt and calls the LLM through an OpenAI-compatible client; returns a validated `MultiTaskActionSchema` Pydantic object. |
| `services/notion/` | Notion API client, automatic mapping of task fields to database properties by type, import/export, status and comment handling. |
| `services/tasks/` | CRUD for tasks, schedule conflict resolution, sync with the scheduler and Notion, and the `processor.py` entry point that routes parsed AI commands to the right services. |
| `services/scheduler.py` | Global `APScheduler` instance, one-off and cron notification jobs. |
| `database/repositories/` | The single layer with direct PostgreSQL access (`asyncpg`). |
| `database/migrations/` | Versioned `.sql` migrations with a custom runner (no Alembic). |
| `middlewares/` | Gives each Update an isolated connection from the pool within a transaction, and prepares the `user` object. |
| `keyboards/` | Reply and inline keyboards. |
| `messages.py` | All of the bot's user-facing text, in both languages, in one place. |
| `utils/` | Task list formatting, pagination, date and timezone handling. |

### On the database

The schema is applied through `database/migrations/*.sql` and the `database/migrations/runner.py` runner, which tracks already-applied migrations in a dedicated `schema_migrations` table. To add a new migration, just drop in a `.sql` file with the next numeric prefix (`003_...`) — it will be picked up and applied automatically on the next startup.

### On the LLM client

`services/ai/service.py` uses an `AsyncOpenAI` client, so the provider can be swapped via `.env` (`OPENAI_DEFAULT_URL`, `OPENAI_DEFAULT_MODEL`) — any OpenAI-compatible endpoint works: OpenAI itself, Gemini through a compatible proxy, xAI, local models (LM Studio, Ollama with an OpenAI-compatible server), and so on. Voice transcription uses a separate Groq key.

---

## Tech stack

- **Python 3.12**
- **aiogram 3** — asynchronous framework for the Telegram Bot API; FSM for multi-step flows (Notion registration)
- **PostgreSQL + asyncpg** — main storage, no ORM, manual connection pool
- **APScheduler** — scheduler for one-off reminders and daily digests
- **OpenAI Python SDK** — unified client for any OpenAI-compatible LLM provider, structured JSON-mode output
- **Groq (Whisper Large v3 Turbo)** — speech recognition
- **Notion API** (version `2025-09-03`, with `data_sources` support) — via a custom lightweight async client built on `aiohttp`
- **Pydantic** — validation of the AI's structured response
- **aiohttp** — health-check HTTP server and HTTP client for Notion
- **Docker** — ready-to-use `Dockerfile` for production deployment

---

## Installation and setup

### Prerequisites

- Python 3.12+
- A running PostgreSQL server
- A Telegram bot token from @BotFather
- A Groq API key (for voice recognition)
- An API key for an OpenAI-compatible LLM provider (OpenAI, Gemini, xAI, local server, etc.)
- (optional) Notion integration — the token is created by the bot's users themselves via `/add_notion`; no global setup is required in `.env`

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd <PROJECT_FOLDER_NAME>
```

### 2. Environment variables

Copy `.env.example` to `.env` and fill in your own values:

```bash
cp .env.example .env
```

```env
TG_BOT_TOKEN=your_telegram_bot_token_here
GROQ_API_KEY=your_groq_api_key_here

# OpenAI API (OpenAI, Gemini, xAI, Local, etc.)
OPENAI_API_KEY=your_llm_api_key_here
OPENAI_DEFAULT_URL=https://api.openai.com/v1
OPENAI_DEFAULT_MODEL=gpt-4o-mini

# Format: Continent/City (America/New_York)
TIMEZONE=your_timezone_here

# id1,id2,id3,...
ADMIN_IDS=list_of_tg_ids_of_admins

# PostgreSQL
DB_HOST=
DB_PORT=
DB_USER=
DB_PASS=
DB_NAME=
```

> **About `ADMIN_IDS`**: a comma-separated list of administrators' Telegram IDs (spaces are trimmed automatically either way). These are the people who will receive requests to approve Notion account linking.

### 3a. Running locally

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt

python main.py
```

On startup, the bot automatically applies any missing SQL migrations to the specified PostgreSQL database — there's no need to create tables manually.

### 3b. Running with Docker

```bash
docker build -t task-manager-bot .
docker run --env-file .env -p 80:80 task-manager-bot
```

Inside the container, a lightweight `aiohttp` server runs alongside long polling on port `80` with a `/healthz` endpoint — it's not part of the bot's logic and exists solely to pass health checks on deployment platforms (Kubernetes, PaaS, etc.).

---

## Bot commands

| Command / button | Description |
|---|---|
| `/start` | Welcome message and a brief overview of the bot's capabilities |
| `/add_notion` | Step-by-step FSM setup for Notion integration (token → database → data source → member → statuses) |
| `/fetch_notion_tasks` | Imports incomplete tasks assigned to the user from Notion into the bot |
| `/change_language` | Switches the interface between Russian and English |
| `/cancel` | Cancels the current step of Notion setup |
| "My tasks" | Active tasks with pagination |
| "My completed tasks" | Completed tasks with pagination |
| "Today's tasks" | Active tasks due today |
| "Overdue tasks" | Tasks past their deadline, plus bulk actions and Notion sync |
| any text or voice message | Processed by the AI as one or more task commands |

---

## Project structure

```
.
├── main.py                       # Entry point: bot setup, DB pool, migrations, scheduler
├── config.py                     # Reads .env, timezone, database DSN
├── messages.py                   # All bot text (RU/EN) in one place
├── Dockerfile
├── database/
│   ├── models.py                  # Enums: TaskStatus, TaskImportance
│   ├── pool.py                    # asyncpg connection pool singleton
│   ├── schemas.py                 # Pydantic schemas for the AI's response
│   ├── migrations/                # .sql migrations + automatic runner
│   ├── repositories/              # UserRepository, TaskRepository, SearchRepository,
│   │                               # NotionWorkspaceRepository, base.py
│   └── crud/                      # Legacy wrappers (gradually being replaced by repositories/)
├── handlers/                      # aiogram handlers by domain
├── keyboards/                     # Reply and inline keyboards
├── middlewares/                   # DbSessionMiddleware, UserMiddleware
├── services/
│   ├── scheduler.py                # Global APScheduler + notifications/digests
│   ├── whisper_service.py          # Voice transcription via Groq
│   ├── ai/                         # Prompt building + LLM calls, parsing into MultiTaskActionSchema
│   ├── notion/                     # Notion API client, import/export, service utilities
│   └── tasks/                      # CRUD, schedule conflicts, sync, command processor
└── utils/                          # Formatting, pagination, dates, language context
```

---

## Important operational notes

- **Task database hygiene.** Once a single user accumulates more than roughly 2000 tasks, the AI — which receives the full list as context — starts making mistakes when matching commands to specific tasks. It's recommended to periodically complete or delete old tasks; the "Overdue tasks" section exists for exactly this purpose.
- **Administrator approval is mandatory.** Until at least one user from `ADMIN_IDS` clicks "Approve," a Notion account link stays in a pending state and is never activated.
- **Tasks with no deadline.** Tasks with no explicitly specified deadline are assigned a placeholder timestamp (2060-01-01) — they're excluded from reminders and shown in lists under a separate "No date" section.

---

## Security

- The `.env` file and any files containing real databases (`*.db*`) are excluded from git via `.gitignore` — never commit secrets.
- All tokens (Telegram, Groq, LLM provider, Notion) are read exclusively from environment variables.
- The database connection for each Update is wrapped in a transaction — if an unhandled exception occurs in a handler, changes are automatically rolled back, protecting against partially applied operations.

> **Note:** if, during development, you ever committed or shared files like `test.py` / `script.py` / `result.txt` containing real keys or tokens, make sure to revoke those keys in the corresponding services and generate new ones — even if the files themselves are now covered by `.gitignore`.

---

## Contributing

Pull requests and issues are welcome. For significant changes, it's recommended to open an issue first describing the proposed change.

---

## License

This project is licensed under the MIT License.

```
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
