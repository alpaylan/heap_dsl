from z3 import *


"""
This example demonstrates how two chunks are allocated. 
This is an attempt to generalize allocation of multiple chunks.
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

chunks = []
for i in range(5):
    chunks.append(SymChunk(i))


heap_size = 0x400

chunk_positions = [0x000, 0x100, 0x200, 0x300]

temps = [[] for i in range(5)]

for i in chunk_positions:
    for j in range(5):
        temps[j].append(chunks[j].pos == i)
        
s = Solver()

for tmp in temps:
    s.add(Or(tmp))

positions = []

for i in chunks:
    positions.append(i.pos)


s.add(Distinct(positions))

for i in range(5):
    s.add(And(chunks[i].pos + chunks[i].size <= heap_size , chunks[i].pos + chunks[i].size > 0))


for i in range(5):
    s.add(chunks[i].size == 0x100)

print(s.check())


if s.check() == sat:
    m = s.model()
    for d in m:
        print(d, m[d])
