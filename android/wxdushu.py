# wxdushu.py
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from typing import Tuple, List

from appium.webdriver.applicationstate import ApplicationState
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.wait import WebDriverWait

from android import logger
from android.base_test import AppiumHelper


def get_book_articles(access_token: str, book_id: str, offset: int = 0, count: int = 20) -> dict:
    """
    获取书籍文章列表，缓存24小时有效

    Args:
        access_token: 访问令牌
        book_id: 书籍ID
        offset: 偏移量，默认36
        count: 获取数量，默认20

    Returns:
        dict: 响应数据
    """
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cache_dir = os.path.join(current_dir, "cache")
    cache_file = os.path.join(cache_dir, f"{book_id}.json")

    # 检查缓存是否存在且有效
    try:
        if os.path.exists(cache_file):
            with open(cache_file, 'r', encoding='utf-8') as f:
                cached_data = json.load(f)
                # 检查缓存是否过期（24小时 = 86400秒）
                if time.time() - cached_data.get('cache_timestamp', 0) < 86400:
                    return cached_data['data']
    except Exception as e:
        print(f"读取缓存失败: {e}")

    url = "https://i.weread.qq.com/book/articles"
    # 设置请求头
    headers = {
        "accessToken": access_token,
        "vid": "919746777",
        "baseapi": "31",
        "appver": "9.3.0.10165975",
        "User-Agent": "WeRead/9.3.0 WRBrand/other Dalvik/2.1.0 (Linux; U; Android 12; wuying android12 Build/1.6.1_localgpu_gpu_1727_20250103)",
        "osver": "12",
        "channelId": "11",
        "basever": "9.3.0.10165973",
        "Host": "i.weread.qq.com"
    }

    # 设置请求参数
    params = {
        "count": count,
        "offset": offset,
        "bookId": book_id,
        "synckey": 1747794180
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # 检查请求是否成功

        # 创建缓存目录
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        # 准备缓存数据（添加时间戳）
        cache_data = {
            'cache_timestamp': time.time(),
            'data': response.json()
        }

        # 写入缓存文件
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=4)

        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None


import requests
import base64


def encode_image(image_path):
    # 读取并编码图片为base64
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def send_image_request(image_path):
    # OpenAI API endpoint
    url = "https://idealab.alibaba-inc.com/api/openai/v1/chat/completions"

    # 你的API密钥
    api_key = "bbc6f66d28ea4f2da34d993c7fb6340e"

    # 获取base64编码的图片
    base64_image = encode_image(image_path)

    # 准备请求头
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # 准备请求体
    payload = {
        "model": "claude37_sonnet",  # 使用支持视觉的模型
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "这个图片是一个人机校验的图片(720*1280)(w*h)，要选出和描述相符的图片，可能是一个或者多个，你需要返回符合的图片的坐标的中心点，坐标格式为：[[x1,y1],[x2,y2]...]，其他内容不用返回"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 129024
    }

    try:
        # 发送POST请求
        response = requests.post(url, headers=headers, json=payload)

        # 检查响应状态
        response.raise_for_status()

        # 获取响应结果
        result = response.json()

        # 打印结果
        print(result)

        # 提取AI的回答
        if 'choices' in result and len(result['choices']) > 0:
            answer = result['choices'][0]['message']['content']
            print("\nAI's response:", answer)
            return answer

    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


class DuShuHelper:
    def __init__(self, udid):
        capabilities = dict(
            platformName='Android',
            automationName='uiautomator2',
            deviceName='Android',
            unicodeKeyboard=True,
            resetKeyboard=True,
            noReset=True,
            forceAppLaunch=True,
            autoGrantPermissions=True,
            disableIdLocatorAutocompletion=True,
            newCommandTimeout=300,  # 5分钟
            udid=udid
        )

        appium_server_url = 'http://localhost:4723'
        appium_helper = AppiumHelper(appium_server_url, capabilities)
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

    def launch_app(self, app_package: str, app_activity: str) -> None:
        """
        打开指定应用。
        """
        # 综合检查应用状态
        try:
            # 检查应用状态
            app_state = self.appium_helper.driver.query_app_state(app_package)
            if app_state in [ApplicationState.NOT_RUNNING, ApplicationState.NOT_INSTALLED]:
                logger.info(f"App is not running (state: {app_state}), starting it")
                self.appium_helper.driver.activate_app(app_package)
                return

            # 尝试获取当前activity
            try:
                current_activity = self.appium_helper.driver.current_activity
                if not current_activity:
                    logger.info("App might be starting, skipping home action")
                    return
            except Exception:
                logger.info("Unable to get current activity, app might be starting")
                return

            # 执行重启操作
            self.appium_helper.driver.terminate_app(app_package)
            self.appium_helper.driver.activate_app(app_package)

        except Exception as e:
            logger.warning(f"Error during home operation: {str(e)}")
            # 如果出错，尝试直接启动应用
            try:
                self.appium_helper.driver.activate_app(app_package)
            except Exception as e2:
                logger.error(f"Failed to activate app: {str(e2)}")
                raise e

        # 等待主页面加载
        WebDriverWait(self.appium_helper.driver, timeout=30).until(
            lambda driver: driver.current_activity == app_activity)
        time.sleep(1)  # 等待页面完全加载

    def _get_access_token(self):
        try:
            wait_for_find = self.appium_helper.wait_for_find
            # 先启动"HttpCanary"工具
            self.launch_app("com.guoshi.httpcanary", ".ui.HomeActivity")
            # 检查当前是否是抓包状态
            if not wait_for_find(by=AppiumBy.ID, value="com.guoshi.httpcanary:id/id0036").text=="抓包中...":
                # 点击“开始抓包”按钮
                wait_for_find(by=AppiumBy.ID, value="com.guoshi.httpcanary:id/id00ac").click()
                sleep(1)
            # 启动“微信读书”APP
            self.launch_app("com.tencent.weread", ".LauncherActivity")
            sleep(2)
            # 点击搜索框
            self.appium_helper.driver.tap([(293, 85)])
            # 搜索框中填入"aliyun"
            wait_for_find(by=AppiumBy.ID, value="id_searchTextInput").send_keys("aliyun")
            # 切换到公众号tab
            wait_for_find(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("id_searchResultTabBar").childSelector(new UiSelector().text("公众号"))').click()
            sleep(5)
            self.check_machine(wait_for_find)
            # 点击第一个公众号
            self.appium_helper.driver.tap([(220, 277)])
            self.check_machine(wait_for_find)
            # 切换到“HttpCanary”工具
            self.appium_helper.driver.activate_app("com.guoshi.httpcanary")
            sleep(1)
            # 随便找一个200OK的请求
            wait_for_find(by=AppiumBy.ID, value="com.guoshi.httpcanary:id/id00b5").click()
            sleep(1)
            # 点击“请求”按钮
            wait_for_find(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("com.guoshi.httpcanary:id/id00d4").childSelector(new UiSelector().text("请求"))').click()
            # 点击accessToken按钮
            wait_for_find(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().textContains("accessToken")').click()
            # 获取accessToken
            access_token = wait_for_find(by=AppiumBy.ID, value="android:id/message").text
            return access_token
        except:
            return None
        finally:
            try:
                # 关闭“HttpCanary”工具
                self.appium_helper.driver.terminate_app("com.guoshi.httpcanary")
                # 关闭“微信读书”APP
                self.appium_helper.driver.terminate_app("com.tencent.weread")
            except Exception as e:
                logger.error(f"Error during app termination: {str(e)}")
                pass

    def check_machine(self, wait_for_find):
        for i in range(3):
            # 如果触发了人机校验
            try:
                wait_for_find(by=AppiumBy.ID, value='com.tencent.weread:id/tcaptcha_container', timeout=5)
                self.appium_helper.driver.get_screenshot_as_file("screenshot.png")
                coordinates = send_image_request("screenshot.png")
                # 先解析成列表
                points: List[Tuple[int, int]] = [(x[0], x[1]) for x in json.loads(coordinates)]
                # 逐个点击每个坐标点，每次点击间隔1秒
                for point in points:
                    self.appium_helper.driver.tap([point])
                    time.sleep(1)  # 延时1秒
                self.appium_helper.driver.tap([(585, 869)])
            except:
                continue

    def get_book_data(self, book_id):
        book_data = get_book_articles(self.stored_token, book_id)
        # if not book_data:
        #     access_token = self._get_access_token()
        #     logger.info(f"获取到的access_token: {access_token}")
        #     self.save_token(access_token)
        #     book_data = get_book_articles(access_token, book_id)
        logger.info(f"获取到的书籍数据: {book_data}")
        return book_data



def run_helper(udid):
    helper = DuShuHelper(udid=udid)
    helper.get_book_data("MP_WXS_2398221140")


if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=2) as executor:
        # 提交任务
        # future1 = executor.submit(run_helper, "10.0.0.51:5555")
        future2 = executor.submit(run_helper, "10.0.0.51:5555")

        # 等待任务完成
        # future1.result()
        future2.result()
