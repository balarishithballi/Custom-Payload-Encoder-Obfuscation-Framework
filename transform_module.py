import random
import re

NOISE_CHARS = ["#", "@", "$", "%", "&"]


def reverse_text(text):
    return {"success": True, "result": text[::-1]}


def escape_convert(text):
    try:
        escaped = text.encode("unicode_escape").decode("ascii")
        return {"success": True, "result": escaped}
    except Exception as e:
        return {"success": False, "error": str(e)}


def alternating_split(text):
    part_a = text[0::2]
    part_b = text[1::2]
    return {"success": True, "part_a": part_a, "part_b": part_b}


def alternating_merge(part_a, part_b):
    result = []
    len_a = len(part_a)
    len_b = len(part_b)
    total = len_a + len_b
    ai, bi = 0, 0
    for i in range(total):
        if i % 2 == 0 and ai < len_a:
            result.append(part_a[ai])
            ai += 1
        elif bi < len_b:
            result.append(part_b[bi])
            bi += 1
        elif ai < len_a:
            result.append(part_a[ai])
            ai += 1
    return {"success": True, "result": "".join(result)}


def insert_noise(text, count):
    try:
        count = int(count)
    except (ValueError, TypeError):
        return {"success": False, "error": "Noise count must be a number."}

    if count < 1 or count > 10:
        return {"success": False, "error": "Noise count must be between 1 and 10."}

    if not text:
        return {"success": False, "error": "Input text cannot be empty."}

    chars = list(text)
    total_positions = len(chars) + count
    insert_positions = sorted(random.sample(range(total_positions), count))

    result = []
    orig_idx = 0
    for pos in range(total_positions):
        if pos in insert_positions:
            result.append(random.choice(NOISE_CHARS))
        else:
            if orig_idx < len(chars):
                result.append(chars[orig_idx])
                orig_idx += 1

    return {"success": True, "result": "".join(result)}


def remove_noise(noisy_text):
    cleaned = re.sub(r"[#@$%&]", "", noisy_text)
    return {"success": True, "result": cleaned}


def run_transform_tests():
    results = []
    sample = "HELLOWORLD"

    # Alternating split and merge
    split = alternating_split(sample)
    merged = alternating_merge(split["part_a"], split["part_b"])
    results.append({
        "test": "Alternating split → merge → original",
        "passed": merged["result"] == sample,
        "detail": merged["result"]
    })

    # Noise insert and remove
    noisy = insert_noise(sample, 5)
    if noisy["success"]:
        cleaned = remove_noise(noisy["result"])
        results.append({
            "test": "Noise insert → remove → original",
            "passed": cleaned["result"] == sample,
            "detail": cleaned["result"]
        })
    else:
        results.append({"test": "Noise insert → remove → original", "passed": False, "detail": noisy.get("error")})

    return results
