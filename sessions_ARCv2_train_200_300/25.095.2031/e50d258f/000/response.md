## Perception

The input is a 10x10 grid of digits. The digits used are 0, 1, 2, and 8. The digit '0' appears to function as a background or empty space. The digits '1', '2', and '8' form distinct clusters or shapes within the grid, separated by the '0' digits.

The output is a smaller rectangular grid containing only the digits '1', '2', and '8'. The '0' digits are absent in the output. The dimensions of the output grid vary between examples.

The core transformation seems to involve identifying a specific cluster of non-zero digits in the input grid and extracting the minimal rectangular region (bounding box) that encompasses this cluster. Based on the examples, the selected cluster is the one whose bounding box contains *only* non-zero digits from the input grid (no '0's fall within the selected bounding box).

## Facts


```yaml
Data:
  - type: Grid
    description: Represents the input and output structures.
    properties:
      rows: Integer (Input is 10, Output varies)
      columns: Integer (Input is 10, Output varies)
      cells: List of Lists of Integers

Digits:
  - type: BackgroundDigit
    value: 0
    description: Represents empty space, separating foreground objects.
  - type: ForegroundDigit
    value: [1, 2, 8]
    description: Represents the content of objects or patterns.

Objects:
  - type: ConnectedComponent
    description: A cluster of adjacent (horizontally or vertically) ForegroundDigits. Input grids may contain multiple components.
    properties:
      cells: List of coordinates containing ForegroundDigits belonging to the component.
      bounding_box: The minimal rectangle enclosing all cells of the component.
        properties:
          min_row: Integer
          max_row: Integer
          min_col: Integer
          max_col: Integer
      is_solid: Boolean (Derived property - True if the bounding box in the input grid contains only ForegroundDigits, False otherwise)

Transformation:
  - action: IdentifyComponents
    description: Find all distinct ConnectedComponents of ForegroundDigits in the input grid.
  - action: CalculateBoundingBoxes
    description: Determine the minimal bounding box for each identified component.
  - action: CheckSolidity
    description: For each component's bounding box, check if all cells within that box in the *input* grid contain ForegroundDigits.
  - action: SelectComponent
    description: Choose the single component whose bounding box is solid (contains no BackgroundDigits).
    assumption: Exactly one such component exists in each input.
  - action: ExtractSubgrid
    description: Create the output grid by copying the portion of the input grid defined by the selected component's bounding box.
```


## Natural Language Program

1.  **Identify Non-Zero Components:** Scan the input grid and identify all distinct connected components formed by adjacent (sharing an edge) non-zero digits (1, 2, or 8). Treat the digit 0 as empty space separating components.
2.  **Determine Bounding Boxes:** For each identified component, calculate its minimal bounding box by finding the minimum and maximum row and column indices occupied by the digits within that component.
3.  **Find Solid Bounding Box:** Examine each component's bounding box. Check if the rectangular subgrid defined by this bounding box in the original input grid contains *only* non-zero digits (i.e., it contains no 0s).
4.  **Select Target Component:** Select the component whose bounding box was identified as solid in the previous step. (Based on the examples, it's assumed there will be exactly one such component).
5.  **Extract Output:** The output grid is the rectangular subgrid from the input grid corresponding exactly to the bounding box of the selected solid component.