import os
import requests
import pytest

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://dinho-rodas-bh.preview.emergentagent.com").rstrip("/")

def test_public_and_quote_flow():
    public = requests.get(f"{BASE_URL}/api/public", timeout=20)
    assert public.status_code == 200
    data = public.json()
    assert all(k in data for k in ("services", "gallery", "faqs", "settings"))
    quote = requests.post(f"{BASE_URL}/api/quotes", data={"name":"TEST_Ana", "phone":"31999999999", "vehicle":"Civic"}, timeout=20)
    assert quote.status_code == 200
    assert quote.json()["name"] == "TEST_Ana"

def test_auth_and_services_crud():
    bad = requests.post(f"{BASE_URL}/api/auth/login", json={"email":"wrong@example.com", "password":"wrong"}, timeout=20)
    assert bad.status_code == 401
    good = requests.post(f"{BASE_URL}/api/auth/login", json={"email":"admin@dinhorodas.com", "password":"Dinho#2026"}, timeout=20)
    assert good.status_code == 200 and good.json().get("token")
    headers = {"Authorization": f"Bearer {good.json()['token']}"}
    created = requests.post(f"{BASE_URL}/api/admin/services", json={"title":"TEST Serviço", "description":"Teste"}, headers=headers, timeout=20)
    assert created.status_code == 200
    item_id = created.json()["id"]
    listed = requests.get(f"{BASE_URL}/api/admin/services", headers=headers, timeout=20)
    assert listed.status_code == 200 and any(x["id"] == item_id for x in listed.json())
    deleted = requests.delete(f"{BASE_URL}/api/admin/services/{item_id}", headers=headers, timeout=20)
    assert deleted.status_code == 200 and deleted.json()["ok"] is True