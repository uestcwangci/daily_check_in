# wechat_gongzhong.py
from concurrent.futures import ThreadPoolExecutor
from time import sleep

from appium.webdriver.common.appiumby import AppiumBy

from android import logger
from android.base_test import AppiumHelper


class WechatHelper:
    def __init__(self, udid):
        self.capabilities = dict(
            platformName='Android',
            automationName='uiautomator2',
            deviceName='Android',
            packageName='com.tencent.mm',
            appActivity='.ui.LauncherUI',
            unicodeKeyboard=True,
            resetKeyboard=True,
            noReset=True,
            forceAppLaunch=True,
            autoGrantPermissions=True,
            newCommandTimeout=300,  # 5分钟
            udid=udid
        )

        appium_server_url = 'http://localhost:4723'
        appium_helper = AppiumHelper(appium_server_url, self.capabilities)
        self.appium_helper = appium_helper
        self.udid = udid
        self.filename = 'wx_token.txt'
        self.stored_token = self._load_token()

    def _load_token(self):
        """读取存储的数据"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            return ''
        except Exception as e:
            print(f"读取文件失败: {e}")
            return ''

    def save_token(self, text):
        """保存数据"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                f.write(text)
            self.stored_token = text
            return True
        except Exception as e:
            print(f"保存失败: {e}")
            return False

    def get_book_list(self, official_account_name: str):
        try:
            wait_for_find = self.appium_helper.wait_for_find
            # 点击“通讯录”tab
            wait_for_find(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("com.tencent.mm:id/icon_tv").text("通讯录")').click()
            # 点击“公众号”
            wait_for_find(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("com.tencent.mm:id/sdg").text("公众号")').click()
            # 点击“搜索”
            wait_for_find(by=AppiumBy.ID, value='com.tencent.mm:id/fr').click()
            # 输入公众号名称
            wait_for_find(by=AppiumBy.ID, value='com.tencent.mm:id/d98').send_keys(official_account_name)
            # 等待搜索
            sleep(3)
            # 点击搜索
            wait_for_find(by=AppiumBy.ID, value='com.tencent.mm:id/phq').click()
            # 等待搜索结果
            sleep(5)
            # 点击第一个公众号
            self.appium_helper.driver.tab([(440, 358)])
            sleep(2)
            # 点击第一篇文章
            self.appium_helper.driver.tab([(450, 908)])
            sleep(2)
            # 点击右上角...
            self.appium_helper.driver.tab([(824, 90)])
            sleep(2)
            # 点击“复制链接”
            self.appium_helper.driver.tab([(808, 712)])
            sleep(2)
            # 获取剪贴板内容
            url_list = []
            url_list.append(self.appium_helper.driver.get_clipboard_text())
            # 返回
            self.appium_helper.driver.back()
            #
        except:
            return None
        finally:
            try:
                # 关闭应用
                self.appium_helper.driver.terminate_app(self.capabilities['packageName'])
            except Exception as e:
                logger.error(f"Error during app termination: {str(e)}")
                pass


def run_helper(udid):
    helper = WechatHelper(udid=udid)
    helper.get_book_list("阿里云")


if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=2) as executor:
        # 提交任务
        # future1 = executor.submit(run_helper, "10.0.0.51:5555")
        future2 = executor.submit(run_helper, "10.0.0.55:5555")

        # 等待任务完成
        # future1.result()
        future2.result()
