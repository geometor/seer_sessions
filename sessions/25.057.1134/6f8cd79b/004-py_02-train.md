
## example 1
*input:*
```
0 0 0
0 0 0
0 0 0
```
*expected output:*
```
8 8 8
8 0 8
8 8 8
```
*transformed output:*
```
8 8 8
8 0 8
8 8 8
```
size: True
palette: True
color count: True
pixels off: 0
PASSED

## example 2
*input:*
```
0 0 0
0 0 0
0 0 0
0 0 0
```
*expected output:*
```
8 8 8
8 0 8
8 0 8
8 8 8
```
*transformed output:*
```
8 8 8
8 8 8
8 8 8
8 8 8
```
size: True
palette: True
color count: False
pixels off: 2
**FAILED!**

## example 3
*input:*
```
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
```
*expected output:*
```
8 8 8 8
8 0 0 8
8 0 0 8
8 0 0 8
8 8 8 8
```
*transformed output:*
```
8 8 8 8
8 8 8 8
8 8 8 8
8 8 8 8
8 8 8 8
```
size: True
palette: True
color count: False
pixels off: 6
**FAILED!**

## example 4
*input:*
```
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```
*expected output:*
```
8 8 8 8 8 8
8 0 0 0 0 8
8 0 0 0 0 8
8 0 0 0 0 8
8 8 8 8 8 8
```
*transformed output:*
```
8 8 8 8 8 8
8 8 8 8 8 8
8 8 8 8 8 8
8 8 8 8 8 8
8 8 8 8 8 8
```
size: True
palette: True
color count: False
pixels off: 12
**FAILED!**
