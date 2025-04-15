# avatar.py
from time import sleep

from appium.webdriver.common.appiumby import AppiumBy
from android.base_test import AppiumHelper
from concurrent.futures import ThreadPoolExecutor


class AvatarHelper:
    def __init__(self, udid):
        capabilities = dict(
            platformName='Android',
            automationName='uiautomator2',
            deviceName='Android',
            appPackage='com.avatar.buyer.client',
            appActivity='com.avatar.module.main.ui.MainActivity',
            unicodeKeyboard=True,
            resetKeyboard=True,
            noReset=True,
            forceAppLaunch=True,
            autoGrantPermissions=True,
            newCommandTimeout=300,  # 5分钟
            udid=udid
        )

        appium_server_url = 'http://localhost:4723'
        appium_helper = AppiumHelper(appium_server_url, capabilities)
        self.appium_helper = appium_helper

    def qian_dao(self):
        wait_for_find = self.appium_helper.wait_for_find
        wait_for_finds = self.appium_helper.wait_for_finds
        # 点击“我”按钮
        wait_for_find(AppiumBy.ID, "com.avatar.buyer.client:id/rb_space").click()
        # 点击“任务中心”按钮
        wait_for_find(AppiumBy.ID, "com.avatar.buyer.client:id/rl_task_center").click()
        sleep(3)
        # 如果有广告弹窗，点击关闭
        self.appium_helper.click(358, 1057)
        sleep(3)
        # 点击开下收下
        self.appium_helper.click(367, 852)
        try:
            self.appium_helper.driver.terminate_app(self.appium_helper.driver.capabilities["appPackage"])
            self.appium_helper.driver.quit()
        except Exception as e:
            pass


def run_helper(udid):
    helper = AvatarHelper(udid=udid)
    helper.qian_dao()


if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=2) as executor:
        # 提交任务
        future1 = executor.submit(run_helper, "10.0.0.51:5555")

        # 等待任务完成
        future1.result()
