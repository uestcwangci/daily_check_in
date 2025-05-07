# longhu.py
from android import logging
from time import sleep

from appium.webdriver.common.appiumby import AppiumBy
from concurrent.futures import ThreadPoolExecutor
from android.base_qiandao_helper import QianDaoHelper


class LongHuHelper(QianDaoHelper):
    def __init__(self, udid):
        super().__init__(appPackage='com.longfor.supera', appActivity='.main.MainActivity', udid=udid)

    def qian_dao(self):
        wait_for_find = self.appium_helper.wait_for_find
        wait_for_finds = self.appium_helper.wait_for_finds
        try:
            # 点击设备按钮
            sleep(2)
            # 点击“会员”按钮
            tabs = wait_for_finds(by=AppiumBy.ID, value="com.longfor.supera:id/tab_text")
            for tab in tabs:
                if '会员' in tab.text:
                    tab.click()
                    break
            # 向下滑动
            self.appium_helper.driver.swipe(400, 900, 400, 600)
            # 点击“抽奖按钮"
            sleep(2)
            wait_for_finds(by=AppiumBy.ID, value="com.longfor.supera:id/img_item")[1].click()
            # 向下滑动
            self.appium_helper.driver.swipe(400, 900, 400, 700)
            # 点击“点击抽奖”按钮
            sleep(2)
            wait_for_find(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("点击抽奖")').click()
            # 点击“去签到”按钮
            wait_for_find(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("去签到")').click()
            sleep(2)
            # 返回
            self.appium_helper.driver.back()
            # 再进入抽奖页面
            wait_for_finds(by=AppiumBy.ID, value="com.longfor.supera:id/img_item")[1].click()
            sleep(2)
            try:
                # 点击“点击抽奖”按钮
                wait_for_find(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("点击抽奖")').click()
                logging.info(f"{self.udid} 龙湖抽奖成功")
            except:
                self.appium_helper.click(360, 900)
                logging.info(f"{self.udid} 龙湖抽奖成功")
            sleep(10)
            # 返回
            self.appium_helper.driver.back()
            # 点击“签到”按钮
            wait_for_finds(by=AppiumBy.ID, value="com.longfor.supera:id/img_item")[0].click()
            logging.info(f"{self.udid} 龙湖签到成功")
            sleep(10)
        except Exception as e:
            logging.error(f"Error during qian_dao: {e}")
        finally:
            # 退出
            try:
                self.appium_helper.driver.terminate_app(self.appium_helper.driver.capabilities["appPackage"])
                self.appium_helper.driver.quit()
            except Exception as e:
                pass


def run_helper(udid):
    helper = LongHuHelper(udid=udid)
    helper.qian_dao()


if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=2) as executor:
        # 提交任务
        # future1 = executor.submit(run_helper, "10.0.0.51:5555")
        future2 = executor.submit(run_helper, "localhost:5556")

        # 等待任务完成
        # future1.result()
        future2.result()
