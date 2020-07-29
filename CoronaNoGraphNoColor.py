import os
import random
import sys
import time

Originrows = 200
Origincolums = 200


# to print in green
def print_green(skk): print("\033[92m {}\033[00m".format(skk))


# to print in red
def print_red(skk): print("\033[91m {}\033[00m".format(skk))


def run_game():
    clear_console()
    flag = False
    print("Welcome to our CoronaVirus simulator!")
    x = float(input("Enter value (between 0 to 1) for chance of infection (P): "))
    p = float("{:.2f}".format(x))
    k = int(input("Please Enter the Severity of Social Distancing:"))
    generations = int(input("Please Enter the Number of Generations:"))
    if k > 0:
        flag = True
        kgen = int(input("Please Enter From Which Generation to Start the Social Distancing:"))

    print("Starting Simulation with P = {0} K= {1} :".format(p, k))
    # set size of the grid
    rows = Originrows
    cols = Origincolums
    resize_console(rows, cols)
    ktodo = 0
    initial_n, current_generation = create_initial_grid(rows, cols)
    next_generation = get_blank_grid(rows, cols)
    print(initial_n)
    # create an output file for this run
    file_str = "N{0}; P{1}; K{2}.txt".format(initial_n, p, k)
    output = open(file_str, "w")

    for curr_gen in range(1, generations + 1):
        print_grid(rows, cols, current_generation, curr_gen, "Infection")
        inf = count_infected(rows, cols, current_generation)
        if inf == initial_n:
            export_results_forgraph(output, curr_gen, inf)
            print("\n\rAll cells are infected, game over!")
            break
        if flag == True:
            if curr_gen > kgen:
                ktodo = k
        if ktodo == 0:
            next_generation = calculate_next_grid_Solitery0(rows, cols, current_generation, next_generation, p,
                                                            curr_gen)
        if ktodo == 1:
            next_generation = calculate_next_grid_Solitery1(rows, cols, current_generation, next_generation, p,
                                                            curr_gen)
        if ktodo == 2:
            next_generation = calculate_next_grid_Solitery2(rows, cols, current_generation, next_generation, p,
                                                            curr_gen)
        if ktodo == 3:
            next_generation = calculate_next_grid_Solitery3(rows, cols, current_generation, next_generation, p,
                                                            curr_gen)
        if ktodo == 4:
            next_generation = calculate_next_grid_Solitery4(rows, cols, current_generation, next_generation, p,
                                                            curr_gen)
        if ktodo == 5:
            next_generation = calculate_next_grid_Solitery5(rows, cols, current_generation, next_generation, p,
                                                            curr_gen)
        if ktodo == 6:
            next_generation = calculate_next_grid_Solitery6(rows, cols, current_generation, next_generation, p,
                                                            curr_gen)
        if ktodo == 7:
            next_generation = calculate_next_grid_Solitery7(rows, cols, current_generation, next_generation, p,
                                                            curr_gen)
        if ktodo == 8:
            next_generation = calculate_next_grid_Solitery8(rows, cols, current_generation, next_generation, p,
                                                            curr_gen)
        time.sleep(1.5)
        current_generation = copy_grid(rows, cols, next_generation, current_generation)
        next_generation = get_blank_grid(rows, cols)
        export_results_forgraph(output, curr_gen, inf)

    output.close()
    # input("Press <Enter> to exit.")


#
# def export_results(f, gen, infected):
#     out_str = ""
#     out_str += "generation: {0}\n".format(gen)
#     out_str += "infected cells: {0}\n\r".format(infected)
#     f.write(out_str)


def export_results_forgraph(f, gen, infected):
    out_str = ""
    out_str += "{0},{1}\n".format(gen, infected)
    f.write(out_str)


def count_infected(rows, cols, grid):
    inf_count = 1
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 2:
                inf_count += 1
    return inf_count


def get_blank_grid(rows, cols):
    grid = []
    for row in range(rows):
        grid_rows = []
        for col in range(cols):
            grid_rows += [0]
        grid += [grid_rows]
    return grid


def copy_grid(rows, cols, grid1, grid2):
    for row in range(rows):
        for col in range(cols):
            grid2[row][col] = grid1[row][col]
    return grid2


def clear_console():
    """
    Clears the console using a system command based on the user's operating system.
    """

    if sys.platform.startswith('win'):
        os.system("cls")
    elif sys.platform.startswith('linux'):
        os.system("clear")
    else:
        print("Unable to clear terminal. Your operating system is not supported.\n\r")


def resize_console(rows, cols):
    """
    Re-sizes the console to the size of rows x columns
    :param rows: Int - The number of rows for the console to re-size to
    :param cols: Int - The number of columns for the console to re-size to
    """

    if cols < 32:
        cols = 32

    if sys.platform.startswith('win'):
        command = "mode con: cols={0} lines={1}".format(cols + cols, rows + 5)
        os.system(command)
    elif sys.platform.startswith('linux'):
        command = "\x1b[8;{rows};{cols}t".format(rows=rows + 3, cols=cols + cols)
        sys.stdout.write(command)
    else:
        print("Unable to resize terminal. Your operating system is not supported.\n\r")


def create_initial_grid(rows, cols):
    """
    Creates a random list of lists that contains 'X' and '-' to represent the cells.
    :param rows: the number of rows that the Game of Life grid will have
    :param cols: the number of columns that the Game of Life grid will have
    :return: A list of lists containing 1s for live cells and 0s for dead cells
    """
    n_count = 0
    grid = []
    for row in range(rows):
        grid_rows = []
        for col in range(cols):
            # Generate a random number and based on that decide whether to add a live or dead cell to the grid
            if random.randint(0, 4) == 0:
                grid_rows += [1]
                n_count += 1
            else:
                grid_rows += [0]
        grid += [grid_rows]

    # randomize patient-zero cell
    while True:
        infected_row = random.randint(0, rows - 1)
        infected_col = random.randint(0, cols - 1)
        if grid[infected_row][infected_col] == 1:
            grid[infected_row][infected_col] = 2
            break

    return n_count, grid


def get_mov_cord(cur_row, cur_col, randomized_num):
    # case '5' is no change in position
    if randomized_num == 5:
        return cur_row, cur_col

    if randomized_num == 6:
        return cur_row, cur_col + 1

    if randomized_num == 8:
        return cur_row + 1, cur_col

    if randomized_num == 4:
        return cur_row, cur_col - 1

    if randomized_num == 2:
        return cur_row - 1, cur_col

    if randomized_num == 1:
        return cur_row - 1, cur_col - 1

    if randomized_num == 3:
        return cur_row - 1, cur_col + 1

    if randomized_num == 9:
        return cur_row + 1, cur_col + 1

    if randomized_num == 7:
        return cur_row + 1, cur_col - 1


def print_grid(rows, cols, grid, generation, state):
    clear_console()

    # A single output string is used to help reduce the flickering caused by printing multiple lines
    output_str = ""

    infected_count = 0
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 2:
                infected_count += 1

    # Compile the output string together and then print it to console
    # output_str += "Generation {0} - To exit the program early press <Ctrl-C>\n\r".format(generation)
    output_str += "\n\rGeneration {0}: {1}\n\r".format(generation, state)

    output_str += "Infected: {0}\n\r".format(infected_count)

    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 0:
                output_str += ". "
            elif grid[row][col] == 1:
                # output_str += "@ "
                output_str += "@ "
            else:
                output_str += "X "
        output_str += "\n\r"
    print(output_str, end=" ")


def calculate_next_grid_Solitery0(rows, cols, current_grid, next_grid, p, gen):
    """
    Analyzes the current generation of the Game of Life grid and determines what cells live, die or get infected in the
    next generation.
    """

    """ cell movement logic """
    for row in range(rows):
        for col in range(cols):
            if not current_grid[row][col] == 0:
                temp = random.randint(1, 9)
                next_row, next_col = get_mov_cord(row, col, temp)
                # fix out of bound cells
                next_row = next_row % rows
                next_col = next_col % cols

                # if the next position is not vacant, stay in place and continue to next cell
                if not next_grid[next_row][next_col] == 0 or not current_grid[next_row][next_col] == 0:
                    next_grid[row][col] = current_grid[row][col]
                    #   print("[" + str(row) + "]" + "[" + str(col) + "] stays")
                    continue
                # else move
                else:

                    # print("moving [" + str(row) + "]" + "[" + str(col) + "] to: [" + str(next_row) + "]" + "[" + str(
                    #   next_col) + "]")

                    # if the cell is sick
                    if current_grid[row][col] == 2:
                        next_grid[next_row][next_col] = 2
                    else:
                        next_grid[next_row][next_col] = 1
                    current_grid[row][col] = 0

    if gen == 1:
        print_grid(rows, cols, next_grid, gen, "Patient Zero")
    else:
        print_grid(rows, cols, next_grid, gen, "Movement")

    """
    corona virus spread logic. For each infected cell, check his neighbours and decide whether they will get sick too
    """
    for i_row in range(rows):
        for i_col in range(cols):
            if next_grid[i_row][i_col] == 2:
                for neighbour in range(1, 10):
                    if neighbour == 5:
                        continue
                    # get the neighbour coordinates
                    n_row, n_col = get_mov_cord(i_row, i_col, neighbour)
                    n_row = n_row % rows
                    n_col = n_col % cols

                    if next_grid[n_row][n_col] == 1:
                        # calculate if neighbour will get infected
                        temp = random.randint(1, 100)
                        if temp <= (p * 100):
                            next_grid[n_row][n_col] = 2

    print_grid(rows, cols, next_grid, gen, "Infection")

    return next_grid


def calculate_next_grid_Solitery1(rows, cols, current_grid, next_grid, p, gen):
    """
    Analyzes the current generation of the Game of Life grid and determines what cells live, die or get infected in the
    next generation.
    """

    """ cell movement logic """
    for row in range(rows):
        for col in range(cols):
            if not current_grid[row][col] == 0:
                temp = random.randint(1, 9)
                next_row, next_col = get_mov_cord(row, col, temp)
                # fix out of bound cells
                next_row = next_row % rows
                next_col = next_col % cols

                # if the next position is not vacant, stay in place and continue to next cell
                if not next_grid[next_row][next_col] == 0 or not current_grid[next_row][next_col] == 0:
                    next_grid[row][col] = current_grid[row][col]
                    #   print("[" + str(row) + "]" + "[" + str(col) + "] stays")
                    continue
                # else move
                else:

                    # print("moving [" + str(row) + "]" + "[" + str(col) + "] to: [" + str(next_row) + "]" + "[" + str(
                    #   next_col) + "]")

                    # if the cell is sick
                    if current_grid[row][col] == 2:
                        next_grid[next_row][next_col] = 2
                    else:
                        next_grid[next_row][next_col] = 1
                    current_grid[row][col] = 0

    if gen == 1:
        print_grid(rows, cols, next_grid, gen, "Patient Zero")
    else:
        print_grid(rows, cols, next_grid, gen, "Movement")

    """
    corona virus spread logic. For each infected cell, check his neighbours and decide whether they will get sick too
    """
    for i_row in range(rows):
        for i_col in range(cols):
            if next_grid[i_row][i_col] == 2:
                for neighbour in range(1, 10):
                    if neighbour == 5 or neighbour == 4:
                        continue
                    # get the neighbour coordinates
                    n_row, n_col = get_mov_cord(i_row, i_col, neighbour)
                    n_row = n_row % rows
                    n_col = n_col % cols

                    if next_grid[n_row][n_col] == 1:
                        # calculate if neighbour will get infected
                        temp = random.randint(1, 100)
                        if temp <= (p * 100):
                            next_grid[n_row][n_col] = 2

    print_grid(rows, cols, next_grid, gen, "Infection")

    return next_grid


def calculate_next_grid_Solitery2(rows, cols, current_grid, next_grid, p, gen):
    """
    Analyzes the current generation of the Game of Life grid and determines what cells live, die or get infected in the
    next generation.
    """

    """ cell movement logic """
    for row in range(rows):
        for col in range(cols):
            if not current_grid[row][col] == 0:
                temp = random.randint(1, 9)
                next_row, next_col = get_mov_cord(row, col, temp)
                # fix out of bound cells
                next_row = next_row % rows
                next_col = next_col % cols

                # if the next position is not vacant, stay in place and continue to next cell
                if not next_grid[next_row][next_col] == 0 or not current_grid[next_row][next_col] == 0:
                    next_grid[row][col] = current_grid[row][col]
                    #   print("[" + str(row) + "]" + "[" + str(col) + "] stays")
                    continue
                # else move
                else:

                    # print("moving [" + str(row) + "]" + "[" + str(col) + "] to: [" + str(next_row) + "]" + "[" + str(
                    #   next_col) + "]")

                    # if the cell is sick
                    if current_grid[row][col] == 2:
                        next_grid[next_row][next_col] = 2
                    else:
                        next_grid[next_row][next_col] = 1
                    current_grid[row][col] = 0

    if gen == 1:
        print_grid(rows, cols, next_grid, gen, "Patient Zero")
    else:
        print_grid(rows, cols, next_grid, gen, "Movement")

    """
    corona virus spread logic. For each infected cell, check his neighbours and decide whether they will get sick too
    """
    for i_row in range(rows):
        for i_col in range(cols):
            if next_grid[i_row][i_col] == 2:
                for neighbour in range(1, 10):
                    if neighbour == 5 or neighbour == 4 or neighbour == 8:
                        continue
                    # get the neighbour coordinates
                    n_row, n_col = get_mov_cord(i_row, i_col, neighbour)
                    n_row = n_row % rows
                    n_col = n_col % cols

                    if next_grid[n_row][n_col] == 1:
                        # calculate if neighbour will get infected
                        temp = random.randint(1, 100)
                        if temp <= (p * 100):
                            next_grid[n_row][n_col] = 2

    print_grid(rows, cols, next_grid, gen, "Infection")

    return next_grid


def calculate_next_grid_Solitery3(rows, cols, current_grid, next_grid, p, gen):
    """
    Analyzes the current generation of the Game of Life grid and determines what cells live, die or get infected in the
    next generation.
    """

    """ cell movement logic """
    for row in range(rows):
        for col in range(cols):
            if not current_grid[row][col] == 0:
                temp = random.randint(1, 9)
                next_row, next_col = get_mov_cord(row, col, temp)
                # fix out of bound cells
                next_row = next_row % rows
                next_col = next_col % cols

                # if the next position is not vacant, stay in place and continue to next cell
                if not next_grid[next_row][next_col] == 0 or not current_grid[next_row][next_col] == 0:
                    next_grid[row][col] = current_grid[row][col]
                    #   print("[" + str(row) + "]" + "[" + str(col) + "] stays")
                    continue
                # else move
                else:

                    # print("moving [" + str(row) + "]" + "[" + str(col) + "] to: [" + str(next_row) + "]" + "[" + str(
                    #   next_col) + "]")

                    # if the cell is sick
                    if current_grid[row][col] == 2:
                        next_grid[next_row][next_col] = 2
                    else:
                        next_grid[next_row][next_col] = 1
                    current_grid[row][col] = 0

    if gen == 1:
        print_grid(rows, cols, next_grid, gen, "Patient Zero")
    else:
        print_grid(rows, cols, next_grid, gen, "Movement")

    """
    corona virus spread logic. For each infected cell, check his neighbours and decide whether they will get sick too
    """
    for i_row in range(rows):
        for i_col in range(cols):
            if next_grid[i_row][i_col] == 2:
                for neighbour in range(1, 10):
                    if neighbour == 5 or neighbour == 8 or neighbour == 7 or neighbour == 4:
                        continue
                    # get the neighbour coordinates
                    n_row, n_col = get_mov_cord(i_row, i_col, neighbour)
                    n_row = n_row % rows
                    n_col = n_col % cols

                    if next_grid[n_row][n_col] == 1:
                        # calculate if neighbour will get infected
                        temp = random.randint(1, 100)
                        if temp <= (p * 100):
                            next_grid[n_row][n_col] = 2

    print_grid(rows, cols, next_grid, gen, "Infection")

    return next_grid


def calculate_next_grid_Solitery4(rows, cols, current_grid, next_grid, p, gen):
    """
    Analyzes the current generation of the Game of Life grid and determines what cells live, die or get infected in the
    next generation.
    """

    """ cell movement logic """
    for row in range(rows):
        for col in range(cols):
            if not current_grid[row][col] == 0:
                temp = random.randint(1, 9)
                next_row, next_col = get_mov_cord(row, col, temp)
                # fix out of bound cells
                next_row = next_row % rows
                next_col = next_col % cols

                # if the next position is not vacant, stay in place and continue to next cell
                if not next_grid[next_row][next_col] == 0 or not current_grid[next_row][next_col] == 0:
                    next_grid[row][col] = current_grid[row][col]
                    #   print("[" + str(row) + "]" + "[" + str(col) + "] stays")
                    continue
                # else move
                else:

                    # print("moving [" + str(row) + "]" + "[" + str(col) + "] to: [" + str(next_row) + "]" + "[" + str(
                    #   next_col) + "]")

                    # if the cell is sick
                    if current_grid[row][col] == 2:
                        next_grid[next_row][next_col] = 2
                    else:
                        next_grid[next_row][next_col] = 1
                    current_grid[row][col] = 0

    if gen == 1:
        print_grid(rows, cols, next_grid, gen, "Patient Zero")
    else:
        print_grid(rows, cols, next_grid, gen, "Movement")

    """
    corona virus spread logic. For each infected cell, check his neighbours and decide whether they will get sick too
    """
    for i_row in range(rows):
        for i_col in range(cols):
            if next_grid[i_row][i_col] == 2:
                for neighbour in range(1, 10):
                    if neighbour == 5 or neighbour == 8 or neighbour == 7 or neighbour == 4 or neighbour == 1:
                        continue
                    # get the neighbour coordinates
                    n_row, n_col = get_mov_cord(i_row, i_col, neighbour)
                    n_row = n_row % rows
                    n_col = n_col % cols

                    if next_grid[n_row][n_col] == 1:
                        # calculate if neighbour will get infected
                        temp = random.randint(1, 100)
                        if temp <= (p * 100):
                            next_grid[n_row][n_col] = 2

    print_grid(rows, cols, next_grid, gen, "Infection")

    return next_grid


def calculate_next_grid_Solitery5(rows, cols, current_grid, next_grid, p, gen):
    """
    Analyzes the current generation of the Game of Life grid and determines what cells live, die or get infected in the
    next generation.
    """

    """ cell movement logic """
    for row in range(rows):
        for col in range(cols):
            if not current_grid[row][col] == 0:
                temp = random.randint(1, 9)
                next_row, next_col = get_mov_cord(row, col, temp)
                # fix out of bound cells
                next_row = next_row % rows
                next_col = next_col % cols

                # if the next position is not vacant, stay in place and continue to next cell
                if not next_grid[next_row][next_col] == 0 or not current_grid[next_row][next_col] == 0:
                    next_grid[row][col] = current_grid[row][col]
                    #   print("[" + str(row) + "]" + "[" + str(col) + "] stays")
                    continue
                # else move
                else:

                    # print("moving [" + str(row) + "]" + "[" + str(col) + "] to: [" + str(next_row) + "]" + "[" + str(
                    #   next_col) + "]")

                    # if the cell is sick
                    if current_grid[row][col] == 2:
                        next_grid[next_row][next_col] = 2
                    else:
                        next_grid[next_row][next_col] = 1
                    current_grid[row][col] = 0

    if gen == 1:
        print_grid(rows, cols, next_grid, gen, "Patient Zero")
    else:
        print_grid(rows, cols, next_grid, gen, "Movement")

    """
    corona virus spread logic. For each infected cell, check his neighbours and decide whether they will get sick too
    """
    for i_row in range(rows):
        for i_col in range(cols):
            if next_grid[i_row][i_col] == 2:
                for neighbour in range(1, 10):
                    if neighbour == 5 or neighbour == 8 or neighbour == 7 or neighbour == 4 or neighbour == 1 or neighbour == 9:
                        continue
                    # get the neighbour coordinates
                    n_row, n_col = get_mov_cord(i_row, i_col, neighbour)
                    n_row = n_row % rows
                    n_col = n_col % cols

                    if next_grid[n_row][n_col] == 1:
                        # calculate if neighbour will get infected
                        temp = random.randint(1, 100)
                        if temp <= (p * 100):
                            next_grid[n_row][n_col] = 2

    print_grid(rows, cols, next_grid, gen, "Infection")

    return next_grid


def calculate_next_grid_Solitery6(rows, cols, current_grid, next_grid, p, gen):
    """
    Analyzes the current generation of the Game of Life grid and determines what cells live, die or get infected in the
    next generation.
    """

    """ cell movement logic """
    for row in range(rows):
        for col in range(cols):
            if not current_grid[row][col] == 0:
                temp = random.randint(1, 9)
                next_row, next_col = get_mov_cord(row, col, temp)
                # fix out of bound cells
                next_row = next_row % rows
                next_col = next_col % cols

                # if the next position is not vacant, stay in place and continue to next cell
                if not next_grid[next_row][next_col] == 0 or not current_grid[next_row][next_col] == 0:
                    next_grid[row][col] = current_grid[row][col]
                    #   print("[" + str(row) + "]" + "[" + str(col) + "] stays")
                    continue
                # else move
                else:

                    # print("moving [" + str(row) + "]" + "[" + str(col) + "] to: [" + str(next_row) + "]" + "[" + str(
                    #   next_col) + "]")

                    # if the cell is sick
                    if current_grid[row][col] == 2:
                        next_grid[next_row][next_col] = 2
                    else:
                        next_grid[next_row][next_col] = 1
                    current_grid[row][col] = 0

    if gen == 1:
        print_grid(rows, cols, next_grid, gen, "Patient Zero")
    else:
        print_grid(rows, cols, next_grid, gen, "Movement")

    """
    corona virus spread logic. For each infected cell, check his neighbours and decide whether they will get sick too
    """
    for i_row in range(rows):
        for i_col in range(cols):
            if next_grid[i_row][i_col] == 2:
                for neighbour in range(1, 10):
                    if neighbour == 5 or neighbour == 8 or neighbour == 7 or neighbour == 4 or neighbour == 1 \
                            or neighbour == 9 or neighbour == 6:
                        continue
                    # get the neighbour coordinates
                    n_row, n_col = get_mov_cord(i_row, i_col, neighbour)
                    n_row = n_row % rows
                    n_col = n_col % cols

                    if next_grid[n_row][n_col] == 1:
                        # calculate if neighbour will get infected
                        temp = random.randint(1, 100)
                        if temp <= (p * 100):
                            next_grid[n_row][n_col] = 2

    print_grid(rows, cols, next_grid, gen, "Infection")

    return next_grid


def calculate_next_grid_Solitery7(rows, cols, current_grid, next_grid, p, gen):
    """
    Analyzes the current generation of the Game of Life grid and determines what cells live, die or get infected in the
    next generation.
    """

    """ cell movement logic """
    for row in range(rows):
        for col in range(cols):
            if not current_grid[row][col] == 0:
                temp = random.randint(1, 9)
                next_row, next_col = get_mov_cord(row, col, temp)
                # fix out of bound cells
                next_row = next_row % rows
                next_col = next_col % cols

                # if the next position is not vacant, stay in place and continue to next cell
                if not next_grid[next_row][next_col] == 0 or not current_grid[next_row][next_col] == 0:
                    next_grid[row][col] = current_grid[row][col]
                    #   print("[" + str(row) + "]" + "[" + str(col) + "] stays")
                    continue
                # else move
                else:

                    # print("moving [" + str(row) + "]" + "[" + str(col) + "] to: [" + str(next_row) + "]" + "[" + str(
                    #   next_col) + "]")

                    # if the cell is sick
                    if current_grid[row][col] == 2:
                        next_grid[next_row][next_col] = 2
                    else:
                        next_grid[next_row][next_col] = 1
                    current_grid[row][col] = 0

    if gen == 1:
        print_grid(rows, cols, next_grid, gen, "Patient Zero")
    else:
        print_grid(rows, cols, next_grid, gen, "Movement")

    """
    corona virus spread logic. For each infected cell, check his neighbours and decide whether they will get sick too
    """
    for i_row in range(rows):
        for i_col in range(cols):
            if next_grid[i_row][i_col] == 2:
                for neighbour in range(1, 10):
                    if neighbour == 5 or neighbour == 8 or neighbour == 7 or neighbour == 4 or neighbour == 1 \
                            or neighbour == 9 or neighbour == 6 or neighbour == 3:
                        continue
                    # get the neighbour coordinates
                    n_row, n_col = get_mov_cord(i_row, i_col, neighbour)
                    n_row = n_row % rows
                    n_col = n_col % cols

                    if next_grid[n_row][n_col] == 1:
                        # calculate if neighbour will get infected
                        temp = random.randint(1, 100)
                        if temp <= (p * 100):
                            next_grid[n_row][n_col] = 2

    print_grid(rows, cols, next_grid, gen, "Infection")

    return next_grid


def calculate_next_grid_Solitery8(rows, cols, current_grid, next_grid, p, gen):
    """
    Analyzes the current generation of the Game of Life grid and determines what cells live, die or get infected in the
    next generation.
    """

    """ cell movement logic """
    for row in range(rows):
        for col in range(cols):
            if not current_grid[row][col] == 0:
                temp = random.randint(1, 9)
                next_row, next_col = get_mov_cord(row, col, temp)
                # fix out of bound cells
                next_row = next_row % rows
                next_col = next_col % cols

                # if the next position is not vacant, stay in place and continue to next cell
                if not next_grid[next_row][next_col] == 0 or not current_grid[next_row][next_col] == 0:
                    next_grid[row][col] = current_grid[row][col]
                    #   print("[" + str(row) + "]" + "[" + str(col) + "] stays")
                    continue
                # else move
                else:

                    # print("moving [" + str(row) + "]" + "[" + str(col) + "] to: [" + str(next_row) + "]" + "[" + str(
                    #   next_col) + "]")

                    # if the cell is sick
                    if current_grid[row][col] == 2:
                        next_grid[next_row][next_col] = 2
                    else:
                        next_grid[next_row][next_col] = 1
                    current_grid[row][col] = 0

    if gen == 1:
        print_grid(rows, cols, next_grid, gen, "Patient Zero")
    else:
        print_grid(rows, cols, next_grid, gen, "Movement")

    """
    corona virus spread logic. For each infected cell, check his neighbours and decide whether they will get sick too
    """
    for i_row in range(rows):
        for i_col in range(cols):
            if next_grid[i_row][i_col] == 2:
                for neighbour in range(1, 10):
                    if neighbour == 5 or neighbour == 8 or neighbour == 7 or neighbour == 4 or neighbour == 1 \
                            or neighbour == 9 or neighbour == 6 or neighbour == 3 or neighbour == 2:
                        continue
                    # get the neighbour coordinates
                    n_row, n_col = get_mov_cord(i_row, i_col, neighbour)
                    n_row = n_row % rows
                    n_col = n_col % cols

                    if next_grid[n_row][n_col] == 1:
                        # calculate if neighbour will get infected
                        temp = random.randint(1, 100)
                        if temp <= (p * 100):
                            next_grid[n_row][n_col] = 2

    print_grid(rows, cols, next_grid, gen, "Infection")

    return next_grid


run_game()
