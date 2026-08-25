def test_risk_check_stays_within_latency_budget():

    response = client.post(
        "/v1/risk/check",
        json=valid_payload(),
    )

    assert response.status_code == 200

    elapsed_ms = float(
        response.headers["X-Process-Time-Ms"]
    )

    assert elapsed_ms < 100