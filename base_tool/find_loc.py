import time
from base_tool.get_matches import get_matches, get_wait_matches

class get_mul_matches():
    def __init__(self, AndroidDevice, json_reader):
        self.device = AndroidDevice
        self.json = json_reader

    def get_and_clik(self,target_names,beijing_name=None,maskname=None,thresholds=[0.7],time_out=5):
        time.sleep(2)
        dian,parms= get_wait_matches(beijingjson=self.json, targetjson=self.json,
                                               device=self.device,
                                               target_names=target_names, beijing_name=beijing_name,
                                               maskname=maskname, stop_on_first_match=True, thresholds=thresholds, time_out=time_out)
        if dian != [0]:
            time.sleep(2)
            if self.device.tap_on_screen(dian[0]):
                time.sleep(2)
                return True
            else:
                return False

        else:
            print('未找到需要点击的点')
            return False
    def get_wait(self,target_names,beijing_name=None,maskname=None,thresholds=[0.7],time_out=5):
        time.sleep(2)
        dian, parms = get_wait_matches(beijingjson=self.json, targetjson=self.json,
                                       device=self.device,
                                       target_names=target_names, beijing_name=beijing_name,
                                       maskname=maskname, stop_on_first_match=True, thresholds=thresholds,
                                       time_out=time_out)
        if dian != [0]:
            return True
        else:
            return False




