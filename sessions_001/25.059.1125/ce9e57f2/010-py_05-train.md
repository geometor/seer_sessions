
## example 1
*input:*
```
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0
0 2 0 2 0 2 0 0 0
0 2 0 2 0 2 0 2 0
0 2 0 2 0 2 0 2 0
0 2 0 2 0 2 0 2 0
```
*expected output:*
```
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0
0 2 0 2 0 2 0 0 0
0 8 0 2 0 2 0 2 0
0 8 0 8 0 8 0 2 0
0 8 0 8 0 8 0 8 0
```
*transformed output:*
```
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0
0 2 0 2 0 2 0 0 0
0 2 0 2 0 2 0 2 0
0 8 0 8 0 8 0 8 0
0 8 0 8 0 8 0 8 0
```
size: True
palette: True
color count: True
pixels off: 2
**FAILED!**

## example 2
*input:*
```
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
0 2 0 0 0 0 0 2 0
0 2 0 2 0 0 0 2 0
0 2 0 2 0 0 0 2 0
0 2 0 2 0 2 0 2 0
0 2 0 2 0 2 0 2 0
0 2 0 2 0 2 0 2 0
```
*expected output:*
```
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
0 2 0 0 0 0 0 2 0
0 2 0 2 0 0 0 2 0
0 2 0 2 0 0 0 2 0
0 8 0 2 0 2 0 8 0
0 8 0 8 0 2 0 8 0
0 8 0 8 0 8 0 8 0
```
*transformed output:*
```
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
0 2 0 0 0 0 0 2 0
0 2 0 2 0 0 0 2 0
0 2 0 2 0 0 0 2 0
0 2 0 2 0 2 0 2 0
0 8 0 8 0 8 0 8 0
0 8 0 8 0 8 0 8 0
```
size: True
palette: True
color count: False
pixels off: 3
**FAILED!**

## example 3
*input:*
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0
0 2 0 0 0 0 0 2 0
0 2 0 0 0 0 0 2 0
0 2 0 0 0 0 0 2 0
0 2 0 0 0 2 0 2 0
0 2 0 2 0 2 0 2 0
0 2 0 2 0 2 0 2 0
0 2 0 2 0 2 0 2 0
```
*expected output:*
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0
0 2 0 0 0 0 0 2 0
0 2 0 0 0 0 0 2 0
0 2 0 0 0 0 0 2 0
0 2 0 0 0 2 0 8 0
0 8 0 2 0 2 0 8 0
0 8 0 2 0 8 0 8 0
0 8 0 8 0 8 0 8 0
```
*transformed output:*
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0
0 2 0 0 0 0 0 2 0
0 2 0 0 0 0 0 2 0
0 2 0 0 0 0 0 2 0
0 2 0 0 0 2 0 2 0
0 2 0 2 0 2 0 2 0
0 8 0 8 0 8 0 8 0
0 8 0 8 0 8 0 8 0
```
size: True
palette: True
color count: False
pixels off: 4
**FAILED!**
