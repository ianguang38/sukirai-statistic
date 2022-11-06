#!/usr/bin/python
# -*- coding: UTF-8 -*-

from odbc import odbcInstance
from urllib import parse,request
from bs4 import BeautifulSoup
import threading
import re

def main(person,page):
    sem=threading.Semaphore(20)
    lock = threading.Lock()
    connect=odbcInstance()
    def run(n): 
        with sem:
            
            url="https://suki-kira.com/people/result/"+person+"/"+str(n)+"#toc"

            f=get_html()
            # f=get_html(beta=False,url=url)

            bs = BeautifulSoup(f, "html.parser")
            regex = re.compile('(?<=>)[^<]*(?=<)')
            li = bs.select('body > div > div > div > div > p')
            
            # if len(li)==0:
            #     print(f)
            #     with open("failed.html",mode="w",encoding="utf-8") as w:
            #         w.write(f)
            #     return

            print(len(li))
            print("start",n)
            for i in li:#每项是一条评论
                id=int(i.parent.contents[3].contents[0].string[:-1])
                support="text-danger" in i.parent.contents[3]["class"]
                comment_list=regex.findall(str(i))
                ref=None
                if len(comment_list)>1 and re.match("&gt;&gt;",comment_list[1]):
                    ref=int(comment_list.pop(1)[8:])
                comment="".join(comment_list)
                time=i.parent.contents[3].contents[3].string
                print(id)
                print(ref)
                print(time)
                print(support)
                print(comment)
                print("---------------------------------------")
                insert_comment(
                    parse.unquote(person),
                    id,ref,support,comment,time
                )

                
            # with lock:
            #     print("success ",n)
            print("success ",n)
    def get_html(beta=True,url=None):
        if beta:
            # ff=open("download.html",mode="r",encoding="utf-8")
            ff=open("download.html",mode="r",encoding="utf-8")
            f=ff.read()
            ff.close()
        else:
            header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}
            req = request.Request(url, headers=header)
            f =request.urlopen(req).read().decode("utf-8")
        return f
    def insert_comment(person,cid,ref,support,comment,time):
        print("insert",cid)
        sql = '''
            INSERT INTO comment_data (person,cid,ref,support,comment,time)
                VALUES (%s,%s,%s,%s,%s,%s)
            '''                           
        try:           
            connect.update(sql,(person,cid,ref,support,comment,time))
        except Exception as e:
            print("!!ERROR!!",e)

    for n in range(page[0],page[1]):
        threading.Thread(target=run(n))
           


if __name__ == '__main__':
    # main(parse.quote("黛灰(VTuber)"),(1,200))
    main(parse.quote("剣持刀也"),(1000,10000))
    