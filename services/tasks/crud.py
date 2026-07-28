"""
services/tasks/crud.py

Сервис CRUD-операций над задачами.
Изменения (Этап 4):
  - db: Connection заменён на task_repo: TaskRepository + search_repo: SearchRepository.
  - Все прямые вызовы database.crud.task.* заменены на методы репозиториев.
  - Зависимости вводятся через конструктор (DI).
"""

from datetime import datetime

from aiogram import Bot

from messages import TaskMessages
from database.schemas import TaskActionSchema
from database.repositories import TaskRepository, SearchRepository
from keyboards.reply_keyboards import get_main_kb
from keyboards.inline_keyboards import get_pagination_keyboard
from utils.context import user_lang
from config import TIMEZONE, TASKS_LIMIT_OF_PAGES
from utils.formatters import get_display_end_time
from utils.action_result import ActionResult
# Метка «задача без срока» и проверка — единое определение (DRY)
from utils.date_utils import FALLBACK_TASK_TIMESTAMP, is_fallback_timestamp

from services.tasks.conflict import ConflictService
from services.tasks.scheduler import SchedulerService
from services.tasks.notion_sync import NotionSyncService
from keyboards.inline_keyboards import get_conflict_resolution_keyboard

from utils.formatters import capitalize_first


class TaskCRUDService:
    """
    Сервис для выполнения CRUD-операций (создание, поиск, обновление, удаление) с задачами.

    Координирует действия с:
    - SchedulerService  — управление напоминаниями в APScheduler.
    - NotionSyncService — синхронизация с Notion API.
    - ConflictService   — проверка и разрешение временных коллизий.

    Зависимости получает через конструктор (инъекция зависимостей).
    Не выполняет прямых SQL-запросов — делегирует их репозиториям.
    """

    def __init__(
        self,
        task_repo: TaskRepository,
        search_repo: SearchRepository,
        user: dict,
        bot: Bot,
        conflict_service: ConflictService,
        scheduler_service: SchedulerService,
        notion_service: NotionSyncService,
    ):
        """
        Инициализирует CRUD-сервис со всеми необходимыми зависимостями.

        Args:
            task_repo (TaskRepository): Репозиторий задач (asyncpg).
            search_repo (SearchRepository): Репозиторий кэша поиска (asyncpg).
            user (dict): Словарь пользователя из БД.
            bot (Bot): Экземпляр бота Telegram.
            conflict_service (ConflictService): Зависимость для управления коллизиями.
            scheduler_service (SchedulerService): Зависимость планировщика уведомлений.
            notion_service (NotionSyncService): Зависимость синхронизации с Notion.
        """
        self.task_repo = task_repo
        self.search_repo = search_repo
        self.user = user
        self.bot = bot
        self.tz = TIMEZONE
        self.conflict_service = conflict_service
        self.scheduler_service = scheduler_service
        self.notion_service = notion_service

    async def create(self, command: TaskActionSchema) -> ActionResult:
        """
        Создаёт новую задачу в репозитории, планирует уведомления
        и обрабатывает коллизии времени.

        Args:
            command (TaskActionSchema): Параметры новой задачи.

        Returns:
            ActionResult: Подтверждение создания (или форма разрешения конфликта).
        """
        # Определяем время начала задачи
        if not command.time:
            # ИИ вернул null — пользователь не указал срок.
            # Назначаем метку «без срока» (2060), чтобы планировщик не отправил уведомление.
            task_timestamp = FALLBACK_TASK_TIMESTAMP
            localized_dt = datetime.fromtimestamp(task_timestamp, self.tz)
            display_time = None  # Не отображаем дату в подтверждении
        else:
            # Парсим время, указанное пользователем
            try:
                naive_dt = datetime.strptime(command.time, "%Y-%m-%d %H:%M")
                localized_dt = self.tz.localize(naive_dt)
                task_timestamp = int(localized_dt.timestamp())
                display_time = command.time
            except Exception:
                return ActionResult(text=TaskMessages.invalid_time_format())

        # Разрешаем статус и мультиселект для Notion
        notion_status = command.status or self.user.get("notion_status_created")
        notion_multi_select = command.multi_select

        capitalized_content = capitalize_first(command.content)
        capitalized_details = capitalize_first(command.details)

        # Создаём запись о задаче через репозиторий
        new_task_id = await self.task_repo.create(
            user_id=self.user["id"],
            time_val=task_timestamp,
            content=capitalized_content,
            details=capitalized_details,
            duration=command.duration,
            importance=command.importance,
            notion_status=notion_status,
            notion_multi_select=notion_multi_select,
        )

        # Добавляем напоминание о задаче в планировщик
        self.scheduler_service.update_scheduler_jobs(
            task_id=new_task_id,
            content=capitalized_content,
            details=capitalized_details,
            localized_dt=localized_dt,
            duration=command.duration,
            importance=command.importance,
        )

        # Проверяем на наличие временных конфликтов (только для задач с реальным сроком)
        conflict_task = None
        if command.time:
            conflict_task = await self.conflict_service.check_conflict(
                task_timestamp, command.duration, exclude_task_id=new_task_id
            )

        # Если обнаружен конфликт — возвращаем интерактивную форму разрешения коллизии
        if conflict_task:
            warning_text = TaskMessages.conflict_warning(
                new_task_content=capitalized_content,
                new_task_time=display_time,
                old_task_content=conflict_task["content"],
                old_task_time=datetime.fromtimestamp(
                    conflict_task["time"], self.tz
                ).strftime("%Y-%m-%d %H:%M"),
            )
            kb = get_conflict_resolution_keyboard(
                old_task_id=conflict_task["id"],
                new_task_id=new_task_id,
                old_task_content=conflict_task["content"],
                new_task_content=command.content,
                add_to_notion=command.add_to_notion,
            )
            return ActionResult(text=warning_text, keyboard=kb, send_separately=True)

        # Конфликтов нет — формируем обычное подтверждение
        # Время окончания показываем только если у задачи есть реальный срок
        display_end_time = get_display_end_time(localized_dt, command.duration) if display_time else None
        confirm_text = TaskMessages.task_created(
            content=capitalized_content,
            display_time=display_time,
            details=capitalized_details,
            display_end_time=display_end_time,
            importance=command.importance,
        )

        # Синхронизация с Notion (если пользователь явно запросил add_to_notion)
        if command.add_to_notion:
            new_task = await self.task_repo.get_by_id(new_task_id)
            if new_task:
                await self.notion_service.add_single_task_to_notion(new_task)
                confirm_text += TaskMessages.notion_task_added()

        return ActionResult(text=confirm_text, task_time=command.time)

    async def update(self, command: TaskActionSchema) -> ActionResult:
        """
        Обновляет параметры существующей задачи в репозитории
        и синхронизирует изменения в планировщике и Notion.

        Args:
            command (TaskActionSchema): Параметры изменения.

        Returns:
            ActionResult: Подтверждение обновления.
        """
        task_id = command.task_id or (command.task_ids[0] if command.task_ids else None)
        if not task_id:
            return ActionResult(text=TaskMessages.task_update_id_missing())

        task = await self.task_repo.get_by_id(task_id)
        if not task:
            return ActionResult(text=TaskMessages.task_not_found())

        # Защита: редактировать можно только свои задачи
        if task["user_id"] != self.user["id"]:
            return ActionResult(text=TaskMessages.task_update_access_denied())

        new_time_timestamp = task["time"]
        # Если задача уже была без срока — показываем «без срока», а не 2060 год
        if is_fallback_timestamp(task["time"]):
            display_time = None
        else:
            display_time = datetime.fromtimestamp(task["time"], self.tz).strftime("%Y-%m-%d %H:%M")

        # Пересчитываем время начала при необходимости
        if command.time is not None:
            try:
                naive_dt = datetime.strptime(command.time, "%Y-%m-%d %H:%M")
                localized_dt = self.tz.localize(naive_dt)
                new_time_timestamp = int(localized_dt.timestamp())
                display_time = command.time
            except Exception:
                return ActionResult(text=TaskMessages.invalid_update_time_format())
        else:
            localized_dt = datetime.fromtimestamp(new_time_timestamp, self.tz)

        new_duration = command.duration if command.duration is not None else task.get("duration")
        new_importance = command.importance if command.importance is not None else task.get("importance")

        new_content = capitalize_first(command.content) if command.content is not None else task["content"]
        new_details = capitalize_first(command.details) if command.details is not None else task.get("details")

        # Сохраняем изменения через репозиторий
        await self.task_repo.update(
            task_id,
            content=new_content,
            details=new_details,
            time=new_time_timestamp,
            duration=new_duration,
            importance=new_importance,
            notion_status=command.status,
            notion_multi_select=command.multi_select,
        )

        # Обновляем напоминание в планировщике
        self.scheduler_service.update_scheduler_jobs(
            task_id=task_id,
            content=new_content,
            details=new_details,
            localized_dt=localized_dt,
            duration=new_duration,
            importance=new_importance,
        )

        # Получаем обновлённую задачу для синхронизации с Notion
        updated_task = await self.task_repo.get_by_id(task_id)
        notion_was_updated = False
        if updated_task and updated_task.get("notion_added") == 1:
            await self.notion_service.update_task_in_notion(updated_task)
            notion_was_updated = True

        # Время окончания показываем только если у задачи есть реальный срок
        display_end_time = get_display_end_time(localized_dt, new_duration) if display_time else None
        confirm_text = TaskMessages.task_updated(
            content=new_content,
            display_time=display_time,
            details=new_details,
            display_end_time=display_end_time,
            importance=new_importance,
        )

        # Если статус был обновлён, добавляем название статуса в подтверждение
        if command.status is not None:
            confirm_text += TaskMessages.status_updated_notification(command.status)

        # Если задача была синхронизирована с Notion — уведомляем пользователя
        if notion_was_updated:
            confirm_text += TaskMessages.notion_task_updated()

        return ActionResult(text=confirm_text, task_time=command.time)

    async def select(self, command: TaskActionSchema) -> ActionResult:
        """
        Ищет задачи и возвращает их список с пагинацией.

        Args:
            command (TaskActionSchema): Параметры поиска.

        Returns:
            ActionResult: Результаты поиска с кнопками навигации.
        """
        if not command.task_ids:
            return ActionResult(text=TaskMessages.search_empty())

        # Сохраняем историю поиска через репозиторий
        await self.search_repo.save(
            user_id=self.user["id"],
            task_ids=command.task_ids,
            query=command.content or "поиск",
        )

        limit = TASKS_LIMIT_OF_PAGES
        total_count = len(command.task_ids)

        # Достаём первую страницу задач из репозитория
        tasks = await self.task_repo.get_by_ids(
            user_id=self.user["id"],
            ids=command.task_ids,
            limit=limit,
            offset=0,
        )

        if not tasks:
            return ActionResult(text=TaskMessages.search_not_found(), task_time=command.time)

        response_text = TaskMessages.search_results(
            query=command.content or "поиск", tasks=tasks, tz=self.tz
        )

        # Если задач больше, чем лимит страницы — добавляем индикатор пагинации
        if total_count > limit:
            lang = user_lang.get()
            page_word = "Page" if lang == "en" else "Страница"
            from_word = "of" if lang == "en" else "из"
            total_pages = (total_count + limit - 1) // limit
            response_text += f"\n\n<i>{page_word} 1 {from_word} {total_pages}</i>"

        kb = get_pagination_keyboard(total_count, 1, limit, "page_select")

        return ActionResult(
            text=response_text,
            keyboard=kb or get_main_kb(),
            send_separately=True,
            task_time=command.time,
        )

    async def delete(self, command: TaskActionSchema) -> ActionResult:
        """
        Завершает (удаляет) указанные задачи, стирая напоминания и обновляя статус в Notion.

        Args:
            command (TaskActionSchema): Запрос на удаление.

        Returns:
            ActionResult: Текст подтверждения выполнения.
        """
        # Объединяем task_id и task_ids в единый список без дублей
        task_ids: list[int] = []
        if command.task_id:
            task_ids.append(command.task_id)
        if command.task_ids:
            for tid in command.task_ids:
                if tid not in task_ids:
                    task_ids.append(tid)

        if not task_ids:
            return ActionResult(text=TaskMessages.task_delete_id_missing())

        completed_titles: list[str] = []
        not_found_count = 0
        denied_count = 0

        for tid in task_ids:
            task = await self.task_repo.get_by_id(tid)
            if not task:
                not_found_count += 1
                continue
            if task["user_id"] != self.user["id"]:
                denied_count += 1
                continue

            # Помечаем задачу как выполненную в репозитории
            await self.task_repo.complete(tid)
            # Удаляем напоминание из планировщика
            self.scheduler_service.remove_scheduler_jobs(tid)
            # Синхронизируем изменение статуса с Notion
            await self.notion_service.sync_task_status_to_notion(task, "complete")
            completed_titles.append(task["content"])

        if not completed_titles:
            if denied_count > 0:
                return ActionResult(text=TaskMessages.task_delete_access_denied())
            elif not_found_count > 0:
                return ActionResult(text=TaskMessages.task_not_found())

        if len(completed_titles) == 1:
            return ActionResult(text=TaskMessages.task_completed(completed_titles[0]), task_time=command.time)

        return ActionResult(text=TaskMessages.tasks_completed_plural(completed_titles), task_time=command.time)
