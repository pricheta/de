# DE by pricheta

## Project Overview
Custom desktop environment/launcher application built with PyQt6. Displays fullscreen button menus for launching applications or performing system actions (reboot/poweroff).

## Tech Stack
- **Python 3.14+**
- **PyQt6** - GUI framework
- **Pydantic** - Configuration validation
- **mypy/ruff/black** - Code quality tools

## Architecture

### Entry Point
- `__main__.py` - Loads config from JSON, initializes WindowManager, starts FifoReader thread

### Core Modules
| File | Description |
|------|-------------|
| `code/fifo_reader.py` | Reads from named pipe (FIFO), emits signals on messages |
| `code/window.py` | Window & WindowManager classes, widget factory |
| `code/const.py` | Logger, type definitions, WidgetName enum |
| `code/widgets/base.py` | PrichetaWidget base class (QGridLayout) |
| `code/widgets/button_menu.py` | ButtonMenu widget - grid of clickable buttons |

### Configuration
- `conf/config.json` - Main config with FIFO_PATH and WINDOWS list
- Each window has: TITLE, X, Y, WIDTH, HEIGHT, CSS_FILE_PATH, WIDGETS
- Supported widgets: "Button Menu" (grid of buttons launching commands)
- CSS stylesheets in `conf/*/style.css`

## IPC Mechanism
1. External process writes window name to FIFO (`/tmp/pricheta_de`)
2. FifoReader thread reads message and emits signal
3. WindowManager builds and shows corresponding window
4. On button click: executes command, optionally hides window

## Commands
```bash
python -m code          # Run application
ruff check             # Lint
mypy                  # Type check
black                 # Format
```

## Key Patterns
- Pydantic models for config validation (AppConfig, WindowConfig, ButtonMenuConfig)
- Signal/slot pattern for FIFO → GUI communication
- Widgets are QLayouts containing other widgets
- Window stays hidden on close (destroyed only when new window opens)