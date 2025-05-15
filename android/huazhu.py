# huazhu.py
from datetime import datetime

from android import logging
from time import sleep

from appium.webdriver.common.appiumby import AppiumBy
from android.base_test import AppiumHelper
from concurrent.futures import ThreadPoolExecutor
from android.base_qiandao_helper import QianDaoHelper


class HuaZhuHelper(QianDaoHelper):
    def __init__(self, udid='10.0.0.51:5555'):
        super().__init__(appPackage='com.htinns', appActivity='com.huazhu.main.RnMainActivity', udid=udid)

    def qian_dao(self):
        wait_for_find = self.appium_helper.wait_for_find
        wait_for_finds = self.appium_helper.wait_for_finds
        try:
            # 点击设备按钮
            sleep(2)
            # 点击“会员”按钮
            wait_for_find(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("会员")').click()
            # 点击“签到”按钮
            wait_for_find(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("签到")').click()
            sleep(10)
            # 去掉广告
            self.appium_helper.driver.tap([(230, 915)])
            sleep(5)
            # 向下滑动
            self.appium_helper.driver.swipe(400, 800, 400, 600, duration=1000)
            sleep(2)
            # 点击“签到”按钮
            self.appium_helper.driver.tap([(360, 1094)])
            logging.info(f"{self.udid} 华住签到成功")
            sleep(5)
            # 去广告
            self.appium_helper.driver.tap([(360, 804)])
            # 点击"立即抽奖"按钮
            self.appium_helper.driver.tap([(360, 435)])
            logging.info(f"{self.udid} 华住抽奖成功")
            sleep(5)
        except Exception as e:
            logging.error(f"Error during qian_dao: {e}")
            raise e
        finally:
            try:
                self.appium_helper.driver.terminate_app(self.appium_helper.driver.capabilities["appPackage"])
                self.appium_helper.driver.quit()
            except Exception as e:
                pass


def run_helper(udid):
    helper = HuaZhuHelper(udid=udid)
    helper.qian_dao()


if __name__ == '__main__':

    with ThreadPoolExecutor(max_workers=2) as executor:
        # 提交任务
        future1 = executor.submit(run_helper, "10.0.0.51:5555")

        # 等待任务完成
        future1.result()
