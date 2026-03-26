import sys
import time
import os
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from typing import Optional, Union
from .core import HuzzRegistry, _GLOBAL_REGISTRY

# --- Cross-Platform Keyboard Handling ---
_IS_WINDOWS = os.name == 'nt'

if _IS_WINDOWS:
    import msvcrt
else:
    import tty
    import termios
    import select

def get_key() -> Optional[str]:
    """Detects a key press in a non-blocking way across platforms."""
    if _IS_WINDOWS:
        if msvcrt.kbhit():
            try:
                return msvcrt.getch().decode('utf-8').lower()
            except UnicodeDecodeError:
                return None
    else:
        # Linux/macOS non-blocking read
        dr, dw, de = select.select([sys.stdin], [], [], 0)
        if dr:
            return sys.stdin.read(1).lower()
    return None

def setup_terminal():
    """Sets up the terminal for non-blocking input on Linux/macOS."""
    if not _IS_WINDOWS:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setcbreak(fd)
        return old_settings
    return None

def restore_terminal(old_settings):
    """Restores terminal settings on Linux/macOS."""
    if not _IS_WINDOWS and old_settings:
        fd = sys.stdin.fileno()
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

# --- TUI Components ---

def create_layout() -> Layout:
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main"),
        Layout(name="footer", size=3)
    )
    return layout

def make_header() -> Panel:
    now = datetime.now().strftime("%H:%M:%S")
    return Panel(
        f"[bold magenta]💅 huzz dashboard[/bold magenta] | [dim]v0.4.0[/dim] | [cyan]{now}[/cyan] | [yellow]press 'q' to exit[/yellow]",
        border_style="magenta"
    )

def make_table(registry: HuzzRegistry) -> Table:
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
        a_color = "green" if asset.aura > 80 else "yellow" if asset.aura > 40 else "red"
        
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
    console = Console()
    reg = registry or _GLOBAL_REGISTRY
    layout = create_layout()
    
    # Platform-specific setup
    old_term_settings = setup_terminal()

    try:
        with Live(layout, console=console, screen=True, refresh_per_second=4):
            start_time = time.time()
            while True:
                if duration is not None and time.time() - start_time > duration:
                    break

                key = get_key()
                if key == 'q':
                    break

                reg.audit()
                layout["header"].update(make_header())
                layout["main"].update(Panel(make_table(reg), title=f"[bold cyan]{reg.name}[/bold cyan]", border_style="cyan"))
                
                assets = reg.get_assets()
                avg_aura = sum(a.aura for a in assets) / len(assets) if assets else 0
                layout["footer"].update(Panel(f"[bold white]system aura: {avg_aura:.1f}[/bold white] | [dim italic]no cap detected[/dim italic] | [dim]press 'q' to quit[/dim]", border_style="magenta"))
                
                time.sleep(0.2)
    except KeyboardInterrupt:
        pass
    finally:
        restore_terminal(old_term_settings)
        console.print("[bold magenta]💅 huzz out.[/bold magenta]")

def main():
    run_tui()

if __name__ == "__main__":
    main()
