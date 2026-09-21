"""Exports en TXT, Markdown, CSV, JSON. Pas de Qt/Pygame."""
import json
import csv
import io
from datetime import datetime


def export_txt(report_text, filepath):
    """Export report as plain text."""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report_text)
    return filepath


def export_markdown(report_text, timeline_events=None, metrics=None, filepath=None):
    """Export as Markdown with optional sections."""
    lines = []
    lines.append("# Rapport de simulation")
    lines.append(f"\n*Généré le {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")
    lines.append("## Résumé\n")
    lines.append(report_text)

    if metrics:
        lines.append("\n## Métriques\n")
        lines.append("| Métrique | Valeur |")
        lines.append("|----------|--------|")
        for k, v in metrics.items():
            lines.append(f"| {k} | {v} |")

    if timeline_events:
        lines.append("\n## Événements importants\n")
        for event in timeline_events[:50]:
            lines.append(f"- {event}")

    content = "\n".join(lines)
    if filepath:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
    return content


def export_csv(metrics_dict, filepath):
    """Export metrics as CSV."""
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Métrique", "Valeur"])
        for k, v in metrics_dict.items():
            writer.writerow([k, v])
    return filepath


def export_json(data, filepath, indent=2):
    """Export full data as JSON."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False, default=str)
    return filepath


def export_full_report(result, timeline_events=None, directory="."):
    """Export a complete report in all formats."""
    from .studio_reports import build_report, build_short_summary

    report = build_report(result)
    summary = build_short_summary(result)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    scenario = result.get("scenario", "standard")
    base = f"report_{scenario}_{timestamp}"

    exports = {}
    exports["txt"] = export_txt(report, f"{directory}/{base}.txt")
    exports["markdown"] = export_markdown(
        report, timeline_events, result.get("metrics", {}),
        f"{directory}/{base}.md"
    )
    exports["csv"] = export_csv(result.get("metrics", {}), f"{directory}/{base}.metrics.csv")
    exports["json"] = export_json(result, f"{directory}/{base}.json")

    return exports
