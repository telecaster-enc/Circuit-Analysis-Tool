import numpy

komponen = [
    {"nama": "V1", "tipe": "V", "node_a": 1, "node_b": 0, "nilai": 9},
    {"nama": "R1", "tipe": "R", "node_a": 1, "node_b": 2, "nilai": 100},
    {"nama": "R2", "tipe": "R", "node_a": 2, "node_b": 3, "nilai": 220},
    {"nama": "R3", "tipe": "R", "node_a": 2, "node_b": 3, "nilai": 330},
    {"nama": "R4", "tipe": "R", "node_a": 3, "node_b": 0, "nilai": 300}
]

nodes = set()
for k in komponen:
    nodes.add(k["node_a"])
    nodes.add(k["node_b"])
nodes.discard(0)  
print(sorted(nodes))  

tegangan_diketahui = {}
for k in komponen:
    if k["tipe"] == "V" and k["node_b"] == 0:
        tegangan_diketahui[k["node_a"]] = k["nilai"]
    elif k["tipe"] == "V" and k["node_a"] == 0:
        tegangan_diketahui[k["node_b"]] = -k["nilai"]
print("Tegangan diketahui:", tegangan_diketahui)

node_hitung = [n for n in nodes if n not in tegangan_diketahui]
print("Node yang perlu dihitung lewat KCL:", node_hitung)