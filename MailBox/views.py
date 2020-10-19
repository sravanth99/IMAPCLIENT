from django.shortcuts import render,redirect
import math
from . import Imap_utility
import os
from . import Pickle_util
from . import indiutil
from django.contrib import messages

def other(request,foldername,page_num):
    print('hey',page_num)
    IMP = 'INBOX All Mail'
    try:
        pkl=Pickle_util.PickleData('userinfo.pkl')
        d = pkl.depickle()
        user=d['user']
        pas=d['pas']
        host=d['host']
        client = Imap_utility.CustomMailBox(user,pas,host,folder=foldername)
        fname=None
        rename=None
        cur= client.get_cur()
        Info = client.get_info(cur)
        F= client.get_folders()
        cur = [cur,cur.split('/')[-1]]
        Folders = []
        if request.method=="GET":
            fname = request.GET.get('folder-name')
            rename = request.GET.get('new-name')
        if fname:
            stat = client.create_folder(fname)
            if stat=='no':
                messages.warning(request,f"specified folder {fname} already exists!")
            else:
                messages.success(request,f"{fname} has been created successfully!")
        if rename:
            ok=True
            for f in F:
                if rename == f['name'].split('/')[-1]:
                    ok=False
                    messages.warning(request,'Folder already exists!')
                    break
            if ok:
                cur = [rename,rename.split('/')[-1]]
                client.rename_folder(rename)
                messages.success(request,'updated successfully!')
        if request.method=="POST":
            delete = request.POST.get('delete')
            print('delte to be fone',delete)
            if cur[1] not in IMP:
                client.delete_folder(cur[0])
                messages.success(request,f'{cur[1]} has been deleted successfully!')
                return redirect('pagenated',foldername='INBOX',page_num=1)
            messages.warning(request,'You cannot delete this folder!')
    except:
        messages.info(request,'Please login!')
        print('redirectiong to login')
        return redirect('login')
    for f in F:
        if '\\Noselect' in f['flags']:
            continue
        if f['name']!=cur[0]:
            Folders.append([f['name'],f['name'].split('/')[-1]])
    now,last = client.getbypagenum(page_num,'')
    context = {'msgs':now,'D':list(Info.items()),'last':last,'pn':page_num,'prev':max(page_num-1,1),'nxt':min(page_num+1,last),
    'folders':Folders,'cur':cur,'type_name': 'Folder'}
    return render(request,'MailBoX/dumb.html',context)

def loginview(request):
    if request.method=='POST':
        user = request.POST.get('email')
        pas = request.POST.get('password')
        host = request.POST.get('host')
        if not (host):
            host='imap.gmail.com'
        mb = Imap_utility.CustomMailBox(user,pas,host)
        if mb.authuser():
            d = {'user':user,'pas':pas,'host':host}
            pkl = Pickle_util.PickleData('userinfo.pkl')
            pkl.dump_object(d)
            messages.success(request,'HELLO User')
            return redirect('pagenated',page_num=1,foldername='INBOX')
        else:
            messages.info(request,'please enter valid credentials!')
            messages.warning(request,'Please make sure that you\'ve enabled imap')
    return render(request,'MailBox/login.html')
def logoutview(request):
    messages.info(request,'you\'ve been logged out!')
    os.remove('userinfo.pkl')
    return redirect('login')

def pageview(request,foldername,uid):
    try:
        pkl=Pickle_util.PickleData('userinfo.pkl')
        d = pkl.depickle()
        user=d['user']
        pas=d['pas']
        host=d['host']
        client = Imap_utility.CustomMailBox(user,pas,host,folder=foldername)
        Mailobj = next(client.getbyuid(uid))
        cur= client.get_cur()
        cur = [cur,cur.split('/')[-1]]
        if request.method=="POST":
            delete = request.POST.get('delete')
            move =  request.POST.get('fname')
            cpfolder =  request.POST.get('copyfname')
            if delete:
                client.delete_msg(Mailobj.uid)
                messages.success(request,'Message has been deleted successfully!')
                return redirect('pagenated',page_num=1,foldername=foldername)
            if move:
                client.move_msgto(move,Mailobj.uid)
                messages.success(request,'1 message has been moved !')
                return redirect('pagenated',page_num=1,foldername=foldername)
            if cpfolder:
                client.copy_msgto(cpfolder,Mailobj.uid)
                messages.success(request,'1 message has been copied !')
                return redirect('pagenated',page_num=1,foldername=foldername)
    except:
        messages.info(request,'Please login!')
        return redirect('login')
    statpath = os.path.join('MailBoX','static','MailBoX')
    for f in os.listdir(statpath):
        os.remove(os.path.join(statpath,f))
    attach_names = []
    for att in Mailobj.attachments:
        with open(os.path.join(statpath,att.filename),'wb') as f:
            attach_names.append(att.filename)
            f.write(att.payload)
    top,bottom,card = indiutil.get_patches(foldername,Mailobj.subject,Mailobj.html,attach_names,len(attach_names))
    with open('MailBox/templates/MailBoX/pageview.html','wb') as f:
        f.write(top)
        f.write(card)
        f.write(bottom)
    F= client.get_folders()
    Folders = []
    for f in F:
        if '\\Noselect' in f['flags']:
            continue
        if f['name']!=cur[0]:
            Folders.append([f['name'],f['name'].split('/')[-1]])
    context = {'D':Mailobj.from_values.items(),'type_name': 'Message','folders':Folders}
    return render(request,'MailBox/pageview.html',context)
def subjectview(self,foldername,subject,page_num):
    pass
