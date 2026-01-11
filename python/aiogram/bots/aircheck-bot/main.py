import asyncio
import aiohttp
from datetime import datetime, timezone, timedelta

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from config import TELEGRAM_BOT_TOKEN, IQAIR_API_KEY, OPENWEATHER_API_KEY

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

TASHKENT_TZ = timezone(timedelta(hours=5))

@dp.message(CommandStart())
async def handle_start(message: Message):
    await message.answer(
        f"Hey {message.from_user.first_name}\n\n"
        "I can check air quality and weather for you\n"
        "Use /air to get current AQI + weather."
    )

@dp.message(Command("air"))
async def get_air_quality(message: Message):
    async with aiohttp.ClientSession() as session:
        aqi_url = "https://api.airvisual.com/v2/nearest_city"
        async with session.get(aqi_url, params={"key": IQAIR_API_KEY}) as resp:
            aqi_data = await resp.json()

        if aqi_data["status"] != "success":
            await message.answer("Failed to fetch air quality data.")
            return

        city = aqi_data["data"]["city"]
        country = aqi_data["data"]["country"]
        aqi = aqi_data["data"]["current"]["pollution"]["aqius"]
        aqi_ts = aqi_data["data"]["current"]["pollution"]["ts"]

        aqi_time = datetime.fromisoformat(aqi_ts.replace("Z", "+00:00")).astimezone(TASHKENT_TZ).strftime("%Y-%m-%d %H:%M %Z")

        weather_info = aqi_data["data"]["current"]["weather"]
        temp = weather_info["tp"]
        humidity = weather_info["hu"]
        wind = weather_info["ws"]
        pressure = weather_info["pr"]

        if aqi <= 50:
            status = "Good"
        elif aqi <= 100:
            status = "Moderate"
        elif aqi <= 150:
            status = "Unhealthy for sensitive groups"
        elif aqi <= 200:
            status = "Unhealthy"
        else:
            status = "Very Unhealthy"

        weather_url = "https://api.openweathermap.org/data/2.5/weather"
        weather_params = {
            "q": city,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"
        }
        async with session.get(weather_url, params=weather_params) as resp:
            weather_data = await resp.json()

        if weather_data.get("cod") == 200:
            description = weather_data["weather"][0]["description"].capitalize()
            weather_ts = weather_data["dt"]
            weather_time = datetime.utcfromtimestamp(weather_ts).replace(tzinfo=timezone.utc).astimezone(TASHKENT_TZ).strftime("%Y-%m-%d %H:%M %Z")
        else:
            description = "N/A"
            weather_time = "N/A"

    await message.answer(
        f"Air & Weather Report\n\n"
        f"Location: {city}, {country}\n"
        f"AQI (US): {aqi} — {status}\n"
        f"AQI Last Checked: {aqi_time}\n\n"
        f"Temperature: {temp}°C\n"
        f"Humidity: {humidity}%\n"
        f"Wind: {wind} m/s\n"
        f"Pressure: {pressure} hPa\n"
        f"Weather: {description}\n"
        f"Weather last checked: {weather_time}"
    )

async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())