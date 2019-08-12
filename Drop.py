
import re
import smtplib
import time
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from lxml import etree

from conf import *


def findDiscuss():

    array = []
    for i in range(3,20):
        response = requests.get("https://www.nowcoder.com/discuss?type=0&order=0&pageSize=30&expTag=0&page="+str(i),headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'} )
        selector = etree.HTML(response.text)
        clearfixs = selector.xpath("/html/body/div[1]/div[2]/div[2]/div/div[4]/ul/li")

        for clearfix in clearfixs:
            url = "https://www.nowcoder.com"+clearfix.xpath("./div[@class='discuss-detail']/div/a[1]/@href")[0]
            classes = clearfix.xpath("./div[@class='discuss-detail']/div/a[@class='tag-label']/text()")
            title = clearfix.xpath("./div[@class='discuss-detail']/div/a[1]/text()")
            result = getContent(url, title, classes)
            if(result):
                array.append(result)


def getContent(url,title,classes):
    response = requests.get(url,headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'})
    selector = etree.HTML(response.text)
    strs = selector.xpath("/html/body/div[1]/div[2]/div[2]/div[1]/div[2]")[0].xpath('string(.)')
    match = re.search(r'([0-9a-zA-Z_]+@[0-9a-zA-Z_]+\.[a-z]+)', strs)
    if match:
        email = match.group(0)
        title = ''.join(title).replace("\n", "")
        try:
            time.sleep(60)
            sent_email(to=email)
            print(title + " "+ email + " " +url+" 发送成功 ")
        except Exception as  e:
            print(e)
            print(title  + " "+ email+ " " +url + " 发送失败 ")




def sent_email(to):
    fromaddr = FROM
    toaddrs = [to]
    subject = SUBJECT
    msg = MIMEMultipart('alternative')
    msg['From'] = Header(fromaddr, 'utf-8')
    msg['To'] = Header(','.join(toaddrs), 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    html = CONTENT
    fp = open("./"+FILE_NAME, 'rb')
    HTML_Contents = MIMEText(html, 'html')
    attach = MIMEApplication(fp.read(), _subtype="pdf")
    fp.close()
    attach.add_header('Content-Disposition', 'attachment', filename=FILE_NAME)
    msg.attach(attach)
    msg.attach(HTML_Contents)
    username = FROM
    password = PASSWORD
    server = smtplib.SMTP_SSL(HOST, PORT)
    server.login(username, password)
    server.sendmail(fromaddr, toaddrs, msg.as_string())
    server.quit()


if __name__ == '__main__':
    findDiscuss()
    # sent_email("2039176261@qq.com")


