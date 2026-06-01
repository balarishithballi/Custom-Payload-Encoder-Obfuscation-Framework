import json
from datetime import datetime


def build_report(original_text, transformation_used, transform_result,
                 analysis_results=None, pattern_results=None):
    report = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "original_text": original_text,
        "transformation": {
            "type": transformation_used,
            "result": transform_result
        },
        "analysis": analysis_results or {},
        "pattern_matching": pattern_results or {}
    }
    return report


def report_to_json(report):
    try:
        return json.dumps(report, indent=4, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)})


def build_summary_text(report):
    lines = []
    lines.append("=" * 50)
    lines.append("TEXT ENCODING ANALYSIS REPORT")
    lines.append("=" * 50)
    lines.append(f"Timestamp     : {report.get('timestamp', 'N/A')}")
    lines.append(f"Original Text : {report.get('original_text', '')[:80]}")
    lines.append(f"Transformation: {report.get('transformation', {}).get('type', 'N/A')}")
    lines.append("")

    analysis = report.get("analysis", {})
    if analysis:
        lines.append("--- Analysis ---")
        if "entropy" in analysis:
            lines.append(f"Shannon Entropy : {analysis['entropy']}")
        if "similarity" in analysis:
            lines.append(f"Similarity Score: {analysis['similarity']}")
        if "top_chars" in analysis:
            lines.append("Top Characters:")
            for char, count in analysis["top_chars"][:5]:
                display_char = repr(char) if char in (" ", "\t", "\n") else char
                lines.append(f"  '{display_char}': {count}")

    pattern = report.get("pattern_matching", {})
    if pattern:
        lines.append("")
        lines.append("--- Pattern Matching ---")
        lines.append(f"Original matches    : {pattern.get('original_matches', [])}")
        lines.append(f"Transformed matches : {pattern.get('transformed_matches', [])}")

    lines.append("=" * 50)
    return "\n".join(lines)
