# check_linode_loadbalance_plugin
This is plugin provides check linode loadbalance status so that dynamic add/del IP from cloudflare with cloudflare API


Background:
Cause Linode origin Loadbalance just has 100Mbps bandwidth, in fact, we have more than 100Mbps useage in our production env. Therefore we have create double linode instances behind cloudflare DNS resolving, in order not to single instance bandwitdh limit, so we can't use the way of VIP by heartbeat or keepalived.
Finally, I wrote the script to provide above function.
