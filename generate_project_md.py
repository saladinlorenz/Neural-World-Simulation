#!/usr/bin/env python3
"""Génère PROJECT.md avec l'arborescence complète + le code source de chaque fichier Python."""

import os
import glob

ROOT = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(ROOT, "PROJECT.md")

EXCLUDE_DIRS = {"__pycache__", ".git", "node_modules", ".venv", "venv", "env", ".idea", ".vscode"}
EXCLUDE_FILES = {"generate_project_md.py", "PROJECT.md"}

# Fichiers à inclure dans l'ordre souhaité
PRIORITY_FILES = [
    "main.py",
    "requirements.txt",
]

GAME_FILES_ORDER = [
    "__init__.py",
    "config.py",
    "camera.py",
    "world.py",
    "worldgen.py",
    "entities.py",
    "brain.py",
    "brain_api.py",
    "engine.py",
    "renderer.py",
    "dashboard.py",
    "simulation.py",
    "clock.py",
    "save.py",
    "assets_manager.py",
    "assets_api.py",
    "affordance_definitions.py",
    "ui_kit.py",
    "ui_api.py",
]


def build_tree(root, prefix=""):
    """Construit l'arborescence au format texte."""
    lines = []
    entries = []

    for name in os.listdir(root):
        if name in EXCLUDE_DIRS or name in EXCLUDE_FILES:
            continue
        path = os.path.join(root, name)
        entries.append((name, path, os.path.isdir(path)))

    # Dossiers d'abord, puis fichiers
    dirs = sorted([e for e in entries if e[2]])
    files = sorted([e for e in entries if not e[2]])

    all_entries = dirs + files

    for i, (name, path, is_dir) in enumerate(all_entries):
        is_last = (i == len(all_entries) - 1)
        connector = "└── " if is_last else "├── "
        if is_dir:
            lines.append(f"{prefix}{connector}{name}/")
            ext = "    " if is_last else "│   "
            lines.extend(build_tree(path, prefix + ext))
        else:
            lines.append(f"{prefix}{connector}{name}")

    return lines


def get_file_description(rel_path):
    """Retourne une description courte du fichier."""
    descriptions = {
        "main.py": "Point d'entrée principal",
        "requirements.txt": "Dépendances",
        "game/__init__.py": "Package du laboratoire",
        "game/config.py": "Constantes globales (GRID, TILE, couleurs...)",
        "game/camera.py": "Caméra avec zoom/tilt 2.5D",
        "game/world.py": "WorldGrid (tiles, items, feux, phéromones)",
        "game/worldgen.py": "Génération procédurale (fBm, biomes, pentes)",
        "game/entities.py": "Being, Sheep, ClanKnowledge",
        "game/brain.py": "Cerveau neuronal (Elman, REINFORCE)",
        "game/brain_api.py": "API publique du cerveau",
        "game/engine.py": "Moteur : build_world, populate, place",
        "game/renderer.py": "Rendu (terrain, entités, nuit, pluie)",
        "game/dashboard.py": "Interface complète (panneaux, onglets)",
        "game/simulation.py": "Boucle de simulation (perception→action→conséquence)",
        "game/clock.py": "Temps : jour/nuit, saisons, météo",
        "game/save.py": "Sauvegarde/chargement (pickle)",
        "game/assets_manager.py": "Catalogue d'assets (découverte, sprites)",
        "game/assets_api.py": "API lecture seule des assets",
        "game/affordance_definitions.py": "Registre des affordances",
        "game/ui_kit.py": "Widgets graphiques (boutons, jauges, etc.)",
        "game/ui_api.py": "API publique UI",
    }
    return descriptions.get(rel_path, "")


def count_lines(content):
    """Compte le nombre de lignes."""
    return len(content.splitlines())


def main():
    print(f"Génération de {MD_PATH}...")

    # 1) Arborescence
    tree_lines = ["E:\\my world2\\"]
    tree_lines.extend(build_tree(ROOT))
    tree_str = "\n".join(tree_lines)

    # 2) Collecter les fichiers Python
    py_files = []

    # Fichiers racine
    for fname in PRIORITY_FILES:
        fpath = os.path.join(ROOT, fname)
        if os.path.isfile(fpath):
            rel = os.path.relpath(fpath, ROOT).replace("\\", "/")
            py_files.append((rel, fpath))

    # Fichiers game/
    game_dir = os.path.join(ROOT, "game")
    if os.path.isdir(game_dir):
        # D'abord ceux dans l'ordre souhaité
        added = set()
        for fname in GAME_FILES_ORDER:
            fpath = os.path.join(game_dir, fname)
            if os.path.isfile(fpath):
                rel = os.path.relpath(fpath, ROOT).replace("\\", "/")
                py_files.append((rel, fpath))
                added.add(fname)

        # Puis les autres fichiers .py non encore ajoutés
        for fname in sorted(os.listdir(game_dir)):
            if fname.endswith(".py") and fname not in added and fname not in EXCLUDE_FILES:
                fpath = os.path.join(game_dir, fname)
                rel = os.path.relpath(fpath, ROOT).replace("\\", "/")
                py_files.append((rel, fpath))

    # 3) Générer le markdown
    md_parts = []
    md_parts.append("# Univers Vivant — Documentation Complète du Projet\n")
    md_parts.append("> IA émergente 2D avec terrain procédural, cerveaux neuronaux, sociétés et civilisations.\n")
    md_parts.append("---\n")

    # Arborescence
    md_parts.append("## Arbre du Projet\n")
    md_parts.append("```")
    md_parts.append(tree_str)
    md_parts.append("```\n")
    md_parts.append("---\n")

    # Chaque fichier
    total_lines = 0
    for rel, fpath in py_files:
        desc = get_file_description(rel)
        header = f"## {rel}"
        if desc:
            header += f"  \n*{desc}*"

        try:
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            try:
                with open(fpath, "r", encoding="latin-1") as f:
                    content = f.read()
            except Exception:
                md_parts.append(f"{header}\n\n*(fichier binaire ou illisible)*\n")
                md_parts.append("---\n")
                continue

        nlines = count_lines(content)
        total_lines += nlines

        if rel == "requirements.txt":
            md_parts.append(f"{header}\n")
            md_parts.append("```")
            md_parts.append(content.rstrip())
            md_parts.append("```\n")
        else:
            md_parts.append(f"{header}\n")
            md_parts.append("```python")
            md_parts.append(content.rstrip())
            md_parts.append("```\n")

        md_parts.append("---\n")

    # Footer
    md_parts.append(f"*Généré automatiquement — {len(py_files)} fichiers, ~{total_lines} lignes de code.*\n")

    # 4) Écrire
    md_content = "\n".join(md_parts)
    with open(MD_PATH, "w", encoding="utf-8") as f:
        f.write(md_content)

    size_kb = os.path.getsize(MD_PATH) / 1024
    print(f"  {len(py_files)} fichiers, {total_lines} lignes")
    print(f"  {size_kb:.0f} Ko -> {MD_PATH}")
    print("OK")


if __name__ == "__main__":
    main()
