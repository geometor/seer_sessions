
## example 1
*input:*
```
8 8 3 8 8
8 8 3 8 8
3 3 3 3 3
8 8 3 8 8
4 8 3 8 8
```
*expected output:*
```
8 8
4 8
```
*transformed output:*
```
8 8 3 8 8
8 8 3 8 8
3 3 3 3 3
8 8 3 8 8
4 8 3 8 8
```
size: False
palette: False
color count: False
pixels off: None
**FAILED!**

## example 2
*input:*
```
4 4 4 2 4 4 4
4 4 4 2 4 1 4
4 4 4 2 4 4 4
2 2 2 2 2 2 2
4 4 4 2 4 4 4
4 4 4 2 4 4 4
4 4 4 2 4 4 4
```
*expected output:*
```
4 4 4
4 1 4
4 4 4
```
*transformed output:*
```
4 4 4
4 1 4
4 4 4
```
size: True
palette: True
color count: True
pixels off: 0
PASSED
