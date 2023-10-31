# -*-coding:utf-8-*-
# @Time    :2023/10/3015:59
# @Author  :DWL
# @Email   :1419007050@qq.com
# @File    :action.py
# @Software:PyCharm
import unittest
import HTMLTestRunnerNew

if __name__ == '__main__':
    con = unittest.TestLoader().discover('.', pattern='practre.py')

    with open('Log.html', 'wb') as f:
        runner = HTMLTestRunnerNew.HTMLTestRunner(f, 2, tester='Dany', title='考试', description='这是一考试')
        runner.run(con)
