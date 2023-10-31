# -*-coding:utf-8-*-
# @Time    :2023/10/3014:36
# @Author  :DWL
# @Email   :1419007050@qq.com
# @File    :day10.30.py
# @Software:PyCharm
import unittest
import ddt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from parameterized import parameterized


# 测试手机发布会项目：
# 测试登录：
@ddt.ddt
class TestLog(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Edge()
        self.driver.get('http://127.0.0.1:8000/')
        self.driver.maximize_window()
        self.driver.implicitly_wait(20)

    def tearDown(self) -> None:
        self.driver.quit()

    @ddt.data(['admin', 'admin111', 0], ['admin', 'admin123456', 1])
    @ddt.unpack
    def test_log_in(self, name, password, status):
        self.driver.find_element(By.ID, 'inputUsername').send_keys(name)
        self.driver.find_element(By.ID, 'inputPassword').send_keys(password)
        self.driver.find_element(By.XPATH, '/html/body/div/form/button').click()

        if status == 0:
            con = self.driver.find_element(By.XPATH, '/html/body/div/form/p')
            self.assertIn(con.text, self.driver.page_source)
            print('输入有误，登录失败')

        else:
            print('登录成功')

#
# # 测试签到：
@ddt.ddt
class TestSign(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Edge()
        self.driver.get('http://127.0.0.1:8000/')
        self.driver.maximize_window()
        self.driver.implicitly_wait(20)
        self.driver.find_element(By.ID, 'inputUsername').send_keys('admin')
        self.driver.find_element(By.ID, 'inputPassword').send_keys('admin123456')
        self.driver.find_element(By.XPATH, '/html/body/div/form/button').click()
        self.driver.find_element(By.PARTIAL_LINK_TEXT, 'sign').click()
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def tearDown(self) -> None:
        self.driver.quit()

    @ddt.data(['153116722199', 0], ['15311672219', 1])
    @ddt.unpack
    def test_sign_num(self, num, ststus):

        self.driver.find_element(By.XPATH, '/html/body/div/div/div[1]/form/div/div[1]/input').send_keys(num)

        if ststus == 0:
            con = self.driver.find_element(By.XPATH, '/html/body/div/div/div[1]/div/font')
            self.assertIn(con.text, self.driver.page_source)
            print('手机号输入有误')

        elif ststus == 1:
            sign_buttn = self.driver.find_element(By.XPATH, '/html/body/div/div/div[1]/div/font')
            if self.assertIn(sign_buttn.text, self.driver.page_source):
                print('登录成功')
            else:
                print('无效按钮')


# 测试添加嘉宾
@ddt.ddt
class TestAddPeople(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Edge()
        self.driver.get('http://127.0.0.1:8000/')
        self.driver.maximize_window()
        self.driver.implicitly_wait(20)
        self.driver.find_element(By.ID, 'inputUsername').send_keys('admin')
        self.driver.find_element(By.ID, 'inputPassword').send_keys('admin123456')
        self.driver.find_element(By.XPATH, '/html/body/div/form/button').click()
        self.driver.find_element(By.PARTIAL_LINK_TEXT, '嘉宾').click()
        self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[2]/button').click()

    def tearDown(self) -> None:
        self.driver.quit()

    # 测试添加嘉宾时，是否从下拉框选择相应发布会以及邮箱是否填写正确
    @ddt.data(['123456789', '987654321@qq.com', '一二三', 0],   ['123456789', '987654321@qq', '一二三', 1],
              ['123456789', '987654321@qq.com', '一二三', 1])
    @ddt.unpack
    def test_se_lct0(self, phone, email, name, index):

        self.driver.find_element(By.ID, 'id_phone').send_keys(phone)
        self.driver.find_element(By.ID, 'id_email').send_keys(email)
        self.driver.find_element(By.ID, 'id_realname').send_keys(name)
        self.driver.find_element(By.ID, 'id_sign').click()
        self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/form/div[7]/div/button').click()

        self.s = Select(self.driver.find_element(By.ID, 'id_event'))
        self.s.select_by_index(index)

        if index == 0:
            con = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/form/div[6]/div/p')
            self.assertIn(con.text, self.driver.page_source)
            print('请在下拉框中选择一项')

        elif index == 1 and email == '987654321@qq':
            con = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/form/div[6]/div/p')
            self.assertIn(con.text, self.driver.page_source)
            print('添加失败，请输入正确邮箱')
        else:
            print('添加成功')


if __name__ == '__main__':
    unittest.main(verbosity=2)