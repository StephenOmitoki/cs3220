#AI Assignment 2 - Task 3
#Reflex Cat-Agent vs Random Mouse-Agent


import random


#--------------------------------------------------
# LOCATIONS
#--------------------------------------------------

loc_A = (0, 0)
loc_B = (0, 1)
loc_C = (1, 0)
loc_D = (1, 1)


#--------------------------------------------------
# THING CLASS
#--------------------------------------------------

class Thing:

    def __repr__(self):

        return '<{}>'.format(
            getattr(
                self,
                '__name__',
                self.__class__.__name__
            )
        )


    def is_alive(self):

        return (
            hasattr(self, 'alive')
            and self.alive
        )


#--------------------------------------------------
# AGENT CLASS
#--------------------------------------------------

class Agent(Thing):

    def __init__(
        self,
        program=None
    ):

        self.alive = True

        self.performance = 0

        self.location = None

        self.program = program


#--------------------------------------------------
# DIRECTIONS
#--------------------------------------------------

directions = {

    True: 'Left to Right',

    False: 'Right to Left'

}


#--------------------------------------------------
# PRO CAT AGENT
#--------------------------------------------------

class proCatAgent(Agent):

    def __init__(
        self,
        program=None
    ):

        super().__init__(
            program
        )


        #True:
        #Left to Right

        #False:
        #Right to Left
        self.direction = True


        #given by instructor example
        self.performance = 30


        print(
            "ProAgent-Cat will move",
            directions[self.direction],
            "with a performance",
            self.performance
        )


    def changeDirection(self):

        self.direction = (
            not self.direction
        )


        print(
            "ProAgent-Cat will move",
            directions[self.direction]
        )


#--------------------------------------------------
# MOUSE AGENT
#--------------------------------------------------

class MouseAgent(Agent):

    def __init__(
        self,
        program=None,
        size=1
    ):

        super().__init__(
            program
        )


        self.size = size


        #given by instructor example
        self.performance = 5


        print(
            "Mouse Agent has a performance",
            self.performance
        )


#--------------------------------------------------
# RANDOM AGENT PROGRAM
#--------------------------------------------------

def RandomAgentProgram(
    actions
):

    def program(
        percept
    ):

        return random.choice(
            actions
        )


    return program


#--------------------------------------------------
# REFLEX AGENT PROGRAM
#--------------------------------------------------

def ReflexAgentProgram(
    rules,
    interpret_input,
    rule_match
):


    def program(
        percept
    ):


        state = interpret_input(
            percept
        )


        action = rule_match(

            state,

            rules
        )


        return action


    return program


#--------------------------------------------------
# TASK 3 RULES
#--------------------------------------------------

cat2Rules = {

    'Clear': 'Go ahead',

    'Last room': 'Check direction',

    'Mouse': 'Catch'

}


#--------------------------------------------------
# MOUSE POSSIBLE LOCATIONS
#--------------------------------------------------

mouseAgentLocations = [

    loc_A,

    loc_B,

    loc_C,

    loc_D

]


#--------------------------------------------------
# RULE MATCH
#--------------------------------------------------

def rule_match(
    state,
    rules
):

    return rules[
        state
    ]


#--------------------------------------------------
# INTERPRET TASK 3 PERCEPT
#--------------------------------------------------

def interpret_input_A4pro(
    percept
):


    #Task 3 percept:
    #location, agents, things
    loc, agents, things = percept


    #combine everything in room
    percepts = (
        agents
        +
        things
    )


    print(
        percepts
    )


    status = 'Clear'


    #--------------------------------------------------
    # MOUSE FOUND
    #--------------------------------------------------

    for p in percepts:


        if isinstance(
            p,
            MouseAgent
        ):


            print(
                "Oh! the Mouse is here"
            )


            return 'Mouse'


    #--------------------------------------------------
    # END ROOM
    #--------------------------------------------------

    if status == 'Clear':


        if (
            loc == loc_D
            or
            loc == loc_A
        ):


            status = 'Last room'


    print(
        "Loc:",
        loc,
        "status:",
        status
    )


    return status


#--------------------------------------------------
# CREATE RANDOM MOUSE AGENT
#--------------------------------------------------

def RandomMouseAgent():


    return MouseAgent(

        RandomAgentProgram(
            mouseAgentLocations
        )

    )


#--------------------------------------------------
# CREATE REFLEX CAT AGENT
#--------------------------------------------------

def ReflexAgentA4pro():


    return proCatAgent(

        ReflexAgentProgram(

            cat2Rules,

            interpret_input_A4pro,

            rule_match

        )

    )


#--------------------------------------------------
# ENVIRONMENT CLASS
#--------------------------------------------------

class Environment:

    def __init__(self):

        self.agents = []


    def percept(
        self,
        agent
    ):

        print(
            "I don't know how to percept."
        )


    def execute_action(
        self,
        agent,
        action
    ):

        print(
            "I don't know how to execute_action."
        )


    def default_location(
        self,
        thing
    ):

        return None


    def is_done(self):

        return not any(

            agent.is_alive()

            for agent in self.agents
        )


    #--------------------------------------------------
    # ONE ENVIRONMENT STEP
    #--------------------------------------------------

    def step(self):


        if not self.is_done():


            actions = []


            #------------------------------------------
            # FIRST:
            # EVERY AGENT DECIDES WHAT TO DO
            #------------------------------------------

            for agent in self.agents:


                if agent.alive:


                    print(

                        type(agent).__name__,

                        "Performance:",

                        agent.performance
                    )


                    #get percept
                    percept = self.percept(
                        agent
                    )


                    #send percept to Agent Program
                    action = agent.program(
                        percept
                    )


                    print(
                        "Agent",
                        type(agent).__name__,
                        "percepted",
                        percept
                    )


                    print(
                        "Agent decided to do",
                        action
                    )


                    actions.append(
                        action
                    )


                else:


                    print(
                        "Agent",
                        type(agent).__name__,
                        "is dead."
                    )


                    actions.append(
                        ""
                    )


            print(
                "Agents:",
                self.agents,
                "Actions:",
                actions
            )


            print(
                "Paired:",
                list(
                    zip(
                        self.agents,
                        actions
                    )
                )
            )


            #------------------------------------------
            # SECOND:
            # EXECUTE ACTIONS
            #------------------------------------------

            for agent, action in zip(

                self.agents.copy(),

                actions

            ):


                print(

                    type(agent).__name__,

                    action
                )


                self.execute_action(

                    agent,

                    action
                )


        else:


            print(
                "There is no one here who could work..."
            )


    #--------------------------------------------------
    # RUN ENVIRONMENT
    #--------------------------------------------------

    def run(
        self,
        steps=10
    ):


        for step in range(
            steps
        ):


            #show current states
            for agent in self.agents:


                print(

                    "loc:",

                    agent.location,

                    "perf:",

                    agent.performance
                )


            if self.is_done():


                print(
                    "We can't find a live agent"
                )


                return


            print(
                "step {}:".format(
                    step + 1
                )
            )


            self.step()


#--------------------------------------------------
# ENVIRONMENT PRO
#--------------------------------------------------

class environmentPro(Environment):

    def __init__(self):

        super().__init__()

        self.things = []


    #--------------------------------------------------
    # LIST THINGS AT LOCATION
    #--------------------------------------------------

    def list_things_at(
        self,
        location,
        thingClass=Thing
    ):


        result = []


        for thing in self.things:


            if (

                thing.location == location

                and isinstance(
                    thing,
                    thingClass
                )

            ):


                result.append(
                    thing
                )


        return result


    #--------------------------------------------------
    # IS AGENT ALIVE
    #--------------------------------------------------

    def is_agent_alive(
        self,
        agent
    ):

        return agent.alive


#--------------------------------------------------
# CAT FRIENDLY HOUSE 2
#--------------------------------------------------

class catFriendlyHouse2_env(
    environmentPro
):


    def __init__(self):


        super().__init__()


        #Task 3 has 4 rooms
        self.locations = [

            loc_A,

            loc_B,

            loc_C,

            loc_D

        ]


    #--------------------------------------------------
    # RANDOM LOCATION
    #--------------------------------------------------

    def default_location(
        self,
        thing
    ):


        print(
            "The item is starting in random location..."
        )


        return random.choice(
            self.locations
        )


    #--------------------------------------------------
    # LIST AGENTS AT LOCATION
    #--------------------------------------------------

    def list_agents_at(
        self,
        location,
        thingClass=Thing
    ):


        result = []


        for agent in self.agents:


            if (

                agent.location == location

                and isinstance(
                    agent,
                    thingClass
                )

            ):


                result.append(
                    agent
                )


        return result


    #--------------------------------------------------
    # PERCEPT
    #--------------------------------------------------

    def percept(
        self,
        agent
    ):


        #things in current room
        things = self.list_things_at(
            agent.location
        )


        #agents in current room
        agents = self.list_agents_at(
            agent.location
        )


        return (

            agent.location,

            agents,

            things

        )


    #--------------------------------------------------
    # ADD THING
    #--------------------------------------------------

    def add_thing(
        self,
        thing,
        location=None
    ):


        #------------------------------------------
        # AGENT
        #------------------------------------------

        if isinstance(
            thing,
            Agent
        ):


            if thing in self.agents:


                print(
                    "Can't add the same agent twice"
                )


            else:


                if location is not None:

                    thing.location = location


                else:

                    thing.location = (
                        self.default_location(
                            thing
                        )
                    )


                #IMPORTANT:
                #do NOT reset performance here
                self.agents.append(
                    thing
                )


                print(
                    "Welcome! You are added in location",
                    thing.location
                )


        #------------------------------------------
        # NORMAL THING
        #------------------------------------------

        else:


            if thing in self.things:


                print(
                    "Can't add the same thing twice"
                )


            else:


                if location is not None:

                    thing.location = location


                else:

                    thing.location = (
                        self.default_location(
                            thing
                        )
                    )


                self.things.append(
                    thing
                )


    #--------------------------------------------------
    # DELETE AGENT
    #--------------------------------------------------

    def delete_agent(
        self,
        agent
    ):


        if agent in self.agents:


            self.agents.remove(
                agent
            )


    #--------------------------------------------------
    # MOVE CAT ONE ROOM
    #--------------------------------------------------

    def move_cat(
        self,
        agent
    ):


        currentIndex = (
            self.locations.index(
                agent.location
            )
        )


        #------------------------------------------
        # LEFT TO RIGHT
        #------------------------------------------

        if agent.direction:


            agent.location = (
                self.locations[
                    currentIndex + 1
                ]
            )


        #------------------------------------------
        # RIGHT TO LEFT
        #------------------------------------------

        else:


            agent.location = (
                self.locations[
                    currentIndex - 1
                ]
            )


        #Cat movement costs 5
        agent.performance -= 5


        print(
            "The Agent decided to Go ahead at location:",
            agent.location
        )


        #Cat performance <= 0
        if agent.performance <= 0:


            print(
                "GAME OVER!"
            )


            agent.alive = False


    #--------------------------------------------------
    # CHECK DIRECTION
    #--------------------------------------------------

    def check_direction(
        self,
        agent
    ):


        print(
            "The Agent decided to Check direction at location:",
            agent.location
        )


        #change direction
        agent.changeDirection()


        currentIndex = (
            self.locations.index(
                agent.location
            )
        )


        #after changing direction,
        #move one room
        if agent.direction:


            agent.location = (
                self.locations[
                    currentIndex + 1
                ]
            )


        else:


            agent.location = (
                self.locations[
                    currentIndex - 1
                ]
            )


        #movement costs 5
        agent.performance -= 5


        if agent.performance <= 0:


            print(
                "GAME OVER!"
            )


            agent.alive = False


    #--------------------------------------------------
    # CAT CATCH MOUSE
    #--------------------------------------------------

    def cat_catch_mouse(
        self,
        cat
    ):


        #find MouseAgent at Cat location
        mice = self.list_agents_at(

            cat.location,

            MouseAgent

        )


        if len(
            mice
        ) == 0:


            print(
                "Agent tried to Catch, but no MouseAgent was found at",
                cat.location
            )


            return


        mouse = mice[0]


        print(
            "Cat found",
            mouse,
            "at",
            cat.location
        )


        print(
            "Cat performance:",
            cat.performance
        )


        print(
            "Mouse performance:",
            mouse.performance
        )


        #------------------------------------------
        # CAT IS TOO WEAK
        #------------------------------------------

        if (

            cat.performance

            <

            mouse.performance * 5

        ):


            print(
                "Cat is too weak to catch the Mouse."
            )


            #assignment:
            #Cat loses 10 performance
            cat.performance -= 10


            if cat.performance <= 0:


                print(
                    "GAME OVER!"
                )


                cat.alive = False


        #------------------------------------------
        # CAT IS STRONG ENOUGH
        #------------------------------------------

        else:


            print(
                "The Agent did Catch",
                mouse,
                "at location:",
                cat.location
            )


            #assignment:
            #catching/eating Mouse gives +10
            cat.performance += 10


            #Mouse is removed
            self.delete_agent(
                mouse
            )


            #if only Cat remains
            if len(
                self.agents
            ) == 1:


                print(
                    "There is nothing for Agent Cat here. Done!"
                )


                cat.alive = False


    #--------------------------------------------------
    # EXECUTE ACTION
    #--------------------------------------------------

    def execute_action(
        self,
        agent,
        action
    ):


        #------------------------------------------
        # DEAD AGENT
        #------------------------------------------

        if not self.is_agent_alive(
            agent
        ):


            return


        #==========================================
        # CAT AGENT
        #==========================================

        if isinstance(
            agent,
            proCatAgent
        ):


            print(
                "Some items are still there ...."
            )


            #--------------------------------------
            # GO AHEAD
            #--------------------------------------

            if action == 'Go ahead':


                self.move_cat(
                    agent
                )


            #--------------------------------------
            # CATCH
            #--------------------------------------

            elif action == 'Catch':


                self.cat_catch_mouse(
                    agent
                )


            #--------------------------------------
            # CHECK DIRECTION
            #--------------------------------------

            elif action == 'Check direction':


                self.check_direction(
                    agent
                )


        #==========================================
        # MOUSE AGENT
        #==========================================

        elif isinstance(
            agent,
            MouseAgent
        ):


            print(
                "the Agent Mouse is still running with a performance",
                agent.performance
            )


            #RandomMouseAgent action
            #is one of the four locations
            agent.location = action


            print(
                "The Agent Mouse decided to move to",
                agent.location
            )


            #Mouse movement costs 1
            agent.performance -= 1


            #Mouse cannot move anymore
            #if performance <= 0
            if agent.performance <= 0:


                agent.alive = False


                print(
                    "Agent",
                    agent,
                    "is dead."
                )


                #IMPORTANT:
                #do not remove Mouse
                #it stays at last location
                #so Cat can still catch it


    #--------------------------------------------------
    # IS DONE
    #--------------------------------------------------

    def is_done(
        self
    ):


        no_agents = not any(

            agent.is_alive()

            for agent in self.agents

        )


        return no_agents


#--------------------------------------------------
# MAIN PROGRAM
#--------------------------------------------------

def main():


    print(
        "================================"
    )


    print(
        "TASK 3 - CAT AGENT VS MOUSE AGENT"
    )


    print(
        "================================"
    )


    #--------------------------------------------------
    # CREATE ENVIRONMENT
    #--------------------------------------------------

    e2 = catFriendlyHouse2_env()


    #--------------------------------------------------
    # CREATE RANDOM MOUSE
    #--------------------------------------------------

    mouseAgent = (
        RandomMouseAgent()
    )


    e2.add_thing(
        mouseAgent
    )


    print(
        "Mouse Agent is located at {}.".format(
            mouseAgent.location
        )
    )


    #--------------------------------------------------
    # CREATE REFLEX CAT
    #--------------------------------------------------

    catAgent = (
        ReflexAgentA4pro()
    )


    e2.add_thing(
        catAgent
    )


    print(
        "Cat Agent is located at {}.".format(
            catAgent.location
        )
    )


    #--------------------------------------------------
    # SHOW INITIAL ENVIRONMENT
    #--------------------------------------------------

    print(
        "State of the House Environment: {}.".format(
            e2.locations
        )
    )


    print(
        "N of agents: {}.".format(
            len(e2.agents)
        )
    )


    for a in e2.agents:


        print(
            "loc:",
            a.location,
            "perf:",
            a.performance
        )


    #--------------------------------------------------
    # RUN CRAZY HOUSE
    #--------------------------------------------------

    print(
        "\n--- STARTING CRAZY HOUSE ---"
    )


    e2.run()


    #--------------------------------------------------
    # FINAL RESULT
    #--------------------------------------------------

    print(
        "\n================================"
    )


    print(
        "FINAL RESULT"
    )


    print(
        "================================"
    )


    print(
        "Cat location:",
        catAgent.location
    )


    print(
        "Cat performance:",
        catAgent.performance
    )


    print(
        "Cat alive:",
        catAgent.alive
    )


    if mouseAgent in e2.agents:


        print(
            "Mouse location:",
            mouseAgent.location
        )


        print(
            "Mouse performance:",
            mouseAgent.performance
        )


        print(
            "Mouse alive:",
            mouseAgent.alive
        )


    else:


        print(
            "Mouse was caught and removed."
        )


#--------------------------------------------------
# START PROGRAM
#--------------------------------------------------

if __name__ == "__main__":

    main()