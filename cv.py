import cv2
import numpy as np

class Result:
    def __init__(self, image=None, match_loc=None):
        self.image = image
        self.match_loc = match_loc

class Finder:
    def __init__(self, templatefile: str) -> None:
        self.template = cv2.imread(templatefile)
        if self.template is None:
            raise ValueError(f"模板图像加载失败: {templatefile}")
        self.method = cv2.TM_CCOEFF_NORMED

    def search(self, image, threshold=0.8, isRGB=False):
        if image is None:
            raise ValueError("原始图像为空")

        h, w = self.template.shape[:2]

        result = cv2.matchTemplate(image, self.template, self.method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            match_loc = max_loc
            matched_region = image[match_loc[1]:match_loc[1]+h, match_loc[0]:match_loc[0]+w]

            if matched_region.shape[:2] != (h, w):
                return Result(image)

            if isRGB:
                template_mean_color = np.mean(self.template, axis=(0, 1))  # BGR
                region_mean_color = np.mean(matched_region, axis=(0, 1))
                color_diff = np.linalg.norm(region_mean_color - template_mean_color)
                if color_diff > 20.0:
                    # print(f"图案匹配但颜色不同（color_diff={color_diff:.2f}），忽略")
                    return Result(image)

            # 匹配成功，画框
            right_bottom = (match_loc[0] + w, match_loc[1] + h)
            cv2.rectangle(image, match_loc, right_bottom, (0, 255, 0), 2)
            return Result(image, match_loc)

        return Result(image)