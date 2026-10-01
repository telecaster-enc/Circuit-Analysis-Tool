import numpy as np
import matplotlib.pyplot as plt
import math

komponen = [
    {"nama": "V1", "tipe": "V", "node_a": 1, "node_b": 0, "nilai": 9},
    {"nama": "R1", "tipe": "R", "node_a": 1, "node_b": 2, "nilai": 100},
    {"nama": "R2", "tipe": "R", "node_a": 2, "node_b": 0, "nilai": 220},
    {"nama": "R3", "tipe": "R", "node_a": 2, "node_b": 0, "nilai": 330},
    {"nama": "R4", "tipe": "R", "node_a": 2, "node_b": 3, "nilai": 150},
    {"nama": "R5", "tipe": "R", "node_a": 3, "node_b": 0, "nilai": 470},
]
nodes = {}
tegangan_diketahui = {}
node_hitung = []
V_hitung = {}
arus = {}
tegangan_resistor = {}
V_semua = {0: 0.0}
solved = False
seeker = True

def seek():
    for k in komponen:
        print(f"{k["nama"]} Node A: {k["node_a"]} Node B: {k["node_b"]} Value: {k["nilai"]} {"V" if k["tipe"] == 'V' else 'Ω'}")

def clear(all):
    global komponen, nodes, tegangan_diketahui, node_hitung, V_hitung, arus, tegangan_resistor, V_semua
    if all:
        komponen = []
    nodes = {}
    tegangan_diketahui = {}
    node_hitung = []
    V_hitung = {}
    arus = {}
    tegangan_resistor = {}
    V_semua = {0: 0.0}

def solve_kvl():
    nodes = sorted(set(k["node_a"] for k in komponen) | set(k["node_b"] for k in komponen) - {0})
    #print("Node yang dihitung:", nodes)
    for k in komponen:
        if k["tipe"] == "V" and k["node_b"] == 0:
           tegangan_diketahui[k["node_a"]] = k["nilai"]
        elif k["tipe"] == "V" and k["node_a"] == 0:
            tegangan_diketahui[k["node_b"]] = -k["nilai"]
    #print("Tegangan diketahui:", tegangan_diketahui)
    global node_hitung
    node_hitung = [n for n in nodes if n not in tegangan_diketahui]
    #print("Node yang perlu dihitung lewat KCL:", node_hitung)
    idx = {n: i for i, n in enumerate(node_hitung)}
    n = len(node_hitung)
    G = np.zeros((n, n))
    I = np.zeros(n)
    for k in komponen:
        if k["tipe"] != "R":
            continue
        g = 1 / k["nilai"]
        a, b = k["node_a"], k["node_b"]

        if a in idx and b in idx:
            G[idx[a]][idx[a]] += g
            G[idx[b]][idx[b]] += g
            G[idx[a]][idx[b]] -= g
            G[idx[b]][idx[a]] -= g
        elif a in idx:
            G[idx[a]][idx[a]] += g
            v_b = tegangan_diketahui.get(b, 0) 
            I[idx[a]] += g * v_b
        elif b in idx:
            G[idx[b]][idx[b]] += g
            v_a = tegangan_diketahui.get(a, 0)
            I[idx[b]] += g * v_a

    #print("Matriks G:\n", G)
    #print("Vektor I:\n", I)

    V_hitung = np.linalg.solve(G, I)
    V_semua.update(tegangan_diketahui)
    V_semua.update(dict(zip(node_hitung, V_hitung)))

def solve_kcl_and_VR():
    for k in komponen:
        if k["tipe"] == "R":
            arus[k["nama"]] = (V_semua[k["node_a"]] - V_semua[k["node_b"]]) / k["nilai"]
            tegangan_resistor[k["nama"]] = (V_semua[k["node_a"]] - V_semua[k["node_b"]]) 
    #output()

def check_kcl_error():
    result = 0
    for n in node_hitung:
        keluar = 0
        for k in komponen:
            if k["tipe"] != "R":
                continue
            if k["node_a"] == n:
                keluar += arus[k["nama"]]
            elif k["node_b"] == n:
                keluar -= arus[k["nama"]]
        if math.isclose(keluar, 0, abs_tol=1e-9):
            result+=1
    if result == len(node_hitung):
        output()

def visualize():
    print("meow")

def output():
    print("\n=== Tegangan Node ===")
    for n in sorted(V_semua):
        print(f"Node {n}: {V_semua[n]:.3f} V")

    print("\n=== Tegangan Resistor ===")
    for n in sorted(tegangan_resistor):
        print(f"{n}: {tegangan_resistor[n]:.3f} V")

    print("\n=== Arus Cabang ===")
    for nama, i in arus.items():
        print(f"{nama}: {i*1000:.2f} mA")
    clear(False)

while True:
    readuser = input(">")
    if readuser == "solve":
        solve_kvl()
        solve_kcl_and_VR()
        check_kcl_error()
        solved = True
    elif readuser == "-h" or readuser == "help":
        print("Perintah yang tersedia:")
        print("  <komponen> <node_a> <node_b> <nilai>  -- tambah/ubah komponen, contoh: R1 1 2 100")
        print("  seek       -- tampilkan semua komponen yang sudah dimasukkan")
        print("  seeker on  -- tampilkan semua komponen yang sudah dimasukkan setelah input")
        print("  seeker off -- mematikan tampilan semua komponen yang sudah dimasukkan setelah input")
        print("  solve      -- selesaikan rangkaian (tegangan node & arus cabang)")
        print("  visualize  -- tampilkan grafik tegangan vs node")
        print("  clear      -- hapus semua komponen")
        print("  -h/help    -- tampilkan bantuan ini")
        print("\nFormat nama komponen: R untuk resistor, V untuk sumber tegangan")
        print("Node 0 selalu dianggap ground (0V)")
    elif readuser == "clear":
        clear(True)
        solved = False
    elif readuser == "visualize":
        if solved:
            visualize()
        else:
            solve_kvl()
            solve_kcl_and_VR()
            check_kcl_error()
            visualize()
    elif readuser == "seek":
        seek()
    elif readuser == "seeker on":
        seeker = True
    elif readuser == "seeker off":
        seeker = False
    else:
        split = readuser.split()
        try:
            replace = False
            if split[0][0] == 'R':
                tipe_k = 'R'
            elif split[0][0] == 'V':
                tipe_k = 'V'
            else:
                raise ValueError
            node_a = int(split[1])
            node_b = int(split[2])
            value = float(split[3])
            for k in komponen:
                if k["nama"] == split[0]:
                    k["node_a"] = node_a
                    k["node_b"] = node_b
                    k["nilai"] = value
                    replace = True
            if not replace:
                komponen.append({"nama": split[0], "tipe": tipe_k, "node_a": node_a, "node_b": node_b, "nilai": value})
            solved = False
            if seeker:
                seek()
        except IndexError:
            print("Input Error")
        except ValueError:
            print("Input Error")