# Text Encoding & Transformation Analysis Framework

## Project Overview

A safe educational framework built with Python and Streamlit for studying:
- Text encoding (Base64, XOR, ROT13)
- Reversible string transformations
- Statistical text analysis (Shannon entropy, frequency analysis)
- Pattern matching and keyword detection

Suitable for BCA / BSc Cyber Security students, academic demonstrations, and research presentations.

---

## Project Structure

```
text_encoding_framework/
│
├── app.py                  # Main Streamlit application
├── encoding_module.py      # Base64, XOR, ROT13
├── transform_module.py     # Reverse, split, noise, merge
├── analysis_module.py      # Entropy, frequency, similarity
├── pattern_module.py       # Keyword and regex matching
├── report_module.py        # Report generation and export
├── utils.py                # Shared utility helpers
├── sample_data.py          # Educational sample strings
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## Objectives

1. Demonstrate common text encoding techniques in a safe, educational context
2. Allow students to observe the effect of transformations on text
3. Provide statistical analysis tools (entropy, frequency, similarity)
4. Show how pattern matching behaves on original vs transformed text
5. Export analysis reports in JSON format

---

## Module Explanations

### encoding_module.py
Implements Base64 encode/decode, XOR encode/decode (with hex output), and ROT13.
XOR output is always displayed as lowercase hexadecimal — never as raw bytes.

### transform_module.py
Implements reverse, escape conversion, alternating split/merge, and noise insertion.
Noise characters (#, @, $, %, &) are inserted at random positions. All transforms are reversible.

### analysis_module.py
Implements character frequency analysis, Shannon entropy calculation (rounded to 4 decimal places),
and Jaccard similarity scoring between two texts.

### pattern_module.py
Implements keyword matching against educational keywords and custom regex pattern matching.
Includes before/after transformation comparison showing transformation impact on pattern matching.

### report_module.py
Builds structured reports from all analysis results. Supports JSON export and human-readable text summaries.

---

## Architecture

```
User Input (Streamlit)
        │
        ├── encoding_module  → Base64 / XOR / ROT13
        ├── transform_module → Reverse / Split / Noise
        ├── analysis_module  → Entropy / Frequency / Similarity
        ├── pattern_module   → Keywords / Regex / Comparison
        └── report_module    → JSON / Text Summary Export
```

---

## Running Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Streamlit Cloud Deployment

### Steps

1. Push this folder to a GitHub repository (public or private)
2. Go to https://share.streamlit.io
3. Click "New app"
4. Select your GitHub repo, branch, and set main file to `app.py`
5. Click Deploy

### Required Files for Deployment
- `app.py` (entry point)
- `requirements.txt`
- All `.py` module files in the same directory

### Common Issues

| Issue | Fix |
|-------|-----|
| ModuleNotFoundError | Check all .py files are committed to the repo root |
| App crashes on load | Check requirements.txt has `streamlit>=1.32.0` |
| Encoding errors | Ensure all files are saved as UTF-8 |

---

## Self-Test Output (Expected)

```
✅ Base64 encode → decode → original
✅ XOR encode → decode → original
✅ ROT13 transform → transform → original
✅ Alternating split → merge → original
✅ Noise insert → remove → original
✅ Entropy returns numeric value
✅ Similarity score between 0 and 1
✅ Entropy handles empty string
```

---

## Example Outputs

### Base64 Encode
Input:  `Hello, BCA Student!`
Output: `SGVsbG8sIEJDQSBTdHVkZW50IQ==`

### XOR Encode (key=42)
Input:  `Hello`
Output: `62571e5655` (lowercase hex)

### ROT13
Input:  `Python`
Output: `Clguba`

### Shannon Entropy
Input:  `Python is a popular programming language`
Output: `3.8271`

---

## Future Enhancements

1. Add AES encryption demonstration (educational, no key export)
2. Caesar cipher with adjustable shift
3. Morse code transformation
4. Visual entropy histogram chart
5. Side-by-side hex dump viewer
6. Multiple file batch analysis
7. Export reports as PDF
8. Dark/light theme toggle
9. Transformation chaining (apply multiple transforms in sequence)
10. Save/load session state

---

## Viva Voce Questions and Answers

**Q1. What is Base64 encoding?**
A: Base64 encodes binary or text data into a set of 64 printable ASCII characters. It uses A–Z, a–z, 0–9, +, and /. It increases data size by about 33% and is commonly used in email and web protocols.

**Q2. Is Base64 a form of encryption?**
A: No. Base64 is encoding, not encryption. It is fully reversible without any key. It provides no security by itself — it only changes the representation of data.

**Q3. How does XOR encoding work?**
A: XOR (exclusive OR) applies a bitwise operation between each byte of the input and a key value. If the key is K and input byte is B, output is B XOR K. Applying XOR twice with the same key returns the original data.

**Q4. Why is XOR output shown as hexadecimal in this project?**
A: XOR produces raw byte values that may include non-printable characters, which cannot be safely displayed as text. Converting to lowercase hexadecimal ensures the output is always printable and transferable.

**Q5. What is ROT13?**
A: ROT13 shifts each letter in the alphabet by 13 positions. Since there are 26 letters, applying ROT13 twice always returns the original text: ROT13(ROT13(text)) == text.

**Q6. What is Shannon entropy and what does it measure?**
A: Shannon entropy (H) measures the average information content or unpredictability in a string. It is calculated as H = -Σ p(x) log2(p(x)). Higher entropy means more diverse characters; lower entropy means repetitive or predictable content.

**Q7. What does a Shannon entropy of 0 mean?**
A: It means all characters in the string are identical — there is no variation or unpredictability.

**Q8. What is the alternating split transformation?**
A: It separates characters at even positions (Part A) and odd positions (Part B). For "HELLO": Part A = "HLO", Part B = "EL". The original can be reconstructed by interleaving Part A and Part B.

**Q9. What is the purpose of noise insertion?**
A: Noise insertion adds random characters (#, @, $, %, &) at random positions in the text. The original text can be recovered by removing all noise characters. It demonstrates how text can be obscured while remaining recoverable.

**Q10. What is Jaccard similarity?**
A: Jaccard similarity measures the overlap between two sets. It is: |A ∩ B| / |A ∪ B|. In this project, the sets are the unique characters in each text. A score of 1.0 means identical character sets; 0.0 means no overlap.

**Q11. What is the difference between encoding and encryption?**
A: Encoding transforms data using a publicly known algorithm, with no key — anyone can reverse it. Encryption uses a secret key so only the key holder can decrypt the data.

**Q12. Why is this project safe for academic use?**
A: It uses only standard library Python functions on harmless educational text. It contains no malware, no exploit code, no payload delivery, no command execution, and no security control bypass techniques.

**Q13. What is Streamlit and why was it chosen?**
A: Streamlit is a Python library for building interactive web apps with minimal code. It was chosen because it integrates naturally with Python data science code and requires no frontend JavaScript knowledge.

**Q14. What is session state in Streamlit?**
A: Session state (st.session_state) stores values that persist across user interactions within the same browser session. Without it, all variables reset every time the user clicks a button.

**Q15. What does frequency analysis reveal about a text?**
A: It shows which characters appear most often. In English, E, T, A, O are typically most common. Frequency analysis is a fundamental technique in classical cryptanalysis.

**Q16. Why is XOR considered a symmetric operation?**
A: Because XOR with the same key is its own inverse: (B XOR K) XOR K = B. The same key and operation both encode and decode, making it symmetric.

**Q17. What validation is applied to XOR decode input?**
A: The input is checked to ensure all characters are valid hexadecimal digits (0–9, a–f, A–F) and that the total length is even, since each byte requires exactly two hex digits.

**Q18. What are the noise symbols used in this project?**
A: #, @, $, %, and & — printable ASCII symbols unlikely to appear in normal educational text, making them easy to remove without affecting the original content.

**Q19. How does the pattern comparison feature work?**
A: It runs keyword matching on both the original and transformed text, then compares the results to show which keywords are still matched after transformation, which were lost, and whether any new matches appeared.

**Q20. What is the purpose of the JSON report export?**
A: The JSON report captures the original text, transformation used, analysis results, pattern matching results, and timestamp in a structured format. It can be saved, shared, and used in academic submissions or presentations.
