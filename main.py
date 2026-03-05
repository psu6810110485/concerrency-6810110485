import asyncio
import time
import sys
import math
import re
import aiohttp
from concurrent.futures import ProcessPoolExecutor

# ==========================================
# 3. Process Pool: คำนวณโมเดลสภาพอากาศ (CPU-Bound)
# ==========================================
def run_climate_simulation(weather_data):
    city, temp_text = weather_data
    match = re.search(r'-?\d+', temp_text)
    if not match:
        return f"📍 {city}: ดึงข้อมูลล้มเหลว"
    
    temp_celsius = int(match.group())
    
    simulation_result = 0
    for i in range(5_000_000): # จำลองการทำงานหนัก
        simulation_result += math.sin(temp_celsius) * math.cos(i % 100)
    
    return f"📍 {city}: อุณหภูมิจริง {temp_celsius}°C | (วิเคราะห์เสร็จสิ้น: {abs(simulation_result):.2f})"

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
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_real_temperature(session, city) for city in cities]
        real_weather_data = await asyncio.gather(*tasks)

    print("✅ ดึงข้อมูลสำเร็จ กำลังส่งให้ Process Pool คำนวณ...")

    # --- เริ่ม Process Pool ---
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(run_climate_simulation, real_weather_data))

    print("\n📊 ผลลัพธ์การประมวลผลอุณหภูมิ:")
    for res in results:
        print(res)

    print(f"\n🎉 ทำงานเสร็จสิ้นภายใน: {time.time() - start_time:.2f} วินาที")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())