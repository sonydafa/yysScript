import cv2
import numpy as np
class Result():
    def __init__(self,image=None,match_loc=None) -> None:
        self.image=image
        self.match_loc=match_loc
class Finder():
    def __init__(self,templatefile:str) -> None:
        
        # 创建模板图像（需要被查找的目标）
        self.template = cv2.imread(templatefile)
        self.method = cv2.TM_CCOEFF_NORMED

    def search(self,image):
        # 加载原始图像
        



        # 设置匹配算法为TM_CCOEFF_NORMED

        # 对原始图像应用模板匹配算法
        result = cv2.matchTemplate(image, self.template, self.method)

        threshold = 0.8
        loc = np.where( result >= threshold)
        # 在原始图像上画出边界框
        min_max = cv2.minMaxLoc(result)
        if loc[0].size>0:
            match_loc = min_max[3] 
            right_bottom = (match_loc[0] + self.template.shape[1], match_loc[1] + self.template.shape[0]) 


            cv2.rectangle(image, match_loc,right_bottom, (0,255,0), 5, 8, 0 )

        # 显示包含匹配结果的图像
        # cv2.imshow('Matched Image', image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

            # cv2.imwrite('result.png',image)
            return Result(image,match_loc)
        else:
            # cv2.imwrite('result.png',image)

            return Result(image)