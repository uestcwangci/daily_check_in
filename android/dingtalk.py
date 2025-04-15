# dingtalk.py
from time import sleep

from appium.webdriver.common.appiumby import AppiumBy
from android.base_test import AppiumHelper
from concurrent.futures import ThreadPoolExecutor


class DingTalkHelper:
    def __init__(self, udid):
        capabilities = dict(
            platformName='Android',
            automationName='uiautomator2',
            deviceName='Android',
            appPackage='com.alibaba.android.rimet',
            appActivity='.biz.LaunchHomeActivity',
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

    def _enter_chat(self, chat_type: str, value: str):
        """
        进入聊天（单聊或群聊）
        chat_type: "contact（联系人）" || "group（群组） || "workapp（工作台）"
        value: 搜索的名称
        """
        # 回到首页
        self.appium_helper.call_jsapi("internal.automator", "navigateToHome")
        sleep(2)

        # 点击搜索按钮
        self.appium_helper.wait_for_find(AppiumBy.ID, "com.alibaba.android.rimet:id/search_btn").click()

        # 根据类型选择不同的标签
        tab_text = "联系人" if chat_type == "contact" else "群组"
        self.appium_helper.wait_for_find(by=AppiumBy.ANDROID_UIAUTOMATOR, value=f'new UiSelector().resourceId("com.alibaba.android.rimet:id/tv_name").fromParent(new UiSelector().text("{tab_text}"))', timeout=5).click()

        # 输入搜索内容
        self.appium_helper.wait_for_find(by=AppiumBy.ID, value="android:id/search_src_text", timeout=15).send_keys(value)

        # Native页面
        # 点击第一个搜索结果
        self.appium_helper.wait_for_find(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
            value='new UiSelector().resourceId("com.alibaba.android.rimet:id/list_view").childSelector(new UiSelector().index(1))',
            timeout=15
        ).click()

    def ri_cheng(self, key):
        try:
            wait_for_find = self.appium_helper.wait_for_find
            wait_for_finds = self.appium_helper.wait_for_finds
            # 进入单聊
            self._enter_chat("contact", key)
            # 点击“聊天设置”
            wait_for_find(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("聊天设置")').click()
            # 点击头像
            wait_for_find(AppiumBy.ID, 'com.alibaba.android.rimet:id/new_tv_avatar_oto').click()
            # 截图
            zhuangtai_png =  self.appium_helper.driver.get_screenshot_as_png()
            # 点击“他的日程”
            wait_for_find(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("他的日程")').click()
            sleep(3)
            # 截图
            richeng_png =  self.appium_helper.driver.get_screenshot_as_png()
        except:
            pass
        finally:
            try:
                self.appium_helper.driver.terminate_app(self.appium_helper.driver.capabilities["appPackage"])
                self.appium_helper.driver.quit()
            except Exception as e:
                pass


if __name__ == '__main__':
    helper = DingTalkHelper(udid="DingTalkHelper")
    helper.ri_cheng()

