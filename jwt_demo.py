import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "dev_secret"

exp = datetime.now(timezone.utc) + timedelta(minutes=30)
token = jwt.encode({'sub': '1', 'exp': exp, 'text': 'hello'}, SECRET_KEY, algorithm='HS256')
# print(token)


# 압축한 토큰이 유효한지 검사
decoded_data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
print(decoded_data)