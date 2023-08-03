from tkinter import *
from tkinter.messagebox import showerror
from tkinter.ttk import *

import pulp
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


def check_entries():
    if not obj_x.get() or not obj_y.get():
        return False

    for eq_entry in equations_entries:
        if not eq_entry[0] or not eq_entry[1] or not eq_entry[2]:
            return False

    return True


# Function to solve the problem
def solve():
    if not check_entries():
        showerror("Info", "S’il vous plaît remplir tous les champs.")
        return
    else:
        # Retrieve user input data
        objective = obj_var.get()
        c = [float(obj_x.get()), float(obj_y.get())]
        equations = []
        for eq_entry in equations_entries:
            x_val = float(eq_entry[1].get())
            y_val = float(eq_entry[3].get())
            val = float(eq_entry[5].get())
            sign = eq_entry[6].get()
            equation = [x_val, y_val, val, sign]
            equations.append(equation)

        # Create the linear programming problem
        prob = pulp.LpProblem("Linear Programming Problem", pulp.LpMaximize if objective == "max" else pulp.LpMinimize)

        # Create the decision variables
        x = pulp.LpVariable("x", lowBound=0)
        y = pulp.LpVariable("y", lowBound=0)

        # Set the objective function
        prob += c[0] * x + c[1] * y

        # Add the constraints
        for equation in equations:
            if equation[3] == "<=":
                prob += equation[0] * x + equation[1] * y <= equation[2]
            else:
                prob += equation[0] * x + equation[1] * y >= equation[2]

        # Solve the problem
        prob.solve()

        # Clear any existing plots
        for widget in result_frame.winfo_children():
            widget.destroy()

        # Create a Figure and an Axes for the plot
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        # Calculate the maximum value of x and y from the constraints
        max_x = max_y = 0
        for equation in equations:
            if equation[0]:
                max_x = max(max_x, equation[2] / equation[0])
            if equation[1]:
                max_y = max(max_y, equation[2] / equation[1])

        # Set a minimum value for max_x and max_y to avoid division by zero
        # max_x = max(max_x, 1)
        # max_y = max(max_y, 1)
        #
        # # Set the axis limits based on max_x and max_y
        # ax.set_xlim(0, max_x * 1.1)
        # ax.set_ylim(0, max_y * 1.1)

        # Determine the maximum value of x and y from the optimal solution
        optimal_x = pulp.value(x)
        optimal_y = pulp.value(y)
        max_x = max(max_x, optimal_x)
        max_y = max(max_y, optimal_y)

        # Adjust the axis limits to include the optimal solution
        ax.set_xlim(0, max_x * 1.1)
        ax.set_ylim(0, max_y * 1.1)

        # Plot the constraint lines and shade the infeasible regions
        x_vals = [0, max_x]
        # x_vals = [-25, 25]
        for equation in equations:
            if equation[1] != 0:
                y_vals = [(equation[2] - equation[0] * x) / equation[1] for x in x_vals]
                ax.plot(x_vals, y_vals, label=f'{equation[0]}x + {equation[1]}y {equation[3]} {equation[2]}')
                if equation[3] == "<=":
                    ax.fill_between(x_vals, y_vals, max_y, color='gray', alpha=0.5)
                else:
                    ax.fill_between(x_vals, 0, y_vals, color='gray', alpha=0.5)
            else:
                ax.axvline(equation[2] / equation[0], label=f'{equation[0]}x {equation[3]} {equation[2]}')
                if equation[3] == "<=":
                    ax.fill_betweenx([0, max_y], equation[2] / equation[0], max_x, color='gray', alpha=0.5)
                else:
                    ax.fill_betweenx([0, max_y], 0, equation[2] / equation[0], color='gray', alpha=0.5)

        # Plot the objective function line
        if c[1] != 0:
            y_vals = [-(c[0] * x_val) / c[1] for x_val in x_vals]
            # y_vals = [-25, 25]
            ax.plot(x_vals, y_vals, 'r-', label='Fonction objectif')
        else:
            ax.axvline(pulp.value(prob.objective) / c[0], color='r', label='Fonction objectif')

        # Plot the optimal solution point
        if prob.status == 1:
            ax.plot(pulp.value(x), pulp.value(y), 'bo', label='Solution optimal')
            ax.annotate(f'({pulp.value(x):.2f}, {pulp.value(y):.2f})', (pulp.value(x), pulp.value(y)),
                        textcoords="offset points", xytext=(0, 10), ha='center')

            # Plot the parallel lines from the objective function to the optimal solution
            if c[1] != 0:
                slope = -c[0] / c[1]
                intercept = pulp.value(prob.objective) / c[1]
                y_vals_parallel = [slope * x_val + intercept for x_val in x_vals]
                ax.plot(x_vals, y_vals_parallel, 'g--', label='Ligne Parallelle')
            else:
                optimal_x = pulp.value(prob.objective) / c[0]
                ax.axvline(optimal_x, color='g', linestyle='--', label='Ligne Parallelle')

        else:
            ax.text(0.5, 0.6, 'Pas de solution optimale', ha='center', va='center', transform=ax.transAxes)

        # Set the axis labels
        ax.set_xlabel('x1')
        ax.set_ylabel('x2')

        # Set the title and legend
        ax.set_title('Region et Solution optimale')
        ax.legend()

        # Create a FigureCanvasTkAgg object to display the plot
        canvas = FigureCanvasTkAgg(fig, master=result_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=1)

        # Display the objective function equation and the optimal solution
        eq_str = f"{c[0]}x + {c[1]}y = {pulp.value(prob.objective)}"
        solution_str = f"Solution optimal: ({pulp.value(x):.2f}, {pulp.value(y):.2f})"
        Label(result_frame, text=eq_str).pack()
        Label(result_frame, text=solution_str).pack()


# Create the main window
root = Tk()
root.title("Programmation lineaire Resolution Graphique")

# Set the default style
style = Style()
style.theme_use('clam')

# Create the frames
input_frame = Frame(root)
input_frame.pack(side=LEFT, fill=Y)
result_frame = Frame(root)
result_frame.pack(side=RIGHT, fill=BOTH, expand=1)

# Create the input fields and labels
Label(input_frame, text="Objective:").grid(row=0, column=0)
obj_var = StringVar(value="max")
Radiobutton(input_frame, text="Maximize", variable=obj_var, value="max").grid(row=0, column=1)
Radiobutton(input_frame, text="Minimize", variable=obj_var, value="min").grid(row=0, column=2)
Label(input_frame, text="x1:").grid(row=1, column=0)
obj_x = Entry(input_frame)
obj_x.grid(row=1, column=1)
Label(input_frame, text="x2:").grid(row=1, column=2)
obj_y = Entry(input_frame)
obj_y.grid(row=1, column=3)

Label(input_frame, text="Subject to:").grid(row=2, column=0)

# Create a list to store the equation entry fields
equations_entries = []

# Button to add another equation entry
add_eq_button = Button(input_frame, text="Add Equation")

# Button to delete the last equation entry
del_eq_button = Button(input_frame, text="Supprimer Equation")

# Button to solve the problem
solve_button = Button(input_frame, text="Resoudre", command=solve)

clear_button = Button(input_frame, text="Tout effacer")


# Function to add another equation entry
def add_equation_entry():
    row = len(equations_entries) + 3

    x_label = Label(input_frame, text="x1:")
    x_label.grid(row=row, column=0)
    x_entry = Entry(input_frame)
    x_entry.grid(row=row, column=1)

    y_label = Label(input_frame, text="x2:")
    y_label.grid(row=row, column=2)
    y_entry = Entry(input_frame)
    y_entry.grid(row=row, column=3)

    sign_var = StringVar(value="<=")
    sign_label = OptionMenu(input_frame, sign_var, "<=", ">=")
    sign_label.grid(row=row, column=4)
    val_entry = Entry(input_frame)
    val_entry.grid(row=row, column=5)

    # equations_entries.append((x_entry, y_entry, val_entry, sign_var))
    equations_entries.append((x_label, x_entry, y_label, y_entry, sign_label, val_entry, sign_var))

    # Move the buttons to the bottom of the last equation entry
    add_eq_button.grid_forget()
    del_eq_button.grid_forget()
    solve_button.grid_forget()
    add_eq_button.grid(row=len(equations_entries) + 3, columnspan=6, pady=(10, 0))
    del_eq_button.grid(row=len(equations_entries) + 4, columnspan=6, pady=(10, 0))
    solve_button.grid(row=len(equations_entries) + 5, columnspan=6, pady=(10, 0))
    clear_button.grid(row=len(equations_entries) + 6, columnspan=6, pady=(10, 0))


# Function to delete the last equation entry

def del_equation_entry():
    if equations_entries:
        for widget in equations_entries[-1][:6]:
            widget.destroy()
        equations_entries.pop()

        # Move the buttons to the bottom of the last equation entry
        add_eq_button.grid_forget()
        del_eq_button.grid_forget()
        solve_button.grid_forget()
        clear_button.grid_forget()
        add_eq_button.grid(row=len(equations_entries) + 3, columnspan=6, pady=(10, 0))
        del_eq_button.grid(row=len(equations_entries) + 4, columnspan=6, pady=(10, 0))
        solve_button.grid(row=len(equations_entries) + 5, columnspan=6, pady=(10, 0))
        clear_button.grid(row=len(equations_entries) + 6, columnspan=6, pady=(10, 0))


def clear_all():
    # Clear the objective function entry fields
    obj_x.delete(0, END)
    obj_y.delete(0, END)

    # Clear the constraint entry fields
    for eq_entry in equations_entries:
        eq_entry[1].delete(0, END)
        eq_entry[3].delete(0, END)
        eq_entry[5].delete(0, END)

    # Clear the plot
    for widget in result_frame.winfo_children():
        widget.destroy()


# Set the command for the add_eq_button and del_eq_button after defining their respective functions
add_eq_button.configure(command=add_equation_entry)
del_eq_button.configure(command=del_equation_entry)
clear_button.configure(command=clear_all)

# Add initial equation entry
add_equation_entry()

# Position the buttons on the right side
add_eq_button.grid(row=len(equations_entries) + 3, columnspan=6, pady=(10, 0))
del_eq_button.grid(row=len(equations_entries) + 4, columnspan=6, pady=(10, 0))
solve_button.grid(row=len(equations_entries) + 5, columnspan=6, pady=(10, 0))
clear_button.grid(row=len(equations_entries) + 6, columnspan=6, pady=(10, 0))

root.mainloop()
