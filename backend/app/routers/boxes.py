from fastapi import APIRouter, HTTPException
from app.repositories import boxes as repo
from app.schemas.estimate import BoxPatch
router = APIRouter()
@router.get("/boxes")
def list_boxes(): return {"items": repo.list_boxes()}
@router.get("/boxes/{bid}")
def get_box(bid: int):
    r = repo.get_box(bid)
    if not r: raise HTTPException(404)
    return r
@router.patch("/boxes/{bid}")
def patch_box(bid: int, body: BoxPatch):
    r = repo.set_default_flap(bid, body.flap_m)
    if not r: raise HTTPException(404)
    return r
