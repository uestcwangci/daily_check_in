# dianwang.py
from datetime import datetime

from android import logging
from time import sleep

from appium.webdriver.common.appiumby import AppiumBy
from android.base_test import AppiumHelper
from concurrent.futures import ThreadPoolExecutor
from android.base_qiandao_helper import QianDaoHelper


class DianWangHelper(QianDaoHelper):
    def __init__(self, udid='10.0.0.51:5555'):
        super().__init__(appPackage='com.sgcc.wsgw.cn', appActivity='com.sgcc.wsgw.rnbundle.activity.HomeReactActivity', udid=udid)

    def qian_dao(self):
        wait_for_find = self.appium_helper.wait_for_find
        wait_for_finds = self.appium_helper.wait_for_finds
        try:
            # 点击设备按钮
            sleep(2)
            # 点击“签到”按钮
            wait_for_find(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("签到")').click()
            logging.info(f"{self.udid} 电网签到成功")
            # 返回
            sleep(5)
            self.appium_helper.driver.back()
            self.appium_helper.driver.back()
            self.appium_helper.driver.activate_app(self.appium_helper.driver.capabilities["appPackage"])
            sleep(2)
            # 点击“签到”按钮
            wait_for_find(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("签到")').click()
            sleep(10)
            # 计算今天是不是当月的第8天、第15天、第21天、第28天
            if datetime.now().day == 8:
                # 点击第8天抽奖按钮
                self.appium_helper.driver.tap([(114, 1080)])
                logging.info(f"{self.udid} 第8天抽奖成功")
            elif datetime.now().day == 15:
                # 点击第15天抽奖按钮
                self.appium_helper.driver.tap([(273, 1080)])
                logging.info(f"{self.udid} 第15天抽奖成功")
            elif datetime.now().day == 21:
                # 点击第21天抽奖按钮
                self.appium_helper.driver.tap([(432, 1080)])
                logging.info(f"{self.udid} 第21天抽奖成功")
            elif datetime.now().day == 28:
                # 点击第28天抽奖按钮
                self.appium_helper.driver.tap([(591, 1080)])
                logging.info(f"{self.udid} 第28天抽奖成功")
            sleep(5)
        except Exception as e:
            logging.error(f"Error during qian_dao: {e}")
            raise e
        finally:
            # 退出
            try:
                self.appium_helper.driver.terminate_app(self.appium_helper.driver.capabilities["appPackage"])
                self.appium_helper.driver.quit()
            except Exception as e:
                pass


def run_helper(udid):
    helper = DianWangHelper(udid=udid)
    helper.qian_dao()


if __name__ == '__main__':

    with ThreadPoolExecutor(max_workers=2) as executor:
        # 提交任务
        future1 = executor.submit(run_helper, "10.0.0.51:5555")

        # 等待任务完成
        future1.result()
