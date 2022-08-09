from app import create_app


def test_hook(self):
    assert self.get('/runner').status_code == 200
    response = self.get('/runner')
    assert response.data == b'Hello this message is coming from hook Blueprint.'
