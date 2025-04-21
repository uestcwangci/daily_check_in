from concurrent.futures import ThreadPoolExecutor
from android.longhu import LongHuHelper
from android.dianwang import DianWangHelper
from android.base_qiandao_helper import QianDaoHelper

def run_helper(udid):
    longhu_helper = LongHuHelper(udid)
    dianwang_helper = DianWangHelper(udid)
    longhu_helper.qian_dao()
    dianwang_helper.qian_dao()


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=2) as executor:
        # 提交任a务
        future1 = executor.submit(run_helper, "10.0.0.51:5555")
        # future2 = executor.submit(run_helper, "localhost:5556")

        # 等待任务完成a'a
        future1.result()
        # future2.result()