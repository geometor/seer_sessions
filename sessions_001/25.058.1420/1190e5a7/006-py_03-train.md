
## example 1
*input:*
```
3 7 3 3 3 3 3 3 3 3 7 3 3 7 3
3 7 3 3 3 3 3 3 3 3 7 3 3 7 3
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
3 7 3 3 3 3 3 3 3 3 7 3 3 7 3
3 7 3 3 3 3 3 3 3 3 7 3 3 7 3
3 7 3 3 3 3 3 3 3 3 7 3 3 7 3
3 7 3 3 3 3 3 3 3 3 7 3 3 7 3
3 7 3 3 3 3 3 3 3 3 7 3 3 7 3
3 7 3 3 3 3 3 3 3 3 7 3 3 7 3
3 7 3 3 3 3 3 3 3 3 7 3 3 7 3
3 7 3 3 3 3 3 3 3 3 7 3 3 7 3
3 7 3 3 3 3 3 3 3 3 7 3 3 7 3
3 7 3 3 3 3 3 3 3 3 7 3 3 7 3
3 7 3 3 3 3 3 3 3 3 7 3 3 7 3
3 7 3 3 3 3 3 3 3 3 7 3 3 7 3
```
*expected output:*
```
3 3 3 3
3 3 3 3
```
*transformed output:*
```
3 3
3 3
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**

## example 2
*input:*
```
1 1 1 1 8 1 1 1 1 1 1
1 1 1 1 8 1 1 1 1 1 1
1 1 1 1 8 1 1 1 1 1 1
8 8 8 8 8 8 8 8 8 8 8
1 1 1 1 8 1 1 1 1 1 1
1 1 1 1 8 1 1 1 1 1 1
1 1 1 1 8 1 1 1 1 1 1
1 1 1 1 8 1 1 1 1 1 1
1 1 1 1 8 1 1 1 1 1 1
8 8 8 8 8 8 8 8 8 8 8
1 1 1 1 8 1 1 1 1 1 1
```
*expected output:*
```
1 1
1 1
1 1
```
*transformed output:*
```
0 0
0 0
```
size: False
palette: False
color count: False
pixels off: None
**FAILED!**

## example 3
*input:*
```
3 3 3 3 3 3 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3 1 3 1 3 1 3
3 3 3 3 3 3 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3 1 3 1 3 1 3
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
3 3 3 3 3 3 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3 1 3 1 3 1 3
3 3 3 3 3 3 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3 1 3 1 3 1 3
3 3 3 3 3 3 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3 1 3 1 3 1 3
3 3 3 3 3 3 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3 1 3 1 3 1 3
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
3 3 3 3 3 3 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3 1 3 1 3 1 3
3 3 3 3 3 3 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3 1 3 1 3 1 3
3 3 3 3 3 3 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3 1 3 1 3 1 3
3 3 3 3 3 3 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3 1 3 1 3 1 3
3 3 3 3 3 3 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3 1 3 1 3 1 3
3 3 3 3 3 3 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3 1 3 1 3 1 3
3 3 3 3 3 3 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3 1 3 1 3 1 3
3 3 3 3 3 3 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3 1 3 1 3 1 3
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
3 3 3 3 3 3 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3 1 3 1 3 1 3
3 3 3 3 3 3 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3 1 3 1 3 1 3
3 3 3 3 3 3 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3 1 3 1 3 1 3
3 3 3 3 3 3 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3 1 3 1 3 1 3
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
3 3 3 3 3 3 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3 1 3 1 3 1 3
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
3 3 3 3 3 3 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3 1 3 1 3 1 3
3 3 3 3 3 3 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3 1 3 1 3 1 3
3 3 3 3 3 3 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3 1 3 1 3 1 3
```
*expected output:*
```
3 3 3 3 3
3 3 3 3 3
3 3 3 3 3
3 3 3 3 3
3 3 3 3 3
3 3 3 3 3
```
*transformed output:*
```
0 0
0 0
```
size: False
palette: False
color count: False
pixels off: None
**FAILED!**
