# Lab 6, Task 1: Vancouver tour planning with CSP and AC-3.

import math
import os
import webbrowser

from contextlib import redirect_stdout
from pathlib import Path

from pyvis.network import Network

from src.CSPclass import CSP
from src.algorithms import AC3
from src.utils import different_values_constraint


# Define attractions, possible days, and pairwise restrictions.
def make_tour():

    variables = [
        "Stanley Park",
        "Granville Island",
        "Vancouver Aquarium",
        "Science World",
        "Gastown",
        "Capilano Suspension Bridge",
        "Canada Place"
    ]

    days = [
        "Mon", "Tue", "Wed", "Thu",
        "Fri", "Sat", "Sun"
    ]

    domains = {
        attraction: days[:]
        for attraction in variables
    }

    domains["Granville Island"] = ["Tue"]
    domains["Capilano Suspension Bridge"] = ["Wed"]

    neighbors = {
        attraction: [
            other
            for other in variables
            if other != attraction
        ]
        for attraction in variables
    }

    return CSP(
        variables=variables,
        domains=domains,
        neighbors=neighbors,
        constraints=different_values_constraint
    )


# Draw every attraction and every different-day constraint.
def draw_tour(csp, domains, filename, title):

    net = Network(
        heading=title,
        height="850px",
        width="100%",
        bgcolor="#f8fafc",
        font_color="#111827",
        cdn_resources="in_line"
    )

    for index, attraction in enumerate(csp.variables):

        angle = 2 * math.pi * index / len(csp.variables)

        domain_text = ", ".join(domains[attraction])

        net.add_node(
            attraction,
            label=attraction + "\n" + domain_text,
            title=attraction + "<br>Domain: " + domain_text,
            x=550 * math.cos(angle),
            y=450 * math.sin(angle),
            shape="box",
            color=(
                "#fde68a"
                if len(domains[attraction]) == 1
                else "#bfdbfe"
            ),
            physics=False,
            font={"size": 18}
        )

    for index, attraction in enumerate(csp.variables):

        for other in csp.variables[index + 1:]:

            net.add_edge(
                attraction,
                other,
                title="Different tour days",
                color="#94a3b8",
                smooth=False
            )

    net.toggle_physics(False)

    filename.write_text(
        net.generate_html(notebook=False),
        encoding="utf-8"
    )


# Run AC-3 and compare the requested domains.
def main():

    csp = make_tour()

    folder = Path(__file__).resolve().parent

    before_file = folder / "lab6_1_before.html"
    after_file = folder / "lab6_1_after.html"

    requested = [
        "Vancouver Aquarium",
        "Science World",
        "Gastown"
    ]

    print("LAB 6, TASK 1: VANCOUVER TOUR")

    print("\nBEFORE AC-3")

    for attraction in requested:
        print(attraction + ":", csp.domains[attraction])

    draw_tour(
        csp,
        csp.domains,
        before_file,
        "Vancouver CSP before AC-3"
    )

    # Hide the supplied algorithm's long queue trace.
    with open(os.devnull, "w") as quiet:

        with redirect_stdout(quiet):
            consistent, checks = AC3(csp)

    print("\nAC-3 found no empty domain:", consistent)
    print("Constraint checks:", checks)

    print("\nAFTER AC-3")

    for attraction in requested:
        print(attraction + ":", csp.curr_domains[attraction])

    draw_tour(
        csp,
        csp.curr_domains,
        after_file,
        "Vancouver CSP after AC-3"
    )

    print("\nYellow nodes: fixed day.")
    print("Blue nodes: multiple possible days.")

    print(
        "Each edge means the attractions "
        "must have different days."
    )

    print(
        "AC-3 reduces domains; it does not "
        "select a complete schedule."
    )

    print("\nGraphs saved:")
    print(before_file)
    print(after_file)

    webbrowser.open(before_file.as_uri())
    webbrowser.open(after_file.as_uri())


if __name__ == "__main__":
    main()