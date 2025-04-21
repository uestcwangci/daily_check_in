from android.base_test import AppiumHelper
from abc import ABC, abstractmethod

class QianDaoHelper:
    def __init__(self, appPackage, appActivity, udid):
        capabilities = dict(
            platformName='Android',
            automationName='uiautomator2',
            deviceName='Android',
            appPackage=appPackage,
            appActivity=appActivity,
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
        self.udid = udid

    @abstractmethod
    def qian_dao(self):
        pass

