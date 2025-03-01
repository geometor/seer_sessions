def code_execution(input_grid, output_grid, predicted_grid):
    """
    Executes code to compare the predicted output with the actual output.
    This will count the number of differences.
    """
    import numpy as np

    diff = predicted_grid - output_grid
    n_diff = np.sum(diff != 0)
    print(f'diffs: {n_diff}')

    # Calculate Intersection of Union (IOU)
    intersection = np.sum((output_grid > 0) & (predicted_grid > 0))
    union = np.sum((output_grid > 0) | (predicted_grid > 0))

    iou = intersection / union if union != 0 else 0.0
    print(f"IOU Score: {iou}")
    return

#Example Usage:
input_grid = np.array([[0,0,0],[0,1,0],[0,0,0]])
output_grid = np.array([[0,0,0],[0,1,0],[0,1,0]])
predicted_grid = np.array([[0,0,0],[0,1,0],[0,1,0]])

print("Example 1:")
code_execution(input_grid,output_grid,predicted_grid)


input_grid = np.array([[0,0,0,0],[0,3,0,0],[0,1,0,0],[0,0,0,0]])
output_grid = np.array([[0,0,0,0],[0,3,0,0],[0,1,0,0],[0,1,0,0]])
predicted_grid = np.array([[0,0,0,0],[0,3,0,0],[0,1,0,0],[0,1,0,0]])
print("\nExample 2:")
code_execution(input_grid,output_grid,predicted_grid)

input_grid = np.array([[0,0,0,0],[0,0,1,0],[0,0,0,0],[0,3,0,0]])
output_grid = np.array([[0,0,0,0],[0,0,1,0],[0,0,1,0],[0,3,0,0]])
predicted_grid = np.array([[0,0,0,0],[0,0,1,0],[0,0,1,0],[0,3,0,0]])

print("\nExample 3:")
code_execution(input_grid,output_grid,predicted_grid)