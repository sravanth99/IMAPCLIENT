## importing required packages #################
from imap_tools import MailBox,AND,OR,NOT
from django.http import HttpResponse
from imapclient import IMAPClient
import os
import math
class CustomMailBox():
    def __init__(self,user,pas,host='imap.gmail.com',n_per_page=40,folder='INBOX'):
        self.user=user
        self.pwd = pas
        self.host = host
        self.folder = folder
        self.n_per_page = n_per_page
    def authuser(self):
        try:
            self.Mb_main = MailBox(host=self.host)
            self.Mb_main.login(self.user,self.pwd)
            d = dict()
            for f in self.Mb_main.folder.list():
                d[f['name'].split('/')[-1]] = f['name']
            self.Mb_main.folder.set(d[self.folder])
            return d
        except:
            return False
    def getbypagenum(self,page_number,searchterm):
        d = self.authuser()
        if d:

            print(page_number,self.n_per_page,'ufifidh')
            mb = IMAPClient(self.host)
            mb.login(self.user,self.pwd)
            mb.select_folder(d[self.folder])
            if searchterm:
                ids= mb.search(['OR',['OR',[u'TEXT',f'{searchterm}'],['FROM',f'{searchterm}']],['OR',[u'SUBJECT',f'{searchterm}'],[u'BODY',f'{searchterm}']]])
            else:
                ids = mb.search()
            print(len(ids),'hmmm')
            last = math.ceil(len(ids)/self.n_per_page)
            print(last,'last page')
            page_number = last-page_number+1
            start = max(0,((page_number-1)*self.n_per_page))
            end = min(len(ids),(page_number*self.n_per_page))
            print(start,end)
            print(ids[start:end])
            return (next(self.Mb_main.fetch(AND(uid=f'{m}'),headers_only=True,reverse=True) )for m in reversed(ids[start:end])),last
    def getbyuid(self,uid):
        if self.authuser():
            return self.Mb_main.fetch(AND(uid=uid))
    def getbysearch(self,text):
        if self.authuser():
            return self.Mb_main.fetch(OR(subject=text))
    def get_searched_chunks(self):
        gen = self.get_searched_chunks()
        pass
    def get_info(self,folder='INBOX'):
        if self.authuser():
            return self.Mb_main.folder.status(folder)
    def get_folders(self):
        if self.authuser():
            return self.Mb_main.folder.list()
    def get_cur(self):
        if self.authuser():
            return self.Mb_main.folder.get()
    def create_folder(self,folder):
        if self.authuser():
            if self.Mb_main.folder.exists(folder):
               return 'no'
            self.Mb_main.folder.create(folder)
            return 'ok'
    def delete_folder(self,folder):
        if self.authuser():
            self.Mb_main.folder.delete(folder)
    def rename_folder(self,folder):
        d = self.authuser()
        if d:
            self.Mb_main.folder.rename(d[self.folder],folder)
    def delete_msg(self,uid):
        if self.authuser():
            self.Mb_main.delete(uid)
    def move_msgto(self,folder,uid):
        if self.authuser():
            self.Mb_main.move(uid,folder)
    def copy_msgto(self,folder,uid):
        if self.authuser():
            self.Mb_main.copy(uid,folder)
