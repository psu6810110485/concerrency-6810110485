import asyncio
import time
import sys
import aiohttp

# ==========================================
# 1. Asyncio: ดึงข้อมูลจาก API สภาพอากาศพร้อมกัน
# ==========================================
async def fetch_real_temperature(session, city):
    url = f"https://wttr.in/{city}?format=%t"
    try:
        async with session.get(url) as response:
            temp_text = await response.text()
            return (city, temp_text.strip())
    except Exception as e:
        return (city, "Error")

async def main():
    start_time = time.time()
    print("🌍 เริ่มระบบวิเคราะห์อุณหภูมิ Real-time\n")

    cities = ["Songkhla", "Bangkok", "Chiang Mai", "Phuket"]
    
    # --- เริ่ม Asyncio ---
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_real_temperature(session, city) for city in cities]
        real_weather_data = await asyncio.gather(*tasks)

    print("✅ ดึงอุณหภูมิปัจจุบันสำเร็จ:")
    for data in real_weather_data:
        print(f"📍 {data[0]}: {data[1]}")

    print(f"\n🎉 ทำงานเสร็จสิ้นภายใน: {time.time() - start_time:.2f} วินาที")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())