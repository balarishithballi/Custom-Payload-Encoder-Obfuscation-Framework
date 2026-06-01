import streamlit as st
import json

from encoding_module import (
    base64_encode, base64_decode,
    xor_encode, xor_decode,
    rot13_transform,
    run_encoding_tests
)
from transform_module import (
    reverse_text, escape_convert,
    alternating_split, alternating_merge,
    insert_noise, remove_noise,
    run_transform_tests
)
from analysis_module import char_frequency, shannon_entropy, similarity_score, run_analysis_tests
from pattern_module import keyword_match, regex_match, compare_patterns, EDUCATIONAL_KEYWORDS
from report_module import build_report, report_to_json, build_summary_text
from sample_data import SAMPLE_TEXTS, DEFAULT_TEXT
from utils import validate_text_input, truncate_display

st.set_page_config(
    page_title="Text Encoding & Transformation Framework",
    page_icon="🔐",
    layout="wide"
)

# ─── Session State Defaults ────────────────────────────────────────────────────
if "last_report" not in st.session_state:
    st.session_state.last_report = None
if "transform_result" not in st.session_state:
    st.session_state.transform_result = ""
if "original_text" not in st.session_state:
    st.session_state.original_text = DEFAULT_TEXT


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("⚙️ Settings")
    st.markdown("---")

    st.subheader("🔑 XOR Settings")
    xor_key = st.slider("XOR Key (0–255)", min_value=0, max_value=255, value=42)

    st.subheader("🔊 Noise Settings")
    noise_count = st.slider("Noise Characters to Insert", min_value=1, max_value=10, value=3)

    st.subheader("📊 Analysis Settings")
    top_n = st.slider("Top-N Characters to Show", min_value=1, max_value=20, value=10)

    st.subheader("🔍 Sample Texts")
    selected_sample = st.selectbox("Load a sample text:", ["(none)"] + SAMPLE_TEXTS)
    if selected_sample != "(none)":
        st.session_state.original_text = selected_sample

    st.markdown("---")
    st.caption("Text Encoding & Transformation Analysis Framework")
    st.caption("Educational Use Only | BCA / BSc Cyber Security")


# ─── Header ───────────────────────────────────────────────────────────────────
st.title("🔐 Text Encoding & Transformation Analysis Framework")
st.markdown(
    "An educational tool for studying **text encoding**, "
    "**reversible transformations**, **pattern matching**, and **statistical analysis**."
)
st.markdown("---")

# ─── Text Input ───────────────────────────────────────────────────────────────
input_text = st.text_area(
    "📝 Enter Text for Analysis",
    value=st.session_state.original_text,
    height=100,
    key="main_input"
)
if input_text:
    st.session_state.original_text = input_text

# ─── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔒 Encoding",
    "🔄 Transformations",
    "📊 Analysis",
    "🔍 Pattern Matching",
    "📋 Reports"
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — ENCODING
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.header("Text Encoding")
    st.info("Encode and decode text using Base64, XOR (hex output), and ROT13.")

    col1, col2 = st.columns(2)

    # ── Base64 ──
    with col1:
        st.subheader("📦 Base64")
        if st.button("Base64 Encode", key="b64_enc"):
            valid, err = validate_text_input(input_text)
            if not valid:
                st.error(err)
            else:
                result = base64_encode(input_text)
                if result["success"]:
                    st.success("Encoded successfully")
                    st.code(result["result"], language=None)
                    st.session_state.transform_result = result["result"]
                    st.session_state.last_report = build_report(
                        input_text, "Base64 Encode", result["result"]
                    )
                else:
                    st.error(result["error"])

        b64_decode_input = st.text_input("Base64 string to decode:", key="b64_decode_in")
        if st.button("Base64 Decode", key="b64_dec"):
            if not b64_decode_input.strip():
                st.error("Please enter a Base64 string to decode.")
            else:
                result = base64_decode(b64_decode_input)
                if result["success"]:
                    st.success("Decoded successfully")
                    st.code(result["result"], language=None)
                else:
                    st.error(result["error"])

    # ── XOR ──
    with col2:
        st.subheader(f"🔑 XOR (Key: {xor_key})")
        if st.button("XOR Encode → Hex", key="xor_enc"):
            valid, err = validate_text_input(input_text)
            if not valid:
                st.error(err)
            else:
                result = xor_encode(input_text, key=xor_key)
                if result["success"]:
                    st.success("XOR encoded (hex output)")
                    st.code(result["result"], language=None)
                    st.session_state.transform_result = result["result"]
                    st.session_state.last_report = build_report(
                        input_text, f"XOR Encode (key={xor_key})", result["result"]
                    )
                else:
                    st.error(result["error"])

        xor_decode_input = st.text_input("Hex string to XOR-decode:", key="xor_decode_in")
        if st.button("XOR Decode", key="xor_dec"):
            if not xor_decode_input.strip():
                st.error("Please enter a hex string to decode.")
            else:
                result = xor_decode(xor_decode_input, key=xor_key)
                if result["success"]:
                    st.success("Decoded successfully")
                    st.code(result["result"], language=None)
                else:
                    st.error(result["error"])

    # ── ROT13 ──
    st.subheader("🔁 ROT13")
    if st.button("Apply ROT13", key="rot13_btn"):
        valid, err = validate_text_input(input_text)
        if not valid:
            st.error(err)
        else:
            result = rot13_transform(input_text)
            if result["success"]:
                st.success("ROT13 applied")
                st.code(result["result"], language=None)
                st.session_state.transform_result = result["result"]
                st.session_state.last_report = build_report(
                    input_text, "ROT13", result["result"]
                )
                double = rot13_transform(result["result"])
                st.caption(f"ROT13 applied twice returns: `{truncate_display(double['result'], 80)}`")
            else:
                st.error(result["error"])

    # ── Self-Tests ──
    st.markdown("---")
    if st.button("▶ Run Encoding Self-Tests", key="enc_tests"):
        tests = run_encoding_tests()
        for t in tests:
            icon = "✅" if t["passed"] else "❌"
            st.write(f"{icon} **{t['test']}** → `{truncate_display(str(t['detail']), 60)}`")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — TRANSFORMATIONS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.header("String Transformations")
    st.info("Apply reversible text transformations and inspect the results.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔃 Reverse Text")
        if st.button("Reverse", key="rev_btn"):
            valid, err = validate_text_input(input_text)
            if not valid:
                st.error(err)
            else:
                r = reverse_text(input_text)
                st.success("Text reversed")
                st.code(r["result"], language=None)
                st.session_state.transform_result = r["result"]
                st.session_state.last_report = build_report(input_text, "Reverse", r["result"])

        st.subheader("🔠 Escape Sequences")
        if st.button("Convert Escape Chars", key="esc_btn"):
            valid, err = validate_text_input(input_text)
            if not valid:
                st.error(err)
            else:
                r = escape_convert(input_text)
                if r["success"]:
                    st.success("Escape conversion done")
                    st.code(r["result"], language=None)
                else:
                    st.error(r["error"])

    with col2:
        st.subheader("✂️ Alternating Split")
        if st.button("Split (Even/Odd chars)", key="split_btn"):
            valid, err = validate_text_input(input_text)
            if not valid:
                st.error(err)
            else:
                r = alternating_split(input_text)
                st.success("Split complete")
                st.write(f"**Part A** (even positions): `{r['part_a']}`")
                st.write(f"**Part B** (odd positions): `{r['part_b']}`")
                st.session_state["split_a"] = r["part_a"]
                st.session_state["split_b"] = r["part_b"]

        st.subheader("🔗 Merge Parts")
        merge_a = st.text_input("Part A:", value=st.session_state.get("split_a", ""), key="merge_a")
        merge_b = st.text_input("Part B:", value=st.session_state.get("split_b", ""), key="merge_b")
        if st.button("Merge → Reconstruct", key="merge_btn"):
            if not merge_a and not merge_b:
                st.error("Enter Part A and/or Part B to merge.")
            else:
                r = alternating_merge(merge_a, merge_b)
                if r["success"]:
                    st.success("Merged")
                    st.code(r["result"], language=None)
                else:
                    st.error(r["error"])

    st.subheader(f"🔊 Noise Insertion (count = {noise_count})")
    if st.button(f"Insert {noise_count} Noise Character(s)", key="noise_btn"):
        valid, err = validate_text_input(input_text)
        if not valid:
            st.error(err)
        else:
            r = insert_noise(input_text, noise_count)
            if r["success"]:
                st.success("Noise inserted")
                st.code(r["result"], language=None)
                st.session_state["noisy_text"] = r["result"]
                st.session_state.last_report = build_report(
                    input_text, f"Noise Insertion (n={noise_count})", r["result"]
                )
            else:
                st.error(r["error"])

    noisy_input = st.text_input(
        "Noisy text to clean:",
        value=st.session_state.get("noisy_text", ""),
        key="noisy_in"
    )
    if st.button("Remove Noise Characters", key="denoise_btn"):
        if not noisy_input.strip():
            st.error("Enter noisy text to clean.")
        else:
            r = remove_noise(noisy_input)
            st.success("Noise removed")
            st.code(r["result"], language=None)

    st.markdown("---")
    if st.button("▶ Run Transform Self-Tests", key="trans_tests"):
        tests = run_transform_tests()
        for t in tests:
            icon = "✅" if t["passed"] else "❌"
            st.write(f"{icon} **{t['test']}** → `{truncate_display(str(t['detail']), 60)}`")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.header("Text Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"📊 Character Frequency (Top {top_n})")
        if st.button("Analyse Frequency", key="freq_btn"):
            valid, err = validate_text_input(input_text)
            if not valid:
                st.error(err)
            else:
                r = char_frequency(input_text, top_n=top_n)
                if r["success"]:
                    st.write(f"Total characters: **{r['total_chars']}**")
                    rows = []
                    for i, (char, count) in enumerate(r["results"], 1):
                        display = repr(char) if char in (" ", "\t", "\n") else char
                        rows.append({"Rank": i, "Character": display, "Count": count})
                    st.table(rows)
                else:
                    st.error(r["error"])

    with col2:
        st.subheader("🌀 Shannon Entropy")
        if st.button("Calculate Entropy", key="entropy_btn"):
            valid, err = validate_text_input(input_text)
            if not valid:
                st.error(err)
            else:
                r = shannon_entropy(input_text)
                if r["success"]:
                    val = r["entropy"]
                    st.metric("Shannon Entropy (bits)", val)
                    if val < 2:
                        st.info("Low entropy — highly repetitive text.")
                    elif val < 4:
                        st.info("Moderate entropy — mixed content.")
                    else:
                        st.info("High entropy — diverse or encoded-looking text.")
                else:
                    st.error(r.get("error"))

    st.subheader("🤝 Similarity Comparison")
    compare_text = st.text_input("Enter second text to compare against input:", key="compare_in")
    if st.button("Compare Similarity", key="sim_btn"):
        valid, err = validate_text_input(input_text)
        if not valid:
            st.error(err)
        elif not compare_text.strip():
            st.error("Please enter a second text to compare.")
        else:
            r = similarity_score(input_text, compare_text)
            if r["success"]:
                st.metric("Jaccard Similarity", r["percentage"])
                st.progress(r["score"])
            else:
                st.error(r["error"])

    st.markdown("---")
    if st.button("▶ Run Analysis Self-Tests", key="ana_tests"):
        tests = run_analysis_tests()
        for t in tests:
            icon = "✅" if t["passed"] else "❌"
            st.write(f"{icon} **{t['test']}** → `{t['detail']}`")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — PATTERN MATCHING
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.header("Pattern Matching")
    st.info(
        "This module demonstrates **pattern matching behaviour** and "
        "**transformation impact analysis** using keyword and regex matching."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏷️ Keyword Matching")
        custom_kw = st.text_input(
            "Custom keywords (comma-separated, leave blank for defaults):",
            key="custom_kw"
        )
        if st.button("Run Keyword Match", key="kw_btn"):
            valid, err = validate_text_input(input_text)
            if not valid:
                st.error(err)
            else:
                kw_list = [k.strip() for k in custom_kw.split(",") if k.strip()] or EDUCATIONAL_KEYWORDS
                r = keyword_match(input_text, kw_list)
                if r["count"] > 0:
                    st.success(f"Found {r['count']} keyword(s): {r['matched']}")
                else:
                    st.warning("No keywords matched in this text.")

    with col2:
        st.subheader("🔎 Regex Matching")
        regex_pattern = st.text_input("Enter regex pattern:", value=r"\b\w{6,}\b", key="regex_in")
        if st.button("Run Regex Match", key="regex_btn"):
            valid, err = validate_text_input(input_text)
            if not valid:
                st.error(err)
            else:
                r = regex_match(input_text, regex_pattern)
                if r["success"]:
                    st.success(f"{r['count']} unique match(es) found")
                    if r["matches"]:
                        st.write(r["matches"])
                    else:
                        st.warning("No matches found for this pattern.")
                else:
                    st.error(r["error"])

    st.subheader("🔀 Before/After Transformation Comparison")
    transformed_compare = st.text_input(
        "Paste transformed text here to compare pattern matching results:",
        value=st.session_state.transform_result,
        key="trans_compare"
    )
    if st.button("Compare Pattern Matching", key="cmp_btn"):
        valid, err = validate_text_input(input_text)
        if not valid:
            st.error(err)
        elif not transformed_compare.strip():
            st.error("Please enter transformed text to compare.")
        else:
            r = compare_patterns(input_text, transformed_compare)
            if r["success"]:
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("Original Matches", len(r["original_matches"]))
                    st.write(r["original_matches"])
                with c2:
                    st.metric("Transformed Matches", len(r["transformed_matches"]))
                    st.write(r["transformed_matches"])
                with c3:
                    st.metric("Still Present", len(r["still_matched"]))
                    st.write(r["still_matched"])
                if r["lost_after_transform"]:
                    st.warning(f"Keywords no longer matched after transformation: {r['lost_after_transform']}")
                if r["new_in_transformed"]:
                    st.info(f"New matches in transformed text: {r['new_in_transformed']}")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — REPORTS
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.header("Reports")

    if st.button("🔄 Generate Full Report for Current Input", key="gen_report"):
        valid, err = validate_text_input(input_text)
        if not valid:
            st.error(err)
        else:
            freq_r = char_frequency(input_text, top_n=10)
            ent_r = shannon_entropy(input_text)
            kw_r = keyword_match(input_text)

            analysis_data = {
                "entropy": ent_r.get("entropy"),
                "top_chars": freq_r.get("results", []),
                "total_chars": freq_r.get("total_chars", 0)
            }
            pattern_data = {
                "original_matches": kw_r.get("matched", []),
                "transformed_matches": []
            }

            if st.session_state.transform_result:
                kw_trans = keyword_match(st.session_state.transform_result)
                pattern_data["transformed_matches"] = kw_trans.get("matched", [])
                sim = similarity_score(input_text, st.session_state.transform_result)
                analysis_data["similarity"] = sim.get("score")

            report = build_report(
                input_text,
                "Full Analysis Report",
                st.session_state.transform_result or "(no transformation applied)",
                analysis_data,
                pattern_data
            )
            st.session_state.last_report = report

    if st.session_state.last_report:
        report = st.session_state.last_report
        st.subheader("📄 Report Summary")
        st.text(build_summary_text(report))

        json_str = report_to_json(report)
        st.subheader("⬇️ Download Report")
        st.download_button(
            label="Download JSON Report",
            data=json_str,
            file_name="encoding_analysis_report.json",
            mime="application/json"
        )

        st.subheader("🔍 Raw JSON Preview")
        st.json(report)
    else:
        st.info("No report generated yet. Apply a transformation or click 'Generate Full Report' above.")
