from __future__ import annotations

from pathlib import Path


def is_page_number(line: str) -> bool:
    s = line.strip()
    # Les pages de l'édition sont de simples chiffres isolés
    return s.isdigit() and len(s) <= 4


def iter_paragraphs(lines: list[str]) -> list[list[str]]:
    paragraphs: list[list[str]] = []
    current: list[str] = []

    for raw in lines:
        line = raw.rstrip("\n")
        stripped = line.strip()

        # Ignorer les lignes vides
        if not stripped:
            if current:
                paragraphs.append(current)
                current = []
            continue

        # Ignorer les numéros de page isolés
        if is_page_number(stripped):
            continue

        # Dialogues : ligne commençant par un tiret cadratin / demi-cadratin
        if stripped.startswith("—"):
            if current:
                paragraphs.append(current)
                current = []
            paragraphs.append([line])
            continue

        # Ligne normale : faire partie du paragraphe courant
        current.append(line)

    if current:
        paragraphs.append(current)

    return paragraphs


def join_paragraph(lines: list[str]) -> str:
    """Recolle les lignes en un seul paragraphe propre."""
    parts: list[str] = []
    for raw in lines:
        s = raw.strip()
        if not s:
            continue
        if not parts:
            parts.append(s)
            continue

        prev = parts[-1]
        # Gestion simple des césures : mot coupé avec un tiret en fin de ligne
        if prev.endswith("-"):
            parts[-1] = prev[:-1] + s
        else:
            parts[-1] = prev + " " + s

    return parts[0] if parts else ""


def convert(input_path: Path, output_path: Path) -> None:
    text = input_path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()

    paragraphs = iter_paragraphs(lines)

    out_lines: list[str] = []

    for para_lines in paragraphs:
        joined = join_paragraph(para_lines)
        if not joined:
            continue
        out_lines.append(joined)
        out_lines.append("")  # ligne vide entre paragraphes

    output_path.write_text("\n".join(out_lines), encoding="utf-8")


def main() -> None:
    base = Path(__file__).resolve().parent
    input_path = base / "Seigneur_de_Lumiere.txt"
    output_path = base / "seigneur_de_lumiere.md"

    if not input_path.exists():
        raise SystemExit(f"Fichier introuvable : {input_path}")

    convert(input_path, output_path)
    print(f"Fichier généré : {output_path}")


if __name__ == "__main__":
    main()
