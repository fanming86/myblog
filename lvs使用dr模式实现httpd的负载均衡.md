---


---

<h2 id="简介">简介</h2>
<p>关于lvs的介绍就不多说了，可以移步我的另外一篇博文：<a href="https://www.ifanm.com/post/24/">lvs简介</a></p>
<p>在DR模式的群集中，LVS负载调度器作为群集的访问入口，但不作为网关使用；服务器池中的所有节点都各自接入internet，发送给客户端的WEB响应数据包不需要经过LVS负载调度器。如图所示</p>

<table>
<thead>
<tr>
<th align="center">节点</th>
<th>真实IP</th>
<th align="right">虚拟IP (vip)</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">调度器</td>
<td>192.168.0.253</td>
<td align="right">192.168.0.250</td>
</tr>
<tr>
<td align="center">webserver1–lvs1</td>
<td>192.168.0.100</td>
<td align="right">192.168.0.250</td>
</tr>
<tr>
<td align="center">webserver2–lvs2</td>
<td>192.168.0.104</td>
<td align="right">192.168.0.250</td>
</tr>
</tbody>
</table><h2 id="调度器配置">调度器配置</h2>
<h3 id="、先停掉防火墙，关闭selinux">1、先停掉防火墙，关闭selinux</h3>
<p>systemctl stop firewalld<br>
setenforce 0</p>
<h3 id="、设置虚拟ip">2、设置虚拟IP</h3>
<pre class=" language-bash"><code class="prism  language-bash"><span class="token punctuation">[</span>root@client ~<span class="token punctuation">]</span><span class="token comment"># cd /etc/sysconfig/network-scripts/</span>
<span class="token punctuation">[</span>root@client network-scripts<span class="token punctuation">]</span><span class="token comment"># cp ifcfg-ens33 ifcfg-ens33:0</span>
</code></pre>
<p>在此文件中添加或修改以下内容：</p>
<pre class=" language-bash"><code class="prism  language-bash">DEVICE<span class="token operator">=</span>ens33:0
NM_CONTROLLED<span class="token operator">=</span>no
ONBOOT<span class="token operator">=</span>yes
IPADDR<span class="token operator">=</span>192.168.0.250
NETMASK<span class="token operator">=</span>255.255.255.0
</code></pre>
<p>修改完成后重启网络，查看IP：</p>
<pre class=" language-bash"><code class="prism  language-bash"><span class="token punctuation">[</span>root@client network-scripts<span class="token punctuation">]</span><span class="token comment"># systemctl restart network</span>
<span class="token punctuation">[</span>root@client network-scripts<span class="token punctuation">]</span><span class="token comment"># ifconfig ens33:0</span>
ens33:0: flags<span class="token operator">=</span>4163<span class="token operator">&lt;</span>UP,BROADCAST,RUNNING,MULTICAST<span class="token operator">&gt;</span>  mtu 1500
inet 192.168.0.250  netmask 255.255.255.0  broadcast 192.168.0.255
ether 00:0c:29:7b:85:8b  txqueuelen 1000  <span class="token punctuation">(</span>Ethernet<span class="token punctuation">)</span>
</code></pre>
<h3 id="、开启路由转发功能">3、开启路由转发功能</h3>
<p>echo ‘1’ &gt; /proc/sys/net/ipv4/ip_forward</p>
<p>或者直接修改配置文件<br>
/etc/sysctl.conf<br>
sysctl -p  #使配置文件立即生效</p>
<h3 id="、安装和启动ipvsadm">4、安装和启动ipvsadm</h3>
<p>yum install ipvsadm -y<br>
systemctl start ipvsadm</p>
<h4 id="ipvsadm启动时报错：">ipvsadm启动时报错：</h4>
<p>Dec  3 19:10:52 client bash: /bin/bash: /etc/sysconfig/ipvsadm: 没有那个文件或目录</p>
<h4 id="解决：">解决：</h4>
<p>ipvsadm --save &gt; /etc/sysconfig/ipvsadm</p>
<h3 id="、添加虚拟服务器-和真实服务器">5、添加虚拟服务器 和真实服务器</h3>
<pre class=" language-bash"><code class="prism  language-bash"><span class="token comment">#添加虚拟服务器</span>
ipvsadm -A -t 192.168.0.250:80 -s wrr

<span class="token comment">#参数说明：</span>
-A：--add-service，表示添加一个虚拟服务器
-t：--tcp-service，指定这是一个tcp的虚拟服务器
-u：--udp-service，指定这是一个udp的虚拟服务器
192.168.0.250:80：表示提供服务的ip地址以及端口号
-s：--scheduler，指定调度器，“rr<span class="token operator">|</span>wrr<span class="token operator">|</span>lc<span class="token operator">|</span>wlc<span class="token operator">|</span>lblc<span class="token operator">|</span>lblcr<span class="token operator">|</span>dh<span class="token operator">|</span>sh<span class="token operator">|</span><span class="token function">sed</span><span class="token operator">|</span>nq”选择一种，默认是wlc
</code></pre>
<h4 id="删除服务器：">删除服务器：</h4>
<pre class=" language-bash"><code class="prism  language-bash">ipvsadm -d -t 192.168.0.250:80 -r 192.168.0.101:80
</code></pre>
<h4 id="为此虚拟服务器添加真实服务器：">为此虚拟服务器添加真实服务器：</h4>
<pre class=" language-bash"><code class="prism  language-bash">ipvsadm -a -t 192.168.0.250:80 -r 192.168.0.100:80 -g -w 1
ipvsadm -a -t 192.168.0.250:80 -r 192.168.0.104:80 -g -w 1
192.168.0.100
192.168.0.104
以上两个ip为httpd服务所在的两个机器
</code></pre>
<h4 id="查看已经添加的真实服务器：">查看已经添加的真实服务器：</h4>
<p>ipvsadm -L</p>
<pre class=" language-bash"><code class="prism  language-bash"><span class="token punctuation">[</span>root@client network-scripts<span class="token punctuation">]</span><span class="token comment"># ipvsadm -L</span>
IP Virtual Server version 1.2.1 <span class="token punctuation">(</span>size<span class="token operator">=</span>4096<span class="token punctuation">)</span>
Prot LocalAddress:Port Scheduler Flags
-<span class="token operator">&gt;</span> RemoteAddress:Port  Forward Weight ActiveConn InActConn
TCP  client.example.com:http wrr
-<span class="token operator">&gt;</span> 192.168.0.100:http  Route  1  0  0
-<span class="token operator">&gt;</span> 192.168.0.104:http  Route  1  0  0
</code></pre>
<h2 id="webserver配置">webserver配置</h2>
<p>web服务器的配置以下为一台机器中的，若在环境中有多台机器，则更改对应的真实IP即可，虚拟IP都一样</p>
<h3 id="、配置ip">1、配置ip</h3>
<pre class=" language-bash"><code class="prism  language-bash"><span class="token punctuation">[</span>root@lvs1 ~<span class="token punctuation">]</span><span class="token comment"># cd /etc/sysconfig/network-scripts/</span>
<span class="token punctuation">[</span>root@lvs1 network-scripts<span class="token punctuation">]</span><span class="token comment"># cp ifcfg-lo ifcfg-lo:0</span>
<span class="token punctuation">[</span>root@lvs1 network-scripts<span class="token punctuation">]</span><span class="token comment"># vim ifcfg-lo:0</span>
</code></pre>
<h4 id="配置文件内容如下：">配置文件内容如下：</h4>
<pre class=" language-bash"><code class="prism  language-bash"><span class="token comment">#此处的子网掩码为四个1</span>

DEVICE<span class="token operator">=</span>lo:0
IPADDR<span class="token operator">=</span>192.168.0.250
NETMASK<span class="token operator">=</span>255.255.255.255
NAME<span class="token operator">=</span>loopback
ONBOOT<span class="token operator">=</span>yes
</code></pre>
<h4 id="重启网络，查看ip">重启网络，查看IP</h4>
<pre class=" language-bash"><code class="prism  language-bash"><span class="token punctuation">[</span>root@lvs1 network-scripts<span class="token punctuation">]</span><span class="token comment"># systemctl restart network</span>
<span class="token punctuation">[</span>root@lvs1 network-scripts<span class="token punctuation">]</span><span class="token comment"># ifconfig lo:0</span>
lo:0: flags<span class="token operator">=</span>73<span class="token operator">&lt;</span>UP,LOOPBACK,RUNNING<span class="token operator">&gt;</span>  mtu 65536
inet 192.168.0.250  netmask 255.255.255.255
loop  txqueuelen 1  <span class="token punctuation">(</span>Local Loopback<span class="token punctuation">)</span>
</code></pre>
<h3 id="、抑制arp">2、抑制arp</h3>
<pre class=" language-bash"><code class="prism  language-bash"><span class="token keyword">echo</span> <span class="token string">"1"</span> <span class="token operator">&gt;</span> /proc/sys/net/ipv4/conf/lo/arp_ignore
<span class="token keyword">echo</span> <span class="token string">"2"</span> <span class="token operator">&gt;</span> /proc/sys/net/ipv4/conf/lo/arp_announce
<span class="token keyword">echo</span> <span class="token string">"1"</span> <span class="token operator">&gt;</span> /proc/sys/net/ipv4/conf/all/arp_ignore
<span class="token keyword">echo</span> <span class="token string">"2"</span> <span class="token operator">&gt;</span> /proc/sys/net/ipv4/conf/all/arp_announce
</code></pre>
<h4 id="arp_ignore用来定义网卡在--响应外部arp请求时的响应--级别。">arp_ignore用来定义网卡在  响应外部ARP请求时的响应  级别。</h4>
<blockquote>
<p>0: 默认值， 任何网络接口收到ARP请求后， 如果本机的任意接口有该MAC, 则予以响应。<br>
1: 某个网络接口收到ARP请求后， 判断请求的MAC地址是否是本接口， 是则回应， 否则不回应。LvS调度器会将客户请求转发给真实服务器的ethO接口， 而真实服务器 的VIP地址配置在本地回环设备上。</p>
</blockquote>
<h4 id="arp-_-announce用来定义网卡广播arp包时的级别。">arp _ announce用来定义网卡广播ARP包时的级别。</h4>
<blockquote>
<p>0: 默认值， 任何网络接口接收到ARP请求后， 如果本机的任意接口有该MAC, 则 予以响应。<br>
1: 尽量避免响应MAC地址非本网络接口MAC地址的ARP请求。<br>
2: 不响应MAC地址非本网络接口MAC地址的ARP请求。</p>
</blockquote>
<h4 id="配置脚本--临时配置忽略arp-临时添加虚拟ip">配置脚本  临时配置忽略arp 临时添加虚拟IP</h4>
<pre class=" language-bash"><code class="prism  language-bash">vip<span class="token operator">=</span>192.168.1.250
<span class="token function">ifconfig</span> lo:0 <span class="token variable">$vip</span> broadcast <span class="token variable">$vip</span> netmask 255.255.255.255 up
<span class="token keyword">echo</span> <span class="token string">'1'</span> <span class="token operator">&gt;</span> /proc/sys/net/ipv4/conf/lo/arp_ignore
<span class="token keyword">echo</span> <span class="token string">'1'</span> <span class="token operator">&gt;</span> /proc/sys/net/ipv4/conf/all/arp_ignore
<span class="token keyword">echo</span> <span class="token string">'2'</span> <span class="token operator">&gt;</span> /proc/sys/net/ipv4/conf/lo/arp_announce
<span class="token keyword">echo</span> <span class="token string">'2'</span> <span class="token operator">&gt;</span> /proc/sys/net/ipv4/conf/all/arp_announce
</code></pre>
<h3 id="、安装httpd">3、安装httpd</h3>
<p>yum install httpd</p>
<h3 id="、创建测试页面">4、创建测试页面</h3>
<p>cd /var/www/html/<br>
echo ‘<a href="http://lvs1.example.com">lvs1.example.com</a>’ &gt; index.html</p>
<h2 id="测试">测试</h2>
<p>另外找一台主机使用curl  可以测试，测试结果如下：</p>
<pre class=" language-bash"><code class="prism  language-bash"><span class="token punctuation">[</span>root@client2 ~<span class="token punctuation">]</span><span class="token comment"># curl 192.168.0.250:80</span>
lvs1.example.com
<span class="token punctuation">[</span>root@client2 ~<span class="token punctuation">]</span><span class="token comment"># curl 192.168.0.250:80</span>
lvs2.example.com
<span class="token punctuation">[</span>root@client2 ~<span class="token punctuation">]</span><span class="token comment"># curl 192.168.0.250:80</span>
lvs1.example.com
<span class="token punctuation">[</span>root@client2 ~<span class="token punctuation">]</span><span class="token comment"># curl 192.168.0.250:80</span>
lvs2.example.com
<span class="token punctuation">[</span>root@client2 ~<span class="token punctuation">]</span><span class="token comment"># curl 192.168.0.250:80</span>
lvs1.example.com
<span class="token punctuation">[</span>root@client2 ~<span class="token punctuation">]</span><span class="token comment"># curl 192.168.0.250:80</span>
lvs2.example.com
</code></pre>

