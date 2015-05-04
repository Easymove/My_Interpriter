.386
data SEGMENT
	a DD 12
	a1 DD 171
	a2 DD 0
	a3 DD 0
	a4 DD 0
data ENDS
code SEGMENT
	MOV AX, 23
	MOV a2, AX
	MOV AX, 12
	MOV a3, AX
	MOV AX, -1
	MOV a4, AX
code ENDS
