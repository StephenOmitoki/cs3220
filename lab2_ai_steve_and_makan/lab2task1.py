#AI Assignment 2 - Task 1
#Reflex Delivery Agent


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
            getattr(self, '__name__', self.__class__.__name__)
        )

    def is_alive(self):
        return hasattr(self, 'alive') and self.alive


#--------------------------------------------------
# AGENT CLASS
#--------------------------------------------------

class Agent(Thing):

    def __init__(self, program=None):

        self.alive = True
        self.performance = 0
        self.location = None
        self.program = program


#--------------------------------------------------
# ENVIRONMENT CLASS
#--------------------------------------------------

class Environment:

    def __init__(self):

        self.agents = []


    def percept(self, agent):

        print("I don't know how to percept.")


    def execute_action(self, agent, action):

        print("I don't know how to execute_action.")


    def default_location(self, thing):

        return None


    def is_done(self):

        return not any(
            agent.is_alive()
            for agent in self.agents
        )


    def step(self):

        if not self.is_done():

            actions = []

            for agent in self.agents:

                if agent.alive:

                    print(
                        "\nAgent Performance:",
                        agent.performance
                    )

                    #get the agent's percept
                    percept = self.percept(agent)

                    print(
                        "Agent percepted",
                        percept
                    )

                    #send percept to Agent Program
                    action = agent.program(percept)

                    print(
                        "Agent decided to do",
                        action
                    )

                    actions.append(action)

                else:

                    print("Agent is dead.")

                    actions.append("")


            #execute every agent's action
            for agent, action in zip(
                self.agents,
                actions
            ):

                self.execute_action(
                    agent,
                    action
                )

        else:

            print(
                "There is no one here who could work..."
            )


    def run(self, steps=10):

        for step in range(steps):

            if self.is_done():

                print(
                    "\nWe can't find a live agent"
                )

                return

            print(
                "\n-------------------------"
            )

            print(
                "Step",
                step + 1
            )

            print(
                "-------------------------"
            )

            self.step()


#--------------------------------------------------
# ENVIRONMENT PRO
#--------------------------------------------------

class environmentPro(Environment):

    def __init__(self):

        super().__init__()

        self.things = []


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

                result.append(thing)

        return result


    def add_thing(
        self,
        thing,
        location=None
    ):

        if isinstance(thing, Agent):

            thing.location = (
                location
                if location is not None
                else self.default_location(thing)
            )

            self.agents.append(thing)

            print(
                "Welcome! Agent added at",
                thing.location
            )

        else:

            thing.location = (
                location
                if location is not None
                else self.default_location(thing)
            )

            self.things.append(thing)


    def delete_thing(self, thing):

        if thing in self.agents:

            self.agents.remove(thing)

        elif thing in self.things:

            self.things.remove(thing)


    def is_agent_alive(self, agent):

        return agent.alive


    def update_agent_alive(self, agent):

        if agent.performance <= 0:

            agent.alive = False

            print(
                "Agent",
                agent,
                "is dead."
            )


#--------------------------------------------------
# TASK 1 RECIPIENT CLASSES
#--------------------------------------------------

class OfficeManager(Thing):

    def __init__(self):

        self.name = "Joe"


class ITStaff(Thing):

    def __init__(self):

        self.name = "Jack"


class Student(Thing):

    def __init__(self):

        self.name = "Hanna"


#--------------------------------------------------
# TASK 1 RULES
#--------------------------------------------------

a2proRules = {

    'Office manager': 'Give mail',

    'IT': 'Give donuts',

    'Student': 'Give pizza',

    'Clear': 'Go ahead',

    'Last room': 'Stop'
}


#--------------------------------------------------
# INTERPRET THE PERCEPT
#--------------------------------------------------

def interpret_input_A2pro(percept):

    #separate the percept
    loc, percepts = percept

    status = 'Clear'


    #if nobody is in the room
    if len(percepts) == 0:

        #if this is the final room
        if loc == loc_D:

            status = 'Last room'


    else:

        #check every person in the room
        for p in percepts:

            if isinstance(
                p,
                OfficeManager
            ):

                return 'Office manager'


            elif isinstance(
                p,
                ITStaff
            ):

                return 'IT'


            elif isinstance(
                p,
                Student
            ):

                return 'Student'


    return status


#--------------------------------------------------
# MATCH STATE TO RULE
#--------------------------------------------------

def rule_match_A2pro(
    state,
    rules
):

    return rules[state]


#--------------------------------------------------
# REFLEX AGENT PROGRAM
#--------------------------------------------------

def ReflexAgentProgram(
    rules,
    interpret_input,
    rule_match
):

    def program(percept):

        #convert percept into state
        state = interpret_input(
            percept
        )

        print(
            "State:",
            state
        )

        #find correct action
        action = rule_match(
            state,
            rules
        )

        return action


    return program


#--------------------------------------------------
# CREATE TASK 1 DELIVERY AGENT
#--------------------------------------------------

def ReflexAgentA2pro():

    program = ReflexAgentProgram(
        a2proRules,
        interpret_input_A2pro,
        rule_match_A2pro
    )

    return Agent(program)


#--------------------------------------------------
# COMPANY ENVIRONMENT
#--------------------------------------------------

class CompanyEnvironment(environmentPro):

    def __init__(self):

        super().__init__()

        self.locations = [
            loc_A,
            loc_B,
            loc_C,
            loc_D
        ]


    def default_location(self, thing):

        print(
            "The item is starting in random location..."
        )

        return random.choice(
            self.locations
        )


    def percept(self, agent):

        #find everyone in the current room
        things = self.list_things_at(
            agent.location
        )

        return (
            agent.location,
            things
        )


    def execute_action(
        self,
        agent,
        action
    ):

        if not self.is_agent_alive(agent):

            return


        #------------------------------------------
        # GO TO NEXT ROOM
        #------------------------------------------

        if action == 'Go ahead':

            currentIndex = self.locations.index(
                agent.location
            )

            agent.location = self.locations[
                currentIndex + 1
            ]

            agent.performance -= 1

            print(
                "Delivery Agent moved to",
                agent.location
            )


        #------------------------------------------
        # OFFICE MANAGER
        #------------------------------------------

        elif action == 'Give mail':

            items = self.list_things_at(
                agent.location,
                OfficeManager
            )

            if len(items) > 0:

                print(
                    "Delivered mail to",
                    items[0].name
                )

                agent.performance += 3

                self.delete_thing(
                    items[0]
                )


        #------------------------------------------
        # IT STAFF
        #------------------------------------------

        elif action == 'Give donuts':

            items = self.list_things_at(
                agent.location,
                ITStaff
            )

            if len(items) > 0:

                print(
                    "Delivered donuts to",
                    items[0].name
                )

                agent.performance += 3

                self.delete_thing(
                    items[0]
                )


        #------------------------------------------
        # STUDENT
        #------------------------------------------

        elif action == 'Give pizza':

            items = self.list_things_at(
                agent.location,
                Student
            )

            if len(items) > 0:

                print(
                    "Delivered pizza to",
                    items[0].name
                )

                agent.performance += 3

                self.delete_thing(
                    items[0]
                )


        #------------------------------------------
        # STOP
        #------------------------------------------

        elif action == 'Stop':

            print(
                "Last room checked."
            )

            print(
                "Delivery Agent stopped."
            )

            agent.alive = False


    def is_done(self):

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
        "TASK 1 - REFLEX DELIVERY AGENT"
    )

    print(
        "================================"
    )


    #create environment
    ce = CompanyEnvironment()


    #create recipients
    student = Student()

    itStaff = ITStaff()

    officeManager = OfficeManager()


    #add recipients
    ce.add_thing(student)

    ce.add_thing(itStaff)

    ce.add_thing(officeManager)


    print(
        "\n--- RECIPIENT LOCATIONS ---"
    )

    print(
        student.name,
        "(Student) is at",
        student.location
    )

    print(
        itStaff.name,
        "(IT Staff) is at",
        itStaff.location
    )

    print(
        officeManager.name,
        "(Office Manager) is at",
        officeManager.location
    )


    #create Delivery Agent
    deliveryAgent = ReflexAgentA2pro()


    #add agent
    ce.add_thing(
        deliveryAgent
    )


    #--------------------------------------------
    # IMPORTANT
    #
    # Instructor's Agent starts performance at 0.
    # Moving costs 1.
    #
    # Give it enough starting performance so that
    # we can properly test the complete program.
    #--------------------------------------------

    deliveryAgent.performance = 10


    print(
        "\nDelivery Agent starts at",
        deliveryAgent.location
    )


    print(
        "\n--- STARTING DELIVERY ---"
    )


    #run for maximum 10 steps
    ce.run(10)


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
        "Performance:",
        deliveryAgent.performance
    )

    print(
        "Final location:",
        deliveryAgent.location
    )


    print(
        "\nRecipients still waiting:"
    )


    if len(ce.things) == 0:

        print(
            "Nobody"
        )

    else:

        for person in ce.things:

            print(
                person.name,
                "-",
                type(person).__name__,
                "-",
                person.location
            )


#--------------------------------------------------
# START PROGRAM
#--------------------------------------------------

if __name__ == "__main__":

    main()