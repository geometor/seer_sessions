"""
1.  **Identify Gray Regions:** Find all contiguous regions of gray (5) pixels in the input grid.
2.  **Determine Relative Position**: Sort the regions by the x coordinate of their centroids.
3.  **Apply Color Changes:**
      * The first gray region from left is changed to magenta (6), by modifying 1, 2 or 3 pixels of the area closest to the grid center.
    *   The second gray region from the left, is changed to orange (7), modifying a block whose size can be 1x4 or 2x2 of pixels closest to the grid center.
    *   The next, third, gray region from the left is changed to azure (8), by modifying a block whose size can vary (3x3 or all pixels) of pixels closest to the grid center.
4.  **Leave other pixels unchanged.** White (0) and any remaining gray (5) pixels are kept as they are.
"""

import numpy as np

def find_contiguous_regions(grid, color):
    # Find contiguous regions (blobs) of a specific color.
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    def dfs(row, col, current_region):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        current_region.append((row, col))
        dfs(row + 1, col, current_region)
        dfs(row - 1, col, current_region)
        dfs(row, col + 1, current_region)
        dfs(row, col - 1, current_region)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_region = []
                dfs(row, col, current_region)
                regions.append(current_region)
    return regions

def calculate_centroid(region):
    # Calculate centroid.
    rows, cols = zip(*region)
    return sum(rows) / len(rows), sum(cols) / len(cols)

def distance(point1, point2):
     #Euclidean distance
    return np.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)

def transform(input_grid):
    # Initialize output grid.
    output_grid = np.copy(input_grid)
    grid_center = (input_grid.shape[0] / 2, input_grid.shape[1] / 2)

    # Find gray regions.
    gray_regions = find_contiguous_regions(input_grid, 5)

    # Calculate centroids and sort regions by x-coordinate of centroid.
    centroids = [calculate_centroid(region) for region in gray_regions]
    sorted_regions = [region for _, region in sorted(zip(centroids, gray_regions), key=lambda pair: pair[0][1])]

    # Apply color changes.
    for i, region in enumerate(sorted_regions):
        min_dist = float('inf')
        closest_pixels = []
        for pixel in region:
           dist = distance(pixel, grid_center)
           if dist < min_dist:
              min_dist = dist
              closest_pixels = [pixel]
           elif dist == min_dist:
              closest_pixels.append(pixel)
        
        if i == 0:  # Magenta (6)
            # Modify 1-3 closest pixels
            for pixel in closest_pixels[:3]: #check up to 3 pixels
                output_grid[pixel] = 6

        elif i == 1:  # Orange (7)
            target_pixels = []
            
            if (closest_pixels[0][0] + 1, closest_pixels[0][1]) in region:
               target_pixels.append((closest_pixels[0][0] + 1, closest_pixels[0][1]))
            if (closest_pixels[0][0], closest_pixels[0][1] + 1) in region:
               target_pixels.append((closest_pixels[0][0], closest_pixels[0][1] + 1))
            if (closest_pixels[0][0] + 1, closest_pixels[0][1] + 1) in region:
               target_pixels.append((closest_pixels[0][0] + 1, closest_pixels[0][1] + 1))

            target_pixels.append(closest_pixels[0])
            
            if len(target_pixels) >= 2:
                for pixel in target_pixels:
                    output_grid[pixel]=7


        elif i == 2:  # Azure (8)
            target_pixels = []
            if (closest_pixels[0][0] - 1, closest_pixels[0][1] -1) in region:
               target_pixels.append((closest_pixels[0][0] - 1, closest_pixels[0][1] - 1))
            if (closest_pixels[0][0] - 1, closest_pixels[0][1]) in region:
               target_pixels.append((closest_pixels[0][0] - 1, closest_pixels[0][1]))
            if (closest_pixels[0][0] - 1, closest_pixels[0][1] + 1) in region:
               target_pixels.append((closest_pixels[0][0] - 1, closest_pixels[0][1] + 1))
            if (closest_pixels[0][0], closest_pixels[0][1] - 1) in region:
               target_pixels.append((closest_pixels[0][0], closest_pixels[0][1] - 1))
            if (closest_pixels[0][0], closest_pixels[0][1] + 1) in region:
               target_pixels.append((closest_pixels[0][0], closest_pixels[0][1] + 1))
            if (closest_pixels[0][0] + 1, closest_pixels[0][1] - 1) in region:
               target_pixels.append((closest_pixels[0][0] + 1, closest_pixels[0][1] - 1))
            if (closest_pixels[0][0] + 1, closest_pixels[0][1]) in region:
               target_pixels.append((closest_pixels[0][0] + 1, closest_pixels[0][1]))
            if (closest_pixels[0][0] + 1, closest_pixels[0][1] + 1) in region:
               target_pixels.append((closest_pixels[0][0] + 1, closest_pixels[0][1] + 1))
               
            target_pixels.append(closest_pixels[0])
            
            if len(target_pixels) >=3:
                for pixel in target_pixels:
                    output_grid[pixel]=8
            else: # case where all pixels have to be changed
                for pixel in region:
                   output_grid[pixel] = 8

    return output_grid