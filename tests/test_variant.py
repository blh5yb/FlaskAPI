from pathlib import Path
from tests.conftest import *

resources = Path(__file__).parent / "resources"


class TestNewVariant:
    def test_new_variant(self, client):
        response = client.post("/flask-demo/api/variant", json={
            "chr": "chr1",
            "pos": 123,
            "ref": 'A',
            "alt": "T",
            "quality": 80
        })
        assert response.status_code == 201

    def test_validation_error(self, client):
        response = client.post("/flask-demo/api/variant", json={
            "chr": "chr29",
            "pos": 123,
            "ref": 'A',
            "alt": "T",
            "quality": 80
        })
        assert response.status_code == 500

    def test_get_variant(self, client):
        """test getting variant by id"""
        response = client.get("/flask-demo/api/variant?id=1")
        assert response.status_code == 201

    def test_missing_param(self, client):
        """test missing id returns error"""
        response = client.get("/flask-demo/api/variant")
        assert response.status_code == 500

