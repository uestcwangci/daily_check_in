import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from fastapi.responses import JSONResponse

app = FastAPI()



@app.get("/getAlive")
async def get_alive():
    try:
        with open('android/logs/alive.log', 'r') as file:
            lines = file.readlines()

        recent_lines = lines[-30:] if len(lines) > 30 else lines

        result_lines = []
        for line in recent_lines:
            parts = line.strip().split(' - ')
            if len(parts) == 3:
                time_str = ' '.join(parts[0].split(',')[0].split()[0:2])
                count = parts[2].strip()
                result_lines.append(f"{time_str} - {count}")

        return JSONResponse(content=result_lines)

    except Exception as e:
        return JSONResponse(content={"error": str(e)})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8009)