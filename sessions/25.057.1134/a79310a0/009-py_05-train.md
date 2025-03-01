
## example 1
*input:*
```
8 8 0 0 0
8 8 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```
*expected output:*
```
0 0 0 0 0
2 2 0 0 0
2 2 0 0 0
0 0 0 0 0
0 0 0 0 0
```
*transformed output:*
```
0 8 0 0 0
8 8 0 0 0
0 0 2 0 0
0 0 0 0 0
0 0 0 0 0
```
size: True
palette: False
color count: False
pixels off: 6
**FAILED!**

## example 2
*input:*
```
0 8 0
0 0 0
0 0 0
```
*expected output:*
```
0 0 0
0 2 0
0 0 0
```
*transformed output:*
```
0 0 0
0 2 0
0 0 0
```
size: True
palette: True
color count: True
pixels off: 0
PASSED

## example 3
*input:*
```
0 0 0 0 0
0 8 8 8 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```
*expected output:*
```
0 0 0 0 0
0 0 0 0 0
0 2 2 2 0
0 0 0 0 0
0 0 0 0 0
```
*transformed output:*
```
0 0 0 0 0
0 0 8 8 0
0 0 2 0 0
0 0 0 0 0
0 0 0 0 0
```
size: True
palette: False
color count: False
pixels off: 4
**FAILED!**
