import random
from typing import List, Dict, Callable, Optional
from .models import HuzzEntity

class HuzzRegistry:
    """
    huzz registry: heuristic unit zone zip manager
    extensible framework for full tui observability.
    """
    def __init__(self, name: str = "default registry"):
        self.name = name.lower()
        self.assets: Dict[str, HuzzEntity] = {}

    def add_asset(self, asset: HuzzEntity) -> None:
        """register a new huzz."""
        self.assets[asset.name] = asset

    def get_assets(self) -> List[HuzzEntity]:
        """get all huzz units."""
        return list(self.assets.values())

    def audit(self, update_fn: Optional[Callable[[HuzzEntity], None]] = None) -> List[HuzzEntity]:
        """
        audit the infrastructure.
        refreshes motion and aura levels.
        """
        assets = self.get_assets()
        for asset in assets:
            if update_fn:
                update_fn(asset)
            else:
                # default random motion for the demo vibe
                asset.motion = abs(random.gauss(50, 20))
                if asset.cooked:
                    asset.aura = max(0, asset.aura - 10)
                else:
                    asset.aura = min(100, asset.aura + random.randint(-2, 2))
        return assets

# stylistically compatible hooks
def get_huzz_db() -> List[HuzzEntity]:
    return _GLOBAL_REGISTRY.get_assets()

# global default registry
_GLOBAL_REGISTRY = HuzzRegistry("core infrastructure")
