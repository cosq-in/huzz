import sys
import os
import random
import time

# ensure local src is used
sys.path.append(os.path.join(os.getcwd(), "src"))

from huzz import HuzzRegistry, HuzzEntity
from huzz.cli import run_tui

def main():
    """
    huzz tui demo
    launches an indefinite full-screen observability dashboard.
    """
    # 1. create the registry
    infra = HuzzRegistry("main cloud cluster")

    # 2. populate with assets
    infra.add_asset(HuzzEntity(
        name="payment-gateway", 
        type="api", 
        aura=98,
        locked_in=True
    ))
    infra.add_asset(HuzzEntity(
        name="user-auth-db", 
        type="db", 
        aura=92,
        motion=12.5
    ))
    infra.add_asset(HuzzEntity(
        name="legacy-monolith", 
        type="service", 
        aura=15,
        cooked=True
    ))
    infra.add_asset(HuzzEntity(
        name="scaling-agent", 
        type="k8s-pod", 
        aura=75,
        motion=99.9
    ))

    # 3. launch the indefinite tui toolkit
    # duration=None means it runs until 'q' or Ctrl+C
    run_tui(infra, duration=None)

if __name__ == "__main__":
    main()
