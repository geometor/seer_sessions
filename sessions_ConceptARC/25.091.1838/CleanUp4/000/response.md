Okay, let's break down the task based on the provided examples.

**Perception of Task Elements:**

1.  **Input/Output:** The task takes a grid of colored pixels as input and produces a modified grid as output.
2.  **Colors:** Specific colors seem to trigger actions or are targets of actions: azure (8), green (3), yellow (4), white (0). Other colors (red (2), magenta (6), blue (1), orange (7)) are present but might be part of larger structures or treated as 'noise'.
3.  **Structures/Objects:** The grids contain contiguous blocks of color forming distinct objects. These can be simple spots, lines, or complex shapes like hollow rectangles.
4.  **Key Relationships:**
    *   **Adjacency:** The relationship between adjacent pixels (orthogonal and diagonal) is critical, particularly between azure (8) and green (3) in `train_1`.
    *   **Object Size:** The number of pixels in a contiguous object seems relevant for distinguishing 'major' objects from 'minor' ones or 'noise' in `train_2`.
    *   **Containment:** Some pixels exist 'inside' shapes formed by other colors (e.g., `train_2`), although this might be captured by the object size rule.
5.  **Transformations:** The core transformations observed are:
    *   Changing specific pixels to white (0) based on their color and/or adjacency to other colors (`train_1`, `train_2`).
    *   Changing pixels of one color to another specific color (`train_3`).
    *   Keeping only the largest objects and removing everything else (`train_2`).
6.  **Conditional Logic:** The transformation rule appears to be conditional, depending on the specific content of the input grid. Three distinct rules were identified, applied based on the presence and arrangement of certain colors and object structures.

**Facts (YAML):**


```yaml
task_type: grid_transformation
grid_properties:
  dimensionality: 2
  color_space: 0-9 integer map
  max_size: 30x30
observed_elements:
  - type: pixel
    properties: [color, location]
  - type: object
    definition: contiguous block of same-colored pixels (non-white)
    properties: [color, size (pixel_count), shape, location, pixels]
relationships:
  - type: adjacency
    definition: Orthogonal or diagonal neighboring pixels
    relevance: Used in rule 1 (azure(8) affecting adjacent green(3))
  - type: relative_size
    definition: Comparing pixel counts of different objects
    relevance: Used in rule 2 (selecting the 4 largest objects)
transformations:
  - type: color_change
    details:
      - change_to: white (0) # Removal
        conditions:
          - rule_1: pixel is azure(8) OR pixel is green(3) adjacent to azure(8)
          - rule_2: pixel is not part of the 4 largest objects
      - change_to: green (3)
        conditions:
          - rule_3: pixel is yellow (4)
conditional_rules:
  - condition: Presence of azure(8) AND green(3) pixels, with at least one instance of adjacency (orthogonal or diagonal) between them.
    applies_rule: rule_1
  - condition: Absence of condition_1 AND presence of >= 4 distinct contiguous non-white objects with size >= 10 pixels.
    applies_rule: rule_2
  - condition: Absence of condition_1 and condition_2 AND presence of yellow(4) pixels.
    applies_rule: rule_3
  - default: No change (implied if no conditions met)
```


**Natural Language Program:**

1.  **Analyze the input grid:** Examine the colors and their arrangement.
2.  **Check Rule 1 Condition:** Determine if the grid contains both azure (8) pixels and green (3) pixels, AND if any azure (8) pixel is orthogonally or diagonally adjacent to any green (3) pixel.
    *   **If True (Apply Rule 1):** Create a copy of the input grid. Iterate through the input grid. Change all azure (8) pixels in the copy to white (0). Change all green (3) pixels in the copy that had an azure (8) neighbor (orthogonal or diagonal) in the *original* input grid to white (0). Output the modified copy.
    *   **If False:** Proceed to the next check.
3.  **Check Rule 2 Condition:** Identify all distinct contiguous non-white objects in the grid. Count how many of these objects have a size (pixel count) of 10 or more. Check if this count is 4 or greater.
    *   **If True (Apply Rule 2):** Identify all distinct contiguous non-white objects and calculate their sizes. Select the four objects with the largest sizes (if there's a tie for the 4th position, include all tied objects, potentially resulting in more than 4 being kept). Create a new grid initialized to white (0). Copy only the pixels belonging to these selected largest objects from the input grid to the new grid, maintaining their original colors and positions. Output the new grid.
    *   **If False:** Proceed to the next check.
4.  **Check Rule 3 Condition:** Determine if the grid contains any yellow (4) pixels.
    *   **If True (Apply Rule 3):** Create a copy of the input grid. Change all yellow (4) pixels in the copy to green (3). Output the modified copy.
    *   **If False:** Proceed to the default case.
5.  **Default:** If none of the above conditions were met, output the input grid unchanged.