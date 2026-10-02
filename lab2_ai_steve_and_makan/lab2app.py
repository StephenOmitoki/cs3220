#AI Assignment 2
#Simple Intelligent Agents
#Streamlit Web-App
#3 Tabs - Task 1, Task 2, Task 3

import streamlit as st

import subprocess

import sys

from pathlib import Path


#--------------------------------------------------
# PAGE SETUP
#--------------------------------------------------

st.set_page_config(

    page_title="AI Assignment 2",

    page_icon="🤖",

    layout="wide"

)


#--------------------------------------------------
# TITLE
#--------------------------------------------------

st.title(
    "AI Assignment 2 - Simple Intelligent Agents"
)


st.write(
    "Task 1: Reflex Delivery Agent | "
    "Task 2: Reflex Cat-Agent | "
    "Task 3: Cat-Agent vs Mouse-Agent"
)


#--------------------------------------------------
# FIND CURRENT FOLDER
#--------------------------------------------------

currentFolder = Path(
    __file__
).parent


#--------------------------------------------------
# RUN PYTHON TASK
#--------------------------------------------------

def runTask(
    fileName
):


    #build complete file path
    filePath = (

        currentFolder

        /

        fileName

    )


    #check that file exists
    if not filePath.exists():


        return (

            "ERROR: "

            +

            fileName

            +

            " was not found."
        )


    #run task using same Python
    #that is running Streamlit
    result = subprocess.run(

        [

            sys.executable,

            str(filePath)

        ],

        capture_output=True,

        text=True

    )


    #----------------------------------------------
    # SUCCESS
    #----------------------------------------------

    if result.returncode == 0:


        return result.stdout


    #----------------------------------------------
    # ERROR
    #----------------------------------------------

    else:


        return (

            result.stdout

            +

            "\n"

            +

            result.stderr

        )


#--------------------------------------------------
# CREATE 3 TABS
#--------------------------------------------------

tab1, tab2, tab3 = st.tabs(

    [

        "Task 1 - Delivery Agent",

        "Task 2 - Cat Agent",

        "Task 3 - Cat vs Mouse"

    ]

)


#==================================================
# TASK 1 TAB
#==================================================

with tab1:


    st.header(
        "Task 1 - Reflex Delivery Agent"
    )


    st.write(
        "The Delivery Agent searches the company "
        "and delivers the correct item to each recipient."
    )


    st.info(
        "Office Manager -> Mail\n\n"
        "IT Staff -> Donuts\n\n"
        "Student -> Pizza"
    )


    #----------------------------------------------
    # RUN BUTTON
    #----------------------------------------------

    if st.button(
        "Run Task 1",
        key="runTask1"
    ):


        output1 = runTask(
            "lab2task1.py"
        )


        st.session_state[
            "task1Output"
        ] = output1


    #----------------------------------------------
    # DISPLAY OUTPUT
    #----------------------------------------------

    if "task1Output" in st.session_state:


        st.subheader(
            "Task 1 Output"
        )


        st.code(

            st.session_state[
                "task1Output"
            ],

            language="text"

        )


    #----------------------------------------------
    # CLEAR BUTTON
    #----------------------------------------------

    if st.button(
        "Clear Task 1",
        key="clearTask1"
    ):


        if "task1Output" in st.session_state:


            del st.session_state[
                "task1Output"
            ]


        st.rerun()


#==================================================
# TASK 2 TAB
#==================================================

with tab2:


    st.header(
        "Task 2 - Reflex Cat-Agent"
    )


    st.write(
        "The Cat-Agent moves through a "
        "3-room Cat-Friendly-House."
    )


    st.info(
        "Milk -> Drink\n\n"
        "Sausage -> Eat\n\n"
        "Mouse -> Catch\n\n"
        "Empty room -> GoAhead"
    )


    #----------------------------------------------
    # RUN BUTTON
    #----------------------------------------------

    if st.button(
        "Run Task 2",
        key="runTask2"
    ):


        output2 = runTask(
            "lab2task2.py"
        )


        st.session_state[
            "task2Output"
        ] = output2


    #----------------------------------------------
    # DISPLAY OUTPUT
    #----------------------------------------------

    if "task2Output" in st.session_state:


        st.subheader(
            "Task 2 Output"
        )


        st.code(

            st.session_state[
                "task2Output"
            ],

            language="text"

        )


    #----------------------------------------------
    # CLEAR BUTTON
    #----------------------------------------------

    if st.button(
        "Clear Task 2",
        key="clearTask2"
    ):


        if "task2Output" in st.session_state:


            del st.session_state[
                "task2Output"
            ]


        st.rerun()


#==================================================
# TASK 3 TAB
#==================================================

with tab3:


    st.header(
        "Task 3 - Cat-Agent vs Mouse-Agent"
    )


    st.write(
        "A Reflex Cat-Agent tries to catch "
        "a Random Mouse-Agent in a 4-room house."
    )


    st.info(
        "Cat actions:\n\n"
        "Clear -> Go ahead\n\n"
        "Last room -> Check direction\n\n"
        "Mouse -> Catch"
    )


    #----------------------------------------------
    # RUN BUTTON
    #----------------------------------------------

    if st.button(
        "Run Task 3",
        key="runTask3"
    ):


        output3 = runTask(
            "lab2task3.py"
        )


        st.session_state[
            "task3Output"
        ] = output3


    #----------------------------------------------
    # DISPLAY OUTPUT
    #----------------------------------------------

    if "task3Output" in st.session_state:


        st.subheader(
            "Task 3 Output"
        )


        st.code(

            st.session_state[
                "task3Output"
            ],

            language="text"

        )


    #----------------------------------------------
    # CLEAR BUTTON
    #----------------------------------------------

    if st.button(
        "Clear Task 3",
        key="clearTask3"
    ):


        if "task3Output" in st.session_state:


            del st.session_state[
                "task3Output"
            ]


        st.rerun()


#--------------------------------------------------
# FOOTER
#--------------------------------------------------

st.divider()


st.write(
    "CS3220 - Assignment 2: Simple Intelligent Agents"
)