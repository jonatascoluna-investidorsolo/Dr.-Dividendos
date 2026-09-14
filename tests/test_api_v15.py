from fastapi.testclient import TestClient

from dd_engine.api import app


def test_health():
    client = TestClient(app)
    r = client.get('/health')
    assert r.status_code == 200
    assert r.json()['version'] == '2.4.0'


def test_calculate_still_works():
    client = TestClient(app)
    payload = {
        'ticker': 'TEST3', 'company_name': 'Teste', 'shares': 100,
        'projected_net_income': 1000, 'book_value_per_share': 12,
        'earnings_cagr_5y': 0.05, 'payout_expected': 0.6,
        'current_price': 10,
    }
    r = client.post('/calculate', json=payload)
    assert r.status_code == 200
    assert r.json()['quality_score'] >= 0
