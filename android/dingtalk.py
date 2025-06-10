# dingtalk.py
from time import sleep

from appium.webdriver.common.appiumby import AppiumBy
from android.base_test import AppiumHelper
import logging
import os
import requests


# 设置日志记录器
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 创建一个文件处理器
# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 构建日志文件的绝对路径
log_path = os.path.join(current_dir, 'logs', 'alive.log')

# 确保logs目录存在
os.makedirs(os.path.dirname(log_path), exist_ok=True)

# 使用绝对路径创建文件处理器
file_handler = logging.FileHandler(log_path)
# 设置文件处理器的日志级别
file_handler.setLevel(logging.INFO)
# 创建一个日志格式器
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# 将文件处理器添加到logger
logger.addHandler(file_handler)

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

    def ri_cheng(self):
        try:
            wait_for_find = self.appium_helper.wait_for_find
            wait_for_finds = self.appium_helper.wait_for_finds
            sleep(10)
            # 进入群聊
            self.appium_helper.call_jsapi("biz.util", "openLink",
                                          {"url": "dingtalk://dingtalkclient/action/open_conversation?cid=46704611888"})
            # 点击“聊天设置”
            wait_for_find(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("群聊信息")').click()
            # 找到人数
            fraction = wait_for_find(AppiumBy.ID, 'com.alibaba.android.rimet:id/tv_conversation_mem_count_v2').text
            # 人数示例（1888/3000），截取出分子部分
            clean_fraction = fraction[1:-1]  # 移除首尾的括号
            numerator = int(clean_fraction.split('/')[0])
            # 格式化打印，按照YYYY-MM-DD HH + 人数的格式
            logger.info(f"{numerator}")
            sleep(2)
            # 发送webhook通知
            webhook_url = "https://connector.dingtalk.com/webhook/flow/1032272008132133f95a000c"
            try:
                response = requests.post(
                    webhook_url,
                    json={"count": numerator},
                    headers={"Content-Type": "application/json"}
                )
            except Exception as e:
                logger.error(f"发送钉钉Webhook请求失败: {str(e)}")
            return numerator
        except:
            pass
        finally:
            try:
                self.appium_helper.driver.terminate_app(self.appium_helper.driver.capabilities["appPackage"])
                self.appium_helper.driver.quit()
            except Exception as e:
                pass


if __name__ == '__main__':
    helper = DingTalkHelper(udid="10.0.0.51:5555")
    helper.ri_cheng()

