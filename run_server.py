#!/usr/bin/env python3
"""
Script de lancement du serveur MCP-Odoo
Force l'utilisation du bon environnement Python
"""

import sys
import os
from pathlib import Path

# Force l'utilisation du venv si disponible
venv_python = Path(__file__).parent / ".venv" / "bin" / "python"
if venv_python.exists() and str(venv_python) != sys.executable:
    print(f"🔄 Relancement avec le Python du venv: {venv_python}")
    os.execv(str(venv_python), [str(venv_python)] + sys.argv)

# Ajouter le répertoire src au path
src_path = str(Path(__file__).parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

if __name__ == "__main__":
    from odoo_mcp.server import main
    main() 