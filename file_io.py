import numpy as np

def write_mat(path, mat_list):
    with open(path, "w") as f:
        for mat in mat_list:
            #f.write("ndarray,"+"x".join(map(str,mat.shape))+"\n")
            if len(mat.shape) == 1:
                mat = mat[np.newaxis,:]
            #print(mat)
            serial = []
            for row in mat:
                serial.append( ",".join(map(str, row.tolist())) )

            f.write(" ".join(serial))
            f.write("\n")

def read_mat(path, type = np.float32):
    mats = []
    with open(path, "r") as f:
        for line in f:
            #print (line)
            line = line.strip()
            rows = line.split(" ")

            arr = []
            for row in rows:
                r = list(map(float,row.split(",")))
                arr.append(r)

            mat = np.array(arr)
            mats.append(mat)

    return mats




if __name__ == "__main__":
    m = np.array([[1,2,3],[4,5,6]])
    m2= np.array([0.1,0.2,0.3])

    #write_mat("test.csv", [m,m2])
    m = read_mat("test.csv")
    print(m)