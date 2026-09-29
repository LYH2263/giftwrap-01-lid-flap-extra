from fastapi.testclient import TestClient
from app.main import app


def _client():
    return TestClient(app)


def _run_count(client):
    return len(client.get("/api/runs", params={"limit": 1000}).json()["items"])


def test_zero_flap_equals_legacy_and_no_row():
    with _client() as client:
        before = _run_count(client)
        r = client.get("/api/estimate", params={"box_id": 1}).json()
        assert r["flap_m"] == 0.0
        assert r["box_surface"] == r["effective_surface"] == 0.27
        assert r["paper_m2"] == 0.31
        assert r["ribbon"]["ribbon_m"] == 2.2
        assert r["run_id"] is None
        assert _run_count(client) == before  # save=false 只回算不增行


def test_save_persists_flap_snapshot():
    with _client() as client:
        r = client.post("/api/estimate", json={"box_id": 1, "flap_m": 0.05, "save": True}).json()
        rid = r["run_id"]
        assert rid
        assert r["flap_m"] == 0.05
        assert r["effective_surface"] == 0.32
        assert r["paper_m2"] == 0.368

        # 列表摘要一路
        summary = next(x for x in client.get("/api/runs").json()["items"] if x["id"] == rid)
        assert summary["result"]["flap_m"] == 0.05
        assert summary["result"]["paper_m2"] == 0.368

        # 详情打开一路
        detail = client.get(f"/api/runs/{rid}").json()
        assert detail["result"]["flap_m"] == 0.05
        assert detail["result"]["effective_surface"] == 0.32
        assert detail["result"]["paper_m2"] == 0.368


def test_negative_flap_fails_without_new_row():
    with _client() as client:
        for params, payload in (
            ({"box_id": 1, "flap_m": -0.03}, None),
            (None, {"box_id": 1, "flap_m": -0.03, "save": True}),
        ):
            before = _run_count(client)
            if params is not None:
                resp = client.get("/api/estimate", params=params)
            else:
                resp = client.post("/api/estimate", json=payload)
            assert resp.status_code == 422
            assert _run_count(client) == before  # 用纸档不增行


def test_snapshot_pinned_after_default_changes_and_dry_recompute_matches():
    with _client() as client:
        saved = client.post("/api/estimate", json={"box_id": 1, "flap_m": 0.05, "save": True}).json()
        rid, overlap = saved["run_id"], saved["overlap"]

        # 改主数据默认折入
        patched = client.patch(f"/api/boxes/1", json={"flap_m": 0.09})
        assert patched.status_code == 200
        assert patched.json()["flap_m"] == 0.09

        # 列表与详情两路仍钉住写入值，不按新默认回刷
        summary = next(x for x in client.get("/api/runs").json()["items"] if x["id"] == rid)
        detail = client.get(f"/api/runs/{rid}").json()
        for r in (summary["result"], detail["result"]):
            assert r["flap_m"] == 0.05
            assert r["paper_m2"] == 0.368

        # 算纸台用写入时同参干算，与该编号回看互证
        dry = client.get("/api/estimate", params={"box_id": 1, "flap_m": 0.05, "overlap": overlap}).json()
        assert dry["run_id"] is None
        assert dry["flap_m"] == detail["result"]["flap_m"]
        assert dry["effective_surface"] == detail["result"]["effective_surface"]
        assert dry["paper_m2"] == detail["result"]["paper_m2"]


def test_ribbon_unchanged_with_flap():
    with _client() as client:
        plain = client.get("/api/estimate", params={"box_id": 1}).json()
        flapped = client.get("/api/estimate", params={"box_id": 1, "flap_m": 0.08}).json()
        assert flapped["ribbon"]["ribbon_m"] == plain["ribbon"]["ribbon_m"]
