from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from jose import jwt, JWTError

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

PUBLIC_PATHS = {
    "/docs",
    "/openapi.json",
    "/api/v1/auth/login",
    "/redoc",
    "/auth/login",
    "/api/v1/auth/register",
    "/api/v1/courses","/api/v1/courses"
    "/courses",
}

class TokenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS":
            return await call_next(request)
        path = request.url.path

        # Allow public routes
        if any(path.startswith(p) for p in PUBLIC_PATHS):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        print(f"Authorization header: {auth_header}")  # Debugging line

        if not auth_header or not auth_header.startswith("Bearer "):
            print("Missing or invalid Authorization header")  # Debugging line
            return JSONResponse(
                status_code=403,
                content={"detail": "Missing token"}
            )

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            request.state.user = {
                "id": payload.get("sub"),
                "role": payload.get("role"),
            }

        except JWTError:
            return JSONResponse(
                status_code=405,
                content={"detail": "Invalid token"}
            )

        return await call_next(request)
