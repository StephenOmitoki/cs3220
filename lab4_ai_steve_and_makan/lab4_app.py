#Lab4: Rescue Arena
#Run: python -m streamlit run lab4_app.py

import random
import math

from queue import PriorityQueue

import numpy as np
import streamlit as st


#actions: Left, Up, Right, Down
NAMES = ["Left", "Up", "Right", "Down"]

MOVES = [
    (0, -1),
    (-1, 0),
    (0, 1),
    (1, 0)
]

COSTS = [2, 4, 2, 1]

#robot colours
COLORS = ["#53e3ff", "#c5a3ff"]


#build the transition model
def make_model(maze):

    model = {}

    for row in range(7):

        for column in range(7):

            if maze[row, column] == 1:
                continue

            state = (row, column)

            model[state] = {}

            for action in range(4):

                dr, dc = MOVES[action]

                nr = row + dr
                nc = column + dc

                if 0 <= nr < 7 and 0 <= nc < 7:

                    if maze[nr, nc] != 1:

                        model[state][action] = (nr, nc)

    return model


#Uniform-Cost Search
def ucs(model, start, goal):

    frontier = PriorityQueue()

    #each entry contains cost, position and action sequence
    frontier.put((0, start, []))

    reached = {start: 0}

    while not frontier.empty():

        cost, state, path = frontier.get()

        if cost > reached[state]:
            continue

        if state == goal:
            return path

        for action, target in model[state].items():

            new_cost = cost + COSTS[action]

            if target not in reached or new_cost < reached[target]:

                reached[target] = new_cost

                frontier.put(
                    (new_cost, target, path + [action])
                )

    return None


#check connectivity without selecting a route
def reachable(model, start, goal):

    pending = [start]

    visited = {start}

    while pending:

        state = pending.pop()

        if state == goal:
            return True

        for target in model[state].values():

            if target not in visited:

                visited.add(target)
                pending.append(target)

    return False


#Depth-Limited Search
def dls(model, state, goal, limit, visited):

    if state == goal:
        return []

    if limit == 0:

        for target in model[state].values():

            if target not in visited:
                return "cutoff"

        return None

    cutoff = False

    #action order: Left, Up, Right, Down
    for action, target in model[state].items():

        if target in visited:
            continue

        visited.add(target)

        result = dls(
            model,
            target,
            goal,
            limit - 1,
            visited
        )

        #backtrack before trying another branch
        visited.remove(target)

        if result == "cutoff":

            cutoff = True

        elif result is not None:

            return [action] + result

    if cutoff:
        return "cutoff"

    return None


#Iterative Deepening Search
def IDSearchAgentProgram(model, start, goal):

    if not reachable(model, start, goal):
        return None, []

    limits = []

    #a cycle-free route uses at most number_of_nodes - 1 moves
    for limit in range(len(model)):

        limits.append(limit)

        #restart at the initial state for every depth limit
        result = dls(
            model,
            start,
            goal,
            limit,
            {start}
        )

        if result != "cutoff":
            return result, limits

    return None, limits


class Thing:
    pass


class SecurityDrone(Thing):

    def __init__(self, power):

        self.attack_power = power


class RescueRobot(Thing):

    def __init__(self, name, start, goal, model, energy):

        self.name = name

        self.location = start
        self.energy = float(energy)

        self.state = (start, self.energy)

        self.visited = [start]

        self.known_drones = {}
        self.last_percept = None

        self.status = "Ready"

        self.moves = 0
        self.cost = 0
        self.encounters = 0

        self.limits = []
        self.route = []

        if name == "UCS":

            self.route = ucs(model, start, goal)

        elif name == "IDDFS":

            self.route, self.limits = IDSearchAgentProgram(
                model,
                start,
                goal
            )

        if self.route is None:
            self.status = "No route"

    def observe(self, percept):

        self.last_percept = percept

        power = percept["drone_power"]

        if power is not None:

            location = percept["location"]

            self.known_drones[location] = power

        return power


class Laboratory:

    def __init__(self, seed, energy, mode):

        self.seed = seed
        self.energy = energy
        self.mode = mode

        #the same seed reproduces the same mission
        rng = random.Random(seed)

        self.maze = np.zeros((7, 7), dtype=int)

        cells = []

        for row in range(7):

            for column in range(7):

                cells.append((row, column))

        rng.shuffle(cells)

        #12 walls and 5 drones
        for cell in cells[:12]:
            self.maze[cell] = 1

        for cell in cells[12:17]:
            self.maze[cell] = 2

        self.start = cells[17]
        self.goal = cells[18]

        self.maze[self.start] = 4
        self.maze[self.goal] = 3

        self.model = make_model(self.maze)

        self.drones = {}

        number_of_nodes = len(self.model)

        low = math.ceil(number_of_nodes * 0.10)
        high = math.floor(number_of_nodes * 0.40)

        for cell in cells[12:17]:

            power = rng.randint(low, high)

            self.drones[cell] = SecurityDrone(power)

        if mode == "Compare agents":

            robot_names = ["UCS", "IDDFS"]

        else:

            robot_names = ["Pilot"]

        self.robots = []

        for name in robot_names:

            robot = RescueRobot(
                name,
                self.start,
                self.goal,
                self.model,
                energy
            )

            self.robots.append(robot)

        self.turn = 0

        self.log = [
            "Mission ready. Reach the green rescue target."
        ]

    #report only the drone in the currently occupied cell
    def percept(self, robot):

        power = None

        if robot.location in self.drones:

            power = self.drones[robot.location].attack_power

        return {
            "location": robot.location,
            "energy": robot.energy,
            "drone_power": power
        }

    def move(self, robot, action):

        if robot.status not in ["Ready", "Moving"]:
            return

        if action not in self.model[robot.location]:

            self.log.append(
                robot.name + ": blocked by a wall or boundary."
            )

            return

        robot.location = self.model[robot.location][action]

        robot.moves += 1
        robot.cost += COSTS[action]

        robot.visited.append(robot.location)

        robot.status = "Moving"

        message = (
            robot.name
            + ": "
            + NAMES[action]
            + " → "
            + str(robot.location)
        )

        #sense the current cell after moving
        observation = self.percept(robot)

        power = robot.observe(observation)

        if power is not None:

            robot.encounters += 1

            #assumption: defensive capability equals current energy
            if power >= 2 * robot.energy:

                robot.status = "Captured"

                message += (
                    " | CAPTURED by drone power "
                    + str(power)
                )

            else:

                robot.energy *= 0.90

                message += (
                    " | Defense Mode: "
                    + str(round(robot.energy, 2))
                    + " energy"
                )

        robot.state = (robot.location, robot.energy)

        if robot.status != "Captured":

            if robot.location == self.goal:

                robot.status = "Rescued"

                message += " | RESCUE COMPLETE"

        self.log.append(message)

    def done(self):

        for robot in self.robots:

            if robot.status in ["Ready", "Moving"]:
                return False

        return True

    def step(self):

        if self.done():
            return

        self.turn += 1

        for robot in self.robots:

            if robot.status in ["Ready", "Moving"]:

                action = robot.route[robot.moves]

                self.move(robot, action)

    def result(self):

        if not self.done():

            if self.turn == 0:
                return "Ready to launch"

            return "Mission in progress"

        survivors = []

        for robot in self.robots:

            if robot.status == "Rescued":

                survivors.append(robot)

        if len(survivors) == 0:

            return "No successful rescue. Replay or try a new maze."

        if len(survivors) == 1:

            return survivors[0].name + " completes the rescue!"

        first, second = survivors

        if abs(first.energy - second.energy) < 0.000001:

            return "Tie! Both reached the target with the same energy."

        if first.energy > second.energy:

            winner = first

        else:

            winner = second

        return winner.name + " wins with the highest remaining energy!"


#draw the board using SVG
#this function controls appearance, not the search algorithms
def board_svg(lab, reveal, routes):

    known = set()

    for robot in lab.robots:

        known.update(robot.known_drones)

    svg = [
        '<svg viewBox="0 0 600 600" '
        'xmlns="http://www.w3.org/2000/svg" '
        'role="img" aria-label="Laboratory rescue maze">'
    ]

    svg.append(
        '<rect width="600" height="600" '
        'rx="18" fill="#0b1422"/>'
    )

    #row and column numbers
    for number in range(7):

        svg.append(
            f'<text x="{65 + number * 78}" y="19" '
            f'fill="#899cb4" font-size="12" '
            f'text-anchor="middle">{number}</text>'
        )

        svg.append(
            f'<text x="15" y="{70 + number * 78}" '
            f'fill="#899cb4" font-size="12">{number}</text>'
        )

    cell_colors = {
        0: "#152436",
        1: "#40536a",
        2: "#152436",
        3: "#164b3e",
        4: "#1c4354"
    }

    for row in range(7):

        for column in range(7):

            x = 30 + column * 78
            y = 30 + row * 78

            cell = int(lab.maze[row, column])

            fill = cell_colors[cell]

            svg.append(
                f'<rect x="{x}" y="{y}" width="72" height="72" '
                f'rx="8" fill="{fill}" stroke="#283e55"/>'
            )

            #wall markings
            if cell == 1:

                svg.append(
                    f'<path d="M{x+15} {y+53}l38-38'
                    f'M{x+27} {y+60}l33-33" '
                    f'stroke="#526b85" stroke-width="5"/>'
                )

            #rescue target
            if cell == 3:

                svg.append(
                    f'<path d="M{x+36} {y+17}v30'
                    f'M{x+21} {y+32}h30" '
                    f'stroke="#55efb0" stroke-width="6"/>'
                    f'<text x="{x+36}" y="{y+62}" '
                    f'text-anchor="middle" fill="#77f8c7" '
                    f'font-size="9">RESCUE</text>'
                )

            if cell == 4:

                svg.append(
                    f'<text x="{x+36}" y="{y+64}" '
                    f'text-anchor="middle" fill="#77cde5" '
                    f'font-size="9">START</text>'
                )

            #show drones only when revealed or discovered
            if cell == 2 and (reveal or (row, column) in known):

                power = lab.drones[(row, column)].attack_power

                svg.append(
                    f'<path d="M{x+21} {y+18}l30 25'
                    f'm0-25l-30 25" '
                    f'stroke="#ff7888" stroke-width="4"/>'
                )

                for dx in [20, 52]:

                    for dy in [18, 43]:

                        svg.append(
                            f'<ellipse cx="{x+dx}" cy="{y+dy}" '
                            f'rx="10" ry="5" fill="#142030" '
                            f'stroke="#ff7888"/>'
                        )

                svg.append(
                    f'<circle cx="{x+36}" cy="{y+30}" '
                    f'r="9" fill="#ff7888"/>'
                    f'<text x="{x+36}" y="{y+65}" '
                    f'text-anchor="middle" fill="#ff9ca8" '
                    f'font-size="10">POWER {power}</text>'
                )

    #draw routes and robots
    for index, robot in enumerate(lab.robots):

        color = COLORS[index]

        states = robot.visited

        if routes and robot.route:

            state = lab.start

            states = [state]

            for action in robot.route:

                state = lab.model[state][action]

                states.append(state)

        points = []

        for row, column in states:

            px = 66 + column * 78 + index * 5
            py = 66 + row * 78 + index * 5

            points.append(f"{px},{py}")

        point_text = " ".join(points)

        svg.append(
            f'<polyline points="{point_text}" fill="none" '
            f'stroke="{color}" stroke-width="3" opacity=".5"/>'
        )

        row, column = robot.location

        x = 66 + column * 78
        y = 60 + row * 78

        #separate robots when they occupy the same cell
        if len(lab.robots) == 2:

            if lab.robots[0].location == lab.robots[1].location:

                if index == 0:
                    x -= 16

                else:
                    x += 16

        svg.append(
            f'<g transform="translate({x},{y})">'
            f'<rect x="-14" y="-12" width="28" height="25" '
            f'rx="6" fill="#102234" stroke="{color}" '
            f'stroke-width="2"/>'
            f'<path d="M0-18v6M-18-4v13M18-4v13" '
            f'stroke="{color}" stroke-width="3"/>'
            f'<rect x="-9" y="-5" width="18" height="7" '
            f'rx="3" fill="{color}"/>'
            f'<text y="27" text-anchor="middle" '
            f'fill="{color}" font-size="9">{robot.name}</text>'
            f'</g>'
        )

    return "".join(svg) + "</svg>"


def main():

    st.set_page_config(
        page_title="Lab4 Rescue Arena",
        layout="wide"
    )

    st.markdown(
        """
        <style>
        .stApp {
            background: #080f1b;
            color: #e6eef9;
        }

        .block-container {
            max-width: 1280px;
            padding-top: 2rem;
        }

        [data-testid="stSidebar"] {
            background: #101c2b;
        }

        h1 {
            letter-spacing: -2px;
        }

        .stButton button {
            border-radius: 10px;
        }

        .tag {
            color: #53e3ff;
            font: 12px monospace;
            letter-spacing: 3px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if "lab4" not in st.session_state:

        st.session_state.lab4 = Laboratory(
            7,
            100,
            "Compare agents"
        )

        st.session_state.playing = False

    #sidebar controls
    with st.sidebar:

        st.markdown("### Mission control")

        mode = st.selectbox(
            "Mode",
            ["Compare agents", "Pilot a robot"]
        )

        seed = st.number_input(
            "Maze seed",
            min_value=0,
            max_value=999999,
            value=7
        )

        energy = st.slider(
            "Starting energy",
            min_value=2,
            max_value=100,
            value=100
        )

        st.caption(
            "Defense = current energy. "
            "Try 6 energy to test capture."
        )

        if st.button("Load mission", width="stretch"):

            st.session_state.lab4 = Laboratory(
                int(seed),
                energy,
                mode
            )

            st.session_state.playing = False

        if st.button("Random maze", width="stretch"):

            random_seed = random.randint(0, 999999)

            st.session_state.lab4 = Laboratory(
                random_seed,
                energy,
                mode
            )

            st.session_state.playing = False

        st.caption(
            "Settings apply when you load a mission."
        )

        st.divider()

        reveal = st.toggle(
            "Observer view: reveal drones",
            value=False
        )

        routes = st.toggle(
            "Show planned routes",
            value=False
        )

        st.caption(
            "Hidden drones appear after either robot discovers them. "
            "Revealing drones never changes robot knowledge."
        )

        speed = st.select_slider(
            "Playback speed",
            options=["Slow", "Normal", "Fast"],
            value="Normal"
        )

        st.divider()

        st.write("**Movement costs**")

        st.write(
            "Left: 2 | Up: 4 | Right: 2 | Down: 1"
        )

        st.caption(
            "7 × 7 cells | 12 walls | 5 drones"
        )

    lab = st.session_state.lab4

    st.markdown(
        '<div class="tag">'
        'CS3220 / LAB 4 / LIVE MISSION'
        '</div>',
        unsafe_allow_html=True
    )

    st.title("Rescue Arena")

    st.write(
        "Navigate the laboratory. "
        "Discover drones. Complete the rescue."
    )

    st.caption(
        f"Mission {lab.seed} | "
        f"Start {lab.start} | "
        f"Rescue {lab.goal} | "
        f"{lab.mode}"
    )

    play, step, finish, replay = st.columns(4)

    automatic = lab.mode == "Compare agents"

    play_label = "Play"

    if st.session_state.playing:
        play_label = "Pause"

    if play.button(
        play_label,
        type="primary",
        width="stretch",
        disabled=not automatic or lab.done()
    ):

        st.session_state.playing = not st.session_state.playing

    if step.button(
        "One step",
        width="stretch",
        disabled=not automatic or lab.done()
    ):

        st.session_state.playing = False

        lab.step()

    if finish.button(
        "Finish mission",
        width="stretch",
        disabled=not automatic or lab.done()
    ):

        st.session_state.playing = False

        while not lab.done():

            lab.step()

    if replay.button(
        "Replay same maze",
        width="stretch"
    ):

        st.session_state.lab4 = Laboratory(
            lab.seed,
            lab.energy,
            lab.mode
        )

        st.session_state.playing = False

    speeds = {
        "Slow": 1.2,
        "Normal": 0.65,
        "Fast": 0.25
    }

    interval = None

    if st.session_state.playing:

        interval = speeds[speed]

    #refresh the mission display automatically while playing
    @st.fragment(run_every=interval)
    def mission_display():

        lab = st.session_state.lab4

        if st.session_state.playing:

            lab.step()

            if lab.done():

                st.session_state.playing = False

                st.rerun()

        board, panel = st.columns(
            [1.5, 1],
            gap="large"
        )

        with board:

            st.html(
                board_svg(lab, reveal, routes)
            )

            st.caption(
                "Cyan: UCS / Pilot | Purple: IDDFS | "
                "Red: drone | Green: rescue"
            )

            #manual game controls
            if lab.mode == "Pilot a robot":

                buttons = st.columns(4)

                for action in range(4):

                    if buttons[action].button(
                        NAMES[action],
                        disabled=lab.done(),
                        width="stretch"
                    ):

                        lab.turn += 1

                        lab.move(
                            lab.robots[0],
                            action
                        )

                        st.rerun()

            if lab.done():

                st.info(lab.result())

            else:

                st.write(
                    "**" + lab.result() + "**"
                )

        with panel:

            st.subheader("Robot telemetry")

            text_colors = ["blue", "violet"]

            for index, robot in enumerate(lab.robots):

                with st.container(border=True):

                    text_color = text_colors[index]

                    st.markdown(
                        f"#### :{text_color}[{robot.name}] "
                        f"— {robot.status}"
                    )

                    st.progress(
                        robot.energy / lab.energy,
                        text=(
                            f"Energy: {robot.energy:.1f} "
                            f"/ {lab.energy}"
                        )
                    )

                    a, b, c = st.columns(3)

                    a.metric("Moves", robot.moves)

                    b.metric("Cost", robot.cost)

                    c.metric("Drones", robot.encounters)

            st.markdown(
                "**Mission log · turn "
                + str(lab.turn)
                + "**"
            )

            for message in reversed(lab.log[-5:]):

                st.caption(message)

        #teacher explanation panel
        with st.expander("Explain the AI and perceptions"):

            st.write(
                "UCS finds the lowest movement cost. "
                "IDDFS finds the fewest moves. "
                "A successful robot with the highest "
                "remaining energy wins."
            )

            st.write(
                "After each legal move, percept() reports "
                "location, energy and the drone power in "
                "the occupied cell only. The robot records "
                "the observation before the encounter is resolved."
            )

            for robot in lab.robots:

                st.write("**" + robot.name + "**")

                known_drones = {}

                for cell, power in robot.known_drones.items():

                    known_drones[str(cell)] = power

                planned_actions = []

                if robot.route is not None:

                    for action in robot.route:

                        planned_actions.append(NAMES[action])

                st.json(
                    {
                        "last_percept": robot.last_percept,
                        "current_state": robot.state,
                        "known_drones": known_drones,
                        "planned_actions": planned_actions,
                        "IDDFS_limits": robot.limits
                    }
                )

            st.caption(
                "The last percept contains energy before the "
                "encounter; current_state contains energy after it."
            )

            st.caption(
                "Assumptions: starting energy is configurable; "
                "defense equals current energy; movement does "
                "not drain battery. Defense Mode consumes 10% "
                "on every surviving drone encounter. Capture "
                "occurs when drone power is at least twice "
                "current energy."
            )

            st.caption(
                "Each traversable cell is a graph node. "
                "Drone power uses the 37 graph nodes: 4–14. "
                "Random mazes may have no route."
            )

        with st.expander("Matrix and full mission log"):

            st.caption(
                "Observer data: 0 free, 1 wall, "
                "2 drone, 3 rescue, 4 start"
            )

            st.dataframe(
                lab.maze,
                width="stretch"
            )

            for message in lab.log:

                st.text(message)

    mission_display()


if __name__ == "__main__":
    main()