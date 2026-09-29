from pydantic import BaseModel, Field

class EstimateRequest(BaseModel):
    box_id: int
    overlap: float | None = None
    flap_m: float = Field(default=0.0, ge=0)
    wrap_style: str = "cross"
    save: bool = False
    note: str = ""

class BoxPatch(BaseModel):
    flap_m: float = Field(ge=0)
