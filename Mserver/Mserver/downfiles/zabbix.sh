 rpm -ivh  http://repo.zabbix.com/zabbix/3.2/rhel/7/x86_64/zabbix-release-3.2-1.el7.noarch.rpm
  yum -y  install zabbix-agent
  grep -n "^[a-Z]" /etc/zabbix/zabbix_agentd.conf
    sed -i s#127.0.0.1#10.95.154.133#g /etc/zabbix/zabbix_agentd.conf
  sed -i s#'Hostname=.*'#Hostname=huaredis#g /etc/zabbix/zabbix_agentd.conf
  grep -n "^[a-Z]" /etc/zabbix/zabbix_agentd.conf
  setenforce 0
  systemctl start zabbix-agent.service 
  systemctl enable zabbix-agent.service 
