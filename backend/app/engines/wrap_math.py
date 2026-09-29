def paper_area(length: float, width: float, height: float, overlap: float = 1.15, flap_m: float = 0.0) -> dict:
    """盒体有效贴纸面积与用纸面积。

    盖口折入深度 flap_m（米）：盒口一圈折入内壁的贴合面，口径由盒体
    长边 + 宽边自洽推出，周长 = 2*(L+W)，故折入面积 = 2*(L+W)*flap_m。
    有效表面积在原六面基础上叠加该贴合面后，再乘折边系数得 paper_m2。
    """
    L, W, H = float(length), float(width), float(height)
    d = float(flap_m)
    if min(L, W, H) <= 0:
        raise ValueError("box dimensions must be positive")
    if d < 0:
        raise ValueError("flap_m must be non-negative")
    base = 2 * (L * W + L * H + W * H)
    flap_area = 2 * (L + W) * d
    effective = base + flap_area
    need = effective * float(overlap)
    return {
        "box_surface": round(base, 3),
        "flap_m": round(d, 6),
        "flap_surface": round(flap_area, 3),
        "effective_surface": round(effective, 3),
        "overlap": float(overlap),
        "paper_m2": round(need, 3),
    }


def ribbon_estimate(length: float, width: float, height: float, wrap_style: str = "cross") -> dict:
    """Helper: approximate ribbon length in meters (not stored as primary metric).

    丝带始终按未折入前的外三边走，盖口折入不参与。
    """
    L, W, H = float(length), float(width), float(height)
    girth = 2 * (W + H)
    if wrap_style == "band":
        meters = girth + 0.3
    else:
        meters = girth * 2 + L + 0.5
    return {"wrap_style": wrap_style, "ribbon_m": round(meters, 2)}
