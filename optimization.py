from tkinter import *
import time
import os
import random
import math

def optimization(main_window_terminal, main_window_button1, main_window_button2, main_window_button3, config_dict, progress):
    def simulated_annealing(initial_state):
        """Peforms simulated annealing to find a solution"""
        initial_temp = 100
        final_temp = 1
        alpha = 0.001
        
        current_temp = initial_temp

        # Start by initializing the current state with the initial state
        current_state = initial_state
        solution = current_state

        while current_temp > final_temp:
            next_state = get_next_state(current_state)

            # Check if neighbor is best so far
            cost_diff = get_cost(current_state) - get_cost(next_state)
            #print(get_cost(next_state))

            # if the new solution is better, accept it
            if cost_diff > 0:
                solution = next_state
            # if the new solution is not better, accept it with a probability of e^(-cost/temp)
            else:
                if random.uniform(0, 1) < math.exp(-cost_diff / current_temp):
                    solution = next_state
            # decrement the temperature
            current_temp -= alpha

        return solution

    def get_cost(state):
        #calculate cost for solution
        solution = make_solution(state)
        cost = 0
        for y in solution:
            cost += profile_length - sum(y)
        return cost
        
    def get_next_state(state):
        next_state = state.copy()
        get_new_random = True

        #get random indexes values to swap
        while(get_new_random == True):
            index1 = random.randint(0, (len(next_state)-1))
            index2 = random.randint(0, (len(next_state)-1))
            if (index1 == index2): #cannot be in the same 
                get_new_random = True
            elif (next_state[index1] == next_state[index2]): #cannot be the same values
                get_new_random = True
            else:
                get_new_random = False

        next_state[index1], next_state[index2] = next_state[index2], next_state[index1]
        return next_state

    def make_solution(state):
        #make solution from state        
        solution = list()
        solution_part = list()
        
        for x in state:
            if sum(solution_part) + x <= config_dict["0"]:
                solution_part.append(x)
            else:
                solution.append(solution_part.copy())
                solution_part.clear()
                solution_part.append(x)
        if len(solution_part) > 0:
            solution.append(solution_part.copy())
            solution_part.clear()

        return solution

    def make_initial_state():
        #make initial_state from config_dict 
        initial_state = []
        config_list = list(config_dict.values())
        
        for x in range(1, len(config_list)):
            item_length = int(config_list[x][1])
            for y in range(int(config_list[x][0])):
                initial_state.append(item_length)
        return initial_state

    profile_length = config_dict["0"]
    initial_state = make_initial_state()

    #Do simulated_annealing 10 times to get best solution
    final_cost = get_cost(initial_state)
    for x in range(10):
        state = simulated_annealing(initial_state)
        cost = get_cost(state)
        if cost < final_cost:
            final_state = state.copy()
            final_cost = cost
        progress['value'] += 10
        progress.update_idletasks() #update gui over tasks in code

    #pritn solution in terminal
    final_solution = make_solution(final_state)
    print("Final solution : " + str(final_solution) + "; Wasted material [mm] = " + str(final_cost))
    sec = time.localtime() # get struct_time
    main_window_terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "  Solution found.")
    main_window_terminal.itemconfig(END, fg = "green")
    progress['value'] = 0
    i = 1
    for x in final_solution:
        text = "Profile" + str(i) + " : "
        for y in x:
            text += str(y) + ", "
        main_window_terminal.insert(END, text)
        main_window_terminal.itemconfig(END, fg = "green")
        text = ""
        i += 1
    main_window_terminal.insert(END, "Wasted material [mm] = " + str(final_cost))
    main_window_terminal.itemconfig(END, fg = "green")

    main_window_button1.config(state=NORMAL)
    main_window_button2.config(state=NORMAL)
    main_window_button3.config(state=NORMAL)