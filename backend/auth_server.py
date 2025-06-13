from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from starlette.config import Config
from authlib.integrations.starlette_client import OAuth
from jose import jwt 
import os 
from dotenv import load_dotenv


load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
FRONTEND_URL = os.getenv("FRONTEND_URL")

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=JWT_SECRET)

config = Config(".env")
oauth = OAuth(config)

oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={"scope": "openid email profile"}
)

@app.get("/")
async def root():
    return {"status" : "Auth server is running!"}

@app.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.route("/auth")
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
       
        user = token.get("userinfo")
        

        if not user or "email" not in user:
            return JSONResponse(status_code=400, content={"error": "Failed to authenticate user"})
        
        
        # create JWT token
        jwt_token = jwt.encode({"email": user["email"]}, JWT_SECRET, algorithm="HS256")
        

        # redirect to frontend with JWT token
        redirect_url = f"{FRONTEND_URL}?token={jwt_token}&email={user['email']}"
        
        return RedirectResponse(url=redirect_url)
    
    except Exception as e:
        print("❌ Exception occurred:", str(e))
        return JSONResponse(status_code=500, content={"error": str(e)})
