def describe_grid(grid):
    rows, cols = grid.shape
    unique_colors = np.unique(grid)
    print(f"  Dimensions: {rows}x{cols}")
    print(f"  Unique colors: {unique_colors}")

print("Example 1:")
print("Input:")
describe_grid(example1_input)
print("Expected Output:")
describe_grid(example1_output)
print("Actual Output:")
describe_grid(actual_output1)
if np.array_equal(example1_output, actual_output1):
    print("  Result: Correct")
else:
    print("  Result: Incorrect")


print("\nExample 2:")
print("Input:")
describe_grid(example2_input)
print("Expected Output:")
describe_grid(example2_output)
print("Actual Output:")
describe_grid(actual_output2)
if np.array_equal(example2_output, actual_output2):
    print("  Result: Correct")
else:
    print("  Result: Incorrect")

print("\nExample 3:")
print("Input:")
describe_grid(example3_input)
print("Expected Output:")
describe_grid(example3_output)
print("Actual Output:")
describe_grid(actual_output3)
if np.array_equal(example3_output, actual_output3):
    print("  Result: Correct")
else:
    print("  Result: Incorrect")