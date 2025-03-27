import numpy as np
from collections import Counter

def transform(input_grid):
    """
    Transforms the input grid based on the following rules:
    1. The input grid (9x10) is conceptually divided into six regions by zero-value
       columns (index 3, 6) and a zero-value row (index 4).
       - Top-Left (TL): Rows 0-3, Cols 0-2
       - Top-Middle (TM): Rows 0-3, Cols 4-5
       - Top-Right (TR): Rows 0-3, Cols 7-9
       - Bottom-Left (BL): Rows 5-8, Cols 0-2
       - Bottom-Middle (BM): Rows 5-8, Cols 4-5
       - Bottom-Right (BR): Rows 5-8, Cols 7-9
    2. An output grid (4x5) is initialized with all zeros.
    3. For each of the six input regions, find the most frequent non-zero color.
    4. Place this most frequent color into the corresponding position in the
       output grid:
       - TL -> Output (1, 1)
       - TM -> Output (1, 2)
       - TR -> Output (1, 3)
       - BL -> Output (2, 1)
       - BM -> Output (2, 2)
       - BR -> Output (2, 3)
    5. If a region contains no non-zero colors, the corresponding output pixel
       remains zero.
    """

    # Convert input list of lists to a numpy array for easier slicing
    input_array = np.array(input_grid, dtype=int)

    # Initialize the output grid (4 rows, 5 columns) with zeros
    output_grid = np.zeros((4, 5), dtype=int)

    # Define the boundaries of the six input regions and their corresponding output coordinates
    # Format: (input_row_slice, input_col_slice, output_row, output_col)
    regions = [
        (slice(0, 4), slice(0, 3), 1, 1),  # Top-Left (TL)
        (slice(0, 4), slice(4, 6), 1, 2),  # Top-Middle (TM)
        (slice(0, 4), slice(7, 10), 1, 3), # Top-Right (TR)
        (slice(5, 9), slice(0, 3), 2, 1),  # Bottom-Left (BL)
        (slice(5, 9), slice(4, 6), 2, 2),  # Bottom-Middle (BM)
        (slice(5, 9), slice(7, 10), 2, 3)  # Bottom-Right (BR)
    ]

    # Process each region
    for r_slice, c_slice, out_r, out_c in regions:
        # Extract the pixels for the current region
        region_pixels = input_array[r_slice, c_slice]

        # Flatten the 2D region into a 1D list and filter out zeros
        non_zero_pixels = [pixel for pixel in region_pixels.flatten() if pixel != 0]

        # If there are non-zero pixels in the region
        if non_zero_pixels:
            # Count the frequency of each non-zero color
            color_counts = Counter(non_zero_pixels)

            # Find the color with the highest frequency
            # most_common(1) returns a list of tuples [(color, count)], we take the first one [0]
            # and then the color itself [0]
            most_frequent_color = color_counts.most_common(1)[0][0]

            # Place the most frequent color in the corresponding output grid cell
            output_grid[out_r, out_c] = most_frequent_color
        # If the region only contains zeros, the output cell remains 0 (already initialized)

    # Convert the numpy array back to a list of lists for the expected output format
    return output_grid.tolist()