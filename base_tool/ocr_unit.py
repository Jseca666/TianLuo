from networkx.classes.filters import show_nodes
from paddleocr import PaddleOCR

from base_tool.link_head import calculate_distance


class Uocr:
    def __init__(self, flag):
        if flag==1:
            self.use_angle_cls=True
            self.lang='ch'
            det_model_dir ='tool/ocr_modes/det/ch/ch_PP-OCRv4_det_infer'
            rec_model_dir = 'tool/ocr_modes/rec/ch/ch_PP-OCRv4_rec_infer'
            cls_model_dir = 'tool/ocr_modes/cls/ch_ppocr_mobile_v2.0_cls_infer'
            self.OCR=PaddleOCR( lang=self.lang,show_log=False,det_model_dir=det_model_dir,rec_model_dir=rec_model_dir,
                                cls_model_dir=cls_model_dir)
        # elif flag==0:
        #     self.use_angle_cls = False
        #     self.lang = 'en'
        #     det_model_dir = 'base_tool/ocr_modes/det/en/en_PP-OCRv3_det_infer'
        #     rec_model_dir = 'base_tool/ocr_modes/rec/en/en_PP-OCRv4_rec_infer'
        #     cls_model_dir = 'ocr_modes/cls/ch_ppocr_mobile_v2.0_cls_infer'
        #     self.OCR = PaddleOCR( lang=self.lang, show_log=False,det_model_dir=det_model_dir,rec_model_dir=rec_model_dir,
        #                         cls_model_dir=cls_model_dir)
        else:
            raise ValueError("识别器初始化失败：flag 必须为 0 或 1")
    def SHIBIE(self,image):

        result=self.OCR.ocr(image)
        try:
            if result != []:
                return [line[1][0] for line in result[0]]
        except:
            print('识别失败')
            return None
    def get_ocr(self):
        return PaddleOCR(use_angle_cls=self.use_angle_cls, lang=self.lang,show_log=False)
    def total_shibie(self,image):
        result = self.OCR.ocr(image)
        try:
            if result != []:
                return result
        except:
            print('识别失败')
            return None


