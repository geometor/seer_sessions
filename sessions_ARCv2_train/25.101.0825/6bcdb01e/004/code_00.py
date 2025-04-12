import numpy as np

def analyze_grid(name, grid):
    a = np.array(grid, dtype=int)
    dims = a.shape
    colors, counts = np.unique(a, return_counts=True)
    color_counts = dict(zip(colors, counts))
    print(f"{name}:")
    print(f"  Dimensions: {dims[0]}x{dims[1]}")
    print(f"  Color Counts: {color_counts}")
    # color map: 0:white, 1:blue, 2:red, 3:green, 4:yellow, 5:gray, 6:magenta, 7:orange, 8:azure, 9:maroon
    print(f"    Orange(7): {color_counts.get(7, 0)}")
    print(f"    Azure(8): {color_counts.get(8, 0)}")
    print(f"    Green(3): {color_counts.get(3, 0)}")

# Example 1 Data
train1_in = [
    [8, 7, 7, 8, 7, 8, 7], [7, 8, 8, 7, 7, 7, 8], [7, 7, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 8], [7, 7, 7, 7, 7, 8, 7], [3, 3, 7, 7, 8, 7, 7],
    [7, 7, 7, 8, 7, 7, 7]
]
train1_out_expected = [
    [8, 7, 7, 8, 7, 8, 7], [7, 8, 8, 3, 3, 3, 8], [7, 7, 7, 3, 7, 3, 7],
    [3, 3, 3, 3, 3, 3, 8], [7, 7, 7, 3, 7, 8, 7], [3, 3, 3, 3, 8, 7, 7],
    [7, 7, 7, 8, 7, 7, 7]
]
# Output from the previously failed code (8-way flood fill)
train1_out_code = [
    [8, 3, 3, 8, 3, 8, 3], [3, 8, 8, 3, 3, 3, 8], [3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 8], [3, 3, 3, 3, 3, 8, 3], [3, 3, 3, 3, 8, 3, 3],
    [3, 3, 3, 8, 3, 3, 3]
]


# Example 2 Data
train2_in = [
    [7, 8, 7, 8, 7], [8, 7, 7, 7, 8], [7, 7, 7, 7, 7],
    [7, 3, 7, 7, 8], [7, 3, 7, 8, 7]
]
train2_out_expected = [
    [7, 8, 7, 8, 7], [8, 3, 3, 3, 8], [7, 3, 7, 3, 7],
    [3, 3, 3, 3, 8], [7, 3, 7, 8, 7]
]
# Output from the previously failed code (8-way flood fill)
train2_out_code = [
    [3, 8, 3, 8, 3], [8, 3, 3, 3, 8], [3, 3, 3, 3, 3],
    [3, 3, 3, 3, 8], [3, 3, 3, 8, 3]
]


analyze_grid("Train 1 Input", train1_in)
analyze_grid("Train 1 Expected Output", train1_out_expected)
analyze_grid("Train 1 Code Output (Incorrect)", train1_out_code)

analyze_grid("Train 2 Input", train2_in)
analyze_grid("Train 2 Expected Output", train2_out_expected)
analyze_grid("Train 2 Code Output (Incorrect)", train2_out_code)

# Calculate changes for Expected Output
t1_in_arr = np.array(train1_in)
t1_out_exp_arr = np.array(train1_out_expected)
t1_changed_exp = np.sum(t1_in_arr != t1_out_exp_arr)
t1_o2g_exp = np.sum((t1_in_arr == 7) & (t1_out_exp_arr == 3))
print(f"\nTrain 1 Changes (Input -> Expected Output):")
print(f"  Total pixels changed: {t1_changed_exp}")
print(f"  Orange(7) changed to Green(3): {t1_o2g_exp}")

t2_in_arr = np.array(train2_in)
t2_out_exp_arr = np.array(train2_out_expected)
t2_changed_exp = np.sum(t2_in_arr != t2_out_exp_arr)
t2_o2g_exp = np.sum((t2_in_arr == 7) & (t2_out_exp_arr == 3))
print(f"\nTrain 2 Changes (Input -> Expected Output):")
print(f"  Total pixels changed: {t2_changed_exp}")
print(f"  Orange(7) changed to Green(3): {t2_o2g_exp}")

# Calculate changes for Code Output
t1_out_code_arr = np.array(train1_out_code)
t1_changed_code = np.sum(t1_in_arr != t1_out_code_arr)
t1_o2g_code = np.sum((t1_in_arr == 7) & (t1_out_code_arr == 3))
print(f"\nTrain 1 Changes (Input -> Code Output):")
print(f"  Total pixels changed: {t1_changed_code}")
print(f"  Orange(7) changed to Green(3): {t1_o2g_code}")

t2_out_code_arr = np.array(train2_out_code)
t2_changed_code = np.sum(t2_in_arr != t2_out_code_arr)
t2_o2g_code = np.sum((t2_in_arr == 7) & (t2_out_code_arr == 3))
print(f"\nTrain 2 Changes (Input -> Code Output):")
print(f"  Total pixels changed: {t2_changed_code}")
print(f"  Orange(7) changed to Green(3): {t2_o2g_code}")

# Compare Code vs Expected
t1_diff = np.sum(t1_out_exp_arr != t1_out_code_arr)
t2_diff = np.sum(t2_out_exp_arr != t2_out_code_arr)
print(f"\nComparison (Code vs Expected):")
print(f"  Train 1 Pixels Different: {t1_diff}")
print(f"  Train 2 Pixels Different: {t2_diff}")