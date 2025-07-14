from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os, requests

load_dotenv()

TMDB_BASE = "https://api.themoviedb.org/3/movie/"
API_KEY   = os.getenv("TMDB_API_KEY")

if not API_KEY:
    raise RuntimeError("TMDB_API_KEY not found in environment")

app = FastAPI(title="TMDB Proxy Service")

def call_tmdb(movie_id: int) -> dict:
    url = f"{TMDB_BASE}{movie_id}"
    params = {"api_key": API_KEY, "language": "en-US"}
    r = requests.get(url, params=params, timeout=10)

    if r.status_code == 404:
        raise HTTPException(status_code=404, detail="Movie not found")
    if r.status_code != 200:
        raise HTTPException(status_code=502,
                            detail=f"TMDB error: {r.status_code}")

    return r.json()

@app.get("/movie/{movie_id}")
def fetch_movie(movie_id: int):
    """
    Proxy endpoint that fetches full TMDB metadata
    for the provided movie_id and returns it verbatim.
    """
    data = call_tmdb(movie_id)
    return JSONResponse(content=data)
