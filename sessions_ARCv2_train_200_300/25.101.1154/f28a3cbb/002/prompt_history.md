
## train_1

**input:**
```
9 9 9 6 6 6 6 9 4
9 9 9 6 6 6 4 4 6
9 9 9 6 6 9 6 6 6
6 6 6 6 6 6 6 6 6
6 6 9 6 6 6 6 6 6
6 9 6 6 6 6 6 6 6
9 6 6 6 6 6 4 4 4
6 6 4 6 6 6 4 4 4
6 6 6 4 6 6 4 4 4
```


**output:**
```
9 9 9 9 6 6 6 6 6
9 9 9 6 6 6 6 6 6
9 9 9 9 6 6 6 6 6
9 9 9 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 4 4 4
6 6 6 6 6 6 4 4 4
6 6 6 6 6 4 4 4 4
6 6 6 6 6 4 4 4 4
```


## train_2

**input:**
```
2 2 2 6 6 6 6 6 2
2 2 2 6 6 6 6 6 2
2 2 2 6 6 6 6 6 6
6 6 6 6 2 6 6 6 6
6 2 6 6 6 6 6 5 6
6 6 6 6 5 6 6 6 6
6 6 6 6 6 6 5 5 5
5 6 6 6 6 6 5 5 5
6 6 2 6 6 6 5 5 5
```


**output:**
```
2 2 2 2 6 6 6 6 6
2 2 2 2 6 6 6 6 6
2 2 2 2 6 6 6 6 6
6 2 2 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 5 6
6 6 6 6 6 5 5 5 5
6 6 6 6 6 5 5 5 5
6 6 6 6 6 6 5 5 5
```

## Perception

The task involves processing a 9x9 grid containing a background color and several other colors. Some non-background colors form solid 3x3 blocks, while others appear as scattered individual pixels ("noise"). The transformation aims to clean up the noise and slightly expand the solid blocks based on the location of the noise.

Key observations:
1.  **Background:** There is a dominant background color (magenta/6 in both examples).
2.  **Solid Blocks:** There are distinct 3x3 areas completely filled with a single non-background color (Maroon/9 and Yellow/4 in train_1; Red/2 and Gray/5 in train_2). These blocks are preserved in the output.
3.  **Noise Pixels:** There are scattered pixels of the same colors as the blocks, but not part of the blocks. These noise pixels are removed in the output (replaced by the background color).
4.  **Block Expansion:** Some background pixels immediately adjacent (orthogonally) to the solid blocks change color to match the block. This change only occurs if the background pixel is also adjacent (orthogonally or diagonally) to a noise pixel of the same color as the block.

## Facts


```yaml
GridProperties:
  - size: [9, 9]
  - background_color: Determined as the most frequent color in the input grid (magenta/6).

Objects:
  - type: SolidBlock
    properties:
      - shape: 3x3 square
      - composition: Monochromatic (single non-background color)
      - location: Various (e.g., top-left, bottom-right)
    actions:
      - identify
      - preserve_in_output
  - type: NoisePixel
    properties:
      - shape: 1x1 pixel
      - color: Non-background color, matches a SolidBlock color
      - location: Scattered, not part of a SolidBlock
    actions:
      - identify
      - remove_from_output (replace with background_color)
  - type: BackgroundPixel
    properties:
      - color: background_color
    actions:
      - identify
      - potentially_change_color

Relationships_And_Actions:
  - relationship: Adjacency (Orthogonal)
    applies_to: [BackgroundPixel, SolidBlock]
  - relationship: Adjacency (OrthogonalOrDiagonal)
    applies_to: [BackgroundPixel, NoisePixel]
  - action: ConditionalColorChange
    trigger: A BackgroundPixel `n` changes to color `c` if:
      1. `input[n]` is background_color.
      2. `n` is orthogonally adjacent to a SolidBlock `b` of color `c`.
      3. `n` is orthogonally or diagonally adjacent to a NoisePixel `p` of color `c`.
    target: BackgroundPixel `n`
    result: `output[n]` becomes color `c`.
  - action: Initialization
    target: OutputGrid
    result: Filled with background_color.
  - action: Finalization
    trigger: After processing all conditional changes.
    result: OutputGrid contains preserved SolidBlocks and changed BackgroundPixels. All other pixels (original NoisePixels and unchanged BackgroundPixels) have the background_color.

```


## Natural Language Program

1.  **Identify Background:** Find the color that appears most frequently in the input grid and designate it as the background color.
2.  **Identify Objects:**
    a.  Scan the input grid to locate all solid 3x3 blocks composed of a single non-background color. Record their color and coordinates.
    b.  Identify all other non-background pixels in the input grid that are not part of these 3x3 blocks. These are the "noise pixels". Record their color and coordinates.
3.  **Initialize Output:** Create a new grid of the same dimensions as the input, filled entirely with the background color.
4.  **Preserve Blocks:** Copy the identified 3x3 solid blocks from the input grid onto the output grid at their corresponding locations.
5.  **Determine Expansion:** Create a list to store coordinates of background cells that should change color. Iterate through each identified solid 3x3 block `b` with color `c`:
    a.  For each cell `n` that is orthogonally adjacent to block `b`:
        i.  Check if the cell `n` contained the background color in the *original input grid*.
        ii. Check if the cell `n` is adjacent (using 8-way adjacency, including diagonals) to any *noise pixel* `p` that has the same color `c` as the block `b`.
        iii. If both conditions (i and ii) are true, add the coordinates of cell `n` and the color `c` to the list of changes.
6.  **Apply Expansion:** Iterate through the list of changes. For each coordinate and color pair `(n, c)` in the list, set the color of cell `n` in the output grid to `c`.
7.  **Finalize:** The resulting output grid, containing the preserved blocks and the expanded areas (changed background cells), is the final output. Noise pixels are implicitly removed because they were not copied from the input, and the output grid was initialized with the background color.
```python
import numpy as np
from collections import Counter

"""
Transforms an input grid based on identifying 3x3 solid blocks and surrounding noise pixels.
The core logic involves:
1. Identifying the background color (most frequent).
2. Locating solid 3x3 blocks of non-background colors.
3. Identifying 'noise' pixels (non-background pixels not part of solid blocks).
4. Initializing an output grid with the background color.
5. Copying the solid 3x3 blocks to the output.
6. Expanding the blocks by changing adjacent background pixels according to a specific rule:
   A background pixel 'n' changes to the block's color 'c' if 'n' was originally background,
   is orthogonally adjacent to the block, and is also orthogonally or diagonally adjacent
   to at least one 'noise' pixel of the same color 'c'.
"""

# Helper function to find the most frequent element (background color)
def find_background_color(grid: np.ndarray) -> int:
    """Finds the most frequent color in the grid."""
    counts = Counter(grid.flatten())
    # If grid is empty or has uniform color, handle appropriately
    if not counts:
        # Return a default color (e.g., 0) or raise error if grid shouldn't be empty
        return 0
    # Return the color with the highest count
    return counts.most_common(1)[0][0]

# Helper function to find coordinates of neighbors
def get_neighbor_coords(r: int, c: int, H: int, W: int, include_diagonal: bool) -> set[tuple[int, int]]:
    """Gets valid neighbor coordinates for a cell (r, c) within grid bounds (H, W)."""
    neighbors = set()
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            # Skip self
            if dr == 0 and dc == 0:
                continue
            # Skip diagonal if not included
            if not include_diagonal and abs(dr) + abs(dc) != 1:
                continue
            nr, nc = r + dr, c + dc
            # Check bounds
            if 0 <= nr < H and 0 <= nc < W:
                neighbors.add((nr, nc))
    return neighbors

# Helper function to find solid 3x3 blocks
def find_solid_blocks(grid: np.ndarray, background_color: int) -> tuple[list[tuple[int, set[tuple[int, int]]]], set[tuple[int, int]]]:
    """
    Finds all solid 3x3 blocks of a single non-background color.

    Returns:
        A tuple containing:
        - list_of_blocks: A list of tuples, where each inner tuple is (block_color, block_coords_set).
        - all_block_coords: A set containing coordinates of all pixels belonging to any found solid block.
    """
    H, W = grid.shape
    list_of_blocks = []
    all_block_coords = set()
    # Keep track of pixels already assigned to a block to prevent overlap issues or redundant checks
    visited_block_pixels = set()

    for r in range(H - 2):
        for c in range(W - 2):
            # If this cell is already part of a found block, skip
            if (r, c) in visited_block_pixels:
                continue

            color = grid[r, c]
            # Blocks cannot be background color
            if color == background_color:
                continue

            # Check if it's the top-left of a 3x3 block of the same color
            is_solid_block = True
            current_block_coords = set()
            for i in range(3):
                for j in range(3):
                    coord = (r + i, c + j)
                    # Check color and if this pixel is already part of another block
                    # Check grid bounds implicitly via loop range and coord generation
                    if grid[r + i, c + j] != color or coord in visited_block_pixels:
                        is_solid_block = False
                        break
                    current_block_coords.add(coord)
                if not is_solid_block:
                    break

            if is_solid_block:
                list_of_blocks.append((color, current_block_coords))
                all_block_coords.update(current_block_coords)
                visited_block_pixels.update(current_block_coords) # Mark pixels as used

    return list_of_blocks, all_block_coords

# Main transformation function
def transform(input_grid: list[list[int]]) -> list[list[int]]:
    input_np = np.array(input_grid, dtype=int)
    H, W = input_np.shape
    if H == 0 or W == 0: # Handle empty input case
        return []

    # Step 1: Identify Background Color
    background_color = find_background_color(input_np)

    # Step 2: Identify Solid 3x3 Blocks
    # solid_blocks_list contains tuples: (block_color, set_of_block_coordinates)
    # all_block_coords is a set containing all coordinates occupied by any solid block
    solid_blocks_list, all_block_coords = find_solid_blocks(input_np, background_color)

    # Step 3: Identify Noise Pixels
    # noise_pixels_by_color is a dictionary: {color: set_of_noise_coordinates}
    noise_pixels_by_color = {}
    for r in range(H):
        for c in range(W):
            coord = (r, c)
            color = input_np[r, c]
            # Noise is non-background and not part of any solid block
            if color != background_color and coord not in all_block_coords:
                if color not in noise_pixels_by_color:
                    noise_pixels_by_color[color] = set()
                noise_pixels_by_color[color].add(coord)

    # Step 4: Initialize Output Grid with the background color
    output_np = np.full_like(input_np, background_color)

    # Step 5: Preserve Solid Blocks by copying them to the output grid
    for color, block_coords in solid_blocks_list:
        for r, c in block_coords:
            output_np[r, c] = color # Assume block coords are valid within bounds

    # Step 6: Determine and Apply Expansion based on the rules
    # Store updates in a dictionary to handle potential overlaps (though unlikely needed here)
    expansion_updates = {} # Store updates as {(r, c): color}

    # Iterate through each solid block to check for potential expansion
    for block_color, block_coords in solid_blocks_list:
        # Get the set of noise pixels matching the block's color
        current_noise_set = noise_pixels_by_color.get(block_color, set())
        if not current_noise_set:
            continue # Skip expansion check if no relevant noise exists

        # Find all unique orthogonal neighbors for the entire block
        # These are the candidate cells 'n' for expansion
        potential_expansion_coords = set()
        for r_block, c_block in block_coords:
            potential_expansion_coords.update(get_neighbor_coords(r_block, c_block, H, W, include_diagonal=False))

        # Check each potential coordinate 'n' against the expansion rules
        for r_n, c_n in potential_expansion_coords:
            coord_n = (r_n, c_n)

            # Rule 1: The cell 'n' must be background color in the INPUT grid
            if input_np[r_n, c_n] != background_color:
                continue

            # Rule 2: The cell 'n' must be orthogonally adjacent to the block 'b'.
            # This is implicitly true because potential_expansion_coords was generated
            # from orthogonal neighbors of the block's coordinates.

            # Rule 3: The cell 'n' must be orthogonally or diagonally adjacent to a noise pixel 'p'
            # of the same color as the block.
            neighbors_of_n = get_neighbor_coords(r_n, c_n, H, W, include_diagonal=True)
            # Check if any of n's 8-way neighbors are in the set of noise pixels for this color
            if neighbors_of_n.intersection(current_noise_set):
                # If all rules pass, mark this coordinate for update with the block's color
                expansion_updates[coord_n] = block_color

    # Apply the collected expansion updates to the output grid
    for (r, c), color in expansion_updates.items():
        output_np[r, c] = color

    # Convert the final NumPy array back to a standard Python list of lists for the expected output format
    return output_np.tolist()
```
