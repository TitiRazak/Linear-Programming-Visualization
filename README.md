# Linear Programming Visualization

This project is a graphical interface for solving linear programming problems with two variables. It allows users to input an objective function and multiple constraints, and then visualize the feasible region and the optimal solution.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Dependencies](#dependencies)
- [How to Run](#how-to-run)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

Linear programming is a mathematical optimization technique used to find the best outcome in a mathematical model with linear relationships. It is often used in various fields, including economics, engineering, and operations research. This project provides a user-friendly interface for solving linear programming problems using the PuLP library and visualizing the results.

## Features

- Define the objective as either maximizing or minimizing.
- Input the coefficients and constraints for a linear programming problem.
- Visualize the feasible region and the optimal solution.
- Dynamically add or remove constraints for interactive problem setup.

## Dependencies

The project relies on the following dependencies:

- Python 3.x
- Tkinter for the graphical user interface
- PuLP for solving linear programming problems
- Matplotlib for creating the visualization
- NumPy for numerical operations

You can install these dependencies using Python's package manager, pip:

```bash
pip install pulp matplotlib numpy
```

## How to Run

To run the Linear Programming Visualization project, follow these steps:

1. Clone or download the project repository from [GitHub](https://github.com/yourusername/linear-programming-visualization).

2. Navigate to the project directory:

```bash
cd linear-programming-visualization
```

3. Run the main Python script:

```bash
python linear_programming_visualization.py
```

This will launch the graphical interface where you can define your linear programming problem and visualize the results.

## Usage

1. **Objective Function**: Select whether you want to maximize or minimize your objective function. Enter the coefficients for `x` and `y`.

2. **Constraints**: Define your constraints by clicking the "Add Equation" button to add new entries. Each constraint includes coefficients for `x` and `y`, a relational operator (`<=` or `>=`), and a value. You can add or remove constraints as needed.

3. **Solve**: Click the "Resoudre" button to solve the linear programming problem and visualize the feasible region and optimal solution.

4. **Clear**: To start over, you can click the "Tout effacer" button to clear all input fields and results.

## Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the project on GitHub.

2. Clone your forked repository to your local machine:

```bash
git clone https://github.com/yourusername/linear-programming-visualization.git
```

3. Create a new branch for your feature or bug fix:

```bash
git checkout -b feature-name
```

4. Make your changes, commit them, and push to your repository:

```bash
git add .
git commit -m "Add feature-name"
git push origin feature-name
```

5. Create a pull request from your forked repository to the original repository on GitHub.

Your contribution will be reviewed, and if approved, it will be merged into the project.

## License

This project is licensed under the [MIT License](LICENSE). You are free to use and modify the code for your own purposes.
