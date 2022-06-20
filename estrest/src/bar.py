from event_structure import EventStructure

a = EventStructure().prefix('b').prefix('a')
b = EventStructure().prefix('y').prefix('x')
p = a.product(b)
print(p)
