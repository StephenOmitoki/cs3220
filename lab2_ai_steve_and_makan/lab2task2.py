#AI Assignment 2 - Task 2
#Reflex Cat-Agent


import random


#--------------------------------------------------
# LOCATIONS
#--------------------------------------------------

loc_A = (0, 0)
loc_B = (0, 1)
loc_C = (1, 0)


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
# FOOD CLASS
#--------------------------------------------------

class Food(Thing):

    def __init__(
        self,
        weight=0,
        calories=0,
        energy=0
    ):

        self.weight = weight

        self.calories = calories

        self.energy = energy

        self.location = None


    def sayHi(self):

        print(
            "I am",
            type(self).__name__,
            "- weight:",
            self.weight,
            "- calories:",
            self.calories,
            "- energy:",
            self.energy
        )


#--------------------------------------------------
# MILK
#--------------------------------------------------

class Milk(Food):

    def __init__(
        self,
        weight,
        calories
    ):

        super().__init__(
            weight,
            calories
        )


#--------------------------------------------------
# SAUSAGE
#--------------------------------------------------

class Sausage(Food):

    def __init__(
        self,
        weight,
        calories
    ):

        super().__init__(
            weight,
            calories
        )


#--------------------------------------------------
# MOUSE
#--------------------------------------------------

class Mouse(Food):

    def __init__(
        self,
        size=1
    ):

        self.size = size

        self.weight = 0

        self.calories = 0


        #given directly in assignment
        self.energy = (
            size * 1000
        )


        self.location = None


    def sayHi(self):

        print(
            "I am Mouse",
            "- size:",
            self.size,
            "- energy:",
            self.energy
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
# CAT AGENT
#--------------------------------------------------

class CatAgent(Agent):

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


    def changeDirection(self):

        self.direction = (
            not self.direction
        )


    def getDirection(self):

        if self.direction:

            return "Left to Right"

        else:

            return "Right to Left"


#--------------------------------------------------
# ENVIRONMENT CLASS
#--------------------------------------------------

class Environment:

    def __init__(self):

        self.agents = []


    def is_done(self):

        return not any(

            agent.is_alive()

            for agent in self.agents
        )


    def step(self):


        if self.is_done():

            print(
                "There is no live agent."
            )

            return


        for agent in self.agents:


            if agent.alive:


                print(
                    "\nCat Performance:",
                    agent.performance
                )


                print(
                    "Cat Location:",
                    agent.location
                )


                print(
                    "Cat Direction:",
                    agent.getDirection()
                )


                percept = self.percept(
                    agent
                )


                print(
                    "Cat percepted:",
                    percept
                )


                action = agent.program(
                    percept
                )


                print(
                    "Cat decided to do:",
                    action
                )


                self.execute_action(
                    agent,
                    action
                )


    def run(
        self,
        steps=30
    ):


        for step in range(
            steps
        ):


            if self.is_done():


                print(
                    "\nThe Cat Agent has stopped."
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


                result.append(
                    thing
                )


        return result


    def add_thing(
        self,
        thing,
        location=None
    ):


        if isinstance(
            thing,
            Agent
        ):


            if location is not None:

                thing.location = location


            else:

                thing.location = (
                    self.default_location(
                        thing
                    )
                )


            self.agents.append(
                thing
            )


            print(
                "Welcome! Cat Agent added at",
                thing.location
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


    def delete_thing(
        self,
        thing
    ):


        if thing in self.things:

            self.things.remove(
                thing
            )


#--------------------------------------------------
# TASK 2 RULES
#--------------------------------------------------

catRules = {

    'Milk': 'Drink',

    'Sausage': 'Eat',

    'Mouse': 'Catch',

    'Empty': 'GoAhead'
}


#--------------------------------------------------
# INTERPRET INPUT
#--------------------------------------------------

def interpret_input_A3pro(
    percept
):


    location, status = percept


    #if there are many items
    #deal with one at a time
    if isinstance(
        status,
        list
    ):


        return status[0]


    return status


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


        print(
            "State:",
            state
        )


        action = rule_match(

            state,

            rules
        )


        return action


    return program


#--------------------------------------------------
# CREATE TASK 2 CAT
#--------------------------------------------------

def ReflexAgentA3pro():


    program = ReflexAgentProgram(

        catRules,

        interpret_input_A3pro,

        rule_match
    )


    return CatAgent(
        program
    )


#--------------------------------------------------
# CAT FRIENDLY HOUSE
#--------------------------------------------------

class catFriendlyHouse_env(
    environmentPro
):


    def __init__(self):


        super().__init__()


        #3 rooms in a row
        self.locations = [

            loc_A,

            loc_B,

            loc_C
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
    # PERCEPT
    #--------------------------------------------------

    def percept(
        self,
        agent
    ):


        things = self.list_things_at(

            agent.location,

            Food
        )


        #------------------------------------------
        # EMPTY
        #------------------------------------------

        if len(
            things
        ) == 0:


            status = 'Empty'


        #------------------------------------------
        # ONE ITEM
        #------------------------------------------

        elif len(
            things
        ) == 1:


            status = type(
                things[0]
            ).__name__


        #------------------------------------------
        # MANY ITEMS
        #------------------------------------------

        else:


            status = []


            for thing in things:


                status.append(

                    type(
                        thing
                    ).__name__

                )


        return (

            agent.location,

            status
        )


    #--------------------------------------------------
    # MOVE CAT
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


        #==========================================
        # LEFT TO RIGHT
        #==========================================

        if agent.direction:


            #not at last room
            if currentIndex < (
                len(self.locations) - 1
            ):


                agent.location = (
                    self.locations[
                        currentIndex + 1
                    ]
                )


                #movement costs 1
                agent.performance -= 1


                print(
                    "Cat moved to",
                    agent.location
                )


            #last room
            else:


                #items still remain
                if len(
                    self.things
                ) > 0:


                    print(
                        "Cat reached the last room."
                    )


                    print(
                        "Some items are still in the house."
                    )


                    #change direction
                    agent.changeDirection()


                    print(
                        "Direction changed to:",
                        agent.getDirection()
                    )


                    #move one room back
                    agent.location = (
                        self.locations[
                            currentIndex - 1
                        ]
                    )


                    #movement costs 1
                    agent.performance -= 1


                    print(
                        "Cat moved to",
                        agent.location
                    )


                else:


                    agent.alive = False


        #==========================================
        # RIGHT TO LEFT
        #==========================================

        else:


            #not at first room
            if currentIndex > 0:


                agent.location = (
                    self.locations[
                        currentIndex - 1
                    ]
                )


                #movement costs 1
                agent.performance -= 1


                print(
                    "Cat moved to",
                    agent.location
                )


            #first room
            else:


                print(
                    "Cat reached the first room."
                )


                print(
                    "The hunt is over."
                )


                agent.alive = False


    #--------------------------------------------------
    # FOOD PERFORMANCE
    #--------------------------------------------------

    def food_performance(
        self,
        food
    ):


        #The assignment says Cat performance
        #depends on weight and calories.

        #It does not provide an exact formula.

        #Use calories as the performance gain.
        #Weight is still stored as required.

        return food.calories


    #--------------------------------------------------
    # EXECUTE ACTION
    #--------------------------------------------------

    def execute_action(
        self,
        agent,
        action
    ):


        if not agent.alive:

            return


        #==========================================
        # DRINK
        #==========================================

        if action == 'Drink':


            items = self.list_things_at(

                agent.location,

                Milk
            )


            if len(
                items
            ) > 0:


                milk = items[0]


                gain = self.food_performance(
                    milk
                )


                print(
                    "Cat drank the Milk."
                )


                print(
                    "Milk weight:",
                    milk.weight
                )


                print(
                    "Milk calories:",
                    milk.calories
                )


                print(
                    "Performance gained:",
                    gain
                )


                agent.performance += gain


                self.delete_thing(
                    milk
                )


        #==========================================
        # EAT
        #==========================================

        elif action == 'Eat':


            items = self.list_things_at(

                agent.location,

                Sausage
            )


            if len(
                items
            ) > 0:


                sausage = items[0]


                gain = self.food_performance(
                    sausage
                )


                print(
                    "Cat ate the Sausage."
                )


                print(
                    "Sausage weight:",
                    sausage.weight
                )


                print(
                    "Sausage calories:",
                    sausage.calories
                )


                print(
                    "Performance gained:",
                    gain
                )


                agent.performance += gain


                self.delete_thing(
                    sausage
                )


        #==========================================
        # CATCH
        #==========================================

        elif action == 'Catch':


            items = self.list_things_at(

                agent.location,

                Mouse
            )


            if len(
                items
            ) > 0:


                mouse = items[0]


                print(
                    "Mouse energy:",
                    mouse.energy
                )


                #weak Cat
                if agent.performance < mouse.energy:


                    print(
                        "Cat is too weak to catch the Mouse."
                    )


                    print(
                        "The Mouse survives."
                    )


                    #continue hunting
                    self.move_cat(
                        agent
                    )


                #strong Cat
                else:


                    print(
                        "Cat caught the Mouse."
                    )


                    self.delete_thing(
                        mouse
                    )


        #==========================================
        # GO AHEAD
        #==========================================

        elif action == 'GoAhead':


            self.move_cat(
                agent
            )


        #==========================================
        # ALL ITEMS CONSUMED
        #==========================================

        if len(
            self.things
        ) == 0:


            print(
                "The Cat consumed all items."
            )


            agent.alive = False


    #--------------------------------------------------
    # IS DONE
    #--------------------------------------------------

    def is_done(
        self
    ):


        return not any(

            agent.is_alive()

            for agent in self.agents
        )


#--------------------------------------------------
# MAIN
#--------------------------------------------------

def main():


    print(
        "================================"
    )


    print(
        "TASK 2 - REFLEX CAT AGENT"
    )


    print(
        "================================"
    )


    #--------------------------------------------------
    # CREATE ENVIRONMENT
    #--------------------------------------------------

    e = catFriendlyHouse_env()


    #--------------------------------------------------
    # CREATE FOOD
    #--------------------------------------------------

    milk = Milk(

        weight=200,

        calories=50
    )


    sausage = Sausage(

        weight=150,

        calories=505
    )


    mouse = Mouse(

        size=2
    )


    #--------------------------------------------------
    # RANDOM LOCATIONS
    #--------------------------------------------------

    e.add_thing(
        milk
    )


    e.add_thing(
        sausage
    )


    e.add_thing(
        mouse
    )


    #--------------------------------------------------
    # PRINT LOCATIONS
    #--------------------------------------------------

    print(
        "\n--- FOOD LOCATIONS ---"
    )


    milk.sayHi()


    print(
        "Milk is at",
        milk.location
    )


    sausage.sayHi()


    print(
        "Sausage is at",
        sausage.location
    )


    mouse.sayHi()


    print(
        "Mouse is at",
        mouse.location
    )


    #--------------------------------------------------
    # CREATE CAT
    #--------------------------------------------------

    catAgent = (
        ReflexAgentA3pro()
    )


    #random Cat location
    e.add_thing(
        catAgent
    )


    print(
        "\nState of the House Environment:",
        e.locations
    )


    print(
        "Cat Agent is located at",
        catAgent.location
    )


    print(
        "Cat starting performance:",
        catAgent.performance
    )


    #--------------------------------------------------
    # RUN
    #--------------------------------------------------

    print(
        "\n--- STARTING CAT AGENT ---"
    )


    e.run(
        30
    )


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
        "Cat Performance:",
        catAgent.performance
    )


    print(
        "Cat Final Location:",
        catAgent.location
    )


    print(
        "Cat Final Direction:",
        catAgent.getDirection()
    )


    print(
        "\nItems still in the house:"
    )


    if len(
        e.things
    ) == 0:


        print(
            "None"
        )


    else:


        for thing in e.things:


            print(

                type(
                    thing
                ).__name__,

                "-",

                thing.location
            )


#--------------------------------------------------
# START PROGRAM
#--------------------------------------------------

if __name__ == "__main__":

    main()