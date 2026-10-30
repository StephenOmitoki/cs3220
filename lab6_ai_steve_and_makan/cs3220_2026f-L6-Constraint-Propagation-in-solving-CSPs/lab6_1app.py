# Streamlit interface for Lab 6, Task 1.

import os

from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory

import streamlit as st
import Lab6_1 as lab


# Reuse the graph function from the original program.
def make_graph(csp, domains, title):

    with TemporaryDirectory() as folder:

        filename = Path(folder) / "graph.html"

        lab.draw_tour(
            csp,
            domains,
            filename,
            title
        )

        return filename.read_text(encoding="utf-8")


# Restore the original tour problem.
def reset_demo():

    csp = lab.make_tour()

    st.session_state.csp = csp
    st.session_state.has_run = False

    st.session_state.before_graph = make_graph(
        csp,
        csp.domains,
        "Before AC-3"
    )

    st.session_state.after_graph = None
    st.session_state.consistent = None
    st.session_state.checks = 0


# Apply the supplied AC-3 algorithm once.
def run_ac3():

    csp = st.session_state.csp

    with open(os.devnull, "w") as quiet:

        with redirect_stdout(quiet):
            consistent, checks = lab.AC3(csp)

    st.session_state.consistent = consistent
    st.session_state.checks = checks
    st.session_state.has_run = True

    st.session_state.after_graph = make_graph(
        csp,
        csp.curr_domains,
        "After AC-3"
    )


def main():

    st.set_page_config(
        page_title="Vancouver Tour Lab",
        layout="wide"
    )

    st.title("Vancouver Tour Lab")

    st.caption(
        "Seven attractions, seven days. "
        "No two attractions can share a day."
    )

    if "csp" not in st.session_state:
        reset_demo()

    st.info(
        "Granville Island is fixed to Tuesday. "
        "Capilano Suspension Bridge is fixed to Wednesday."
    )

    run_column, reset_column = st.columns(2)

    if run_column.button(
        "Run AC-3",
        type="primary",
        disabled=st.session_state.has_run
    ):

        with st.spinner("Reducing the possible tour days..."):
            run_ac3()

        st.rerun()

    reset_column.button(
        "Reset",
        on_click=reset_demo
    )

    csp = st.session_state.csp
    has_run = st.session_state.has_run

    domains = (
        csp.curr_domains
        if has_run
        else csp.domains
    )

    before_count = sum(
        len(values)
        for values in csp.domains.values()
    )

    current_count = sum(
        len(values)
        for values in domains.values()
    )

    scores = st.columns(3)

    scores[0].metric(
        "Attractions",
        len(csp.variables)
    )

    scores[1].metric(
        "Remaining choices",
        current_count
    )

    scores[2].metric(
        "Choices removed",
        before_count - current_count
    )

    if has_run:

        if st.session_state.consistent:

            st.success(
                "Tuesday and Wednesday were removed from "
                "every other attraction's domain."
            )

        else:

            st.error(
                "An empty domain was found. "
                "The problem is inconsistent."
            )

        st.caption(
            "Constraint checks: "
            + str(st.session_state.checks)
        )

    st.subheader("Domains before and after")

    comparison = []

    for attraction in csp.variables:

        comparison.append({
            "Attraction": attraction,
            "Before AC-3": ", ".join(
                csp.domains[attraction]
            ),
            "After AC-3": (
                ", ".join(domains[attraction])
                if has_run
                else "Not run yet"
            )
        })

    st.dataframe(
        comparison,
        hide_index=True,
        width="stretch"
    )

    st.caption(
        "The lab specifically requests Vancouver Aquarium, "
        "Science World, and Gastown."
    )

    stage = st.radio(
        "Constraint graph",
        ["Before AC-3", "After AC-3"],
        index=1 if has_run else 0,
        horizontal=True
    )

    if stage == "Before AC-3":

        st.iframe(
            st.session_state.before_graph,
            height=950
        )

    elif has_run:

        st.iframe(
            st.session_state.after_graph,
            height=950
        )

    else:

        st.info(
            "Click Run AC-3 to create the after view."
        )

    st.caption(
        "Yellow: fixed day. Blue: multiple possible days. "
        "Each edge requires different days."
    )

    st.info(
        "AC-3 removes unsupported choices. "
        "It does not choose a complete weekly schedule."
    )


if __name__ == "__main__":
    main()