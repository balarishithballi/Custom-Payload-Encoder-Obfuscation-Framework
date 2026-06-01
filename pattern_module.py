import re

EDUCATIONAL_KEYWORDS = [
    "education", "student", "science", "research",
    "python", "learning", "school", "university",
    "algorithm", "network", "security", "data"
]


def keyword_match(text, keywords=None):
    if keywords is None:
        keywords = EDUCATIONAL_KEYWORDS
    found = []
    text_lower = text.lower()
    for kw in keywords:
        if kw.lower() in text_lower:
            found.append(kw)
    return {"success": True, "matched": found, "count": len(found)}


def regex_match(text, pattern):
    try:
        matches = re.findall(pattern, text)
        unique_matches = list(dict.fromkeys(matches))
        return {"success": True, "matches": unique_matches, "count": len(unique_matches)}
    except re.error as e:
        return {"success": False, "error": f"Invalid regex pattern: {str(e)}"}


def compare_patterns(original, transformed, keywords=None):
    if keywords is None:
        keywords = EDUCATIONAL_KEYWORDS
    orig_result = keyword_match(original, keywords)
    trans_result = keyword_match(transformed, keywords)

    orig_set = set(orig_result["matched"])
    trans_set = set(trans_result["matched"])

    still_matched = list(orig_set & trans_set)
    lost_after_transform = list(orig_set - trans_set)
    new_in_transformed = list(trans_set - orig_set)

    return {
        "success": True,
        "original_matches": orig_result["matched"],
        "transformed_matches": trans_result["matched"],
        "still_matched": still_matched,
        "lost_after_transform": lost_after_transform,
        "new_in_transformed": new_in_transformed
    }
