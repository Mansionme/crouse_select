# This is a sample Python script.
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import threading
'''
需要先配置selenium，方法见Baidu
需要一次选多个课程时需要用多线程方法，不过我没写
目前仅仅在校园网连接情况下正常使用，没有校园网时会转到CAS，登录逻辑不一样，这块还没写呢
'''

#浏览器驱动配置，这里使用的是Chrome，使用时要注意浏览器驱动是否下载
chorm_options = Options()
chorm_options.add_argument('--headless')   #无头模式
dr = webdriver.Chrome(options=chorm_options)
id = input("输入的学号")
pwd = input("输入密码")

def login():
    try:
        dr.get('http://jwcnew.nefu.edu.cn/dblydx_jsxsd/')  #仅在本学校有效
        dr.find_element_by_xpath('//*[@id="Form1"]/div/div/div[2]/div[1]/div[2]/input[1]').send_keys(str(id))
        dr.find_element_by_xpath('//*[@id="pwd"]').send_keys(str(pwd))
        dr.find_element_by_xpath('//*[@id="btnSubmit"]').click()
        print("登录成功 %s"% time.ctime())
        time.sleep(2) #登录成功延时2s
    except Exception as e:
        print(str(e))
        print("检查账号密码")
    return dr

def getAllId(webpage):
    dr = login()
    dr.get(webpage)
    element = dr.find_element_by_css_selector('#divFrmLeft')
    tr = element.find_elements_by_xpath("//tr[contains(@id,'xk')]")
    id_list = []
    crouse_list = []
    name_list = []
    for td in tr:
        id_list.append(td.get_attribute("id"))
        crouse_list.append(td.text)
    for name in crouse_list:
        name_list.append(name.split()[4])  #获得所有课程名字
    name_id_dict = dict(zip(name_list,id_list))  #课程：课程代码键值对
    return name_id_dict

def select_crouse(webpage,name):
    dr = login()
    dr.get(webpage)
    data = getAllId(webpage)
    flag = False
    try:
        data[name]
        print("查询成功，正在选%s这门课 %s"%(name,time.ctime()))
        flag = True
    except:
        print("查询失败,请确认该页面是否有该课程")
        flag = False
    try:
        while (flag):
            dr.find_element_by_xpath('//*[@id="%s"]/td[1]/a'%data[name]).click()
            alert = dr.switch_to.alert
            alert.accept()
            time.sleep(1) #等待下一个alert弹出
            tip = dr.switch_to.alert
            if (tip.text == '选课成功！'):
                break
            print(tip.text+time.ctime())
            tip.accept()

        dr.close()
    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    website = input("输入需要爬取的地址")
    name = input("输入需要抢课的课程名")
    select_crouse(website, name)
