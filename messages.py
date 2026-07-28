
from aiogram.utils.markdown import html_decoration as hd
from utils.context import user_lang
from utils.formatters import format_tasks_list
from utils.formatters import format_importance


class StartMessages:

    @classmethod
    def welcome(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": (
                "👋 <b>Добро пожаловать в умный менеджер задач!</b>\n\n"
                "Я помогу тебе планировать дела прямо из Telegram — голосом или текстом. "
                "Всё, что ты говоришь, я понимаю и сохраняю в твою базу <b>Notion</b>.\n\n"

                "━━━━━━━━━━━━━━━━━━━━\n"
                "🚀 <b>С чего начать?</b>\n\n"
                "1️⃣ <b>Подключи Notion</b> — введи команду /add_notion и следуй инструкции. "
                "Тебе нужно будет вставить токен интеграции Notion и ссылку на базу данных.\n\n"
                "2️⃣ <b>Выбери язык</b> — по умолчанию стоит русский. "
                "Чтобы переключиться на английский, введи /change_language.\n\n"
                "3️⃣ <b>Начни добавлять задачи</b> — просто напиши или надиктуй, что нужно сделать!\n\n"
                "4️⃣ <b>Синхронизируй задачи из Notion</b> — если ты уже ведёшь базу в Notion "
                "и хочешь подтянуть актуальные задачи прямо в бота, введи команду /fetch_notion_tasks. "
                "Я загружу все незавершённые задачи из твоей базы данных и буду учитывать их при напоминаниях.\n\n"

                "━━━━━━━━━━━━━━━━━━━━\n"
                "🛠 <b>Что я умею:</b>\n\n"

                "📝 <b>Создавать задачи в Notion:</b>\n"
                "• <i>«Напомни позвонить маме завтра в 18:00»</i>\n"
                "• <i>«Встреча с командой в пятницу в 10:00, высокий приоритет»</i>\n"
                "• <i>«Сдать отчёт до конца недели»</i>\n\n"

                "🏷 <b>Указывать любые свойства задачи:</b>\n"
                "Просто упомяни в сообщении — и я сам заполню нужные поля:\n"
                "• <b>Дату и время</b> — <i>«завтра в 15:00»</i>, <i>«в следующий понедельник»</i>\n"
                "• <b>Приоритет</b> — <i>«срочно»</i>, <i>«высокий приоритет»</i>, <i>«не к спеху»</i>\n"
                "• <b>Длительность</b> — <i>«на 2 часа»</i>, <i>«45 минут»</i>\n"
                "• <b>Детали</b> — <i>«подготовить слайды, отправить на почту»</i>\n"
                "• <b>Статус</b> — <i>«Поменяй на статус To do today»</i>\n\n"

                "🔔 <b>Напоминать о задачах:</b>\n"
                "Когда наступит время задачи, я напомню тебе простым текстом с содержанием задачи\n\n"

                "💬 <b>Добавлять комментарии к задачам</b> <i>(в разработке)</i>:\n"
                "• <i>«Добавь к задаче про встречу: взять с собой ноутбук»</i>\n\n"

                "🔄 <b>Изменять задачи:</b>\n"
                "• <i>«Перенеси встречу с командой на 12:00»</i>\n"
                "• <i>«Измени приоритет задачи про отчёт на высокий»</i>\n\n"

                "✅ <b>Завершать и удалять:</b>\n"
                "• <i>«Я купил хлеб, отметь задачу выполненной»</i>\n"
                "• <i>«Удали задачу про звонок маме»</i>\n\n"

                "🔍 <b>Искать и просматривать:</b>\n"
                "• <i>«Что у меня запланировано на завтра?»</i>\n"
                "• <i>«Покажи все срочные задачи»</i>\n\n"

                "🎙 <b>Голосовые сообщения:</b>\n"
                "Всё то же самое можно надиктовать голосом — я пойму.\n\n"

                "━━━━━━━━━━━━━━━━━━━━\n"
                "<b>Гигиена задач — важно!</b>\n\n"
                "⚠️ <b>При накоплении 2000+ задач ИИ начинает галлюционировать</b> — "
                "неправильно обрабатывать команды. "
                "Поэтому важно регулярно чистить базу от старых и выполненных задач.\n\n"
                "🗂 <b>Как навести порядок:</b>\n"
                "• Нажми кнопку <b>«Просроченные задачи»</b> под клавиатурой — "
                "там отображаются все задачи с истёкшей датой. "
                "Ты можешь просмотреть их, отметить выполненными или сразу удалить ненужные.\n"
                "• Чтобы удалить все задачи, которые ты уже отметил выполненными в Notion, "
                "просто нажми кнопку: <i>«Синхронизировать выполненные задачи из Notion»</i> — "
                "и я очищу их из базы одной командой.\n\n"
                
                "━━━━━━━━━━━━━━━━━━━━\n"
                "👇 Используй кнопки под клавиатурой, чтобы быстро просмотреть активные, "
                "завершённые или просроченные задачи."
            ),
            "en": (
                "👋 <b>Welcome to your Smart Task Manager!</b>\n\n"
                "I will help you plan your tasks right from Telegram — using voice or text. "
                "Everything you say will be processed and saved directly into your <b>Notion</b> database.\n\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "🚀 <b>How to start?</b>\n\n"
                "1️⃣ <b>Connect Notion</b> — type /add_notion and follow the instructions. "
                "You will need to paste your Notion integration token and database link.\n\n"
                "2️⃣ <b>Choose language</b> — Russian is set by default. "
                "To switch to English, type /change_language.\n\n"
                "3️⃣ <b>Start adding tasks</b> — just type or record what needs to be done!\n\n"
                "4️⃣ <b>Sync tasks from Notion</b> — if you already manage your tasks in Notion "
                "and want to pull them into the bot, use the /fetch_notion_tasks command. "
                "I will load all your incomplete tasks from the database and include them in reminders.\n\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "🛠 <b>What I can do:</b>\n\n"
                "📝 <b>Create tasks in Notion:</b>\n"
                "• <i>\"Remind me to call mom tomorrow at 6 PM\"</i>\n"
                "• <i>\"Team meeting on Friday at 10:00, high priority\"</i>\n"
                "• <i>\"Submit the report by the end of the week\"</i>\n\n"
                "🏷 <b>Set any task properties:</b>\n"
                "Just mention them in your message, and I will fill in the fields for you:\n"
                "• <b>Date and time</b> — <i>\"tomorrow at 15:00\"</i>, <i>\"next Monday\"</i>\n"
                "• <b>Priority</b> — <i>\"urgent\"</i>, <i>\"high priority\"</i>, <i>\"low priority\"</i>\n"
                "• <b>Duration</b> — <i>\"for 2 hours\"</i>, <i>\"45 minutes\"</i>\n"
                "• <b>Details</b> — <i>\"prepare slides, send via email\"</i>\n"
                "• <b>Status</b> — <i>\"Change status to To do today\"</i>\n\n"
                "🔔 <b>Remind you about tasks:</b>\n"
                "When the time comes, I will send you a simple text reminder containing the task details.\n\n"
                "💬 <b>Add comments to tasks</b> <i>(in development)</i>:\n"
                "• <i>\"Add to the meeting task: bring a laptop\"</i>\n\n"
                "🔄 <b>Modify tasks:</b>\n"
                "• <i>\"Reschedule the team meeting to 12:00\"</i>\n"
                "• <i>\"Change the priority of the report task to high\"</i>\n\n"
                "✅ <b>Complete and delete:</b>\n"
                "• <i>\"I bought bread, mark the task as done\"</i>\n"
                "• <i>\"Delete the task about calling mom\"</i>\n\n"
                "🔍 <b>Search and view:</b>\n"
                "• <i>\"What do I have planned for tomorrow?\"</i>\n"
                "• <i>\"Show all urgent tasks\"</i>\n\n"
                "🎙 <b>Voice messages:</b>\n"
                "You can record all of the above via voice — I will understand.\n\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "<b>Task hygiene — important!</b>\n\n"
                "⚠️ <b>When you accumulate 2000+ tasks, the AI starts to hallucinate</b> — "
                "commands may be executed incorrectly."
                "It is important to regularly clean up old and completed tasks.\n\n"
                "🗂 <b>How to tidy up:</b>\n"
                "• Tap the <b>\"Overdue tasks\"</b> button in the reply keyboard — "
                "it shows all tasks with a past due date. "
                "You can review them, mark them as complete, or delete the ones you no longer need.\n"
                "• To remove all tasks you have already marked as done in Notion, "
                "simply press button: <i>\"Sync completed tasks from Notion\"</i> — "
                "and I will wipe them from the database in one go.\n\n"
                
                "━━━━━━━━━━━━━━━━━━━━\n"
                "👇 Use the reply keyboard buttons below to quickly view active, "
                "completed, or overdue tasks."
            ),
        }
        return translations.get(lang, translations["ru"])


class TaskMessages:
    @classmethod
    def tasks_empty(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": "У вас пока нет запланированных задач. Напишите любую задачу, например \"Написать отчет\"",
            "en": "You have no scheduled tasks yet. Write any task, for example \"Write an essay\""
        }
        return translations.get(lang, translations["ru"])


    @classmethod
    def completed_tasks_empty(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": "У вас пока нет выполненных задач.",
            "en": "You have no completed tasks yet."
        }
        return translations.get(lang, translations["ru"])


    @classmethod
    def today_tasks_empty(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": "У вас нет задач на сегодня.",
            "en": "You have no tasks for today."
        }
        return translations.get(lang, translations["ru"])


    @classmethod
    def invalid_request(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": "Некорректный запрос",
            "en": "Invalid request"
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def invalid_time_format(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": "Некорректный формат времени от ИИ",
            "en": "Invalid time format from AI"
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def task_completed_success(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": "Задача успешно выполнена!",
            "en": "Task successfully completed!"
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def task_delayed_success(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": "Задача отложена на 15 минут!",
            "en": "Task delayed by 15 minutes!"
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def task_created(cls, content: str, display_time: str | None, details: str = None, display_end_time: str = None, importance: str = None, notion_status: str = None, notion_multi_select: str = None) -> str:
        lang = user_lang.get()
        escaped_content = hd.quote(content)
        # Локализованная метка для задачи без срока
        no_date_label = "без срока" if lang != "en" else "no due date"
        time_str = display_time if display_time else no_date_label
        translations = {
            "ru": {
                "header": f"<code>СОЗДАНО</code>\n<b>{escaped_content}</b> {time_str}\n",
                "until": f"До {display_end_time}",
                "status": "Статус",
                "sprint": "Спринт"
            },
            "en": {
                "header": f"<code>CREATED</code>\n<b>{escaped_content}</b> {time_str}\n",
                "until": f"Until {display_end_time}",
                "status": "Status",
                "sprint": "Sprint"
            },
        }
        t = translations.get(lang, translations["ru"])
        

        imp_str = format_importance(importance, lang)
        
        text = t["header"]
        if imp_str:
            text = f"{imp_str} " + text
        # Окончание времени показываем только если есть реальный срок
        if display_end_time and display_time:
            text += t["until"]
            
        if notion_status:
            text += f"\n• {t['status']}: <code>{hd.quote(notion_status)}</code>"
        if notion_multi_select:
            text += f"\n• {t['sprint']}: <code>{hd.quote(notion_multi_select)}</code>"

        if details:
            escaped_details = hd.quote(details)
            text += f"\n<i>{escaped_details}</i>"
        return text

    @classmethod
    def task_update_id_missing(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": "Не удалось определить, какую именно задачу нужно изменить.",
            "en": "Failed to identify which specific task to modify."
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def task_not_found(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": "Задача с таким ID не найдена.",
            "en": "Task with this ID not found."
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def task_update_access_denied(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": "У вас нет прав на редактирование этой задачи.",
            "en": "You do not have permission to edit this task."
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def invalid_update_time_format(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": "Некорректный формат времени от ИИ при обновлении.",
            "en": "Invalid time format from AI during update."
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def task_updated(cls, content: str, display_time: str | None, details: str = None, display_end_time: str = None, importance: str = None, notion_status: str = None, notion_multi_select: str = None) -> str:
        lang = user_lang.get()
        escaped_content = hd.quote(content)
        # Локализованная метка для задачи без срока
        no_date_label = "без срока" if lang != "en" else "no due date"
        time_str = display_time if display_time else no_date_label
        translations = {
            "ru": {
                "header": f"<code>ОБНОВЛЕНО</code>\n<b>{escaped_content}</b> {time_str}\n",
                "until": f"До {display_end_time}",
                "status": "Статус",
                "sprint": "Спринт"
            },
            "en": {
                "header": f"<code>UPDATED</code>\n<b>{escaped_content}</b> {time_str}\n",
                "until": f"Until {display_end_time}",
                "status": "Status",
                "sprint": "Sprint"
            },
        }
        t = translations.get(lang, translations["ru"])
        
        from utils.formatters import format_importance
        imp_str = format_importance(importance, lang)
        
        text = t["header"]
        if imp_str:
            text = f"{imp_str} " + text
        # Окончание времени показываем только если есть реальный срок
        if display_end_time and display_time:
            text += t["until"]

        if notion_status:
            text += f"\n• {t['status']}: <code>{hd.quote(notion_status)}</code>"
        if notion_multi_select:
            text += f"\n• {t['sprint']}: <code>{hd.quote(notion_multi_select)}</code>"

        if details:
            escaped_details = hd.quote(details)
            text += f"\n<i>{escaped_details}</i>"
        return text

    @classmethod
    def status_updated_notification(cls, status_name: str) -> str:
        # Возвращает строку уведомления о смене статуса задачи
        lang = user_lang.get()
        status_upper = status_name.upper()
        translations = {
            "ru": f"\n• СТАТУС: {status_upper}",
            "en": f"\n• STATUS: {status_upper}"
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def notion_task_added(cls) -> str:
        """Уведомление о том, что задача была добавлена в Notion."""
        lang = user_lang.get()
        translations = {
            "ru": "\nДобавлено в Notion",
            "en": "\nAdded to Notion"
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def notion_task_updated(cls) -> str:
        """Уведомление о том, что задача была обновлена в Notion."""
        lang = user_lang.get()
        translations = {
            "ru": "\nОбновлено в Notion",
            "en": "\nUpdated in Notion"
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def search_empty(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": "По вашему запросу ничего не найдено.",
            "en": "Nothing found for your request."
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def search_not_found(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": "Задачи не найдены или у вас нет к ним доступа.",
            "en": "Tasks not found or you do not have access to them."
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def search_results(cls, query: str, tasks: list, tz) -> str:
        lang = user_lang.get()
        escaped_query = hd.quote(query)
        translations = {
            "ru": {
                "header": f"<b>Результаты поиска по запросу '{escaped_query}':</b>",
            },
            "en": {
                "header": f"<b>Search results for '{escaped_query}':</b>",
            },
        }
        t = translations.get(lang, translations["ru"])
        

        formatted_list = format_tasks_list(tasks, tz, lang)
        
        return f"{t['header']}\n\n{formatted_list}"

    @classmethod
    def task_delete_id_missing(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": "Не удалось определить, какую именно задачу нужно завершить.",
            "en": "Failed to identify which specific task to complete."
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def task_delete_access_denied(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": "У вас нет прав на завершение этой задачи.",
            "en": "You do not have permission to complete this task."
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def task_completed(cls, content: str) -> str:
        lang = user_lang.get()
        escaped_content = hd.quote(content)
        translations = {
            "ru": f"<code>✅ ВЫПОЛНЕНО</code>\n<b>{escaped_content}</b>",
            "en": f"<code>✅ COMPLETED</code>\n<b>{escaped_content}</b>",
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def tasks_completed_plural(cls, completed_titles: list) -> str:
        lang = user_lang.get()
        tasks_list_str = ", ".join(f"\"{title}\"" for title in completed_titles)
        translations = {
            "ru": f"<code>✅ ВЫПОЛНЕНО</code>\n{tasks_list_str}",
            "en": f"<code>✅ COMPLETED</code>\n{tasks_list_str}",
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def task_notification(cls, content: str, details: str = None, importance: str = None) -> str:
        lang = user_lang.get()
        escaped_content = hd.quote(content)
        translations = {
            "ru": {
                "header": f"{escaped_content}",
            },
            "en": {
                "header": f"🔔 <b>Reminder:</b>\n{escaped_content}",
            },
        }
        t = translations.get(lang, translations["ru"])

        imp_str = format_importance(importance, lang)
        
        text = t["header"]
        if imp_str:
            text = f"{imp_str} " + text
            
        if details:
            escaped_details = hd.quote(details)
            text += f"\n<i>{escaped_details}</i>"
        return text

    @classmethod
    def conflict_warning(cls, new_task_content: str, new_task_time: str, old_task_content: str, old_task_time: str) -> str:
        lang = user_lang.get()
        escaped_new = hd.quote(new_task_content)
        escaped_old = hd.quote(old_task_content)
        translations = {
            "ru": (
                f"Внимание! {old_task_time} уже занято другой задачей <b>{escaped_old}</b>."
                ),
            "en": (
                f"Warning! {old_task_time} is already occupied by another task <b>{escaped_old}</b>."
            )
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def conflict_resolved_move_old(cls, new_title: str, new_time: str, old_title: str, old_new_time: str) -> str:
        lang = user_lang.get()
        escaped_new = hd.quote(new_title)
        escaped_old = hd.quote(old_title)
        translations = {
            "ru": (
                f"Новая задача <b>{escaped_new}</b> успешно запланирована на выбранное время <b>{new_time}</b>.\n"
                f"Старая задача <b>{escaped_old}</b> перенесена на ближайшее свободное время: <b>{old_new_time}</b>."
            ),
            "en": (
                f"New task <b>{escaped_new}</b> is successfully scheduled at the requested time <b>{new_time}</b>.\n"
                f"Old task <b>{escaped_old}</b> has been moved to the nearest free time: <b>{old_new_time}</b>."
            )
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def conflict_resolved_move_new(cls, new_title: str, new_time: str, old_title: str, old_time: str) -> str:
        lang = user_lang.get()
        escaped_new = hd.quote(new_title)
        escaped_old = hd.quote(old_title)
        translations = {
            "ru": (
                f"Старая задача <b>{escaped_old}</b> сохранена на <b>{old_time}</b>.\n"
                f"Новая задача <b>{escaped_new}</b> перенесена на ближайшее свободное время: <b>{new_time}</b>."
            ),
            "en": (
                f"Old task <b>{escaped_old}</b> remains scheduled at <b>{old_time}</b>.\n"
                f"New task <b>{escaped_new}</b> has been moved to the nearest free time: <b>{new_time}</b>."
            )
        }
        return translations.get(lang, translations["ru"])


    @classmethod
    def conflict_ignore(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": "Задачи оставлены параллельно на это время. Расписание сохранено.",
            "en": "Tasks were saved parallely by this time. Schedule were saved."
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def conflict_task_not_found(cls):
        lang = user_lang.get()
        translations = {
            "ru": "Ошибка: одна из конфликтующих задач не найдена.",
            "en": "Error: One of conflict tasks not found."
        }
        return translations.get(lang, translations["ru"])


class AiMessages:
    @classmethod
    def listening(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": "Слушаю...",
            "en": "Listening..."
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def transcription_error(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": "Произошла ошибка при расшифровке аудио.",
            "en": "An error occurred during audio transcription."
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def thinking(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": "Думаю...",
            "en": "Thinking..."
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def no_tasks_found(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": "Не нашёл никаких задач в вашем сообщении. Попробуйте написать иначе.",
            "en": "Found no tasks in your message. Please try phrasing it differently."
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def execution_error(cls, error_detail: str | None) -> str:
        lang = user_lang.get()
        translations = {
            "ru": {
                "prefix": "Ошибка:",
                "default": "Действие не может быть выполнено (возможно, указана дата в прошлом).",
            },
            "en": {
                "prefix": "Error:",
                "default": "Action cannot be performed (possibly date is in the past).",
            },
        }
        t = translations.get(lang, translations["ru"])
        detail = hd.quote(error_detail) if error_detail else t["default"]
        return f"{t['prefix']} {detail}"

    @classmethod
    def unknown_action(cls, content: str) -> str:
        lang = user_lang.get()
        escaped_content = hd.quote(content)
        translations = {
            "ru": f"Не совсем понял, что нужно сделать с '<b>{escaped_content}</b>'.",
            "en": f"Did not completely understand what to do with '<b>{escaped_content}</b>'.",
        }
        return translations.get(lang, translations["ru"])


class LangMessages:
    @classmethod
    def lang_successfully_changed(cls, new_lang: str) -> str:
        lang = new_lang
        translations = {
            "ru": "Язык был успешно изменен!",
            "en": "Language successfully changed."
        }
        return translations.get(lang, translations["ru"])


class NotificationMessages:
    @classmethod
    def task_successfully_completed(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": "\n\n<code>Выполнено</code>",
            "en": "\n\n.<code>Completed</code>"
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def task_delayed(cls, new_time_dt) -> str:
        lang = user_lang.get()
        translations = {
            "ru": f"\n\n<b>Отложено на 15 минут</b> (до {new_time_dt.strftime('%H:%M')})",
            "en": f"\n\n<b>Delayed by 15 minutes</b> (until {new_time_dt.strftime('%H:%M')})"
        }

        return translations.get(lang, translations["ru"])


class NotionMessages:
    @classmethod
    def start_registration(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": (
                "<b>Регистрация Notion</b>\n\n"
                "Чтобы связать бота с вашим Notion, пожалуйста, отправьте ваш <b>Notion Integration Token</b> (Internal Integration Token).\n\n"
                "Вы можете создать интеграцию на странице <a href='https://www.notion.so/my-integrations'>notion.so/my-integrations</a>.\n\n"
                "Если вы хотите пропустить этот шаг, отправьте /skip или нажмите кнопку.\n"
                "Для отмены отправьте /cancel или нажмите кнопку."
            ),
            "en": (
                "<b>Notion Registration</b>\n\n"
                "To link the bot to your Notion, please send your <b>Notion Integration Token</b> (Internal Integration Token).\n\n"
                "You can create an integration at <a href='https://www.notion.so/my-integrations'>notion.so/my-integrations</a>.\n\n"
                "If you want to skip this step, send /skip or press the button.\n"
                "To cancel, send /cancel or press the button."
            )
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def invalid_token(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": (
                "<b>Неверный формат токена!</b>\n\n"
                "Токен Notion должен начинаться с <code>ntn_</code>.\n"
                "Пожалуйста, отправьте корректный токен, пропустите шаг с помощью /skip или отмените регистрацию с помощью /cancel."
            ),
            "en": (
                "<b>Invalid token format!</b>\n\n"
                "Notion token must start with <code>ntn_</code>.\n"
                "Please send a valid token, skip this step with /skip, or cancel with /cancel."
            )
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def ask_db_id(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": (
                "<b>Укажите ID или ссылку на базу данных Notion</b>\n\n"
                "Пожалуйста, отправьте ссылку на вашу базу данных задач Notion или её ID.\n"
                "ID автоматически извлечётся из ссылки вида:\n"
                "<code>https://www.notion.so/[DATABASE_ID]?v=...</code>\n\n"
                "Не забудьте поделиться (Share) вашей базой данных с созданной интеграцией в самом Notion!\n\n"
                "Отправьте ссылку/ID, пропустите шаг с помощью /skip или отмените с помощью /cancel."
            ),
            "en": (
                "<b>Provide Notion Database ID or URL</b>\n\n"
                "Please send the URL of your Notion tasks database or its ID.\n"
                "The ID will be automatically extracted from URLs like:\n"
                "<code>https://www.notion.so/[DATABASE_ID]?v=...</code>\n\n"
                "Don't forget to share your database with the created integration in Notion!\n\n"
                "Send the URL/ID, skip with /skip, or cancel with /cancel."
            )
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def invalid_db_id(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": (
                "<b>Не удалось найти ID базы данных в вашем сообщении!</b>\n\n"
                "Убедитесь, что вы отправили корректную ссылку Notion или 32-значный ID (состоящий из букв a-f и цифр).\n"
                "Пожалуйста, попробуйте снова, пропустите шаг (/skip) или отмените (/cancel)."
            ),
            "en": (
                "<b>Could not find Database ID in your message!</b>\n\n"
                "Make sure you sent a valid Notion URL or a 32-character hex ID (consisting of letters a-f and digits).\n"
                "Please try again, skip this step (/skip), or cancel (/cancel)."
            )
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def connection_failed(cls, error_msg: str) -> str:
        lang = user_lang.get()
        translations = {
            "ru": (
                "<b>Не удалось связаться с Notion!</b>\n\n"
                f"Ошибка от Notion: <code>{error_msg}</code>\n\n"
                "Пожалуйста, убедитесь, что:\n"
                "1. Токен интеграции скопирован без ошибок.\n"
                "2. Ссылка/ID базы данных указаны верно.\n"
                "3. <b>Важно:</b> Вы открыли доступ интеграции к этой базе данных в Notion (через Connections в верхнем правом меню базы данных).\n\n"
                "Давайте попробуем настроить заново. Пожалуйста, отправьте ваш Notion Integration Token:"
            ),
            "en": (
                "<b>Failed to connect to Notion!</b>\n\n"
                f"Error from Notion: <code>{error_msg}</code>\n\n"
                "Please ensure that:\n"
                "1. The integration token is copied correctly.\n"
                "2. The database URL/ID is correct.\n"
                "3. <b>Important:</b> You have granted connection access to the integration on the database page in Notion.\n\n"
                "Let's start the configuration again. Please send your Notion Integration Token:"
            )
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def verifying_connection(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": "<b>Проверяем соединение с Notion...</b> Пожалуйста, подождите.",
            "en": "<b>Checking connection with Notion...</b> Please wait."
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def registration_cancelled(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": "Регистрация Notion отменена.",
            "en": "Notion registration cancelled."
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def registration_success(
        cls, 
        token: str | None, 
        db_id: str | None, 
        created_status: str | None = None,
        completed_status: str | None = None,
        db_name: str | None = None
    ) -> str:
        lang = user_lang.get()
        token_str = token[:4] + "..." + token[-4:] if token else "—"
        db_id_str = db_id if db_id else "—"
        
        # Если имя источника данных переданно, показываем его вместе с ID
        if db_name:
            db_display = f"{db_name} (<code>{db_id_str}</code>)"
        else:
            db_display = f"<code>{db_id_str}</code>"

        created_str = created_status if created_status else "—"
        completed_str = completed_status if completed_status else "—"
        translations = {
            "ru": (
                "<b>Регистрация Notion успешно завершена!</b>\n\n"
                f"• Ключ интеграции: <code>{token_str}</code>\n"
                f"• Источник данных: {db_display}\n"
                f"• Статус при создании: <code>{created_str}</code>\n"
                f"• Статус при выполнении: <code>{completed_str}</code>\n\n"
                "Все настройки сохранены. Теперь ваши задачи будут синхронизироваться с Notion."
            ),
            "en": (
                "<b>Notion registration completed successfully!</b>\n\n"
                f"• Integration Key: <code>{token_str}</code>\n"
                f"• Data Source: {db_display}\n"
                f"• Creating status: <code>{created_str}</code>\n"
                f"• Completion status: <code>{completed_str}</code>\n\n"
                "All settings saved. Now your tasks will synchronize with Notion."
            )
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def ask_notified_status(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": "Выберите статус в Notion, который будет устанавливаться для задачи, когда на неё пришло уведомление:",
            "en": "Select the Notion status to be set for a task when a notification for it arrives:"
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def ask_created_status(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": "Выберите статус в Notion, который будет устанавливаться для задачи при её создании:",
            "en": "Select the Notion status to be set for a task when it is created:"
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def ask_completed_status(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": "Выберите статус в Notion, который будет устанавливаться для выполненных задач:",
            "en": "Select the Notion status to be set for completed tasks:"
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def invalid_status_selection(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": "Пожалуйста, выберите один из статусов на клавиатуре или введите его имя точно так же, как написано.",
            "en": "Please select one of the statuses on the keyboard or type its name exactly as written."
        }
        return translations.get(lang, translations["ru"])


    @classmethod
    def not_configured(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": (
                "Notion не подключён. Используйте /start_registration, "
                "чтобы привязать свою базу данных."
            ),
            "en": (
                "Notion is not connected. Use /start_registration "
                "to link your database."
            ),
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def no_tasks_to_send(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": "Не смог определить, какие задачи отправить в Notion.",
            "en": "Could not determine which tasks to send to Notion.",
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def tasks_sent(cls, success_count: int, total: int, errors: list) -> str:
        lang = user_lang.get()
        if lang == "en":
            text = f"<b>Sent to Notion: {success_count}/{total}</b>"
            if errors:
                joined = "\n".join(f"• {e}" for e in errors[:3])
                text += f"\n\nErrors:\n{joined}"
        else:
            text = f"<b>Отправлено в Notion: {success_count}/{total}</b>"
            if errors:
                joined = "\n".join(f"• {e}" for e in errors[:3])
                text += f"\n\nОшибки:\n{joined}"
        return text

    @classmethod
    def ask_notion_user(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": (
                "<b>Выберите свой аккаунт в списке участников Notion:</b>\n\n"
                "Вы также можете отправить свою почту или имя сообщением, чтобы быстро найти себя."
            ),
            "en": (
                "<b>Select your account from the Notion participants list:</b>\n\n"
                "You can also send your email or name as a message to quickly find yourself."
            )
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def notion_users_found(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": "<b>Найденные участники:</b>",
            "en": "<b>Found participants:</b>"
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def notion_user_not_found_retry(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": "<b>Участник с такой почтой или именем не найден.</b>\n\nПожалуйста, попробуйте ввести другое имя или email для поиска:",
            "en": "<b>Participant with this email or name not found.</b>\n\nPlease try entering another name or email for search:"
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def notion_users_loaded_search_prompt(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": (
                "<b>Список участников загружен!</b>\n\n"
                "Пожалуйста, введите имя или email участника Notion (или его часть) для поиска:"
            ),
            "en": (
                "<b>Participants list loaded!</b>\n\n"
                "Please enter the Notion participant's name or email (or part of it) to search:"
            )
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def notion_users_loading(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": "⏳ Получение списка участников из Notion... Пожалуйста, подождите.",
            "en": "⏳ Retrieving participants list from Notion... Please wait."
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def notion_users_empty(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": "<b>Не удалось найти активных участников в Notion!</b>\n\nУбедитесь, что у вашей интеграции включены разрешения (Capabilities) на чтение пользователей.",
            "en": "<b>Could not find active participants in Notion!</b>\n\nMake sure your integration has read users permissions (Capabilities) enabled."
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def notion_user_approval_pending(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": "<b>Запрос отправлен!</b>\n\nВаш запрос на привязку аккаунта Notion отправлен администраторам на одобрение. Бот уведомит вас, как только запрос будет одобрен.",
            "en": "<b>Request sent!</b>\n\nYour Notion account linking request has been sent to admins for approval. The bot will notify you as soon as it is approved."
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def notion_user_approved_user(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": "🎉 <b>Ваша интеграция с Notion одобрена администратором!</b>\n\nТеперь вы можете полноценно пользоваться ботом и синхронизировать задачи.",
            "en": "🎉 <b>Your Notion integration has been approved by the admin!</b>\n\nNow you can fully use the bot and sync tasks."
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def notion_user_rejected_user(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": "❌ <b>Ваш запрос на интеграцию с Notion был отклонен администратором.</b>\n\nПожалуйста, свяжитесь с администрацией или попробуйте привязать заново.",
            "en": "❌ <b>Your Notion integration request was rejected by the admin.</b>\n\nPlease contact the administrator or try linking again."
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def notion_admin_approval_request(cls, username: str | None, notion_user_name: str) -> str:
        lang = user_lang.get()
        user_str = f"@{username}" if username else "Пользователь без username"
        translations = {
            "ru": f"{user_str} пытается войти в ноушн под именем {notion_user_name}",
            "en": f"{user_str} is trying to log in to Notion as {notion_user_name}"
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def notion_admin_approved(cls, username: str | None, notion_user_name: str) -> str:
        lang = user_lang.get()
        user_str = f"@{username}" if username else "Пользователь"
        translations = {
            "ru": f"Запрос одобрен: {user_str} вошел в ноушн под именем {notion_user_name}",
            "en": f"Request approved: {user_str} logged in to Notion as {notion_user_name}"
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def notion_admin_rejected(cls, username: str | None, notion_user_name: str) -> str:
        lang = user_lang.get()
        user_str = f"@{username}" if username else "Пользователь"
        translations = {
            "ru": f"Запрос отклонен для {user_str} (Ноушн: {notion_user_name})",
            "en": f"Request rejected for {user_str} (Notion: {notion_user_name})"
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def ask_data_source(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": "<b>Мы нашли несколько источников данных (Data Sources) в вашей базе данных.</b>\n\nПожалуйста, выберите тот, который хотите использовать для синхронизации задач:",
            "en": "<b>We found multiple data sources in your database.</b>\n\nPlease select the one you want to use for task synchronization:"
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def no_data_sources_found(cls) -> str:
        lang = user_lang.get()
        translations = {
            "ru": "<b>Источники данных не найдены!</b>\n\nВ указанной базе данных не найдено ни одного источника данных. Пожалуйста, убедитесь, что база данных содержит таблицы/источники.",
            "en": "<b>No data sources found!</b>\n\nNo data sources were found in the specified database. Please make sure the database contains tables/sources."
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def data_source_selected(cls, name: str) -> str:
        lang = user_lang.get()
        translations = {
            "ru": f"Выбран источник данных: <b>{name}</b>",
            "en": f"Selected data source: <b>{name}</b>"
        }
        return translations.get(lang, translations["ru"])


class NotionCommentMessages:
    """Сообщения для операции добавления комментариев к задачам Notion."""

    @classmethod
    def comment_added(cls, task_content: str) -> str:
        """Подтверждение успешного добавления комментария."""
        lang = user_lang.get()
        escaped = hd.quote(task_content)
        translations = {
            "ru": f"Комментарий успешно добавлен к задаче <b>{escaped}</b> в Notion.",
            "en": f"Comment successfully added to task <b>{escaped}</b> in Notion."
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def comment_failed(cls) -> str:
        """Ошибка при добавлении комментария через Notion API."""
        lang = user_lang.get()
        translations = {
            "ru": (
                "Не удалось добавить комментарий в Notion.\n"
                "Убедитесь, что у интеграции включены разрешения "
                "<b>Read comments</b> и <b>Insert comments</b> в настройках Notion."
            ),
            "en": (
                "Failed to add comment to Notion.\n"
                "Make sure your integration has <b>Read comments</b> and "
                "<b>Insert comments</b> permissions enabled in Notion settings."
            )
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def page_not_found(cls) -> str:
        """Задача ещё не добавлена в Notion — нет notion_page_id."""
        lang = user_lang.get()
        translations = {
            "ru": (
                "⚠Эта задача ещё не добавлена в Notion — добавить комментарий невозможно.\n"
                "Сначала экспортируйте задачу в Notion, написав, например: "
                "<i>«Добавь в ноушн задачу N»</i>"
            ),
            "en": (
                "⚠This task has not been added to Notion yet — cannot add a comment.\n"
                "Export the task to Notion first, e.g.: "
                "<i>\"Add task N to Notion\"</i>"
            )
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def task_id_missing(cls) -> str:
        """ИИ не смог определить ID задачи для комментирования."""
        lang = user_lang.get()
        translations = {
            "ru": "Не удалось определить, к какой задаче добавить комментарий.",
            "en": "Could not determine which task to comment on."
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def comment_text_missing(cls) -> str:
        """Текст комментария отсутствует в команде."""
        lang = user_lang.get()
        translations = {
            "ru": (
                "Текст комментария не указан. "
                "Уточните, что именно написать, например:\n"
                "<i>«Добавь комментарий к задаче 2: обсудить с командой»</i>"
            ),
            "en": (
                "Comment text is missing. "
                "Please specify what to write, for example:\n"
                "<i>\"Add comment to task 2: discuss with the team\"</i>"
            )
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def not_configured(cls) -> str:
        """Notion не подключён — нет токена или ID базы данных."""
        lang = user_lang.get()
        translations = {
            "ru": (
                "Notion не подключён. Используйте /add_notion, "
                "чтобы привязать свою базу данных."
            ),
            "en": (
                "Notion is not connected. Use /add_notion "
                "to link your database."
            )
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def task_access_denied(cls) -> str:
        """Пользователь пытается прокомментировать чужую задачу."""
        lang = user_lang.get()
        translations = {
            "ru": "У вас нет прав на комментирование этой задачи.",
            "en": "You do not have permission to comment on this task."
        }
        return translations.get(lang, translations["ru"])

from utils.context import user_lang


class FetchNotionMessages:
    """Сообщения для команды /fetch_notion_tasks."""

    @classmethod
    def notion_not_configured(cls) -> str:
        """Notion не настроен у пользователя."""
        lang = user_lang.get()
        translations = {
            "ru": (
                "⚠<b>Notion не подключён.</b>\n\n"
                "Введите /add_notion, чтобы настроить интеграцию."
            ),
            "en": (
                "⚠<b>Notion is not connected.</b>\n\n"
                "Use /add_notion to set up the integration."
            ),
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def fetching_in_progress(cls) -> str:
        """Индикатор загрузки во время получения задач из Notion."""
        lang = user_lang.get()
        translations = {
            "ru": "Загружаю задачи из Notion...",
            "en": "Fetching tasks from Notion...",
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def fetch_result(cls, imported: int, skipped: int) -> str:
        """
        Результат импорта задач из Notion.

        Args:
            imported: Количество новых импортированных задач.
            skipped: Количество задач, пропущенных (уже в БД).
        """
        lang = user_lang.get()

        if lang == "en":
            if imported == 0:
                return (
                    "<b>Sync complete.</b>\n\n"
                    f"No new tasks found. "
                    f"<i>{skipped} task(s) already in your database.</i>\n\n"
                    "<i>Tasks without a date are saved without a due date "
                    "and won\u2019t trigger reminders.</i>"
                )
            return (
                "<b>Tasks imported from Notion!</b>\n\n"
                f"\u2022 Added: <b>{imported}</b>\n"
                f"\u2022 Already existed/completed: <b>{skipped}</b>\n\n"
                "<i>Tasks without a date are saved without a due date "
                "and won\u2019t trigger reminders.</i>"
            )

        # Русский вариант
        if imported == 0:
            return (
                "<b>Синхронизация завершена.</b>\n\n"
                f"Новых задач не найдено. "
                f"<i>{skipped} задач(-и) уже есть в вашей базе.</i>\n\n"
                "<i>Задачи без даты сохраняются без срока — напоминания по ним не придут.</i>"
            )
        return (
            "<b>Задачи из Notion импортированы!</b>\n\n"
            f"\u2022 Добавлено: <b>{imported}</b>\n"
            f"\u2022 Уже было/выполнено: <b>{skipped}</b>\n\n"
            "<i>Задачи без даты сохраняются без срока — напоминания по ним не придут.</i>"
        )

    @classmethod
    def fetch_error(cls) -> str:
        """Общая ошибка при получении задач из Notion."""
        lang = user_lang.get()
        translations = {
            "ru": (
                "<b>Не удалось получить задачи из Notion.</b>\n\n"
                "Проверьте токен и доступ к базе данных, затем попробуйте снова."
            ),
            "en": (
                "<b>Failed to fetch tasks from Notion.</b>\n\n"
                "Please check your token and database access, then try again."
            ),
        }
        return translations.get(lang, translations["ru"])


"""
Дополнение к messages.py.
Добавить класс DueTasksMessages в конец существующего messages.py.
"""

# ─────────────────────────────────────────────────────────────────────────────
# ВСТАВИТЬ В КОНЕЦ messages.py
# ─────────────────────────────────────────────────────────────────────────────


class DueTasksMessages:
    """
    Все тексты, связанные с просроченными задачами.
    Поддерживает мультиязычность: ru / en.
    """

    @classmethod
    def no_due_tasks(cls) -> str:
        """Сообщение когда просроченных задач нет."""
        lang = user_lang.get()
        translations = {
            "ru": "У вас нет просроченных задач.",
            "en": "You have no overdue tasks.",
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def due_tasks_header(cls, count: int) -> str:
        """
        Заголовок списка просроченных задач.

        Args:
            count: Количество просроченных задач.
        """
        lang = user_lang.get()
        translations = {
            "ru": (
                f"<b>Просроченные задачи: {count}</b>\n"
                "<i>Вы можете выполнить конкретную задачу вручную — "
                "просто напишите боту, например: «выполни задачу 3».</i>\n"
            ),
            "en": (
                f"⚠<b>Overdue tasks: {count}</b>\n"
                "<i>You can complete a specific task manually — "
                "just write, e.g.: \"complete task 3\".</i>\n"
            ),
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def complete_all_success(cls, count: int) -> str:
        """
        Подтверждение массового завершения просроченных задач.

        Args:
            count: Количество задач, помеченных выполненными.
        """
        lang = user_lang.get()
        translations = {
            "ru": f"Готово! Выполнено задач: <b>{count}</b>.",
            "en": f"Done! Tasks completed: <b>{count}</b>.",
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def complete_all_nothing(cls) -> str:
        """Нет задач для массового завершения."""
        lang = user_lang.get()
        translations = {
            "ru": "Просроченных активных задач не найдено.",
            "en": "No active overdue tasks found.",
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def syncing_with_notion(cls) -> str:
        """Нет задач для массового завершения."""
        lang = user_lang.get()
        translations = {
            "ru": "Синхронизирую с Ноушн...",
            "en": "Syncing with Notion...",
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def sync_notion_no_token(cls) -> str:
        """Notion не подключён — синхронизация невозможна."""
        lang = user_lang.get()
        translations = {
            "ru": (
                "Notion не подключён.\n"
                "Используйте /add_notion для настройки интеграции."
            ),
            "en": (
                "Notion is not connected.\n"
                "Use /add_notion to set up the integration."
            ),
        }
        return translations.get(lang, translations["ru"])

    @classmethod
    def sync_notion_success(cls, count: int) -> str:
        """
        Результат синхронизации: задачи из Notion помечены выполненными.

        Args:
            count: Количество задач, автоматически завершённых.
        """
        lang = user_lang.get()
        if count == 0:
            translations = {
                "ru": (
                    "Синхронизация завершена.\n\n"
                    "Все задачи с привязкой к Notion ещё активны там — "
                    "изменений нет."
                ),
                "en": (
                    "Sync complete.\n\n"
                    "All tasks linked to Notion are still active there — "
                    "no changes made."
                ),
            }
        else:
            translations = {
                "ru": (
                    f"Синхронизация завершена.\n\n"
                    f"Задач помечено выполненными: <b>{count}</b>\n"
                    f"(их статус в Notion начинается на «Done»)"
                ),
                "en": (
                    f"Sync complete.\n\n"
                    f"Tasks marked as completed: <b>{count}</b>\n"
                    f"(their status in Notion starts with «Done»)"
                ),
            }
        return translations.get(lang, translations["ru"])

    @classmethod
    def sync_notion_error(cls) -> str:
        """Ошибка при синхронизации с Notion."""
        lang = user_lang.get()
        translations = {
            "ru": (
                "Не удалось выполнить синхронизацию с Notion.\n"
                "Проверьте токен и доступ к базе данных."
            ),
            "en": (
                "Failed to sync with Notion.\n"
                "Please check your token and database access."
            ),
        }
        return translations.get(lang, translations["ru"])