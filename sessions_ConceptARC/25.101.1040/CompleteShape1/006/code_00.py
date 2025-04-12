import numpy as np

# --- Example 1 Data ---
input_1_np = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 2, 0, 0, 2, 1, 1, 0], [0, 1, 1, 2, 0, 0, 2, 1, 1, 0],
    [0, 2, 2, 0, 0, 0, 0, 2, 2, 0], [0, 1, 1, 0, 0, 0, 0, 1, 1, 0],
    [0, 1, 1, 0, 0, 0, 0, 1, 1, 0], [0, 2, 2, 0, 0, 0, 0, 2, 2, 0],
    [0, 1, 1, 2, 1, 1, 2, 1, 1, 0], [0, 1, 1, 2, 1, 1, 2, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])
expected_1_np = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 2, 1, 1, 2, 1, 1, 0], [0, 1, 1, 2, 1, 1, 2, 1, 1, 0], # Target filled with 1
    [0, 2, 2, 0, 0, 0, 0, 2, 2, 0], [0, 1, 1, 0, 0, 0, 0, 1, 1, 0],
    [0, 1, 1, 0, 0, 0, 0, 1, 1, 0], [0, 2, 2, 0, 0, 0, 0, 2, 2, 0],
    [0, 1, 1, 2, 1, 1, 2, 1, 1, 0], [0, 1, 1, 2, 1, 1, 2, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])
# Simulate the CORRECT output based on the code's logic
simulated_actual_1_np = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 2, 1, 1, 2, 1, 1, 0], [0, 1, 1, 2, 1, 1, 2, 1, 1, 0], # Target [2:4, 4:6] filled by V-rule
    [0, 2, 2, 0, 0, 0, 0, 2, 2, 0], [0, 1, 1, 0, 0, 0, 0, 1, 1, 0], # Large rect [4:8, 3:7] skipped by size constraint
    [0, 1, 1, 0, 0, 0, 0, 1, 1, 0], [0, 2, 2, 0, 0, 0, 0, 2, 2, 0],
    [0, 1, 1, 2, 1, 1, 2, 1, 1, 0], [0, 1, 1, 2, 1, 1, 2, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])


# --- Example 2 Data ---
input_2_np = np.array([
    [0, 2, 6, 6, 6, 6, 2, 0], [0, 6, 0, 0, 0, 0, 6, 0],
    [0, 6, 0, 0, 0, 0, 6, 0], [0, 6, 0, 0, 0, 0, 6, 0],
    [0, 6, 0, 0, 0, 0, 6, 0], [0, 2, 6, 6, 0, 0, 2, 0]
])
expected_2_np = np.array([
    [0, 2, 6, 6, 6, 6, 2, 0], [0, 6, 0, 0, 0, 0, 6, 0],
    [0, 6, 0, 0, 0, 0, 6, 0], [0, 6, 0, 0, 0, 0, 6, 0],
    [0, 6, 0, 0, 0, 0, 6, 0], [0, 2, 6, 6, 6, 6, 2, 0] # Target filled with 6
])
# Simulate the CORRECT output based on the code's logic
simulated_actual_2_np = np.array([
    [0, 2, 6, 6, 6, 6, 2, 0], [0, 6, 0, 0, 0, 0, 6, 0], # Large rect [1:5, 2:6] skipped by size constraint
    [0, 6, 0, 0, 0, 0, 6, 0], [0, 6, 0, 0, 0, 0, 6, 0],
    [0, 6, 0, 0, 0, 0, 6, 0], [0, 2, 6, 6, 6, 6, 2, 0]  # Target [5, 4:6] filled by H-Left rule
])

# --- Analysis Function ---
def analyze_diff(expected, actual, name):
    diff = expected != actual
    coords = np.argwhere(diff)
    print(f"\n--- {name} Analysis (Simulated Correct Execution) ---")
    print(f"Total pixel differences: {np.sum(diff)}")
    if np.sum(diff) > 0:
        print("Incorrect pixels (row, col): expected -> actual")
        for r, c in coords:
            print(f"  ({r}, {c}): {expected[r, c]} -> {actual[r, c]}")

# --- Run Analysis ---
analyze_diff(expected_1_np, simulated_actual_1_np, "Example 1")
analyze_diff(expected_2_np, simulated_actual_2_np, "Example 2")

print(f"\nExample 1 Match (Simulated): {np.array_equal(expected_1_np, simulated_actual_1_np)}")
print(f"Example 2 Match (Simulated): {np.array_equal(expected_2_np, simulated_actual_2_np)}")