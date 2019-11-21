import cv2
import glob
import numpy
import file_io

CALIB_FILES = "iphonex_calib/*.JPG"
CALIB_OUT = "calib.txt"
PREVIEW_WIDTH = 640
square_size = 1.0  # 正方形のサイズ
pattern_size = (10, 7)  # 模様のサイズ


def make_preview(img, width):
    fact = width / img.shape[1]
    img = cv2.resize(img, (0,0), None, fact, fact, interpolation=cv2.INTER_AREA)
    return img

pattern_points = numpy.zeros( (numpy.prod(pattern_size), 3), numpy.float32 ) #チェスボード（X,Y,Z）座標の指定 (Z=0)
pattern_points[:,:2] = numpy.indices(pattern_size).T.reshape(-1, 2)
pattern_points *= square_size
obj_points = []
img_points = []


files = glob.glob(CALIB_FILES)
files.sort()

for f in files:
    im = cv2.imread(f, 0)

    print(f)

    preview = make_preview(im, PREVIEW_WIDTH)

    # チェスボードのコーナーを検出
    found, corner = cv2.findChessboardCorners(im, pattern_size)
    # コーナーがあれば
    if found:
        term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1)
        cv2.cornerSubPix(im, corner, (5, 5), (-1, -1), term)
    # コーナーがない場合のエラー処理
    if not found:
        print ('chessboard not found')
        continue
    img_points.append(corner.reshape(-1, 2))  # appendメソッド：リストの最後に因数のオブジェクトを追加
    obj_points.append(pattern_points)
    # corner.reshape(-1, 2) : 検出したコーナーの画像内座標値(x, y)

    #cv2.imshow("f", preview)
    #cv2.waitKey()

# 内部パラメータを計算
K = None
d = None
rms, K, d, r, t = cv2.calibrateCamera(obj_points,img_points,(im.shape[1],im.shape[0]), K ,d)
# 計算結果を表示
print ("RMS = ", rms)
print ("K = \n", K)
print ("d = ", d.ravel())
print("f(焦点距離) = ",K[1][1], " pixels")
# 計算結果を保存
#numpy.savetxt("rms.csv", rms, delimiter =',',fmt="%0.14f")
#numpy.savetxt("K.csv", K, delimiter =',',fmt="%0.14f")

file_io.write_mat(CALIB_OUT, [K,d])

for f in files:
    im = cv2.imread(f)
    undis = make_preview(cv2.undistort(im, K, d), PREVIEW_WIDTH)
    cv2.imshow("undis", undis)
    cv2.waitKey()