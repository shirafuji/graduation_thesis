# import
import numpy as np
import numpy.linalg as LA
import sys
import time

# 引数
args = sys.argv
defect_x = int(args[1]) + 1
defect_y = int(args[2]) + 1

print('start '+str(defect_x)+' '+str(defect_y))
start = time.time()

# 欠陥node特定(0始めでカウント)
base_node = defect_x + defect_y*51
defect_node = []
defect_node.append(base_node+1+51)
defect_node.append(base_node+1+51+1)
defect_node.append(base_node+1+51+1+1)
defect_node.append(base_node+1+51+1+1+1)
defect_node.append(base_node+1+51+51)
defect_node.append(base_node+1+51+51+1)
defect_node.append(base_node+1+51+51+1+1)
defect_node.append(base_node+1+51+51+1+1+1)
defect_node.append(base_node+1+51+51+51)
defect_node.append(base_node+1+51+51+51+1)
defect_node.append(base_node+1+51+51+51+1+1)
defect_node.append(base_node+1+51+51+51+1+1+1)
defect_node.append(base_node+1+51+51+51+51)
defect_node.append(base_node+1+51+51+51+51+1)
defect_node.append(base_node+1+51+51+51+51+1+1)
defect_node.append(base_node+1+51+51+51+51+1+1+1)
ndefect = len(defect_node)

# const
ele_size = 1/2*0.02*0.02
poi = 0.2
e = 1000000000*37
th = 1.0
row = 2400
delta_t = 0.00000008
pow_delta_t = delta_t*delta_t
total_time = 0.0005
total_step = int(total_time/delta_t)
load = 100 #外力最大値
load_time = 0.00001
load_step = int(load_time/delta_t)
load_diff = load/load_step
alpha = 0.58332

# ファイル読み込み:nodeとeleの設定
node_file = "twentyfive_holes_"+str(defect_x)+"_"+str(defect_y)+".1.node"
ele_file = "twentyfive_holes_"+str(defect_x)+"_"+str(defect_y)+".1.ele"
node_path = "../triangle_master/poly/"+node_file
ele_path = "../triangle_master/poly/"+ele_file
with open(node_path) as f_node:
    s_line = f_node.readline()
    number_list = s_line.split()
    nnode_str = number_list[0]
    nnode = int(nnode_str)
    position_with_defect = np.zeros((nnode, 2), dtype=np.float)
    for i in range(nnode):
        s_line = f_node.readline()
        number_list = s_line.split()
        x_str = number_list[1]
        y_str = number_list[2]
        x = float(x_str)
        y = float(y_str)
        position_with_defect[i][0] = x*0.02
        position_with_defect[i][1] = y*0.02
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

# 欠陥nodeの調整
nnode -= len(defect_node)
# 欠陥nodeを取り除いたposition作成
position = np.zeros((nnode, 2), dtype=np.float)
count = 0
for h in range(len(position_with_defect)-1):
    if h in defect_node:
        count = count + 1
    else:
        position[h-count] = position_with_defect[h]
    
# elesの番号を欠陥の分下げていく
for h in range(len(defect_node)):
    target_defect = defect_node[len(defect_node)-1-h]#0始めで何番目か、大きいものから処理を始める
    target_node_number = target_defect + 1#elesでは1始まりの番号が記録
    for hh in range(len(eles)):
        for hhh in range(3):
            if eles[hh][hhh] > target_node_number:
                eles[hh][hhh] -= 1

# 全体剛性行列と全体質量行列・全体集中質量行列の宣言
kt = np.zeros((2*nnode, 2*nnode))
mt = np.zeros((2*nnode, 2*nnode))
imt = np.zeros((2*nnode, 2*nnode))

# 剛性行列と質量行列計算の定義
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
    b=b/2/ele_size
    # 応力-ひずみ関係
    d = np.zeros((3, 3))
    d[0][0] = 1 - poi
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

def calc_ime(ele, imt):
    i = ele[0]
    j = ele[1]
    k = ele[2]
    ime = np.zeros((6, 6))
    for h in range(6):
        ime[h][h] = 1/3
    ime = ele_size*th*row*ime
    imt[2*i-1-1][2*i-1-1] += ime[1-1][1-1]
    imt[2*i-1][2*i-1] += ime[2-1][2-1]
    imt[2*j-1-1][2*j-1-1] += ime[3-1][3-1]
    imt[2*j-1][2*j-1] += ime[4-1][4-1]
    imt[2*k-1-1][2*k-1-1] += ime[5-1][5-1]
    imt[2*k-1][2*k-1] += ime[6-1][6-1]
    return imt

# 合成行列と質量行列の組み込み繰り返し
for h in range(nele):
    ele = eles[h]
    kt = calc_ke(ele, position, kt)
    mt = calc_me(ele, mt)
    imt = calc_ime(ele, imt)

# 外力生成(線形の増減)(左辺中心3点に荷重がかかるとする)(1辺51点)
ft = np.zeros((total_step, 2*(nnode), 1))
# 荷重点の取得
load_point1 = 0
load_point2 = 0
load_point3 = 0
for h in range(nnode):
    if position[h][0] == 0:
        if position[h][1] == 0.48:
            load_point1 = h
        if position[h][1] == 0.5:
            load_point2 = h
        if position[h][1] == 0.52:
            load_point3 = h
# 増える時
for i in range(load_step):
    ft[i+1][load_point1*2][0] = ft[i][load_point1*2][0] + load_diff
    ft[i+1][load_point2*2][0] = ft[i][load_point2*2][0] + load_diff
    ft[i+1][load_point3*2][0] = ft[i][load_point3*2][0] + load_diff
# 減る時
for i in range(load_step):
    ft[load_step+i+1][load_point1*2][0] = ft[load_step+i][load_point1*2][0] - load_diff
    ft[load_step+i+1][load_point2*2][0] = ft[load_step+i][load_point2*2][0] - load_diff
    ft[load_step+i+1][load_point3*2][0] = ft[load_step+i][load_point3*2][0] - load_diff
# 一辺50点の場合の外力(線形の増減)(左辺中心4点に荷重がかかるとする)
# ft = np.zeros((total_step, 2*(nnode), 1))
# for i in range(load_step):
#     ft[i+1][2300][0] = ft[i][2300][0] + load_diff
#     ft[i+1][2400][0] = ft[i][2400][0] + load_diff
#     ft[i+1][2500][0] = ft[i][2500][0] + load_diff
#     ft[i+1][2600][0] = ft[i][2600][0] + load_diff
# for i in range(load_step):
#     ft[load_step+i+1][2300][0] = ft[load_step+i][2300][0] - load_diff
#     ft[load_step+i+1][2400][0] = ft[load_step+i][2400][0] - load_diff
#     ft[load_step+i+1][2500][0] = ft[load_step+i][2500][0] - load_diff
#     ft[load_step+i+1][2600][0] = ft[load_step+i][2600][0] - load_diff

# タイムステップ毎の変位設定
u = np.zeros((total_step+1, 2*nnode, 1))
# 各タイムステップの計算
ct = imt*alpha
left_matrix = imt+delta_t*ct/2
inv_left_matrix = np.linalg.inv(left_matrix)
for h in range(total_step-1):
    step = h+1
    right_matrix = pow_delta_t*ft[step] - pow_delta_t*np.dot(kt, u[step]) + np.dot(imt, (2*u[step]-u[step-1])) + delta_t*np.dot(ct, u[step-1])/2
    u[step+1] = np.dot(inv_left_matrix, right_matrix)


# 書き出し
# アウトプットファイル
output_filename = 'twentyfive_holes_data.csv'
# path
output_path = './vibration_data/'+output_filename
# 内容
defect_size = 5
defect_position_x = defect_x + 2.5
defect_position_y = defect_y + 2.5
content = str(defect_size) + " " + str(defect_position_x) + " " + str(defect_position_y) + " "
#観測点
check_point1 = 0
check_point2 = 0
check_point3 = 0
for h in range(nnode):
    if position[h][0] == 0:
        if position[h][1] == 0.26:
            check_point1 = h
        if position[h][1] == 0.5:
            check_point2 = h
        if position[h][1] == 0.74:
            check_point3 = h
check_point = [check_point1, check_point2, check_point3] #一辺51点とったとき
for point in check_point:
    for h in range(total_step+1):
        if h%5 == 0:
            content += str(u[h][point*2][0]) + " "
content += "\n"
# 書き出し
f = open(output_path, 'a')
f.write(content)
f.close()

elapsed_time = time.time() - start
print(elapsed_time)
print('finish '+str(defect_x)+' '+str(defect_y))

# 今だけグラフ表示
# output2400 = []
# for h in range(total_step+1):
#     output2400.append(u[h][2400][0])
# from matplotlib import pyplot as plt
# time_list = []
# for h in range(total_step+1):
#     time_list.append(h*delta_t)
# plt.plot(time_list, output2400)
# plt.show()