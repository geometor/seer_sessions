import numpy as np
from scipy.spatial.distance import cdist

def describe_grid(grid, name):
    print(f"{name} Grid:")
    print(f"  Shape: {grid.shape}")
    #find location of green and white pixels
    green_coords = [(i, j) for i, row in enumerate(grid) for j, val in enumerate(row) if val == 3]
    white_coords = [(i, j) for i, row in enumerate(grid) for j, val in enumerate(row) if val == 0]
    print(f"    Green Pixels: {green_coords}")
    print(f"    White Pixels: {white_coords}")

    # Calculate distances between green and white pixels
    if green_coords and white_coords:
        distances = cdist(np.array(green_coords), np.array(white_coords), 'cityblock')
        print(f"    Distances between Green and White Pixels (Manhattan):\n{distances}")
        min_distances = np.min(distances, axis=1)
        print(f"    Minimum distance from each Green pixel to a White pixel:\n {min_distances}")
        avg_min_distance = np.mean(min_distances)
        print(f"  Average minimum distance: {avg_min_distance:.2f}")

# Accessing the examples directly
for i, example in enumerate(task_data['train']):
    print(f"\nExample {i + 1}:")
    describe_grid(np.array(example['input']), "Input")
    describe_grid(np.array(example['output']), "Output")
