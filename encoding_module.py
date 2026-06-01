import base64
import codecs


def base64_encode(text):
    try:
        encoded = base64.b64encode(text.encode("utf-8")).decode("utf-8")
        return {"success": True, "result": encoded}
    except Exception as e:
        return {"success": False, "error": str(e)}


def base64_decode(encoded_text):
    try:
        decoded = base64.b64decode(encoded_text.encode("utf-8")).decode("utf-8")
        return {"success": True, "result": decoded}
    except Exception:
        return {"success": False, "error": "Invalid Base64 string. Please check input."}


def xor_encode(text, key=42):
    try:
        xor_bytes = bytes([b ^ key for b in text.encode("utf-8")])
        hex_result = xor_bytes.hex()
        return {"success": True, "result": hex_result}
    except Exception as e:
        return {"success": False, "error": str(e)}


def xor_decode(hex_text, key=42):
    try:
        hex_text = hex_text.strip()
        if not all(c in "0123456789abcdefABCDEF" for c in hex_text):
            return {"success": False, "error": "Input contains non-hexadecimal characters."}
        if len(hex_text) % 2 != 0:
            return {"success": False, "error": "Hex string length must be even."}
        raw_bytes = bytes.fromhex(hex_text)
        decoded = bytes([b ^ key for b in raw_bytes]).decode("utf-8")
        return {"success": True, "result": decoded}
    except UnicodeDecodeError:
        return {"success": False, "error": "Could not decode bytes to text. Check key value."}
    except Exception as e:
        return {"success": False, "error": str(e)}


def rot13_transform(text):
    try:
        result = codecs.encode(text, "rot_13")
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


def run_encoding_tests():
    results = []

    # Base64 roundtrip
    sample = "Hello, Asshole!"
    enc = base64_encode(sample)
    dec = base64_decode(enc["result"]) if enc["success"] else {"success": False}
    results.append({
        "test": "Base64 encode → decode → original",
        "passed": dec.get("result") == sample,
        "detail": dec.get("result", "failed")
    })

    # XOR roundtrip
    enc = xor_encode(sample, key=55)
    dec = xor_decode(enc["result"], key=55) if enc["success"] else {"success": False}
    results.append({
        "test": "XOR encode → decode → original",
        "passed": dec.get("result") == sample,
        "detail": dec.get("result", "failed")
    })

    # ROT13 double transform
    r1 = rot13_transform(sample)
    r2 = rot13_transform(r1["result"]) if r1["success"] else {"success": False}
    results.append({
        "test": "ROT13 transform → transform → original",
        "passed": r2.get("result") == sample,
        "detail": r2.get("result", "failed")
    })

    return results
