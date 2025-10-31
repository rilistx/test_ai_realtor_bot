import json
import random
import asyncio
import aiohttp

from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext

from openai import OpenAI

from core.filters import ContactFilter
from core.keyboards import realtor_button
from core.states import RealtorState
from core.utils import parse_gpt_message, read_gsheet

from core.db.models import DistrictModel, UserModel
from core.config.loader import envs


realtor_router = Router()


async def start_wrapper(
        message: Message,
        state: FSMContext,
) -> None:
    await state.clear()
    ReplyKeyboardRemove()

    await state.update_data({
        "telegram_user_id": message.from_user.id,
        "user_messages": None,
        "agent_messages": None,
        "last_question_order": 1,
        "filters": {
            "name": None,
            "type": None,
            "district": None,
            "rooms": None,
            "state": None,
            "budget": None,
        },
        "telegram_phone_number": None,
    })

    welcome_messages = read_gsheet("weclome_messages")

    welcome_message_text = "".join(welcome_message["message"] for welcome_message in welcome_messages if welcome_message["language"] == "ua")

    await message.answer(
        text=welcome_message_text,
    )

    first_questions = read_gsheet("questions")

    first_question_text = "".join(first_question["question_text"] for first_question in first_questions if first_question["question_key"] == "name")

    await message.answer(
        text=first_question_text,
    )

    await state.update_data({
        "agent_messages": welcome_message_text + "\n\n" + first_question_text,
    })

    await state.set_state(RealtorState.QUESTION)


@realtor_router.message(
    CommandStart(),
)
async def start(
        message: Message,
        state: FSMContext,
) -> None:
    await start_wrapper(
        message=message,
        state=state,
    )


@realtor_router.message(
    Command(commands=["restart"]),
)
async def restart(
        message: Message,
        state: FSMContext,
):
    await state.clear()

    text = "✅ <b>Успіх: Бот успішно перезапущено!</b>"

    await message.answer(
        text=text,
        reply_markup=ReplyKeyboardRemove(),
    )

    await asyncio.sleep(1)

    await start_wrapper(
        message=message,
        state=state,
    )


@realtor_router.message(
    RealtorState.QUESTION,
)
async def question(
        message: Message,
        state: FSMContext,
        client: OpenAI,
) -> None:
    await message.answer(
        text="⏳ Хвилину, обробляю ваш запит...",
    )

    changed = await parse_gpt_message(
        message=message.text,
        state=state,
        client=client,
    )

    state_data = await state.get_data()

    await state.update_data({
        "user_messages": state_data["user_messages"] + "\n\n" + message.text if state_data["user_messages"] else message.text,
    })

    if changed:
        next_states = [key for key, value in state_data["filters"].items() if value is None]

        if len(next_states) == 0:
            text = (
                "Я вже підібрав для вас кілька варіантів по вашим фільтрам!\n"
                "Будь ласка, поділіться вашим номером, щоб я міг відправити результати."
            )

            await state.update_data({
                "agent_messages": state_data["agent_messages"] + "\n\n" + text,
            })

            reply_markup = realtor_button()

            await message.answer(
                text=text,
                reply_markup=reply_markup,
            )

            await state.set_state(RealtorState.PHONE)
        else:
            next_state = random.choice(next_states)
            next_questions = read_gsheet("questions")

            next_question_text = "".join(
                next_question["question_text"] for next_question in next_questions if next_question["question_key"] == next_state
            )

            await state.update_data({
                "agent_messages": state_data["agent_messages"] + "\n\n" + next_question_text,
            })

            for next_question in next_questions:
                if next_question["question_key"] == next_state:
                    await state.update_data({
                        "last_question_order": int(next_question["order"]),
                    })
                    break

            await message.answer(
                text=next_question_text,
            )
    else:
        objections = read_gsheet("objections")
        reactions = read_gsheet("reactions")

        reaction_list = random.choice([objections, reactions])
        reaction_text = random.choice(reaction_list)["response"]

        await message.answer(
            text=reaction_text,
        )

        await state.update_data({
            "agent_messages": state_data["agent_messages"] + "\n\n" + reaction_text,
        })

        last_questions = read_gsheet("questions")

        last_question_text = "".join(
            last_question["question_text"] for last_question in last_questions if last_question["order"] == state_data["last_question_order"]
        )

        await state.update_data({
            "agent_messages": state_data["agent_messages"] + "\n\n" + last_question_text,
        })

        await message.answer(
            text=last_question_text,
        )


@realtor_router.message(
    RealtorState.PHONE,
    ContactFilter(),
)
async def completed(
        message: Message,
        state: FSMContext,
) -> None:
    state_data = await state.get_data()

    text = (
        "✅ <b>Успішно заповнена форма</b>\n"
        "Чекайте, скоро з вами звʼяжеться наш менеджер!"
    )

    await state.update_data({
        "agent_messages": state_data["agent_messages"] + "\n\n" + text,
    })

    reply_markup = ReplyKeyboardRemove()

    await message.answer(
        text=text,
        reply_markup=reply_markup,
    )

    url = "https://bots2.tira.com.ua:8443/api/get_apartments"
    payload = {
        "key": envs.tira_api_key,
        "limit": 3,
        # "offset": 0,
    }
    headers = {
        "Content-Type": "application/json"
    }

    if state_data["filters"]["district"] is not None:
        district = await DistrictModel.filter(name=state_data["filters"]["district"]).first()

        if district is not None:
            payload["district_id"] = district.id

    if state_data["filters"]["rooms"] is not None:
        payload["rooms_in"] = int(state_data["filters"]["rooms"])

    if state_data["filters"]["type"] is not None:
        condition = await DistrictModel.filter(name=state_data["filters"]["type"]).first()

        if condition is not None:
            payload["condition_in"] = condition.id


    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers, ssl=False) as response:
            if response.status == 200:
                # data = await response.json()
                # print(data)  # output: {'status': 'error', 'message': 'wrong offset', 'items': None}
                pass
            else:
                text = await response.text()

                raise (
                    f"Помилка {response.status}: {text}"
                )

    await UserModel.create(
        telegram_user_id=state_data["telegram_user_id"],
        user_messages=state_data["user_messages"],
        agent_messages=state_data["agent_messages"],
        filters=json.dumps(state_data["filters"]),
        telegram_phone_number=str(message.contact.phone_number),
    )

    await state.clear()


@realtor_router.message(
    StateFilter(RealtorState),
)
async def error(
        message: Message,
        state: FSMContext,
) -> None:
    state_data = await state.get_data()

    await state.update_data({
        "user_messages": state_data["user_messages"] + "\n\n" + message.text,
    })

    text = "🆘 <b>Помилка:</b> Не правильний формат номеру телефона"

    await state.update_data({
        "agent_messages": state_data["agent_messages"] + "\n\n" + text,
    })

    reply_markup = ReplyKeyboardRemove()

    await message.answer(
        text=text,
        reply_markup=reply_markup,
    )

    text = (
        "Я вже підібрав для вас кілька варіантів по вашим фільтрам!\n"
        "Будь ласка, поділіться вашим номером, щоб я міг відправити результати."
    )

    await state.update_data({
        "agent_messages": state_data["agent_messages"] + "\n\n" + text,
    })

    reply_markup = realtor_button()

    await message.answer(
        text=text,
        reply_markup=reply_markup,
    )
