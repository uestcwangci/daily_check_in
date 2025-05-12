import functools
from concurrent.futures import ThreadPoolExecutor
from android.longhu import LongHuHelper
from android.dianwang import DianWangHelper
from android.huazhu import HuaZhuHelper
from android import logging



def retry_qiandao(times=2):
    """
    A decorator that retries the qian_dao method specified number of times
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args):
            for _ in range(times):
                try:
                    return func()
                except Exception as e:
                    logging.warning(f"Retry failed for {func.__name__} on {args[0].__class__.__name__}: {e}")
                    continue
            raise Exception(f"Failed to execute {func.__name__} on {args[0].__class__.__name__} after {times} attempts")

        return wrapper

    return decorator


def run_helper(udid):
    # 逐一实例化和执行，避免初始化副作用
    helper_classes = [LongHuHelper, DianWangHelper, HuaZhuHelper]

    for helper_class in helper_classes:
        logging.info(f"Initializing and running qian_dao for {helper_class.__name__}")
        try:
            # 实例化 Helper
            helper = helper_class(udid)
            # 应用重试装饰器到子类的 qian_dao 方法
            decorated_qian_dao = retry_qiandao()(helper.qian_dao)
            # 执行 qian_dao
            decorated_qian_dao(helper)
            logging.info(f"Finished qian_dao for {helper_class.__name__}")
        except Exception as e:
            logging.error(f"Failed qian_dao for {helper_class.__name__}: {e}")


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=1) as executor:
        future1 = executor.submit(run_helper, "10.0.0.51:5555")
        # 如果需要多设备并发，可以取消注释
        # future2 = executor.submit(run_helper, "localhost:5556")
        future1.result()
        # future2.result()