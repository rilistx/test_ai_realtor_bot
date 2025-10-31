import json

from aiogram.fsm.context import FSMContext
from openai import OpenAI


async def parse_gpt_message(message: str, state: FSMContext, client: OpenAI):
    prompt = f"""
    Ти — ШІ-асистент ріелтора.
    Твоє завдання — витягти з повідомлення користувача значення:
    name, type (квартира або будинок), district (район - Таїрова, Центр або Фонтан), rooms (кількість кімнат), 
    state (стан - під оздоблювальні роботи, житлова, євроремонт, від будівельників, капітальний або під ремонт)
    budget (бюджет користувача, якщо уканано не в долларах, то автоматично переводити в доллари).
    Формат відповіді — тільки чистий JSON без коментарів чи додаткового тексту.
    Якщо якихось данних не має то позначати як 'None'.
    Приклад:
    {{
      "name": "Анна",
      "type": "квартира",
      "district": "Центр",
      "rooms": 2,
      "state": "з ремонтом",
      "budget": "70000"
    }}

    Текст користувача: {message}
    """

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "developer", "content": "Talk like a pirate."},
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    result = response.choices[0].message.content

    try:
        result = json.loads(result)
    except json.JSONDecodeError:
        print("Unable to convert string to dictionary")

    state_data = await state.get_data()
    changed = False

    filters = state_data["filters"]

    for key, value in result.items():
        if value != 'None' and state_data['filters'][key] is None:
            filters[key] = value
            changed = True

    if changed:
        await state.update_data({"filters": filters})

    return changed
