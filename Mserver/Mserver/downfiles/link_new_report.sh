#report_db="11.168.18.82"
report_db="10.95.154.188"
config_f="/opt/tools/config/configure.data"
sed -i s#'report_dbname.*'#'report_dbname = report'#g ${config_f}
sed -i s#'report_postgres_ip.*'#"report_postgres_ip = ${report_db}"#g ${config_f}
echo "CHECK:"
if grep 'report_dbname = report' ${config_f} && grep "report_postgres_ip = ${report_db}" ${config_f}
then
echo 'CHECK OK'
python  /opt/tools/configure.pyc
#is web?
  if grep 'enable' ${config_f}|grep 'web'
  then
  sed -i s#'enable":.*'#'enable":true'#g  /opt/www/config/fdw/postgres_fdw.conf  
   if grep true /opt/www/config/fdw/postgres_fdw.conf  
    then 
     echo 'fdw OK'
     cd /opt/www; php yiic psqlfdw
    else
     echo 'fdw err..'
    fi
  echo 
  echo "OK... "
fi
else
  echo 'ERROR..'
fi
