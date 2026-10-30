# Streamlit interface for Lab 6, Task 2.

import os

from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory

import streamlit as st
import Lab6_2py as lab


# Reuse the graph function from the original program.
def make_graph(csp, domains, asterisk, title):

    with TemporaryDirectory() as folder:

        filename = Path(folder) / "graph.html"

        lab.draw_sudoku(
            csp,
            domains,
            asterisk,
            filename,
            title
        )

        return filename.read_text(encoding="utf-8")


# Restore the pictured Sudoku puzzle.
def reset_demo():

    csp, asterisk = lab.make_sudoku()

    st.session_state.csp = csp
    st.session_state.asterisk = asterisk
    st.session_state.has_run = False

    st.session_state.before_graph = make_graph(
        csp,
        csp.domains,
        asterisk,
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
        st.session_state.asterisk,
        "After AC-3"
    )


# Display givens and candidates in a 9-by-9 board.
def draw_board(csp, domains, asterisk, show_candidates):

    html = """
    <style>
    .sudoku-board {
        display: grid;
        grid-template-columns: repeat(9, 1fr);
        max-width: 720px;
        border: 2px solid #334155;
    }

    .sudoku-cell {
        aspect-ratio: 1;
        min-width: 0;
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
        border-right: 1px solid #cbd5e1;
        border-bottom: 1px solid #cbd5e1;
        font-family: monospace;
        color: #111827;
        text-align: center;
    }

    .sudoku-cell small {
        position: absolute;
        top: 2px;
        left: 4px;
        font-size: 10px;
        color: #475569;
    }
    </style>

    <div class="sudoku-board">
    """

    for row_index, row in enumerate("ABCDEFGHI"):

        for column in range(1, 10):

            cell = row + str(column)
            values = domains[cell]

            background = (
                "#fbcfe8"
                if cell in asterisk
                else "#ffffff"
            )

            if len(csp.domains[cell]) == 1:
                background = "#fde68a"

            elif len(values) == 1:
                background = "#86efac"

            if len(values) == 1:

                content = str(values[0])
                font_size = 26

            elif show_candidates:

                content = "<br>".join(
                    " ".join(
                        str(value)
                        for value in values[index:index + 3]
                    )
                    for index in range(0, len(values), 3)
                )

                font_size = 12

            else:

                content = "&middot;"
                font_size = 26

            style = "background:" + background + ";"

            if column % 3 == 0:
                style += "border-right:3px solid #334155;"

            if (row_index + 1) % 3 == 0:
                style += "border-bottom:3px solid #334155;"

            marker = " *" if cell in asterisk else ""

            html += (
                '<div class="sudoku-cell" style="'
                + style
                + '">'
                + '<small>'
                + cell
                + marker
                + '</small>'
                + '<div style="font-size:'
                + str(font_size)
                + 'px;">'
                + content
                + '</div></div>'
            )

    st.html(html + "</div>")


def main():

    st.set_page_config(
        page_title="Asterisk Sudoku Lab",
        layout="wide"
    )

    st.title("Asterisk Sudoku Lab")

    st.caption(
        "Rows, columns, 3-by-3 boxes, and the nine "
        "asterisk cells must each contain 1-9 "
        "without repetition."
    )

    if "csp" not in st.session_state:
        reset_demo()

    run_column, reset_column = st.columns(2)

    if run_column.button(
        "Run AC-3",
        type="primary",
        disabled=st.session_state.has_run
    ):

        with st.spinner("Checking the Sudoku constraints..."):
            run_ac3()

        st.rerun()

    reset_column.button(
        "Reset",
        on_click=reset_demo
    )

    csp = st.session_state.csp
    asterisk = st.session_state.asterisk
    has_run = st.session_state.has_run

    current = (
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
        for values in current.values()
    )

    fixed_count = sum(
        len(values) == 1
        for values in current.values()
    )

    scores = st.columns(3)

    scores[0].metric(
        "Cells with one value",
        str(fixed_count) + " / 81"
    )

    scores[1].metric(
        "Remaining candidates",
        current_count
    )

    scores[2].metric(
        "Candidates removed",
        before_count - current_count
    )

    if has_run:

        if st.session_state.consistent:

            st.success(
                "AC-3 finished without an empty domain. "
                "Some cells still have multiple candidates."
            )

        else:

            st.error(
                "An empty domain was found. "
                "The puzzle is inconsistent."
            )

        new_values = [
            cell + " = " + str(current[cell][0])
            for cell in csp.variables
            if (
                len(csp.domains[cell]) > 1
                and len(current[cell]) == 1
            )
        ]

        st.write(
            "Newly determined cells: "
            + (", ".join(new_values) or "None")
        )

        st.caption(
            "Constraint checks: "
            + str(st.session_state.checks)
        )

    stage = st.radio(
        "View",
        ["Before AC-3", "After AC-3"],
        index=1 if has_run else 0,
        horizontal=True
    )

    if stage == "After AC-3" and not has_run:

        st.info(
            "Click Run AC-3 to create the after view."
        )

        return

    domains = (
        csp.domains
        if stage == "Before AC-3"
        else csp.curr_domains
    )

    graph = (
        st.session_state.before_graph
        if stage == "Before AC-3"
        else st.session_state.after_graph
    )

    board_tab, graph_tab, domains_tab = st.tabs([
        "Sudoku board",
        "Constraint graph",
        "All domains"
    ])

    with board_tab:

        show_candidates = st.checkbox(
            "Show candidate numbers",
            value=True
        )

        draw_board(
            csp,
            domains,
            asterisk,
            show_candidates
        )

        st.caption(
            "Yellow: given. Green: newly determined. "
            "Pink or *: asterisk cell."
        )

        cell = st.selectbox(
            "Inspect a cell",
            csp.variables,
            index=csp.variables.index("C3")
        )

        st.write(
            "Original domain:",
            csp.domains[cell]
        )

        st.write(
            "Domain in this view:",
            domains[cell]
        )

        removed = [
            value
            for value in csp.domains[cell]
            if value not in domains[cell]
        ]

        st.write(
            "Removed in this view:",
            removed
        )

    with graph_tab:

        st.iframe(
            graph,
            height=1100
        )

        st.caption(
            "Each edge connects cells that must differ. "
            "Purple edges connect asterisk cells. "
            "Scroll over the graph to zoom."
        )

    with domains_tab:

        comparison = []

        for cell in csp.variables:

            comparison.append({
                "Cell": cell,
                "Asterisk": (
                    "Yes" if cell in asterisk else "No"
                ),
                "Original domain": ", ".join(
                    str(value)
                    for value in csp.domains[cell]
                ),
                "Domain in this view": ", ".join(
                    str(value)
                    for value in domains[cell]
                )
            })

        st.dataframe(
            comparison,
            hide_index=True,
            width="stretch",
            height=500
        )

    st.info(
        "AC-3 removes unsupported candidates. "
        "This lab's puzzle still needs further reasoning "
        "or search for a complete solution."
    )


if __name__ == "__main__":
    main()