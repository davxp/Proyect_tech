# Aquí guardo cosas de seguridad que uso en varios lados:
# hash de contraseñas y verificación (bcrypt). No uso JWT para mantenerlo simple,
# pero el login valida credenciales con hash real (no texto plano).

from passlib.context import CryptContext

_pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return _pwd_ctx.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    return _pwd_ctx.verify(password, password_hash)
