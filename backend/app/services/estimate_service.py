from fastapi import HTTPException
from app.engines.wrap_math import paper_area, ribbon_estimate
from app.repositories import boxes, history, settings_repo

def run_estimate(box_id: int, overlap: float | None, wrap_style: str, save: bool, note: str, flap_m: float = 0.0):
    box = boxes.get_box(box_id)
    if not box:
        raise HTTPException(404)
    if box.get("data_quality") == "dirty":
        raise HTTPException(422, "dirty box")
    d = float(flap_m or 0.0)
    if d < 0:
        # 折入为负整单失败，用纸档不增行
        raise HTTPException(422, "flap_m must be non-negative")
    ov = float(overlap) if overlap is not None else settings_repo.get_overlap()
    calc = paper_area(box["length"], box["width"], box["height"], ov, d)
    ribbon = ribbon_estimate(box["length"], box["width"], box["height"], wrap_style)
    # save=false 只回算不增行；save=true 以快照写入 flap_m / 有效表面积 / paper_m2
    payload = {**calc, "ribbon": ribbon, "box_id": box_id}
    run_id = history.insert_run(box_id, ov, payload, note) if save else None
    return {"box": box, "run_id": run_id, **calc, "ribbon": ribbon}
