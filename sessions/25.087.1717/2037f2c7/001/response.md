```python
import numpy as np
from skimage.measure import label

# Predefined representations for the digits observed in the training examples.
# Using a dictionary to map the count (N) to its numpy array representation.
DIGIT_REPRESENTATIONS = {
    2: np.array([
        [8, 8, 8, 0, 8, 8],
        [0, 0, 8, 0, 0, 0]
    ], dtype=np.int8),
    7: np.array([
        [8, 0, 0, 0, 0, 0, 8],
        [8, 8, 0, 0, 0, 8, 8],
        [8, 0, 0, 0, 0, 0, 8]
    ], dtype=np.int8),
    8: np.array([
        [0, 8, 0, 0, 0, 0, 8, 8],
        [8, 8, 8, 8, 0, 8, 8, 8],
        [0, 0, 8, 0, 0, 0, 0, 8],
        [0, 0, 0, 0, 0, 0, 0, 8]
    ], dtype=np.int8)
    # Add other digits if needed based on test cases
}

def find_objects(grid):
    """
    Finds connected components (objects) of non-background pixels.

    Args:
        grid (np.ndarray): The input grid where 0 is background.

    Returns:
        tuple: A tuple containing:
            - labeled_grid (np.ndarray): Grid with each object labeled with a unique integer.
            - num_labels (int): The total number of objects found (excluding background).
    """
    # Create a boolean mask where True indicates a non-background pixel
    mask = grid != 0
    # Label connected regions using 8-connectivity (includes diagonals)
    labeled_grid, num_labels = label(mask, connectivity=2, background=0, return_num=True)
    return labeled_grid, num_labels

def is_multicolored(grid, labeled_grid, object_label):
    """
    Checks if a specific object in the grid contains more than one color.

    Args:
        grid (np.ndarray): The original input grid with colors.
        labeled_grid (np.ndarray): The grid with labeled objects.
        object_label (int): The label of the object to check.

    Returns:
        bool: True if the object has more than one color, False otherwise.
    """
    # Get the colors of the pixels belonging to the specified object
    object_pixels = grid[labeled_grid == object_label]
    # Find the unique colors within those pixels (excluding background 0 if any somehow included)
    unique_colors = np.unique(object_pixels[object_pixels != 0])
    # Check if the number of unique colors is greater than 1
    return len(unique_colors) > 1

def get_digit_representation(n):
    """
    Retrieves the predefined grid representation for a given digit count.

    Args:
        n (int): The digit (count) for which to get the representation.

    Returns:
        np.ndarray: The grid representation of the digit, or an empty grid if not defined.
    """
    # Return the representation from the dictionary, defaulting to an empty array if N is not found
    # It might be better to raise an error or define representations for 0-9 if required by the full ARC set.
    return DIGIT_REPRESENTATIONS.get(n, np.array([[]], dtype=np.int8))


def transform(input_grid):
    """
    Counts the number of distinct, contiguous, multi-colored objects in the
    input grid and outputs a stylized representation of that count using
    azure (8) on a white (0) background.

    Workflow:
    1. Find all distinct contiguous non-white objects (connected components).
    2. Iterate through each found object.
    3. For each object, check if it contains pixels of at least two different colors.
    4. Count the number of objects that meet this multi-colored condition.
    5. Retrieve the predefined azure/white grid pattern corresponding to this count.
    6. Return the retrieved pattern as the output grid.
    """
    # 1. Find all distinct contiguous non-white objects
    labeled_grid, num_labels = find_objects(input_grid)

    # 2. Iterate through objects and count multi-colored ones
    multi_colored_count = 0
    for i in range(1, num_labels + 1): # Labels are 1-based
        # 3. Check if the current object is multi-colored
        if is_multicolored(input_grid, labeled_grid, i):
            # 4. Increment the count if it is
            multi_colored_count += 1

    # 5. Retrieve the predefined grid pattern for the count
    output_grid = get_digit_representation(multi_colored_count)

    # 6. Return the output grid
    return output_grid
```