
## example 1
*input:*
```
0 0 8 0
0 8 0 8
0 0 8 0
```
*expected output:*
```
0 0 8 0 0 8 0 0
0 8 0 8 8 0 8 0
0 0 8 0 0 8 0 0
0 0 8 0 0 8 0 0
0 8 0 8 8 0 8 0
0 0 8 0 0 8 0 0
```
*transformed output:*
```
0 0 0 0 0 0 8 0
0 0 0 0 0 8 0 0
0 0 0 0 8 0 0 0
0 0 0 8 0 0 0 8
0 0 8 0 0 0 8 0
0 0 0 0 0 8 0 0
```
size: True
palette: True
color count: False
pixels off: 20
**FAILED!**

## example 2
*input:*
```
0 0 3 3
0 3 0 3
3 3 3 0
```
*expected output:*
```
0 0 3 3 3 3 0 0
0 3 0 3 3 0 3 0
3 3 3 0 0 3 3 3
3 3 3 0 0 3 3 3
0 3 0 3 3 0 3 0
0 0 3 3 3 3 0 0
```
*transformed output:*
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 28
**FAILED!**

## example 3
*input:*
```
3 3 3 3
3 0 0 0
3 0 0 0
```
*expected output:*
```
3 3 3 3 3 3 3 3
3 0 0 0 0 0 0 3
3 0 0 0 0 0 0 3
3 0 0 0 0 0 0 3
3 0 0 0 0 0 0 3
3 3 3 3 3 3 3 3
```
*transformed output:*
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 24
**FAILED!**
