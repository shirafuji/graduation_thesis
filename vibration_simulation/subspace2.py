import numpy as np
import numpy.linalg as LA

def subspace(k,m,n,neig):
    loop_count = 0
    ramda = np.zeros((neig,1)) #初期固有値
    x = np.random.rand(n,neig) #初期固有ベクトル
    y = np.zeros((n, neig))
    k = np.matrix(k)
    k_inv = np.linalg.inv(k)
    for i in range(50):
        loop_count += 1
        ramold = ramda.copy()
        y = np.dot(np.dot(k_inv,m),x)
        kg = np.dot(np.dot(y.T, k), y)
        mg = np.dot(np.dot(y.T, m), y)
        mg = mg + np.eye(neig)*0.01
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
        if max_mod < 0.0001:
            break

    return ramda, x, loop_count

k = [[2,-1,0],[-1,2,-1],[0,-1,1]]
m = [[2,0,0],[0,2,0],[0,0,1]]
n = 3
neig = 3
ramda, x, loop_count = subspace(k, m, n, neig)
print(ramda)
print(1/ramda[0][0])
print(1/ramda[1][0])
print(x)
print(loop_count)