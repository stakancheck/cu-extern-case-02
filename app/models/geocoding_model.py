from pydantic import BaseModel, Field
from typing import Dict, Optional

class GeocodingResponse(BaseModel):
    name: str
    local_names: Optional[Dict[str, str]] = None
    lat: float
    lon: float
    country: str
    state: Optional[str] = None
