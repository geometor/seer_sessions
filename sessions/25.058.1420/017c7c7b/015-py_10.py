def grid_report(grid, label):
    print(f"{label}:")
    print(f"  Shape: {grid.shape}")
    unique, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique, counts))
    print(f"  Colors: {color_counts}")  # Show counts of each color

#Example usage:
#Assuming input_grid, expected_output, and actual_output are available for each training example

#example 1:
input_grid = np.array([[0,0,0],[0,1,0],[0,0,0]])
expected_output = np.array([[0,0,0],[0,2,0],[0,0,0],[0,2,0],[0,0,0]])
actual_output = transform(input_grid)
print("Example 1")
grid_report(input_grid,"input")
grid_report(expected_output, "Expected Output")
grid_report(actual_output, "Actual Output")

#example 2:
input_grid = np.array([[0,0,0,0,0],[0,1,0,0,0],[0,0,0,0,0],[0,0,0,1,0],[0,0,0,0,0]])
expected_output = np.array([[0,0,0,0,0],[0,2,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,2,0],[0,0,0,0,0]])
actual_output = transform(input_grid)
print("\nExample 2")
grid_report(input_grid,"input")
grid_report(expected_output, "Expected Output")
grid_report(actual_output, "Actual Output")

#example 3:
input_grid = np.array([[0,0,0,0,0,0,0],[0,1,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,1,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,1,0],[0,0,0,0,0,0,0]])
expected_output = np.array([[0,0,0,0,0,0,0],[0,2,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,2,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,2,0],[0,0,0,0,0,0,0]])
actual_output = transform(input_grid)
print("\nExample 3")
grid_report(input_grid,"input")
grid_report(expected_output, "Expected Output")
grid_report(actual_output, "Actual Output")
