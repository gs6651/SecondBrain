
#### Structure of Policy

- **Step #1: List**: Site lists (which site (Branch 1, Branch 2, HUB etc.), VPN lists, TLOC lists, access-lists, prefix-lists, as-path-lists. Basically we create group of interests.
- **Step #2: Definition:** What Action. Here we *match* everything defined in step #1 as per our need and accordingly *action* will be taken on it.
- **Step #3: Application:** Where to apply policy. (in-bound or out-bound)

> 	Manager will push centralized policy to Controller via NETCONF transaction. Then further, policy itself won't be pushed to the WAN edge devices, only the results of the policy (after processing by Controller) are advertised via OMP to the overlay. 

#### Centralized policies

<img title="" src="https://cdn.networkacademy.io/sites/default/files/2022-04/types-of-sdwan-policies.svg" alt="Types of Cisco SD-WAN Policies" width="634">

- One type of policy can be applied to a site-list. For example, one control-policy in and one control-policy out but not two control policies in the outbound direction.
- Cisco does not recommend including a site in more than one site-list. Doing this may result in unpredictable behavior of the policies applied to these site-lists.
- The direction of the policy is always **from the perspective of the Controller controller**.
  - Outbound means Controller to WAN Edges and does ***not*** affect the best path selection process and influences only the specific edges in the contorl policy's site list.
  - Inbound means WAN Edges to Controller and it will modifies the attributes in OMP updates before routing information enters the RIB of Controller. It affects the complete overlay fabric.
- **Centralized-*Control*-policy** is use to influence 'route' & 'TLOC' between Controller & WAN edges. It is unidirectional which means it will be applied either inbound or outbound. For example, If we need to manipulate OMP routes that the controller sends and receives, we must configure two control policies. It's of two types:
	- *Topology Policies:* To limit the number of overlay tunnels between sites and controlling the overlay topology.
	- *VPN Membership Policies:* To control the distribution of routing information for specific VPNs. A typical use-case is for creating guest networks that have Internet access but site-to-site communication is restricted.
- **Centralized-*Data*-policy** is directional and can be applied either to the traffic received from the service side of the WAN Edge router, traffic received from the transport side, or both.
- VPN membership policy is always applied to traffic outbound from the Controller controller.

### Order-of-Operation on WAN Edge

- *IP lookup*: 1st thing 1st, IP address lookup, because WAN Edges at the heart are routers 🙂.
- *Local Ingress Policy*: Localized policies are typically used to create ACLs and tie them to WAN Edge interfaces. ACLs can be used for filtering, marking, and traffic policing.
- *Centralized App-Route Policy*: or App-Aware Routing. If it’s configured, the packet being inspected makes a routing decision based on the defined SLA characteristics such as packet loss, latency, jitter, load, cost, and bandwidth of a link.
- *Centralized Data Policy*: It is evaluated after the App-Aware Routing policy and is able to override the App-Aware Routing forwarding decision.
- *Forwarding*: At this point, the destination IP address is compared against the routing table, and the output interface is determined.
- *Security Policy*: If there are security services attached to the WAN Edge, they are processed in the following sequence - Firewall, IPS, URL-Filtering, and lastly AMP (Advanced Malware Protection). The necessary tunnel encapsulations are performed and VPN labels are inserted.
- *Local Egress Policy*: If traffic is denied or manipulated by the egress ACL, those changes will take effect before the packet is forwarded.
- *Queuing and Scheduling*: Egress traffic queuing services such as Low-Latency (LLQ) and Weighted Round Robin (WRR) queuing are performed before the packet leaves.



[[Cisco SDWAN]]