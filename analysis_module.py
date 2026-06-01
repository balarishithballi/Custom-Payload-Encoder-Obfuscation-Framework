import math
from collections import Counter


def char_frequency(text, top_n=10):
    if not text:
        return {"success": False, "error": "Text is empty."}
    counter = Counter(text)
    ordered = sorted(counter.items(), key=lambda x: x[1], reverse=True)
    top = ordered[:top_n]
    return {"success": True, "results": top, "total_chars": len(text)}


def shannon_entropy(text):
    if not text:
        return {"success": True, "entropy": 0.0}
    freq = Counter(text)
    total = len(text)
    entropy = 0.0
    for count in freq.values():
        prob = count / total
        entropy -= prob * math.log2(prob)
    return {"success": True, "entropy": round(entropy, 4)}


def similarity_score(text1, text2):
    if not text1 and not text2:
        return {"success": True, "score": 1.0, "percentage": "100.00%"}
    if not text1 or not text2:
        return {"success": True, "score": 0.0, "percentage": "0.00%"}

    set1 = set(text1)
    set2 = set(text2)
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    score = intersection / union if union > 0 else 0.0
    score = round(score, 4)
    return {"success": True, "score": score, "percentage": f"{score * 100:.2f}%"}


def run_analysis_tests():
    results = []

    # Entropy returns numeric
    e = shannon_entropy("hello world this is a test string")
    results.append({
        "test": "Entropy returns numeric value",
        "passed": e["success"] and isinstance(e["entropy"], float),
        "detail": str(e.get("entropy"))
    })

    # Similarity between 0 and 1
    s = similarity_score("hello", "hello world")
    results.append({
        "test": "Similarity score between 0 and 1",
        "passed": s["success"] and 0.0 <= s["score"] <= 1.0,
        "detail": str(s.get("score"))
    })

    # Entropy of empty string
    e2 = shannon_entropy("")
    results.append({
        "test": "Entropy handles empty string",
        "passed": e2["success"] and e2["entropy"] == 0.0,
        "detail": str(e2.get("entropy"))
    })

    return results
