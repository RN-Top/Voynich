import json

import streamlit as st

st.set_page_config(page_title="Voynich Investigation", layout="wide")


@st.cache_data
def load(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


integrated = load("voynich_integrated.json")
control = load("voynich_control.json")
meta = (integrated or {}).get("metadata", {})

# HEADER
st.title("Voynich Manuscript Investigation")
st.subheader("An open, testable dataset of the Voynich text and pictures, and the tests run on it")
st.caption("Erin Rae Toppe · independent review: Juan Gabriel Molina · no decipherment is claimed")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Pages and panels", meta.get("folios_total", "—"))
c2.metric("Words", f"{meta.get('total_words', 0):,}" if meta else "—")
c3.metric("Pages linked to Yale photos", meta.get("yale_image_coverage", "—"))
c4.metric("Status", "Ongoing")

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(
    ["What has held up", "Hypotheses being tested", "Data", "How we work"]
)

# ---------------------------------------------------------------------------
with tab1:
    st.markdown("## Results that have passed testing")
    st.write(
        "Each of these was pre-registered: the prediction and the pass rule were written down "
        "before the test was run. Details and rerun commands are in FOR_REVIEWERS.md."
    )

    st.markdown("### Plant pages and star labels share rare spellings")
    st.write(
        "14 of 128 opening words on the herbal pages share an unusual letter chunk with the star "
        "labels on f67r2 and f68r1–3, against 4.5 expected by chance (p = 0.0001). Examples: "
        "*koaiin* ~ *okoaly*, *pocheody* ~ *opocphor*, *tydlo* ~ *otydy*. This fits the medieval "
        "idea that each herb belongs to a star. It is the strongest link so far between the text "
        "and something we can name."
    )

    st.markdown("### The text has real structure")
    st.write(
        "- Word order carries information; shuffling it weakens the patterns.\n"
        "- A word's ending predicts how the next word begins.\n"
        "- Word beginnings track the section of the book; endings behave like grammar.\n"
        "- Words ending in -m / -am sit at the end of lines far more than chance.\n"
        "- Pages on the same sheet of parchment share more vocabulary than other pages."
    )

    st.markdown("## Tested and ruled out")
    st.markdown("### Simple substitution ciphers, including Fontana's methods")
    st.write(
        "36 letter-swap ciphers (one or several signs per letter; forwards, reversed or mirrored; "
        "into Latin, Italian or Venetian) were tried. The same program cracks real Latin and Italian "
        "enciphered this way at 94–100%, but none decodes the Voynich. The Voynich is more predictable "
        "letter to letter than Latin or Italian, and a letter swap cannot cause that."
    )
    st.write(
        "Also ruled out: the published Venetian and German glosses, zodiac labels as day names, "
        "the 28 lunar mansions, the Metonic cycle, and a reading as alchemical recipes. "
        "Full list with numbers in VALIDATION.md."
    )

# ---------------------------------------------------------------------------
with tab2:
    st.markdown("## Open hypotheses")
    st.write("These are lines of inquiry, not findings. Each says what would support or rule it out.")

    with st.expander("Giovanni Fontana as author", expanded=True):
        st.write(
            "**Status: open.** Fontana (Padua physician and cipher writer, degrees 1418 and 1421) fits "
            "the parchment's radiocarbon date (1404–1438), and an independent researcher reached him "
            "separately. Simple versions of his cipher methods do not decode the text, but that does not "
            "rule him out as author.\n\n"
            "**Would support it:** a handwriting match against his autograph manuscripts; a symbol-by-symbol "
            "match between his cipher wheel and the ring of symbols on f57v; records from Padua.\n\n"
            "**Would weaken it:** a handwriting comparison that fails; Padua records placing him elsewhere."
        )

    with st.expander("Plant pages linked to star pages"):
        st.write(
            "**Status: supported once, being extended.** Next step: identify the drawn plants, look up "
            "which star medieval herbals assign each one, and test whether the shared spellings follow "
            "those pairings."
        )

    with st.expander("Zodiac pages: solar or lunar counting"):
        st.write(
            "**Status: not yet tested.** Count the figures and stars on each zodiac page, write down "
            "before counting what the sun (about 30 per sign) and the moon (28 or 29.5) would predict, "
            "then compare."
        )

    with st.expander("Irish medical tradition (Ó hÍceadha) and Rhazes"):
        st.write(
            "**Status: not supported so far.** An independent 15-test battery found no Irish lexical signal, "
            "and the Rhazes condition–cause–cure pattern was not distinctive. Kept open pending new sources."
        )

# ---------------------------------------------------------------------------
with tab3:
    st.markdown("## The integrated file")
    st.write(
        "**voynich_integrated.json** holds the whole manuscript in book order: each page's ZL3b text, "
        "labels, drawing type, and its Yale photo link(s)."
    )
    st.write(
        "**voynich_control.json** is the same file with words shuffled across pages. Any pattern found "
        "in the real file should be checked in the control; if it shows up there too, it is not real."
    )
    if meta:
        st.json(
            {
                k: meta.get(k)
                for k in [
                    "text_source",
                    "image_source",
                    "folios_total",
                    "total_words",
                    "unique_words",
                    "total_lines",
                    "pages_by_illustration",
                    "yale_image_coverage",
                ]
            }
        )
    col1, col2 = st.columns(2)
    if integrated:
        col1.download_button(
            "Download voynich_integrated.json",
            json.dumps(integrated),
            "voynich_integrated.json",
            "application/json",
        )
    if control:
        col2.download_button(
            "Download voynich_control.json",
            json.dumps(control),
            "voynich_control.json",
            "application/json",
        )

# ---------------------------------------------------------------------------
with tab4:
    st.markdown("## How we work")
    st.write(
        "- **Fix the test before running it.** The prediction, comparison and pass rule are committed first.\n"
        "- **Keep every result.** Failed tests stay on record next to the ones that passed.\n"
        "- **Check against a control.** Every pattern is compared with shuffled text.\n"
        "- **A reading must predict.** A proposed meaning counts only if it works on pages it wasn't built from."
    )
    st.markdown("### Sources")
    st.write(
        "- Transliteration: ZL3b by René Zandbergen and Gabriel Landini (voynich.nu)\n"
        "- Images: Yale Beinecke Library, MS 408\n"
        "- Code, tests and results: https://github.com/RN-Top/Voynich"
    )

st.markdown("---")
st.caption("Last updated 17 November 2026 · open investigation, not a claimed solution")
