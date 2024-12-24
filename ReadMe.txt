1. Create a Python file on the target server java_process_exporter.py on any desired path
2. Create a config file /etc/init/java_process_exporter.conf with content given
3. Run the below commands:
  3.1 sudo start java-process-exporter
4. Make sure to add the target mentioned in the prometheus-configuration in the /etc/prometheus/prometheus.yml
5. Restart the prometheus -> systemctl restart prometheus
6. Also, make sure to allow port 8000 in the inbound of target server security group from the promethues server
