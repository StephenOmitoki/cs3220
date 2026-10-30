# Lab 6, Task 2: Asterisk Sudoku with CSP and AC-3.

import os
import webbrowser

from contextlib import redirect_stdout
from pathlib import Path

from pyvis.network import Network

from src.CSPclass import CSP
from src.algorithms import AC3
from src.utils import different_values_constraint


# Build the pictured puzzle and all four kinds of constraints.
def make_sudoku():

    rows = "ABCDEFGHI"
    columns = "123456789"

    variables = [
        row + column
        for row in rows
        for column in columns
    ]

    # Zero means the cell is initially empty.
    grid = [
        [0, 1, 0, 0, 0, 0, 0, 6, 0],
        [3, 0, 9, 0, 0, 0, 1, 0, 5],
        [0, 8, 0, 3, 0, 5, 0, 7, 0],
        [0, 0, 2, 0, 7, 0, 8, 0, 0],
        [0, 0, 0, 6, 0, 8, 0, 0, 0],
        [0, 0, 8, 0, 9, 0, 2, 0, 0],
        [0, 2, 0, 4, 0, 1, 0, 9, 0],
        [9, 0, 4, 0, 0, 0, 6, 0, 1],
        [0, 3, 0, 0, 0, 0, 0, 8, 0]
    ]

    asterisk = {
        "B5",
        "C3", "C7",
        "E2", "E5", "E8",
        "G3", "G7",
        "H5"
    }

    filled = {}

    for row in range(9):

        for column in range(9):

            if grid[row][column] != 0:

                cell = rows[row] + columns[column]
                filled[cell] = grid[row][column]

    domains = {
        cell: (
            [filled[cell]]
            if cell in filled
            else list(range(1, 10))
        )
        for cell in variables
    }

    neighbors = {
        cell: []
        for cell in variables
    }

    for X in variables:

        for Y in variables:

            if X == Y:
                continue

            same_row = X[0] == Y[0]

            same_column = X[1] == Y[1]

            same_box = (
                rows.index(X[0]) // 3
                == rows.index(Y[0]) // 3

                and

                (int(X[1]) - 1) // 3
                == (int(Y[1]) - 1) // 3
            )

            same_asterisk = (
                X in asterisk
                and Y in asterisk
            )

            if (
                same_row
                or same_column
                or same_box
                or same_asterisk
            ):
                neighbors[X].append(Y)

    csp = CSP(
        variables=variables,
        domains=domains,
        neighbors=neighbors,
        constraints=different_values_constraint
    )

    return csp, asterisk


# Draw the constraint graph as a Sudoku board.
def draw_sudoku(csp, domains, asterisk, filename, title):

    net = Network(
        heading=title,
        height="1000px",
        width="100%",
        bgcolor="#f8fafc",
        font_color="#111827",
        cdn_resources="in_line"
    )

    rows = "ABCDEFGHI"

    for cell in csp.variables:

        values = [
            str(value)
            for value in domains[cell]
        ]

        # Display candidates in groups of three.
        lines = [
            " ".join(values[index:index + 3])
            for index in range(0, len(values), 3)
        ]

        label = cell + "\n" + "\n".join(lines)

        if len(csp.domains[cell]) == 1:
            background = "#fde68a"

        elif len(domains[cell]) == 1:
            background = "#86efac"

        elif cell in asterisk:
            background = "#fbcfe8"

        else:
            background = "#ffffff"

        net.add_node(
            cell,
            label=label,
            title=cell + "<br>Domain: " + ", ".join(values),
            x=(int(cell[1]) - 1) * 140,
            y=rows.index(cell[0]) * 140,
            shape="box",
            color={
                "background": background,
                "border": (
                    "#c026d3"
                    if cell in asterisk
                    else "#64748b"
                )
            },
            borderWidth=3 if cell in asterisk else 1,
            font={"size": 16},
            physics=False
        )

    for X in csp.variables:

        for Y in csp.neighbors[X]:

            # Add each undirected edge only once.
            if X >= Y:
                continue

            asterisk_edge = (
                X in asterisk
                and Y in asterisk
            )

            net.add_edge(
                X,
                Y,
                color={
                    "color": (
                        "#c026d3"
                        if asterisk_edge
                        else "#94a3b8"
                    ),
                    "opacity": 0.6 if asterisk_edge else 0.15
                },
                smooth=False
            )

    net.toggle_physics(False)

    filename.write_text(
        net.generate_html(notebook=False),
        encoding="utf-8"
    )


# Print all resulting domains and create both visualizations.
def main():

    csp, asterisk = make_sudoku()

    folder = Path(__file__).resolve().parent

    before_file = folder / "lab6_2_before.html"
    after_file = folder / "lab6_2_after.html"

    print("LAB 6, TASK 2: ASTERISK SUDOKU")
    print("Rows: A-I. Columns: 1-9.")
    print("Asterisk cells:", sorted(asterisk))

    draw_sudoku(
        csp,
        csp.domains,
        asterisk,
        before_file,
        "Asterisk Sudoku before AC-3"
    )

    # Hide the supplied algorithm's long queue trace.
    with open(os.devnull, "w") as quiet:

        with redirect_stdout(quiet):
            consistent, checks = AC3(csp)

    print("\nAC-3 found no empty domain:", consistent)
    print("Constraint checks:", checks)

    print("\nDOMAINS FOR ALL CELLS AFTER AC-3")

    for row in "ABCDEFGHI":

        for column in "123456789":

            cell = row + column

            print(cell + ":", csp.curr_domains[cell])

        print()

    original_count = sum(
        len(csp.domains[cell])
        for cell in csp.variables
    )

    remaining_count = sum(
        len(csp.curr_domains[cell])
        for cell in csp.variables
    )

    singleton_count = sum(
        len(csp.curr_domains[cell]) == 1
        for cell in csp.variables
    )

    print("Total candidates before AC-3:", original_count)
    print("Total candidates after AC-3:", remaining_count)

    print(
        "Cells with one remaining value:",
        singleton_count,
        "of 81"
    )

    print("\nNEWLY DETERMINED CELLS")

    for cell in csp.variables:

        if (
            len(csp.domains[cell]) > 1
            and len(csp.curr_domains[cell]) == 1
        ):
            print(cell + " =", csp.curr_domains[cell][0])

    draw_sudoku(
        csp,
        csp.curr_domains,
        asterisk,
        after_file,
        "Asterisk Sudoku after AC-3"
    )

    print("\nYellow: given.")
    print("Green: newly determined.")
    print("Pink background or purple border: asterisk cell.")

    print(
        "Edges connect cells that must "
        "have different values."
    )

    print("AC-3 leaves some cells with multiple candidates.")

    print("\nGraphs saved:")
    print(before_file)
    print(after_file)

    webbrowser.open(before_file.as_uri())
    webbrowser.open(after_file.as_uri())


if __name__ == "__main__":
    main()