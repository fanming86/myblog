---


---

<h2 id="lvs简介">lvs简介</h2>
<pre><code>中文文档：http://www.linuxvirtualserver.org/zh/index.html
</code></pre>
<p>当网站后端服务器承受不住访问的压力，提高服务器性能的解决方案会极大的增加成本时，于是就出现了横向扩展的解决方案。即增加一台或几台服务器，提供相同的服务，通过前端调度器将访问请求分配到后台服务器上。这种多台服务器组成的数组集合就叫做集群。</p>
<blockquote>
<p>LVS是Linux Virtual Server的简写，意思就是Linux虚拟服务器，是一个虚拟的服务器集群系统，可以在UNIX/LINUX平台下实现负载均衡集群功能。该项目在1998年5月由章文嵩博士组织成立，是中国国内最早出现的自由软件项目之一。现在已经被收到linux2.6以上的内核版本中，不需要对系统打补丁就可以轻松实现</p>
</blockquote>
<blockquote>
<p>LVS负载均衡调度技术是在Linux内核中实现的，因此，被称之为Linux虚拟服务器（Linux Virtual Server）。我们使用该软件配置LVS时候，不能直接配置内核中的ipvs，而需要使用ipvs的管理工具ipvsadm进行管理。</p>
</blockquote>
<blockquote>
<p>LVS工作于IOS七层模型的第四层-传输层，通过对TCP, UDP, AH, EST, AH_EST, SCTP等工作在四层的协议的支持，根据目标地址和端口做出转发与否的决策，根据调度算法做出转发至哪一个端口的解决方案</p>
</blockquote>
<blockquote>
<p>LVS集群采用IP负载均衡技术和基于内容请求分发技术</p>
</blockquote>
<blockquote>
<p>IPVS: 称之为IP虚拟服务器(IP Virtual Server，简写为IPVS),是运行在LVS下的提供负载均衡功能的一种技术</p>
</blockquote>
<blockquote>
<p>LVS采用的IP负载均衡技术是在负载调度器的实现技术中效率最高的。目前有三种IP负载均衡技术, 八种调度算法。</p>
</blockquote>
<h3 id="简单术语">简单术语</h3>
<pre><code>术语简写	术语含义
CIP		客户端的IP地址，client ip
DIP		负载均衡器对应的实际IP地址
VIP		需在均衡器提供服务的地址，虚拟地址
RIP		提供服务的节点地址
LB		负载均衡服务器
RS		节点服务器，Real   Server
</code></pre>
<h3 id="lvs有三种负载平衡方式">LVS有三种负载平衡方式</h3>
<pre><code>NAT（Network Address Translation）
DR（Direct Routing）
IP Tunneling
</code></pre>
<h3 id="三种方式：">三种方式：</h3>
<h4 id="、virtual-server-via-network-address-translation-nat（vsnat）">1、Virtual Server via Network Address Translation NAT（VS/NAT）</h4>
<blockquote>
<p>通过网络地址转换，调度器重写请求报文的目标地址，根据预设的调度算法，将请求分派给后端的真实服务器；真实服务器的响应报文通过调度器时，报文的源地址被重写，再返回给客户，完成整个负载调度过程。</p>
</blockquote>
<h4 id="virtual-server-via-ip-tunnelingvstun">Virtual Server via IP Tunneling(VS/TUN)</h4>
<blockquote>
<p>采用NAT技术时，由于请求和响应报文都必须经过调度器地址重写，当客户请求越来越多时，调度器的处理能力将成为瓶颈。为了解决这个问题，调度器把请求报 文通过IP隧道转发至真实服务器，而真实服务器将响应直接返回给客户，所以调度器只处理请求报文。由于一般网络服务应答比请求报文大许多，采用 VS/TUN技术后，集群系统的最大吞吐量可以提高10倍。</p>
</blockquote>
<h4 id="virtual-server-via-direct-routingvsdr">Virtual Server via Direct Routing(VS/DR)</h4>
<blockquote>
<p>VS/DR通过改写请求报文的MAC地址，将请求发送到真实服务器，而真实服务器将响应直接返回给客户。同VS/TUN技术一样，VS/DR技术可极大地 提高集群系统的伸缩性。这种方法没有IP隧道的开销，对集群中的真实服务器也没有必须支持IP隧道协议的要求，但是要求调度器与真实服务器都有一块网卡连 在同一物理网段上。</p>
</blockquote>
<h3 id="八种算法">八种算法</h3>
<h4 id="、轮叫（round-robin）">1、轮叫（Round Robin）</h4>
<blockquote>
<p>调度器通过"轮叫"调度算法将外部请求按顺序轮流分配到集群中的真实服务器上，它均等地对待每一台服务器，而不管服务器上实际的连接数和系统负载。</p>
</blockquote>
<h4 id="、加权轮叫（weighted-round-robin）">2、加权轮叫（Weighted Round Robin）</h4>
<blockquote>
<p>调度器通过"加权轮叫"调度算法根据真实服务器的不同处理能力来调度访问请求。这样可以保证处理能力强的服务器处理更多的访问流量。调度器可以自动问询真实服务器的负载情况，并动态地调整其权值。</p>
</blockquote>
<h4 id="、最少链接（least-connections）">3、最少链接（Least Connections）</h4>
<blockquote>
<p>调度器通过"最少连接"调度算法动态地将网络请求调度到已建立的链接数最少的服务器上。如果集群系统的真实服务器具有相近的系统性能，采用"最小连接"调度算法可以较好地均衡负载。</p>
</blockquote>
<h4 id="、加权最少链接（weighted-least-connections）">4、加权最少链接（Weighted Least Connections）</h4>
<blockquote>
<p>在集群系统中的服务器性能差异较大的情况下，调度器采用"加权最少链接"调度算法优化负载均衡性能，具有较高权值的服务器将承受较大比例的活动连接负载。调度器可以自动问询真实服务器的负载情况，并动态地调整其权值。</p>
</blockquote>
<h4 id="、基于局部性的最少链接（locality-based-least-connections）">5、基于局部性的最少链接（Locality-Based Least Connections）</h4>
<blockquote>
<p>“基于局部性的最少链接” 调度算法是针对目标IP地址的负载均衡，目前主要用于Cache集群系统。该算法根据请求的目标IP地址找出该目标IP地址最近使用的服务器，若该服务器 是可用的且没有超载，将请求发送到该服务器；若服务器不存在，或者该服务器超载且有服务器处于一半的工作负载，则用"最少链接"的原则选出一个可用的服务 器，将请求发送到该服务器。</p>
</blockquote>
<h4 id="、带复制的基于局部性最少链接（locality-based-least-connections-with-replication）">6、带复制的基于局部性最少链接（Locality-Based Least Connections with Replication）</h4>
<blockquote>
<p>"带复制的基于局部性最少链接"调度算法也是针对目标IP地址的负载均衡，目前主要用于Cache集群系统。它与LBLC算法的不同之处是它要维护从一个 目标IP地址到一组服务器的映射，而LBLC算法维护从一个目标IP地址到一台服务器的映射。该算法根据请求的目标IP地址找出该目标IP地址对应的服务 器组，按"最小连接"原则从服务器组中选出一台服务器，若服务器没有超载，将请求发送到该服务器，若服务器超载；则按"最小连接"原则从这个集群中选出一 台服务器，将该服务器加入到服务器组中，将请求发送到该服务器。同时，当该服务器组有一段时间没有被修改，将最忙的服务器从服务器组中删除，以降低复制的 程度。</p>
</blockquote>
<h4 id="、目标地址散列（destination-hashing）">7、目标地址散列（Destination Hashing）</h4>
<blockquote>
<p>"目标地址散列"调度算法根据请求的目标IP地址，作为散列键（Hash Key）从静态分配的散列表找出对应的服务器，若该服务器是可用的且未超载，将请求发送到该服务器，否则返回空。</p>
</blockquote>
<h4 id="、源地址散列（source-hashing）">8、源地址散列（Source Hashing）</h4>
<blockquote>
<p>"源地址散列"调度算法根据请求的源IP地址，作为散列键（Hash Key）从静态分配的散列表找出对应的服务器，若该服务器是可用的且未超载，将请求发送到该服务器，否则返回空。</p>
</blockquote>
<h4 id="参考文档：">参考文档：</h4>
<pre><code>http://www.linuxvirtualserver.org/zh/lvs1.html
</code></pre>

