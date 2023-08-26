from Encryption_single import *

"""Scramble decryption"""



def PWLCM(feature_num, XList, YList, x0, B, t0):
    for i in range(0, feature_num):
        N = len(XList[i])
        xi = x0
        Li, RcLi = [], []
        for s in range(0, t0 + N):
            if 0 <= xi < B:
                xi = xi / B
            elif B <= xi < 0.5:
                xi = (xi - B) / (0.5 - B)
            elif 0.5 <= xi < 1 - B:
                xi = (1 - B - xi) / (0.5 - B)
            else:
                xi = (1 - xi) / B
            Li.append(xi)
        cLi = Li[t0:]
        for j in cLi:
            x = int(N * j) % N
            RcLi.append(x)
        #  X coordinate decryption
        r = 1
        for j in reversed(RcLi):
            XList[i][j], XList[i][N - r] = XList[i][N - r], XList[i][j]
            r += 1
        #  Y coordinate decryption
        r = 1
        for n in reversed(RcLi):
            YList[i][n], YList[i][N - r] = YList[i][N - r], YList[i][n]
            r += 1
    return XList, YList

if __name__ == '__main__':
    fn_r = r"D:\Code-of-CEW\test1.shp"
    XLst, YLst, PLst, feature_num, X_sum, Y_sum = Read_XYPo_fromshp(fn_r)  # Read the vector data to be decrypted
    Xor, Yor = 0.45, 0.55
    a, t0 = 1.5, 1000
    x0, B, = 0.45, 0.25
    XList, YList=PWLCM(feature_num, XLst, YLst,  x0, B, t0)
    fn_w = r"D:\Code-of-CEW\jiemitest1.shp"
    Write_XYPo_toshp(fn_r, fn_w, XList, YList)  # Write out the decrypted vector data
    print("finish")
