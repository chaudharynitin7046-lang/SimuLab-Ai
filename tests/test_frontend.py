import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_serves_index_html():
    response = client.get("/")
    assert response.status_code == 200
    assert "SimuLab AI" in response.text
    assert "<iframe" in response.text

def test_static_assets_served():
    app_js_resp = client.get("/static/app.js")
    assert app_js_resp.status_code == 200
    assert "fetchHeroDemos" in app_js_resp.text

    style_css_resp = client.get("/static/style.css")
    assert style_css_resp.status_code == 200
    assert "Inter" in style_css_resp.text
