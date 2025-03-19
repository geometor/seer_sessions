
## example 1
*input:*
```
3 3 0
0 3 0
3 0 3
```
*expected output:*
```
8 8 0
0 8 0
3 0 3
```
*transformed output:*
```
3 3 0
0 8 0
3 0 3
```
size: True
palette: True
color count: False
pixels off: 2
**FAILED!**

## example 2
*input:*
```
0 3 0 0 0 3
0 3 3 3 0 0
0 0 0 0 3 0
0 3 0 0 0 0
```
*expected output:*
```
0 8 0 0 0 3
0 8 8 8 0 0
0 0 0 0 3 0
0 3 0 0 0 0
```
*transformed output:*
```
0 3 0 0 0 3
0 8 8 8 0 0
0 0 0 0 8 0
0 3 0 0 0 0
```
size: True
palette: True
color count: True
pixels off: 2
**FAILED!**

## example 3
*input:*
```
3 3 0 3
3 3 0 0
3 0 0 3
0 0 3 3
```
*expected output:*
```
8 8 0 3
8 8 0 0
8 0 0 8
0 0 8 8
```
*transformed output:*
```
3 3 0 3
3 8 0 0
3 0 0 3
0 0 3 3
```
size: True
palette: True
color count: False
pixels off: 7
**FAILED!**

## example 4
*input:*
```
3 3 0 0 0 0
0 3 0 0 3 0
3 0 0 0 0 0
0 3 3 0 0 0
0 3 3 0 0 3
```
*expected output:*
```
8 8 0 0 0 0
0 8 0 0 3 0
3 0 0 0 0 0
0 8 8 0 0 0
0 8 8 0 0 3
```
*transformed output:*
```
3 3 0 0 0 0
0 8 0 0 8 0
3 0 0 0 0 0
0 8 8 0 0 0
0 3 3 0 0 3
```
size: True
palette: True
color count: False
pixels off: 5
**FAILED!**
