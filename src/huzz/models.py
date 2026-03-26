from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import Literal, Dict, Any, Optional

class HuzzEntity(BaseModel):
    """
    huzz: heuristic unit zone zip
    the base unit for observability within the huzz framework.
    now fully lowercase and period-free.
    """
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(..., description="unique identifier for the service/asset")
    type: str = Field("generic", description="asset category")
    version: Optional[str] = "1.0.0"
    
    # observability stats
    fine_shi: bool = Field(True, description="functional integrity status")
    going: bool = Field(True, description="operational status")
    
    # new gen z/alpha metrics
    aura: int = Field(default=100, ge=0, le=100, description="overall health/rizz score")
    motion: float = Field(default=0.0, description="activity level / throughput")
    locked_in: bool = Field(False, description="high priority / stable status")
    cooked: bool = Field(False, description="critical failure status")
    
    # custom metadata
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def __repr__(self) -> str:
        status = "✅" if not self.cooked else "💀"
        return f"{status} huzz(name='{self.name}', aura={self.aura})"
