"""
Streamlit interface for the Voynich Computational Research Workbench.

The application keeps measured corpus structure separate from
exploratory lexical interpretation.
"""

import os

import pandas as pd
import streamlit as st

from analyzer import DeciphermentEngine
from author_audit import AuthorSignatureAuditor
from decoder import ZodiacDeciphermentOracle
from engine_decipher import WholeManuscriptDecipherer
from parser import CORPUS_PATH, parse_zl3b


st.set_page_config(
    page_title="Voynich Computational Research Workbench",
    page_icon="📖",
    layout="wide",
)


@st.cache_data(show_spinner=False)
def load_default_corpus():
    """
    Load and parse the default ZL3b-n transcription.

    parser.py automatically downloads a fresh corpus if the local
    default file is missing or obviously truncated.
    """
    return parse_zl3b(CORPUS_PATH)


def display_dataframe_or_message(
    dataframe,
    empty_message="No matching evidence found.",
):
    """
    Display a DataFrame consistently without crashing on empty results.
    """
    if dataframe is None or dataframe.empty:
        st.info(empty_message)
        return

    st.dataframe(
        dataframe,
        use_container_width=True,
        hide_index=True,
    )


st.title("Voynich Computational Research Workbench")

st.caption(
    "Structural corpus analysis, transition statistics, astronomical-domain "
    "comparison, author/colophon auditing, and explicitly labeled lexical "
    "hypotheses. Statistical evidence and semantic interpretation are kept "
    "separate."
)


st.sidebar.header("Corpus")

uploaded_file = st.sidebar.file_uploader(
    "Upload an IVTFF / ZL-style transcription",
    type=["txt"],
    help=(
        "Leave this empty to use data/ZL3b-n.txt. "
        "Uploaded files are parsed directly in memory."
    ),
)


try:
    if uploaded_file is not None:
        df = parse_zl3b(uploaded_file)
        corpus_source_label = uploaded_file.name
        using_uploaded_corpus = True
    else:
        df = load_default_corpus()
        corpus_source_label = CORPUS_PATH
        using_uploaded_corpus = False

except Exception as exc:
    st.error(
        "The corpus could not be loaded or parsed."
    )
    st.exception(exc)
    st.stop()


if df.empty:
    st.error(
        "The parser returned no usable Voynich tokens. "
        "Check the transcription format."
    )
    st.stop()


required_columns = {
    "folio",
    "clean",
    "section",
    "control",
    "carrier_core",
    "exit_port",
    "state",
}

missing_columns = sorted(
    required_columns - set(df.columns)
)

if missing_columns:
    st.error(
        "The parsed corpus is missing required fields: "
        + ", ".join(missing_columns)
    )
    st.stop()


try:
    structural_engine = DeciphermentEngine(df)
    astronomical_engine = ZodiacDeciphermentOracle(df)
    lexical_engine = WholeManuscriptDecipherer(
        df["clean"].dropna()
    )

except Exception as exc:
    st.error(
        "One of the analysis engines could not initialize."
    )
    st.exception(exc)
    st.stop()


token_count = len(df)

folio_count = (
    df["folio"]
    .dropna()
    .astype(str)
    .nunique()
)

vocabulary_count = (
    df["clean"]
    .dropna()
    .astype(str)
    .nunique()
)

section_count = (
    df["section"]
    .dropna()
    .astype(str)
    .nunique()
)


st.sidebar.markdown("---")

st.sidebar.metric(
    "Parsed tokens",
    f"{token_count:,}",
)

st.sidebar.metric(
    "Folios",
    f"{folio_count:,}",
)

st.sidebar.metric(
    "Vocabulary",
    f"{vocabulary_count:,}",
)

st.sidebar.metric(
    "Sections",
    f"{section_count:,}",
)

st.sidebar.caption(
    f"Source: {corpus_source_label}"
)


tabs = st.tabs(
    [
        "Corpus Reader",
        "Structural Evidence",
        "Astronomical Domain",
        "Author / Colophon Audit",
        "Hypothesis Interpreter",
        "Lexical Table",
        "Export",
    ]
)


# ============================================================
# 1. CORPUS READER
# ============================================================

with tabs[0]:
    st.subheader("Corpus Reader")

    st.write(
        "Inspect the parsed transcription and the structural fields "
        "produced by `parser.py`."
    )

    available_sections = sorted(
        df["section"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_section = st.selectbox(
        "Section",
        ["All sections"] + available_sections,
        key="reader_section",
    )

    reader_df = df.copy()

    if selected_section != "All sections":
        reader_df = reader_df[
            reader_df["section"]
            == selected_section
        ]

    available_folios = sorted(
        reader_df["folio"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    if not available_folios:
        st.info(
            "No folios are available for this selection."
        )

    else:
        selected_folio = st.selectbox(
            "Folio",
            available_folios,
            key="reader_folio",
        )

        folio_df = reader_df[
            reader_df["folio"].astype(str)
            == selected_folio
        ].copy()

        st.caption(
            f"{len(folio_df):,} parsed tokens on "
            f"{selected_folio}."
        )

        if "header" in folio_df.columns:
            line_headers = (
                folio_df["header"]
                .dropna()
                .astype(str)
                .drop_duplicates()
                .tolist()
            )

            for header in line_headers:
                line_df = folio_df[
                    folio_df["header"].astype(str)
                    == header
                ].copy()

                token_text = " ".join(
                    line_df["clean"]
                    .dropna()
                    .astype(str)
                    .tolist()
                )

                with st.expander(
                    f"{header} — {token_text[:100]}"
                ):
                    display_columns = [
                        column
                        for column in [
                            "token_idx",
                            "raw",
                            "clean",
                            "control",
                            "carrier_core",
                            "e_grade",
                            "internal_o",
                            "exit_port",
                            "state",
                            "prev_control",
                            "next_control",
                            "prev_state",
                            "next_state",
                        ]
                        if column in line_df.columns
                    ]

                    st.dataframe(
                        line_df[display_columns],
                        use_container_width=True,
                        hide_index=True,
                    )

        else:
            display_dataframe_or_message(
                folio_df
            )


# ============================================================
# 2. STRUCTURAL EVIDENCE
# ============================================================

with tabs[1]:
    st.subheader("Structural Evidence")

    st.write(
        "These panels measure corpus structure. They do not assign "
        "word meanings."
    )

    st.markdown(
        "#### Slot-frame candidates"
    )

    st.caption(
        "Carrier forms observed in the selected "
        "q/qk → aiin/aiiin → q/qk structural frame."
    )

    slot_candidates = (
        structural_engine
        .find_slot_omega_candidates()
    )

    display_dataframe_or_message(
        slot_candidates,
        "No tokens matched the current slot-frame definition.",
    )

    st.markdown(
        "#### Exit-port → next-control routing"
    )

    routing = (
        structural_engine
        .audit_successor_routing()
    )

    if routing.empty:
        st.info(
            "No successor-routing evidence is available."
        )
    else:
        st.dataframe(
            routing,
            use_container_width=True,
        )

    st.markdown(
        "#### Macrostate transition matrix"
    )

    transition_matrix = (
        structural_engine
        .state_transition_matrix()
    )

    if transition_matrix.empty:
        st.info(
            "No state-transition evidence is available."
        )
    else:
        st.dataframe(
            transition_matrix,
            use_container_width=True,
        )

    st.markdown(
        "#### Carrier × section specificity"
    )

    min_occurrences = st.slider(
        "Minimum carrier occurrences",
        min_value=2,
        max_value=50,
        value=5,
        step=1,
        key="structural_min_occurrences",
    )

    specificity = (
        structural_engine
        .compute_carrier_excess_specificity(
            min_occurrences=min_occurrences
        )
    )

    if specificity.empty:
        st.info(
            "No carrier-section PMI matrix is available "
            "at this threshold."
        )
    else:
        st.caption(
            "Positive PMI indicates greater-than-expected association; "
            "negative PMI indicates less-than-expected association."
        )

        st.dataframe(
            specificity,
            use_container_width=True,
        )


# ============================================================
# 3. ASTRONOMICAL DOMAIN
# ============================================================

with tabs[2]:
    st.subheader("Astronomical Domain")

    st.write(
        "This section compares token-carrier behavior in material "
        "classified broadly as astronomical/zodiac versus the rest "
        "of the corpus."
    )

    st.warning(
        "The parser does not invent zodiac signs or clock positions. "
        "A zodiac-by-carrier matrix is only produced when explicit "
        "zodiac metadata exists."
    )

    st.markdown(
        "#### Most frequent astronomical carriers"
    )

    top_limit = st.slider(
        "Number of carriers to show",
        min_value=5,
        max_value=100,
        value=30,
        step=5,
        key="astro_limit",
    )

    top_astro = (
        astronomical_engine
        .top_astronomical_carriers(
            limit=top_limit
        )
    )

    display_dataframe_or_message(
        top_astro,
        "No astronomical-domain carrier rows were detected.",
    )

    st.markdown(
        "#### Astronomical specificity"
    )

    astro_min_occurrences = st.slider(
        "Minimum carrier frequency",
        min_value=2,
        max_value=50,
        value=5,
        step=1,
        key="astro_min_occurrences",
    )

    astro_specificity = (
        astronomical_engine
        .compute_carrier_astronomical_specificity(
            min_occurrences=astro_min_occurrences
        )
    )

    if astro_specificity.empty:
        st.info(
            "No astronomical specificity matrix is "
            "available at this threshold."
        )
    else:
        st.caption(
            "Positive values indicate a carrier occurs more often "
            "in that domain than expected under independence."
        )

        st.dataframe(
            astro_specificity,
            use_container_width=True,
        )

    st.markdown(
        "#### Explicit zodiac metadata"
    )

    zodiac_matrix = (
        astronomical_engine
        .get_zodiac_carrier_matrix()
    )

    if zodiac_matrix.empty:
        st.info(
            "No explicit zodiac-sign labels are present in the "
            "current transcription. No zodiac identities are inferred."
        )
    else:
        st.dataframe(
            zodiac_matrix,
            use_container_width=True,
        )


# ============================================================
# 4. AUTHOR / COLOPHON AUDIT
# ============================================================

with tabs[3]:
    st.subheader("Author / Colophon Audit")

    st.write(
        "Search transcription comments and unusual terminal loci "
        "for material worth manual inspection."
    )

    st.warning(
        "A rare token or unusual terminal locus is not proof of "
        "authorship, a signature, or a colophon."
    )

    if using_uploaded_corpus:
        st.info(
            "The parsed analysis above uses your uploaded corpus. "
            "The author/colophon audit currently scans the on-disk "
            "default transcription because this audit works from "
            "raw source lines."
        )

    if not os.path.exists(CORPUS_PATH):
        st.info(
            "The default corpus file is not available on disk, "
            "so the raw-text author audit cannot run yet."
        )

    else:
        try:
            auditor = AuthorSignatureAuditor(
                CORPUS_PATH
            )

            marginalia = (
                auditor
                .audit_marginalia_and_comments()
            )

            st.markdown(
                "#### Comment / marginalia evidence"
            )

            if marginalia:
                st.dataframe(
                    pd.DataFrame(marginalia),
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.info(
                    "No author/scribe-related transcription comments "
                    "matched the current keyword audit."
                )

            st.markdown(
                "#### Structural candidate loci"
            )

            signature_slots = (
                auditor
                .find_structural_signature_slots()
            )

            display_dataframe_or_message(
                signature_slots,
                "No structural colophon/signature candidates "
                "matched the current rules.",
            )

            st.markdown(
                "#### Candidate token isolation check"
            )

            candidate_text = st.text_input(
                "Candidate tokens",
                value="ydaraishy ytchas oraiin chkor",
                help=(
                    "Enter Voynich tokens separated by spaces. "
                    "The audit counts exact-ish occurrences across "
                    "the raw corpus."
                ),
            )

            candidate_tokens = [
                token.strip()
                for token in candidate_text.split()
                if token.strip()
            ]

            if candidate_tokens:
                isolation = (
                    auditor
                    .cross_check_vocabulary_isolation(
                        candidate_tokens
                    )
                )

                display_dataframe_or_message(
                    isolation
                )

        except Exception as exc:
            st.error(
                "The raw-text author audit could not run."
            )
            st.exception(exc)


# ============================================================
# 5. HYPOTHESIS INTERPRETER
# ============================================================

with tabs[4]:
    st.subheader("Hypothesis Interpreter")

    st.warning(
        "This is an exploratory hypothesis tool, not a validated "
        "Voynich translation system. Curated meanings and morphology "
        "heuristics are labeled with their evidence and confidence."
    )

    phrase = st.text_area(
        "Voynich token sequence",
        value="qokedy daiin chedy",
        height=100,
    )

    if st.button(
        "Interpret sequence",
        type="primary",
    ):
        result = (
            lexical_engine
            .interpret_phrase(phrase)
        )

        if not result["rows"]:
            st.info(
                "Enter at least one usable alphabetic token."
            )

        else:
            st.markdown(
                "#### Exploratory interpretation"
            )

            st.write(
                result["interpretation"]
            )

            st.markdown(
                "#### Token gloss"
            )

            st.code(
                result["gloss"],
                language=None,
            )

            st.markdown(
                "#### Evidence table"
            )

            st.dataframe(
                pd.DataFrame(
                    result["rows"]
                ),
                use_container_width=True,
                hide_index=True,
            )


# ============================================================
# 6. LEXICAL TABLE
# ============================================================

with tabs[5]:
    st.subheader("Lexical Hypothesis Table")

    st.write(
        "Corpus vocabulary with frequency, exploratory role labels, "
        "evidence source, and confidence."
    )

    dictionary_df = (
        lexical_engine
        .get_full_dictionary()
    )

    lexical_search = st.text_input(
        "Search token or hypothesis",
        value="",
        key="lexical_search",
    ).strip()

    shown_dictionary = dictionary_df.copy()

    if lexical_search and not shown_dictionary.empty:
        search_lower = lexical_search.lower()

        mask = pd.Series(
            False,
            index=shown_dictionary.index,
        )

        for column in [
            "voynich_token",
            "latin_lemma",
            "english_hypothesis",
            "induced_role",
            "evidence",
        ]:
            if column in shown_dictionary.columns:
                mask = (
                    mask
                    |
                    shown_dictionary[column]
                    .fillna("")
                    .astype(str)
                    .str.lower()
                    .str.contains(
                        search_lower,
                        regex=False,
                    )
                )

        shown_dictionary = (
            shown_dictionary[mask]
        )

    display_dataframe_or_message(
        shown_dictionary,
        "No lexical entries match that search.",
    )


# ============================================================
# 7. EXPORT
# ============================================================

with tabs[6]:
    st.subheader("Export")

    st.write(
        "Download parsed corpus data and the exploratory lexical table."
    )

    corpus_csv = df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download parsed corpus CSV",
        data=corpus_csv,
        file_name="voynich_parsed_corpus.csv",
        mime="text/csv",
    )

    dictionary_df = (
        lexical_engine
        .get_full_dictionary()
    )

    dictionary_csv = (
        dictionary_df
        .to_csv(index=False)
        .encode("utf-8")
    )

    st.download_button(
        label="Download lexical hypothesis CSV",
        data=dictionary_csv,
        file_name="voynich_lexical_hypotheses.csv",
        mime="text/csv",
    )

    st.caption(
        "Lexical exports contain exploratory hypotheses and should "
        "not be represented as demonstrated translations."
    )