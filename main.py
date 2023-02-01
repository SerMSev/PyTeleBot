import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types


BOT_TOKEN = "5966126408:AAEE7pRcqbos-yG1gmCeIKKQRchzL3H8JXc"


async def start_handler(event: types.Message):
    await event.answer(
        f"Hello, {event.from_user.get_mention(as_html=True)} 👋!",
        parse_mode=types.ParseMode.HTML,
    )

async def image_handler(event: types.Message):
    image = await get_image("https://random-d.uk/api/randomimg")
    if image is not None:
        await save_image(image)


async def quit_handler(message: types.Message):
    await bot.send_message(message.from_user.id, 'Goodbye! See you...')


async def get_image(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                # handle error here
                return None
            image = await resp.content.read()
            return image


async def save_image(image):
    with open("random_image.jpg", "wb") as f:
        f.write(image)


async def main():
    bot = Bot(token=BOT_TOKEN)
    try:
        disp = Dispatcher(bot=bot)
        disp.register_message_handler(start_handler, commands={"start", "restart"})
        disp.register_message_handler(image_handler, commands={"getimage", "get"})
        disp.register_message_handler(quit_handler, commands={"quit"})
        await disp.start_polling()
    finally:
        await bot.close()

asyncio.run(main())
