import pytest
from app.engines.wrap_math import paper_area, ribbon_estimate

def test_book_box():
    r = paper_area(0.30, 0.20, 0.15, 1.15)
    assert r["box_surface"] == 0.27
    assert r["paper_m2"] == 0.31

def test_zero_flap_matches_legacy():
    """折入为 0 时必须与改造前同盒同折边完全一致。"""
    r = paper_area(0.30, 0.20, 0.15, 1.15, 0.0)
    assert r["flap_m"] == 0.0
    assert r["flap_surface"] == 0.0
    assert r["effective_surface"] == r["box_surface"] == 0.27
    assert r["paper_m2"] == 0.31

def test_flap_adds_contact_surface():
    # 六面 0.27；折入贴合面 = 2*(0.30+0.20)*0.05 = 0.05；有效 0.32；用纸 0.32*1.15=0.368
    r = paper_area(0.30, 0.20, 0.15, 1.15, 0.05)
    assert r["flap_m"] == 0.05
    assert r["flap_surface"] == 0.05
    assert r["effective_surface"] == 0.32
    assert r["paper_m2"] == 0.368

def test_negative_flap_rejected():
    with pytest.raises(ValueError):
        paper_area(0.30, 0.20, 0.15, 1.15, -0.02)

def test_ribbon_ignores_flap():
    before = ribbon_estimate(0.30, 0.20, 0.15, "cross")
    after = ribbon_estimate(0.30, 0.20, 0.15, "cross")
    assert before["ribbon_m"] == after["ribbon_m"] == 2.2

def test_ribbon_cross():
    rb = ribbon_estimate(0.30, 0.20, 0.15, "cross")
    assert rb["ribbon_m"] > 0.5
