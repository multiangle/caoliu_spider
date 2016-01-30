__author__ = 'multiangle'

#========================================================
#----------------import package--------------------------
# import python package
import urllib.request as request
import time
import random
import json
import re
import urllib
import os

# import from this folder
from bs4 import BeautifulSoup
import spider_config as config
#========================================================
class spider():
    def __init__(self):
        self.base_url=config.base_url
        # page=self.getData(self.base_url+'/index.php')
        # entry_url=self.parse_main_page(page)
        # page_num=2
        # page_url=entry_url[-3][1]+'&search=&page='+str(page_num)
        # flag_page=self.getData(page_url)
        # thread_link=self.parse_flag_page(flag_page,2)
        # thread_link='http://cl.eecl.me/htm_data/16/1601/1818777.html'
        # thread_page=self.getData(thread_link)
        # self.parse_thread_page(thread_page)

    def parse_main_page(self,page):
        soup=BeautifulSoup(page)
        url_list=[]
        # cate_1=soup.find_all('tbody',attrs={'id':'cate_1'})
        div_id_main=soup.find('div',attrs={'id':'main'})
        div_class_t=div_id_main.find_all('div',attrs={'class':'t'})[1]
        tr_class_tr3=div_class_t.find_all('tr',attrs={'class':'tr3'})
        for item in tr_class_tr3:
            cell=[]
            h2=item.find('h2')
            cell.append(h2.text)
            temp_a=h2.find('a')
            url=config.base_url+'/'+temp_a['href']
            cell.append(url)
            url_list.append(cell)
        div_class_t2=div_id_main.find_all('div',attrs={'class':'t'})[2]
        tr_class_tr3=div_class_t2.find_all('tr',attrs={'class':'tr3'})
        for item in tr_class_tr3:
            cell=[]
            h2=item.find('h2')
            cell.append(h2.text)
            temp_a=h2.find('a')
            url=config.base_url+'/'+temp_a['href']
            cell.append(url)
            url_list.append(cell)
        return url_list

    def parse_flag_page(self,page,page_num):
        # 解析达盖尔的旗帜
        soup=BeautifulSoup(page)
        div_id_main=soup.find('div',attrs={'id':'main'})
        div_class_t=div_id_main.find_all('div',attrs={'class':'t'})[1]
        tr_class_tr3=div_class_t.find_all('tr',attrs={'class':'tr3'})
        if page_num==1:
            start_line=12
            end_line=tr_class_tr3.__len__()-2
        else:
            start_line=0
            end_line=tr_class_tr3.__len__()-2

        page_data=[]
        for i in range(start_line,end_line+1):
            line=tr_class_tr3[i]
            data=line
            cell={}
            td=data.find_all('td')
            h3=td[1].find('h3')
            a=h3.find('a')
            url=config.base_url+'/'+a['href']
            cell['title']=h3.text
            cell['link']=url
            span=td[1].find('span')
            try:
                ret_page_num=int(span.find_all('a')[-1].text)
                cell['ret_page_num']=ret_page_num
            except:
                pass
            cell['author']=td[2].find('a').text
            cell['ret_num']=int(td[3].text)
            page_data.append(cell)
        return  page_data

    def deal_thread(self,url):
        page=self.getData(url)
        page_info=self.parse_thread_page(page)
        pic_url=page_info['pic_url']
        title=page_info['title']
        base_dir='E:\\multiangle\\Coding!\\python\\caoliu_spider\\pic'
        dir=base_dir+'\\'+title
        os.mkdir(dir)
        for i in range(0,pic_url.__len__()):
            self.download_pic(pic_url[i]['src'],dir,str(i)+'.jpg')

    def parse_thread_page(self,page):
        page_info={}
        soup=BeautifulSoup(page)
        div_id_main=soup.find('div',attrs={'id':'main'})
        div_class_t=div_id_main.find_all('div',attrs={'class':'t2'})[0]
        title=div_class_t.find('h4').text
        page_info['title']=title
        # the main content of this thread is in this block
        div_do_not_catch=div_class_t.find_all('div',attrs={'class':'do_not_catch'})[0]
        input_list=div_do_not_catch.find_all('input')
        pic_url=[]
        for line in input_list:
            temp={}
            temp['src']=line['src']
            onclick=line['onclick']
            pattern=re.compile(r"window.open.+?\+encode")
            match=re.match(pattern,onclick).group(0)[13:-8]
            temp['onclick']=match+line['src']
            # type=re.match(r'jpeg',str(line['src']))
            # print(line['src'])
            # temp['type']=type
            pic_url.append(temp)
        page_info['pic_url']=pic_url
        return page_info

    def download_pic(self,url,save_folder,file_name):
        pic=self.getData(url,encoding=False)
        name=save_folder+'\\'+file_name
        f=open(name,'wb')
        f.write(pic)
        f.close()

    def getData(self,url,encoding=True):
        try:
            res=self.getData_inner(url,encoding)
            return res
        except Exception as e:
            reconn_count=1
            while reconn_count<=config.reconn_num:
                time.sleep(max(random.gauss(2,0.5),0.5))
                try:
                    res=self.getData_inner(url,encoding)
                    return res
                except:
                    reconn_count+=1
            raise ConnectionError('Unable to get page')

    def getData_inner(self,url,encoding=True):
        headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) '
                    'AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile'
                    '/12A4345d Safari/600.1.4'}
        req=request.Request(url,headers=headers)
        opener=request.build_opener()
        request.install_opener(opener)
        result=opener.open(req,timeout=config.timeout)
        if encoding:
            return result.read().decode('gbk')
        else:
            return result.read()

def save_page(page,path):
    pass
    #todo

if __name__=='__main__':
    x=spider()
    x.deal_thread('http://cl.eecl.me/htm_data/16/1602/1816262.html')
