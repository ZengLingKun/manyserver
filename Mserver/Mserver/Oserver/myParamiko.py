#!/usr/bin/env python
#encoding:utf8
#author: daijingquan

import paramiko

class myParamiko:
    def __init__(self,hostip,username,password,port=22):
        self.hostip = hostip
        self.port = port
        self.username = username
        self.password = password
        self.obj = paramiko.SSHClient()
        self.transport=paramiko.Transport(hostip,port)
        self.transport.connect(username=self.username,password=self.password)
        self.obj.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.obj.connect(self.hostip,self.port,self.username,self.password)
        self.objsftp = paramiko.SFTPClient.from_transport(self.transport)

    def run_cmd(self,cmd):
        stdin,stdout,stderr = self.obj.exec_command(cmd)
        return stdout.read().strip()+stderr.read().strip()

    def run_cmdlist(self,cmdlist):
        self.resultList = []
        for cmd in cmdlist:
            stdin,stdout,stderr = self.obj.exec_command(cmd)
            self.resultList.append(stdout.read().strip()+stderr.read().strip())
        return self.resultList

    def get(self,remotepath,localpath):
        if '~' in remotepath:
          remotepath=remotepath.replace('~',self.get_home())
        self.objsftp.get(remotepath,localpath)
    def get_home(self):
      return self.run_cmd('cd ~ && pwd')

    def put(self,localpath,remotepath):
        if '~' in remotepath:
          remotepath=remotepath.replace('~',self.get_home())
        with open('/tmp/djq_mypar.log','w') as f:f.write(remotepath)
        self.objsftp.put(localpath,remotepath)

    def getTarPackage(self,path):
        list = self.objsftp.listdir(path)
        for packageName in list:
            stdin,stdout,stderr  = self.obj.exec_command("cd " + path +";"
                                                         + "tar -zvcf /tmp/" + packageName
                                                         + ".tar.gz " + packageName)
            stdout.read()
            self.objsftp.get("/tmp/" + packageName + ".tar.gz","/tmp/" + packageName + ".tar.gz")
            self.objsftp.remove("/tmp/" + packageName + ".tar.gz")
            print "get package from " + packageName + " ok......"

    def close(self):
        self.transport.close()
        self.obj.close()

if __name__ == '__main__':
    sshobj = myParamiko('10.10.8.21','root','xxxxxxxx',22)
    sshobj.close()
