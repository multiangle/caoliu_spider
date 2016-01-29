__author__ = 'multiangle'

#========================================================
#----------------import package--------------------------
# import python package
import urllib.request as request
import time
import random

# import from this folder
from bs4 import BeautifulSoup
import spider_config as config
#========================================================
class spider():
    def __init__(self):
        self.base_url=config.base_url
        page=self.getData(self.base_url+'/index.php')
        entry_url=self.parse_main_page(page)
        flag_page=self.getData(entry_url[-3][1])
        print(flag_page)

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


    def getData(self,url):
        try:
            res=self.getData_inner(url)
            return res
        except Exception as e:
            reconn_count=1
            while reconn_count<=config.reconn_num:
                time.sleep(max(random.gauss(2,0.5),0.5))
                try:
                    res=self.getData_inner(url)
                    return res
                except:
                    reconn_count+=1
            raise ConnectionError('Unable to get page')

    def getData_inner(self,url):
        headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) '
                    'AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile'
                    '/12A4345d Safari/600.1.4'}
        req=request.Request(url,headers=headers)
        opener=request.build_opener()
        request.install_opener(opener)
        result=opener.open(req,timeout=config.timeout)
        return result.read().decode('gbk')

def save_page(page,path):
    pass
    #todo

if __name__=='__main__':
    x=spider()