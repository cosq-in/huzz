import sys
import time
import msvcrt
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn
from typing import Optional, Union
from .core import HuzzRegistry, _GLOBAL_REGISTRY

def create_layout() -> Layout:
    """create the main tui layout."""
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main"),
        Layout(name="footer", size=3)
    )
    return layout

def make_header() -> Panel:
    """create tui header."""
    now = datetime.now().strftime("%H:%M:%S")
    return Panel(
        f"[bold magenta]💅 huzz dashboard[/bold magenta] | [dim]v0.3.2[/dim] | [cyan]{now}[/cyan] | [yellow]press 'q' to exit[/yellow]",
        border_style="magenta"
    )

def make_table(registry: HuzzRegistry) -> Table:
    """create the main huzz status table."""
    table = Table(expand=True, border_style="dim")
    table.add_column("huzz", style="bold white", no_wrap=True)
    table.add_column("type", style="dim")
    table.add_column("fine shi", justify="center")
    table.add_column("is she going", justify="center")
    table.add_column("aura", justify="right")
    table.add_column("motion", justify="right")
    table.add_column("status", justify="center")

    for asset in registry.get_assets():
        fine_icon = "✅" if asset.fine_shi else "❌"
        going_icon = "🚀" if asset.going else "🚧"
        
        # aura colors
        a_color = "green" if asset.aura > 80 else "yellow" if asset.aura > 40 else "red"
        
        # status tags
        status = "[bold cyan]locked in[/bold cyan]" if asset.locked_in else "[dim]vibe check[/dim]"
        if asset.cooked:
            status = "[bold red]cooked[/bold red] 💀"
        elif asset.motion > 80:
            status = "[bold magenta]crushing it[/bold magenta] 🔥"

        table.add_row(
            asset.name,
            asset.type,
            fine_icon,
            going_icon,
            f"[{a_color}]{asset.aura}[/{a_color}]",
            f"{asset.motion:.1f} m/s",
            status
        )
    return table

def run_tui(registry: Optional[HuzzRegistry] = None, duration: Optional[Union[int, float]] = None):
    """
    run the full tui scaled toolkit.
    duration: seconds to run. if None, runs indefinitely until 'q' or Ctrl+C.
    """
    console = Console()
    reg = registry or _GLOBAL_REGISTRY
    layout = create_layout()

    try:
        with Live(layout, console=console, screen=True, refresh_per_second=4):
            start_time = time.time()
            while True:
                # 0. check duration if set
                if duration is not None and time.time() - start_time > duration:
                    break

                # 1. check for manual exit (q or Q)
                if msvcrt.kbhit():
                    key = msvcrt.getch().lower()
                    if key == b'q':
                        break

                # 2. update logic
                reg.audit()
                
                # 3. render components
                layout["header"].update(make_header())
                layout["main"].update(Panel(make_table(reg), title=f"[bold cyan]{reg.name}[/bold cyan]", border_style="cyan"))
                
                # footer with system aura avg
                assets = reg.get_assets()
                avg_aura = sum(a.aura for a in assets) / len(assets) if assets else 0
                layout["footer"].update(Panel(f"[bold white]system aura: {avg_aura:.1f}[/bold white] | [dim italic]no cap detected[/dim italic] | [dim]press 'q' to quit[/dim]", border_style="magenta"))
                
                time.sleep(0.2)
    except KeyboardInterrupt:
        pass # graceful exit on Ctrl+C
    finally:
        console.print("[bold magenta]💅 huzz out.[/bold magenta]")

def main():
    run_tui()

if __name__ == "__main__":
    main()
