from z3 import *



"""
This example demonstrates how a simple overflow bug can corrupt the next chunk.
This corruption can be used to reach exploitation primitives.
"""

"""
Define Symbolic Chunks
ID: Unique Integer Identifier
Position: 32 bit BitVector
Size: 32 bit BitVector
Vulnerable: Boolean Variable indicating vulnerability
"""
class SymChunk:
    def __init__(self, id):
        self.id = id
        self.pos = BitVec('p_' + str(id), 32)
        self.size = BitVec('s_' + str(id), 32)
        self.vulnerable = Bool('v_' + str(id))
    def __str__(self):
        return str(self.id) + " " + str(self.pos) + " " + str(self.size)


"""
Define 5 Symbolic Chunks
"""
chunks = []
for i in range(5):
    chunks.append(SymChunk(i))



"""
Restrict Heap to 0x000-0x500 adress space
"""
heap_size = 0x500


"""
Restrict Chunk Positions to specified values
"""
chunk_positions = [0x000, 0x100, 0x200, 0x300, 0x400]

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


"""
Limitation of the positions
"""
for i in range(5):
    s.add(And(chunks[i].pos + chunks[i].size <= heap_size , chunks[i].pos + chunks[i].size > 0))


"""
All sizes are 0x100 bytes
"""

for i in range(5):
    s.add(chunks[i].size == 0x100)


"""
Write Operation

Chunk C is sized 256 bytes.
Write Access W for Chunk C decides if there exists a vulnerability for the next chunk
Notation: C.size < W 

"""

W = 0x102
vulnerabilities = []
for i in range(5):
    vulnerabilities.append(If(And(chunks[i].pos > chunks[0].pos, chunks[i].pos < chunks[0].pos + W),chunks[i].vulnerable == True,chunks[i].vulnerable == False))

s.add(And(vulnerabilities)) 



"""
Check if constraints are satisfied
"""


print("Are The Contraints Satisfiable: ", s.check())

if s.check() == sat:
    print("An Example Model Case")
    m = s.model()
    for d in m:
        print(d,":",m[d])





"""
Work with concrete values to determine the actual vulnerabilities
"""

concrete_values = {}
for d in m:
    concrete_values[str(d)] = m[d]

print("p_2:", concrete_values["p_2"])
print("s_2:", concrete_values["s_2"])
print("p_0:", concrete_values["p_0"])
print("s_0:", concrete_values["s_0"])
print("Write Access Bount: ", W)
print("Vulnerable Region:", simplify(concrete_values["p_0"] + W - concrete_values["p_2"]))
