from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_post_list():
    res = client.get('/api/posts')
    assert res.status_code == 200 # a랑 b가 같냐고 정의? 역설? 함



def test_post_detail_404():
    res = client.get('/api/posts/9999999')
    assert res.status_code == 404
    assert res.json() == {'detail': "해당 게시물이 없습니다."}



def test_post_create_empty_422():
    res = client.post('/api/posts', json={'content': 'hello', 'user_id': 1})