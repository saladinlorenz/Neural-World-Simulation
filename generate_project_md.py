from __future__ import annotations

import argparse
import os
from datetime import datetime
from pathlib import Path


# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────

DEFAULT_OUTPUT = "PROJECT.md"

INCLUDED_EXTENSIONS = {
    ".py",
    ".txt",
    ".md",
}

EXCLUDED_DIRS = {
    ".git",
    ".github",
    ".idea",
    ".vscode",
    ".vs",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "dist",
    "build",
    "site-packages",
    "data",
    "saves",
    "output",
    "outputs",
    "logs",
    "cache",
    "caches",
}

EXCLUDED_FILENAMES = {
    "PROJECT.md",
}

MAX_FILE_BYTES = 2_000_000

LANGUAGE_BY_EXTENSION = {
    ".py": "python",
    ".txt": "text",
    ".md": "markdown",
}


# ─────────────────────────────────────────────────────────────────────────────
# Utilitaires
# ─────────────────────────────────────────────────────────────────────────────

def is_excluded_path(path: Path, root: Path, output_path: Path) -> bool:
    """
    Retourne True si le fichier/dossier doit être ignoré.
    """
    try:
        relative = path.relative_to(root)
    except ValueError:
        return True

    if path.resolve() == output_path.resolve():
        return True

    if path.name in EXCLUDED_FILENAMES and path.name == output_path.name:
        return True

    for part in relative.parts:
        if part in EXCLUDED_DIRS:
            return True

    return False


def should_include_file(path: Path, root: Path, output_path: Path) -> bool:
    """
    Détermine si un fichier doit être inclus dans le Markdown final.
    """
    if not path.is_file():
        return False

    if is_excluded_path(path, root, output_path):
        return False

    if path.suffix.lower() not in INCLUDED_EXTENSIONS:
        return False

    try:
        if path.stat().st_size > MAX_FILE_BYTES:
            return False
    except OSError:
        return False

    return True


def safe_read_text(path: Path) -> tuple[str | None, str | None]:
    """
    Lit un fichier texte avec plusieurs encodages.
    Retourne (contenu, erreur).
    """
    encodings = (
        "utf-8",
        "utf-8-sig",
        "cp1252",
        "latin-1",
    )

    for encoding in encodings:
        try:
            return path.read_text(encoding=encoding), None
        except UnicodeDecodeError:
            continue
        except OSError as exc:
            return None, f"{type(exc).__name__}: {exc}"

    return None, "Impossible de décoder le fichier comme texte."


def build_tree(root: Path, output_path: Path) -> list[str]:
    """
    Génère une arborescence texte du projet.
    """
    lines = [f"{root.name}/"]

    def walk(directory: Path, prefix: str = "") -> None:
        try:
            entries = sorted(
                directory.iterdir(),
                key=lambda p: (
                    not p.is_dir(),
                    p.name.lower(),
                ),
            )
        except OSError:
            return

        visible_entries = []

        for entry in entries:
            if is_excluded_path(entry, root, output_path):
                continue

            if entry.is_file():
                if entry.suffix.lower() not in INCLUDED_EXTENSIONS:
                    continue

                try:
                    if entry.stat().st_size > MAX_FILE_BYTES:
                        continue
                except OSError:
                    continue

            visible_entries.append(entry)

        for index, entry in enumerate(visible_entries):
            is_last = index == len(visible_entries) - 1
            branch = "└── " if is_last else "├── "
            suffix = "/" if entry.is_dir() else ""
            lines.append(f"{prefix}{branch}{entry.name}{suffix}")

            if entry.is_dir():
                next_prefix = prefix + ("    " if is_last else "│   ")
                walk(entry, next_prefix)

    walk(root)
    return lines


def markdown_header(title: str, level: int = 1) -> str:
    return f"{'#' * level} {title}\n"


def file_section(relative_path: Path, content: str) -> str:
    """
    Génère une section Markdown pour un fichier.
    """
    extension = relative_path.suffix.lower()
    language = LANGUAGE_BY_EXTENSION.get(extension, "")

    # Empêche un contenu contenant ``` de casser le Markdown.
    fence = "```"
    if "```" in content:
        fence = "````"

    result = []
    result.append(markdown_header(str(relative_path).replace("\\", "/"), 2))
    result.append(f"**Type :** `{extension or 'sans extension'}`\n")
    result.append(f"{fence}{language}\n")
    result.append(content.rstrip())
    result.append(f"\n{fence}\n")

    return "\n".join(result)


# ─────────────────────────────────────────────────────────────────────────────
# Génération
# ─────────────────────────────────────────────────────────────────────────────

def generate_markdown(root: Path, output_path: Path) -> tuple[int, int, list[str]]:
    """
    Crée le fichier Markdown.
    Retourne :
    - nombre de fichiers inclus ;
    - nombre de fichiers ignorés ;
    - liste des avertissements.
    """
    warnings: list[str] = []
    included_files: list[Path] = []
    ignored_count = 0

    for current_root, dirs, files in os.walk(root):
        current_path = Path(current_root)

        dirs[:] = [
            dirname
            for dirname in dirs
            if not is_excluded_path(current_path / dirname, root, output_path)
        ]

        for filename in files:
            path = current_path / filename

            if should_include_file(path, root, output_path):
                included_files.append(path)
            else:
                if path.suffix.lower() in INCLUDED_EXTENSIONS:
                    ignored_count += 1

    included_files.sort(
        key=lambda path: str(path.relative_to(root)).lower()
    )

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    document: list[str] = []

    document.append(markdown_header("Documentation complète du projet"))
    document.append(
        "Ce document a été généré automatiquement par `generate_project_md.py`.\n"
    )
    document.append(f"- **Racine du projet :** `{root}`\n")
    document.append(f"- **Date de génération :** `{now}`\n")
    document.append(f"- **Fichiers inclus :** `{len(included_files)}`\n")
    document.append(f"- **Extensions incluses :** `{', '.join(sorted(INCLUDED_EXTENSIONS))}`\n")

    document.append(markdown_header("Arborescence du projet", 2))
    document.append("```text")
    document.extend(build_tree(root, output_path))
    document.append("```\n")

    document.append(markdown_header("Contenu des fichiers", 2))

    for path in included_files:
        relative = path.relative_to(root)

        content, error = safe_read_text(path)

        if error is not None:
            warnings.append(f"{relative}: {error}")
            document.append(markdown_header(str(relative).replace("\\", "/"), 2))
            document.append(f"> ⚠️ Impossible de lire ce fichier : `{error}`\n")
            continue

        document.append(file_section(relative, content))

    if warnings:
        document.append(markdown_header("Avertissements", 2))
        for warning in warnings:
            document.append(f"- {warning}")

    output_path.write_text(
        "\n".join(document) + "\n",
        encoding="utf-8",
    )

    return len(included_files), ignored_count, warnings


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Génère un Markdown unique contenant l'arborescence et tous "
            "les fichiers .py, .txt et .md du projet."
        )
    )

    parser.add_argument(
        "--root",
        default=".",
        help="Dossier racine du projet. Défaut : dossier courant.",
    )

    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help=f"Fichier Markdown généré. Défaut : {DEFAULT_OUTPUT}",
    )

    parser.add_argument(
        "--include-assets",
        action="store_true",
        help=(
            "Inclut les fichiers texte présents dans assets/. "
            "Par défaut, assets/ est exclu."
        ),
    )

    parser.add_argument(
        "--include-data",
        action="store_true",
        help=(
            "Inclut les fichiers texte présents dans data/. "
            "Par défaut, data/ est exclu."
        ),
    )

    args = parser.parse_args()

    root = Path(args.root).resolve()
    output_path = Path(args.output)

    if not output_path.is_absolute():
        output_path = root / output_path

    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Erreur : racine invalide : {root}")

    if args.include_assets:
        EXCLUDED_DIRS.discard("assets")

    if args.include_data:
        EXCLUDED_DIRS.discard("data")
        EXCLUDED_DIRS.discard("saves")

    included, ignored, warnings = generate_markdown(root, output_path)

    print("PROJECT.md généré avec succès.")
    print(f"Racine     : {root}")
    print(f"Sortie     : {output_path}")
    print(f"Inclus     : {included} fichiers")
    print(f"Ignorés    : {ignored} fichiers texte")
    print(f"Avertissements : {len(warnings)}")


if __name__ == "__main__":
    main()
