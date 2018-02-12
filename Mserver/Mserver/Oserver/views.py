#coding:utf-8
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.conf import settings
import os,paramiko,json,threading,Queue,time
from myParamiko import myParamiko
from .models import Server,Category
from django.core import serializers

# Create your views here.
def home(request):
  host_ips=Server.objects.values_list('host_ip')
  return render(request,'analyze_nmon.html',{'host_ips':host_ips})

nmon_files=settings.STATICFILES_DIRS[0]+'nmonaz/'
def file_iterator(file_name, chunk_size=512):
  file_name=os.path.join(nmon_files,file_name)
  with open(file_name) as f:
    while True:
      c = f.read(chunk_size)
      if c:
        yield c
      else:
        break

def file_down(request):
  the_file_name=request.GET['file']
  response = StreamingHttpResponse(file_iterator(the_file_name))
  response['Content-Type'] = 'application/octet-stream'
  response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
  return response


#analyze_nmon_
def analyze_nmon_(host_ip,nmon_file,queue=None):
  is_re=1
  host_info=Server.objects.get(host_ip=host_ip)
  ssh_=myParamiko(host_ip,host_info.host_user,host_info.host_passwd,22)
  nmon_file=ssh_.run_cmd('ls ~/nmon|grep %s' %nmon_file) 
  source_=os.path.join('~/nmon',nmon_file)
  lo_=os.path.join(nmon_files+'nmon_files',nmon_file)
  er=''
  imgs=[]
  try:
    ssh_.get(source_,lo_)
  except Exception as e:er=str(e)+":"+source_+","+lo_
  finally:ssh_.close()
  if is_re:
    er=os.popen('cd %s;sh pyit.sh nmon_files/%s %s' %(nmon_files,nmon_file,host_ip)).read().strip()
  else:
    er='OK'
  imgs_file=os.path.join(nmon_files+'/res/',host_ip+'/'+nmon_file+'/img')
  imgs_file=os.path.join(nmon_files+'/res/',host_ip)
  nmon_file_=os.popen('ls %s|grep %s' %(imgs_file,nmon_file)).read().strip()+'/img'
  imgs_file=os.path.join(imgs_file,nmon_file_)
  if er=='OK':
    imgs=os.popen('ls %s' %imgs_file).read().strip().split('\n')
  data = {'host_ip':host_ip,'imgs':imgs}
  imgs_file=imgs_file[imgs_file.index('/static'):]
  with open('/tmp/djq_getdata.log','w') as f:f.write(imgs_file)
  queue.put([host_ip,[os.path.join(imgs_file,img) for img in imgs]])
  return data

#-------------------------

def many_2_imgs(request):
  countrys=request.GET['countrys']
  nmon_name=request.GET['nmon_name']
  thread = MyThread(analyze_nmon_,countrys.split(','),(nmon_name,))
  returns=thread.start()
  return HttpResponse(json.dumps(returns), content_type='application/json')

def nmon_2_img_many(request):
  all=get_all()
  return render(request,'analyze_nmon_many.html',{'categoryshosts':all})


def add_server(request):
  flg=0
  my=''
  if request.method=='POST':
    try:
      host_password=request.POST.get('host_password')
      host_ip=request.POST.get('host_ip')
      if len(host_ip)<4:flg="Server填写错误！"
      host_user=request.POST.get('host_user')
      my=myParamiko(hostip=host_ip,username=host_user,password=host_password)
      host_category=request.POST.get('category')
      host_category=Category.objects.get(id=int(host_category))
      new_host=Server(where_add='nmon',host_ip=host_ip,host_passwd=host_password,host_user=host_user,category=host_category)
      new_host.save()
    except Exception as e:flg=str(e)
    finally:
      try:my.close()
      except:pass
  return HttpResponse(json.dumps({'aa':flg}), content_type='application/json')


def nmon_2_start_(host_ip,s,c,t,queue):
  flag=0
  try:  
    host_info=Server.objects.get(host_ip=host_ip)
    ssh_=myParamiko(host_ip,host_info.host_user,host_info.host_passwd,22)
    if not host_info.has_nmon:
      flag=nmon_2_host_(host_ip)
      if not 'SUCCESS' in flag:
        queue.put([host_ip,flag])
        return 0
    try:
      cmd_='cd ~/nmon/;./nmon_x86_64_centos7 -s %s -c %s -F 360test_%s_%s.nmon -t' %(s,c,t,host_ip)
      flag=ssh_.run_cmd('%s && echo "%s SUCCESS"' %(cmd_,cmd_))
    except Exception as e:flag=str(e)
    finally:ssh_.close()
  except Exception as e1:flag=str(e1)
  queue.put([host_ip,flag])


def start_all(request):
  countrys=request.GET['categorys']
  s=request.GET['s']
  c=request.GET['c']
  t=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
  thread = MyThread(nmon_2_start_,countrys.split(','),(s,c,t))
  returns=thread.start()
  return HttpResponse(json.dumps(returns), content_type='application/json')
 
def nmon_2_start(request):
  all=get_all()
  return render(request,'start_nmon.html',{'categoryshosts':all})
  


#2_host
def nmon_2_host_(host_ip,queue=None):
  flag=0
  try:  
    host_info=Server.objects.get(host_ip=host_ip)
    ssh_=myParamiko(host_ip,host_info.host_user,host_info.host_passwd,22)
    try:
      ssh_.run_cmd('mkdir -p ~/nmon/ 2>/dev/null')
      #暂时写死centos7
      source_file=os.path.join(nmon_files,'nmon_x86_64_centos7')
      ssh_.put(source_file,'~/nmon/nmon_x86_64_centos7')
      ssh_.run_cmd('chmod +x ~/nmon/nmon_x86_64_centos7 2>/dev/null')
      flag=ssh_.run_cmd('ls ~/nmon/|grep nmon_x86_64_centos7|wc -l')
    except Exception as e:flag=str(e)
    finally:ssh_.close()
  except Exception as e1:flag=str(e1)
  if flag == '1':
    flag=' SUCCESS'
    host_info.has_nmon=1
    host_info.save()
  if queue:
    queue.put([host_ip,flag])
  return flag

def get_all():
  categorys=Category.objects.all()
  all={}
  for category in categorys:
    citys = Server.objects.all().filter(category=category)
    all[category]=[city for city in citys]
  return all


#
def nmon_2_host(request):
  all=get_all()
  return render(request,'put_nmon.html',{'categoryshosts':all})

def put_nmon(request):
  countrys=request.GET['countrys']
  thread = MyThread(nmon_2_host_,countrys.split(','))
  returns=thread.start()
  return HttpResponse(json.dumps(returns), content_type='application/json')

def nmon_2_img(request):
  host_ips=Server.objects.values_list('host_ip')
  host_ips=[[host_ip[0] for host_ip in  host_ips]]
  return render(request,'analyze_nmon.html',{'host_ips':host_ips})



#nmon_2_img:ajax
def analyze_nmon(request):
  host_ip=request.GET['host_ip']
  nmon_file=request.GET['nmon_file']#获取的是全名
  data=analyze_nmon_(host_ip,nmon_file)
  data = json.dumps(data)
  return HttpResponse(data, content_type='application/json')

  
#nmon_2_img:ajax
def getdata(request):
  host_ip = request.GET['pk']
  #host_ip = '10.95.154.197'
  host_info=Server.objects.get(host_ip=host_ip)
  ssh_=myParamiko(host_ip,host_info.host_user,host_info.host_passwd,22)
  nmons=[]
  try:
    nmons=ssh_.run_cmd('ls -rt ~/nmon|grep .nmon|tail -20').split('\n')
    nmons=[nmon for nmon in nmons if len(nmon)>5]
    if len(nmons)==0:nmons=['暂无NMON监控文件,在~/nmon执行。']
    nmons=nmons[::-1]
  except:pass
  finally:ssh_.close()
  data = json.dumps({'host_ip':host_ip,'nmons':nmons})
  return HttpResponse(data, content_type='application/json')



class MyThread() :
  def __init__(self,func,list_,args=[]) :
    self.func = func  #传入线程函数逻辑
    self.queue=Queue.Queue(len(list_))
    self.list_=list_
    self.args=args
  def start(self):
    threads=[]
    for l in self.list_:
      threads.append(threading.Thread(target=self.func,args=[l,]+list(self.args)+[self.queue]))
    for thread_ in threads:
      thread_.start()
    for thread_ in threads:
      thread_.join()
    returns={}
    while not self.queue.empty():
      tmp_list=self.queue.get()
      returns[tmp_list[0]]=tmp_list[1]
    return returns
