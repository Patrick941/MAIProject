import sys
sys.path.append('/home/patrick/Documents/MAIProject/projectVenv/lib/python3.10/site-packages/pydex')
from pydex.core.designer import Designer
import numpy as np

# Step 2: Specifying the Model
def simulate(ti_controls, model_parameters):
    return np.array([
        model_parameters[0] +
        model_parameters[1] * ti_controls[0] +
        model_parameters[2] * ti_controls[1]
    ])

# Step 3: Create a Designer, Pass in the Model
designer_1 = Designer()
designer_1.simulate = simulate

# Step 4: Specify Nominal Model Parameter Values
designer_1.model_parameters = np.ones(3)

# Step 5: Specify Experimental Candidates
tic = designer_1.enumerate_candidates(
    bounds=[
        [-1, 1],
        [-1, 1],
    ],
    levels=[
        5,
        5,
    ],
)
designer_1.ti_controls_candidates = tic

# Step 6: Initialize the Designer
designer_1.initialize(verbose=2)

# Step 7: Design the Optimal Experiment
result = designer_1.design_experiment(
    criterion=designer_1.d_opt_criterion,
    write=False,
    package="scipy",
    optimizer="SLSQP",
)

# Step 8: Visualize the Results
designer_1.print_optimal_candidates()
designer_1.plot_optimal_controls(non_opt_candidates=True)
designer_1.show_plots()