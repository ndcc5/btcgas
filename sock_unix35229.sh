#!/bin/bash

# 获取本机IP地址
local_ip=$(hostname -I | awk '{print $1}')

# 生成danted配置文件
sudo bash -c "cat >/etc/danted.conf <<EOF
# Generated by sockd.info
# Generated for interface $local_ip

internal: $local_ip port = 35229
external: $local_ip

method: username none
clientmethod: none
user.privileged: root
user.notprivileged: nobody
user.libwrap: nobody
client pass {
        from: 0.0.0.0/0 port 1-65535 to: 0.0.0.0/0
        log: connect disconnect error
}
pass {
        from: 0.0.0.0/0 to: 0.0.0.0/0
        protocol: tcp udp
}
EOF"
