import numpy as np
import numpy.linalg as LA
from scipy.integrate import odeint #odeint
import matplotlib.pyplot as plt #to draw graphs

# const
ele_size = 1/2*0.02*0.02
poi = 0.2
e = 100
th = 0.98
row = 2400
nmode = 10
delta_t = 0.000004
total_time = 0.01
total_step = int(total_time/delta_t)
hc = 0.02 #減衰定数
load = 100 #外力最大値
load_time = 0.0001
load_step = int(load_time/delta_t)
load_diff = load/load_step
node_per_edge = 50

# ファイル読み込み:ノード・要素
node_path = "./one_hole_1_1.1.node"
ele_path = "./one_hole_1_1.1.ele"
# node_path = "~/src/github.com/shirafuji/graduation_thesis/vibration_simulation/one_hole_1_1.1.node"
# ele_path = '~/src/github.com/shirafuji/graduation_thesis/vibration_simulation/one_hole_1_1.1.ele'
with open(node_path) as f_node:
    s_line = f_node.readline()
    number_list = s_line.split()
    nnode_str = number_list[0]
    nnode = int(nnode_str)
    position = np.zeros((nnode, 2), dtype=np.int64)
    for i in range(nnode):
        s_line = f_node.readline()
        number_list = s_line.split()
        x_str = number_list[1]
        y_str = number_list[2]
        x = int(x_str)
        y = int(y_str)
        position[i][0] = x
        position[i][1] = y
with open(ele_path) as f_ele:
    s_line = f_ele.readline()
    number_list = s_line.split()
    nele_str = number_list[0]
    nele = int(nele_str)
    eles = np.zeros((nele, 3), dtype=np.int64)
    for h in range(nele):
        s_line = f_ele.readline()
        number_list = s_line.split()
        i_str = number_list[1]
        j_str = number_list[2]
        k_str = number_list[3]
        i = int(i_str)
        j = int(j_str)
        k = k_str
        eles[h][0] = i
        eles[h][1] = j
        eles[h][2] = k

kt = np.zeros((2*nnode, 2*nnode))
mt = np.zeros((2*nnode, 2*nnode))

def calc_ke(ele, position, kt):
    i = ele[0]
    j = ele[1]
    k = ele[2]
    xi = position[i-1][0]
    yi = position[i-1][1]
    xj = position[j-1][0]
    yj = position[j-1][1]
    xk = position[k-1][0]
    yk = position[k-1][1]
    # ひずみ-変位関係
    b = np.zeros((3, 6))
    b[0][0] = yj-yk
    b[0][2] = yk-yi
    b[0][4] = yi-yj
    b[1][1] = xk-xj
    b[1][3] = xi-xk
    b[1][5] = xj-xi
    b[2][0] = xk-xj
    b[2][1] = yj-yk
    b[2][2] = xi-xk
    b[2][3] = yk-yi
    b[2][4] = xj-xi
    b[2][5] = yi-yj
    # 応力-ひずみ関係
    d = np.zeros((3, 3))
    d[0][0] = 1-poi
    d[0][1] = poi
    d[1][0] = poi
    d[1][1] = 1 - poi
    d[2][2] = (1-2*poi)/2
    d = d*e/(1+poi)/(1-2*poi)
    ke = th*ele_size*np.dot(np.dot(b.T, d), b)
    # 全体剛性行列への組み込み
    kt[2*i-1-1][2*i-1-1] += ke[1-1][1-1]
    kt[2*i-1-1][2*i-1] += ke[1-1][2-1]
    kt[2*i-1][2*i-1-1] += ke[2-1][1-1]
    kt[2*i-1][2*i-1] += ke[2-1][2-1]
    kt[2*i-1-1][2*j-1-1] += ke[1-1][3-1]
    kt[2*i-1-1][2*j-1] += ke[1-1][4-1]
    kt[2*i-1][2*j-1-1] += ke[2-1][3-1]
    kt[2*i-1][2*j-1] += ke[2-1][4-1]
    kt[2*i-1-1][2*k-1-1] += ke[1-1][5-1]
    kt[2*i-1-1][2*k-1] += ke[1-1][6-1]
    kt[2*i-1][2*k-1-1] += ke[2-1][5-1]
    kt[2*i-1][2*k-1] += ke[2-1][6-1]

    kt[2*j-1-1][2*i-1-1] += ke[3-1][1-1]
    kt[2*j-1-1][2*i-1] += ke[3-1][2-1]
    kt[2*j-1][2*i-1-1] += ke[4-1][1-1]
    kt[2*j-1][2*i-1] += ke[4-1][2-1]
    kt[2*j-1-1][2*j-1-1] += ke[3-1][3-1]
    kt[2*j-1-1][2*j-1] += ke[3-1][4-1]
    kt[2*j-1][2*j-1-1] += ke[4-1][3-1]
    kt[2*j-1][2*j-1] += ke[4-1][4-1]
    kt[2*j-1-1][2*k-1-1] += ke[3-1][5-1]
    kt[2*j-1-1][2*k-1] += ke[3-1][6-1]
    kt[2*j-1][2*k-1-1] += ke[4-1][5-1]
    kt[2*j-1][2*k-1] += ke[4-1][6-1]

    kt[2*k-1-1][2*i-1-1] += ke[5-1][1-1]
    kt[2*k-1-1][2*i-1] += ke[5-1][2-1]
    kt[2*k-1][2*i-1-1] += ke[6-1][1-1]
    kt[2*k-1][2*i-1] += ke[6-1][2-1]
    kt[2*k-1-1][2*j-1-1] += ke[5-1][3-1]
    kt[2*k-1-1][2*j-1] += ke[5-1][4-1]
    kt[2*k-1][2*j-1-1] += ke[6-1][3-1]
    kt[2*k-1][2*j-1] += ke[6-1][4-1]
    kt[2*k-1-1][2*k-1-1] += ke[5-1][5-1]
    kt[2*k-1-1][2*k-1] += ke[5-1][6-1]
    kt[2*k-1][2*k-1-1] += ke[6-1][5-1]
    kt[2*k-1][2*k-1] += ke[6-1][6-1]

    return kt

def calc_me(ele, mt):
    i = ele[0]
    j = ele[1]
    k = ele[2]
    me = np.zeros((6, 6))
    me[0][0] = 1/6
    me[0][2] = 1/12
    me[0][4] = 1/12
    me[1][1] = 1/6
    me[1][3] = 1/12
    me[1][5] = 1/12
    me[2][0] = 1/12
    me[2][2] = 1/6
    me[2][4] = 1/12
    me[3][1] = 1/12
    me[3][3] = 1/6
    me[3][5] = 1/12
    me[4][0] = 1/12
    me[4][2] = 1/12
    me[4][4] = 1/6
    me[5][1] = 1/12
    me[5][3] = 1/12
    me[5][5] = 1/6
    me = ele_size*th*row*me
    # 全体質量行列への組み込み
    mt[2*i-1-1][2*i-1-1] += me[1-1][1-1]
    mt[2*i-1-1][2*i-1] += me[1-1][2-1]
    mt[2*i-1][2*i-1-1] += me[2-1][1-1]
    mt[2*i-1][2*i-1] += me[2-1][2-1]
    mt[2*i-1-1][2*j-1-1] += me[1-1][3-1]
    mt[2*i-1-1][2*j-1] += me[1-1][4-1]
    mt[2*i-1][2*j-1-1] += me[2-1][3-1]
    mt[2*i-1][2*j-1] += me[2-1][4-1]
    mt[2*i-1-1][2*k-1-1] += me[1-1][5-1]
    mt[2*i-1-1][2*k-1] += me[1-1][6-1]
    mt[2*i-1][2*k-1-1] += me[2-1][5-1]
    mt[2*i-1][2*k-1] += me[2-1][6-1]

    mt[2*j-1-1][2*i-1-1] += me[3-1][1-1]
    mt[2*j-1-1][2*i-1] += me[3-1][2-1]
    mt[2*j-1][2*i-1-1] += me[4-1][1-1]
    mt[2*j-1][2*i-1] += me[4-1][2-1]
    mt[2*j-1-1][2*j-1-1] += me[3-1][3-1]
    mt[2*j-1-1][2*j-1] += me[3-1][4-1]
    mt[2*j-1][2*j-1-1] += me[4-1][3-1]
    mt[2*j-1][2*j-1] += me[4-1][4-1]
    mt[2*j-1-1][2*k-1-1] += me[3-1][5-1]
    mt[2*j-1-1][2*k-1] += me[3-1][6-1]
    mt[2*j-1][2*k-1-1] += me[4-1][5-1]
    mt[2*j-1][2*k-1] += me[4-1][6-1]

    mt[2*k-1-1][2*i-1-1] += me[5-1][1-1]
    mt[2*k-1-1][2*i-1] += me[5-1][2-1]
    mt[2*k-1][2*i-1-1] += me[6-1][1-1]
    mt[2*k-1][2*i-1] += me[6-1][2-1]
    mt[2*k-1-1][2*j-1-1] += me[5-1][3-1]
    mt[2*k-1-1][2*j-1] += me[5-1][4-1]
    mt[2*k-1][2*j-1-1] += me[6-1][3-1]
    mt[2*k-1][2*j-1] += me[6-1][4-1]
    mt[2*k-1-1][2*k-1-1] += me[5-1][5-1]
    mt[2*k-1-1][2*k-1] += me[5-1][6-1]
    mt[2*k-1][2*k-1-1] += me[6-1][5-1]
    mt[2*k-1][2*k-1] += me[6-1][6-1]

    return mt

# 合成行列と質量行列の繰り返し
for h in range(nele):
    ele = eles[h]
    kt = calc_ke(ele, position, kt)
    mt = calc_me(ele, mt)

# 境界条件導入(底の点は全て固定)
# for i in range(node_per_edge):
    
def subspace(k,m,n,neig):
    loop_count = 0
    ramda = np.zeros((neig,1)) #初期固有値
    x = np.random.rand(n,neig) #初期固有ベクトル
    y = np.zeros((n, neig))
    k = np.matrix(k)
    k_inv = np.linalg.inv(k)
    for i in range(50):
        loop_count+=1
        ramold = ramda.copy()
        y = np.dot(np.dot(k_inv,m),x)
        kg = np.dot(np.dot(y.T, k), y)
        mg = np.dot(np.dot(y.T, m), y)
        mg_inv = np.linalg.inv(mg)
        w,v = LA.eig(np.dot(mg_inv, kg)) #w:固有値,v:固有ベクトル
        for i in range(neig):
            ramda[i][0] = w[i]
        p = v.T
        x = np.dot(y, p)
        for i in range(neig):
            max_val = 0
            for j in range(n):
                x_val = abs(x[j, i])
                if x_val > max_val:
                    max_val = x_val
            for j in range(n):
                x[j, i] = x[j, i]/max_val
        han = (ramda - ramold)/ramda
        max_mod = 0
        for i in range(neig):
            if abs(han[i][0]) > max_mod:
                max_mod = abs(han[i][0])
        if max_mod < 0.00001:
            break

    return ramda, x, loop_count

ramda, x, loop_count = subspace(kt, mt, 2*nnode, nmode)

print(ramda.shape)
print(x.shape)
print(ramda)
print(x)
print(loop_count)

# モード重畳法
# 減衰係数は各iで計算する
# ftは(total_step, nnode, 1)
def mode_superimposition_method(kt, mt, ft, ramda, x, delta_t):
    q = np.zeros((nmode, total_step+1, 1)) #一般化変位設定
    ramda_complex = np.zeros((nmode, 1), dtype=complex) # 複素数対応のramda
    ramda_complex = ramda+0.j
    omega = np.zeros((nmode, 1), dtype=complex) #複素数に対応する固有振動数
    omega = np.sqrt(ramda)
    # xの並び順が逆になるバグがあるため並び替えるが後で直す
    phi = np.zeros((2*nnode, nmode))
    for i in range(2*nnode):
        for j in range(nmode):
            phi[i, j] = x[i, nmode-j-1]
    kt_a = np.dot(np.dot(phi.T, kt), phi)
    # ct_a = np.dot(np.dot(phi.T, ct), phi) 減衰係数は各iで計算するため
    mt_a = np.dot(np.dot(phi.T, mt), phi)
    # 各モードについて、タイムステップ毎のfiを求める
    fit = np.zeros((nmode, total_step, 1))
    for i in range(nmode):
        fi = np.zeros((total_step, 1))
        for j in range(total_step):
            fi[j][0] = np.dot(phi.T[i], ft[j])
        fit[i] = fi
    # 各行の処理
    for i in range(nmode):
        # i行目について
        omegai = omega[i][0]
        ki = kt_a[i][i]
        mi = mt_a[i][i]
        ci = 2*mi*hc*omegai
        fi = fit[i]
        qi = np.zeros((total_step+1, 2)) # i個目modeのq
        # 振動方程式を解くloop
        for j in range(total_step):
            p_x = qi[j][0]
            p_v = qi[j][1]
            dvdt = -(ci/mi)*p_v - (ki/mi)*p_x + fi[j][0]/mi
            qi[j+1][1] = p_v+dvdt*delta_t
            qi[j+1][0] = p_x+p_v*delta_t
        for j in range(total_step+1):
            q[i][j][0] = qi[j][0]
       
    # 重ね合わせ
    output = np.zeros((nnode*2, total_step+1, 1))
    q_a = np.zeros((total_step+1, nmode, 1)) # total_step, nmode, 1の形のものを作る
    for i in range(nmode):
        for j in range(total_step+1):
            q_a[j][i][0] = q[i][j][0]
    delta = np.zeros((total_step+1, nnode*2, 1))
    for i in range(total_step+1):
        delta_i = np.dot(phi, q_a[i])
        delta[i] = delta_i
    # ノード毎で変位を見れるよう変更
    for i in range(total_step+1):
        for j in range(nnode*2):
            output[j][i][0] = delta[i][j][0]
    return output

# 外力生成(線形の増減)(中心4点に荷重がかかるとする)
ft = np.zeros((total_step, nnode, 1))
for i in range(load_step):
    ft[i+1][2300][0] = ft[i][2300][0] + load_diff
    ft[i+1][2400][0] = ft[i][2400][0] + load_diff
    ft[i+1][2500][0] = ft[i][2500][0] + load_diff
    ft[i+1][2600][0] = ft[i][2600][0] + load_diff
for i in range(load_step):
    ft[load_step+i+1][2300][0] = ft[load_step+i][2300][0] - load_diff
    ft[load_step+i+1][2400][0] = ft[load_step+i][2400][0] - load_diff
    ft[load_step+i+1][2500][0] = ft[load_step+i][2500][0] - load_diff
    ft[load_step+i+1][2600][0] = ft[load_step+i][2600][0] - load_diff
print(ft)