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
# Output from previous code run (as reported)
actual_1_np = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 2, 1, 1, 2, 1, 1, 0], [0, 1, 1, 2, 1, 1, 2, 1, 1, 0], # Target filled with 1 (correct part)
    [0, 2, 2, 2, 1, 1, 2, 2, 2, 0], [0, 1, 1, 2, 1, 1, 2, 1, 1, 0], # Large rect filled (incorrect part)
    [0, 1, 1, 2, 1, 1, 2, 1, 1, 0], [0, 2, 2, 2, 1, 1, 2, 2, 2, 0], # Large rect filled (incorrect part)
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
# Output from previous code run (as reported)
actual_2_np = np.array([
    [0, 2, 6, 6, 6, 6, 2, 0], [0, 6, 6, 6, 6, 6, 6, 0], # Large rect filled (incorrect)
    [0, 6, 6, 6, 6, 6, 6, 0], [0, 6, 6, 6, 6, 6, 6, 0],
    [0, 6, 6, 6, 6, 6, 6, 0], [0, 2, 6, 6, 0, 0, 2, 0]  # Target NOT filled (incorrect)
])

# --- Analysis Function ---
def analyze_diff(expected, actual, name):
    diff = expected != actual
    coords = np.argwhere(diff)
    print(f"\n--- {name} Analysis ---")
    print(f"Total pixel differences: {np.sum(diff)}")
    if np.sum(diff) > 0:
        print("Incorrect pixels (row, col): expected -> actual")
        for r, c in coords:
            print(f"  ({r}, {c}): {expected[r, c]} -> {actual[r, c]}")

# --- Run Analysis ---
analyze_diff(expected_1_np, actual_1_np, "Example 1")
analyze_diff(expected_2_np, actual_2_np, "Example 2")

# --- Identify Specific Error Types ---
# Error Type 1: White pixels that should have stayed white but were filled
errors_1_filled_wrong = np.argwhere((input_1_np == 0) & (expected_1_np == 0) & (actual_1_np != 0))
print(f"\nExample 1: Pixels incorrectly filled (should be white): {len(errors_1_filled_wrong)}")
# Error Type 2: White pixels that should have been filled but were not
errors_1_not_filled = np.argwhere((input_1_np == 0) & (expected_1_np != 0) & (actual_1_np == 0))
print(f"Example 1: Pixels not filled (should be non-white): {len(errors_1_not_filled)}")
# Error Type 3: White pixels filled with the wrong color
errors_1_wrong_color = np.argwhere((input_1_np == 0) & (expected_1_np != 0) & (actual_1_np != 0) & (expected_1_np != actual_1_np))
print(f"Example 1: Pixels filled with wrong color: {len(errors_1_wrong_color)}")


errors_2_filled_wrong = np.argwhere((input_2_np == 0) & (expected_2_np == 0) & (actual_2_np != 0))
print(f"\nExample 2: Pixels incorrectly filled (should be white): {len(errors_2_filled_wrong)}")
errors_2_not_filled = np.argwhere((input_2_np == 0) & (expected_2_np != 0) & (actual_2_np == 0))
print(f"Example 2: Pixels not filled (should be non-white): {len(errors_2_not_filled)}")
for r,c in errors_2_not_filled: print(f"  ({r},{c}) expected={expected_2_np[r,c]}, actual=0")
errors_2_wrong_color = np.argwhere((input_2_np == 0) & (expected_2_np != 0) & (actual_2_np != 0) & (expected_2_np != actual_2_np))
print(f"Example 2: Pixels filled with wrong color: {len(errors_2_wrong_color)}")
