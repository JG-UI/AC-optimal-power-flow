import matplotlib.pyplot as plt
from pypower.api import runopf, ppoption
from pypower import case14

# Load IEEE 14-bus system data
case_data = case14.case14()

# Modify branch limits to 100 MW
case_data['branch'][:, 5] = 100  # Pmax
case_data['branch'][:, 6] = -100  # Pmin

# Modify bus voltage limits to [0.95, 1.05]
bus_vmax = 1.05
bus_vmin = 0.95
case_data['bus'][:, 11] = bus_vmax  # Vmax
case_data['bus'][:, 12] = bus_vmin  # Vmin

# Modify generator power limits with a minimum value of 20 MW
min_gen_power = 10
case_data['gen'][:, 9] = min_gen_power  # Pmin

# Modify generator power limits with a minimum value of -20 Mvar
min_gen_Qpower = -20
case_data['gen'][:, 4] = min_gen_Qpower  # Qmin

# Modify generator power cost coefficients 

coeff_gen = [[8e-02, 1.50000e+01],
       [2.50000e-01, 2.00000e+01],
       [5.00000e-02, 2.50000e+01],
       [3.00000e-02, 4.00000e+01],
       [1.00000e-02, 3.00000e+01]]
case_data['gencost'][:, 4:6] = coeff_gen 



# Set options for AC OPF
options = ppoption(PF_ALG=2, VERBOSE=0, OUT_ALL=0)

# Run AC OPF
results = runopf(case_data, options)

# Check if AC OPF converged successfully
if results['success']:
    print("AC OPF converged successfully!")
    print("Objective function value:", results['f'])
    print("Optimal generation:\n", results['gen'][:, [1, 2]])
    print("Optimal bus voltages:\n", results['bus'][:, [7, 8]])

    # Extract generator data
    gen_data = case_data['gen']
    gen_names = case_data['gen'][:, 0]

    # Extract normal state generator data
    gen_p_nominal = gen_data[:, 1]

    # Extract optimal generator data
    gen_p_optimal = results['gen'][:, 1]

    # Plot generator power compared to normal state
    plt.figure()
    plt.plot(gen_names, gen_p_nominal, 'bo-', label='Nominal')
    plt.plot(gen_names, gen_p_optimal, 'ro-', label='Optimal')
    plt.xlabel('Generator')
    plt.ylabel('Active Power (MW)')
    plt.title('Generator Power Comparison')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Extract bus voltage data
    bus_data = case_data['bus']
    bus_v_nominal = bus_data[:, 7]
    bus_v_optimal = results['bus'][:, 7]

    # Plot bus voltage magnitudes compared to normal state
    plt.figure()
    plt.plot(range(len(bus_data)), bus_v_nominal, 'bo-', label='Nominal')
    plt.plot(range(len(bus_data)), bus_v_optimal, 'ro-', label='Optimal')
    plt.xlabel('Bus')
    plt.ylabel('Voltage Magnitude (pu)')
    plt.title('Bus Voltage Magnitude Comparison')
    plt.legend()
    plt.grid(True)
    plt.show()

else:
    print("AC OPF did not converge!")
