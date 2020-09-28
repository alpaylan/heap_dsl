from z3 import *

"""
This example demonstrates how overflow bugs are defined and detected. 
This is the first step in realization of bug invocations using symbolic execution. 
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


heap_size = 0x500

chunk_positions = [0x000, 0x100, 0x200, 0x300, 0x400]
write_accesses = [0x100, 0x100, 0x100, 0x101, 0x100]
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


"""
Write Operation

Chunk C is sized 256 bytes.
Write Access W for Chunk C decides if there exists a vulnerability for the next chunk
Notation: C.size < W 

"""


overflows = []
for i in range(5):
    for j in range(5):
        if i == j:
            continue
        overflows.append(And((chunks[i].pos + write_accesses[i] > chunks[j].pos),(chunks[i].pos < chunks[j].pos)))

s.add(Or(overflows))




print(s.check())


if s.check() == sat:
    m = s.model()
    for d in m:
        print(d, m[d])
