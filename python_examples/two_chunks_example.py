from z3 import *

"""
This example demonstrates how two chunks are allocated. 
This is the most primitive case where all variables are hand coded. 
"""

"""
Define Symbolic Chunks
ID: Unique Integer Identifier
Position: 32 bit BitVector
Size: 32 bit BitVector
"""

class SymChunk:
    def __init__(self, id):
        self.id = id
        self.pos = BitVec('p_' + str(id), 32)
        self.size = BitVec('s_' + str(id), 32)

    def __str__(self):
        return str(self.id) + " " + str(self.pos) + " " + str(self.size)

c0 = SymChunk(0)
c1 = SymChunk(1)

heap_size = 0x400

chunk_positions = [0x000, 0x100, 0x200, 0x300]

temp1 = []
temp2 = []

for i in chunk_positions:
    temp1.append(c0.pos == i)
    temp2.append(c1.pos == i)

s = Solver()

s.add(Or(temp1))
s.add(Or(temp2))
s.add(c0.pos != c1.pos)
s.add(And(c0.pos + c0.size <= heap_size , c0.pos + c0.size > 0))
s.add(And(c1.pos + c1.size <= heap_size , c1.pos + c1.size > 0 ))
s.add(c0.size == 0x100)
s.add(c1.size == 0x100)

print(s.check())
m = s.model()
for d in m:
    print(d, m[d])
