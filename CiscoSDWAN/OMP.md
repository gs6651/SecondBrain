
# OMP

- TCP based protocol
- OMP peering is between devices’ system-IPs, it’s not bound to any of DTLS control connections to Controller
- There will be only one peering between WAN Edge & Controller, irrespective of number of WAN connections available

## OMP is responsible for distribution of

- TLOCs among network sites
- Service side reach-ability information
- Service-Chaining information
- Data-Plane security parameters, VPN labels & crypto keys
- Data & Application Aware Routing (AAR) policies

## Routes advertisement with OMP: (3 Types)

- **OMP routes:** LAN routes. It can be [[OSPF]], [[BGP]], static or connected routes. These are redistributed into OMP and advertised towards the Controller. OMP routes resolve their next-hop to a [[TLOC]]. An OMP route is installed in the forwarding table only if the next-hop [[TLOC]] is known and there is a BFD session in UP state associated with that TLOC. By default, OMP only advertises the best route out of multiple equal ones. If no policy is applied, advertise all TLOCs to all WAN Edges. It carries below attributes:
  - *VPN Number:* 1 -to- 65530 (except 512, reserved for OOBM).
  - *Originator*: System-IP of WAN Edge
  - *TLOC*: Next-Hop identifier of the OMP routes
  - *Site-IDs*: Similar to BGP ASN. All sites must have a unique Site-ID, and all WAN Edges must have the same Site-ID on the same site.
  - *Origin-Protocol:* From where WAN Edge has learned it i.e., via connected, static or any dynamic routing protocol
  - *Origin-Metric*: It helps in the best-path algorithm when OMP calculates the most optimal routes toward destinations
  - *OMP Preference:* Similar to BGP’s local-preference. Higher is better. To influence the best path selection in OMP
  - *Tag*: Similar to route-tag. It’s a transitive attribute

- **TLOC routes:** WAN routes. These routes are advertised along with additional attributes such as public and private IP addresses, color, TLOC preference, site ID, weight, tags, and encryption keys. System-IP address is used instead of the interface IP address as an identifier for a TLOC route. A TLOC route advertisement contains the following attributes:
  - Private IPv4/IPv6 addresses and ports: DHCP or manually configured IPs on WAN interfaces
  - Public IPv4/IPv6 addresses and ports: If the WAN Edge sits behind a NAT device, the outside NATed IP addresses and ports are included in the TLOC route advertisements. If not behind NAT, the public and private addresses and ports are the same
  - Color: For logical abstraction between multiple WAN types
  - Encapsulation Type: GRE or IPsec. Must match with remote TLOC
  - TLOC Preference: To influence OMP Best path when having multi-paths. Higher is better, default is 0.
  - Site-ID: To identify the originating site. If remote & local WAN Edges Site-ID is the same, they  will not form a tunnel.
  - Tag: User defined value that can be acted upon in a control policy
  - Weight: A parameter to achieve unequal traffic distribution across multiple TLOCs with equal preferences. Higher means more flows will go through that TLOC compared to other TLOC on WAN Edge.

- **Service routes:**  To exchange embedded services such as firewall, IPS, application-specific optimizations, and load-balancers. Network Service (FW, IPS etc.) must be Layer-2 adjacent to WAN Edge (There must not be a Layer 3 device in-between).  Controller does not advertise Service routes to WAN Edges. Service routes contains the following attributes:
  - VPN-ID: VPN that the service applies to
  - Service-ID: Type of service that is being advertised. 7 pre-defined:
    - FW maps to svc-id 1;
    - IDS maps to svc-id 2;
    - IPS maps to svc-id 3;
    - Custom Services: For customer defined:
      - netsvc1 maps to svc-id 4;
      - netsvc2 maps to svc-id 5;
      - netsvc3 maps to svc-id 6;
      - netsvc4 maps to svc-id 7;
  - Originator ID: System-IP of the WAN Edge that originates the service route
  - TLOC: Where service is located.

## Misc

- By default, only the best 4 routes (according to OMP Best-Path Algorithm) are advertised out. Maximum 16 can be advertised. To change the behavior on Controller, use the command: `omp send-path-limit <1-16>`.
- The OMP best-path algorithm sorts the best routes in descending order (from best to worst).
- The Controller always inserts and keeps all routes sorted, with the best route at the top.
- The `omp ecmp-limit <5>` parameter defines the maximum number of best paths that can be installed in the routing table.
- The `controller-send-path-limit` defines the maximum number of best-paths that a Controller can advertise to another Controller.
- The `omp send-backup-paths` tell Controller to advertise the first set of non-best routes.

## OMP Best-Path Selection

- *Route State:* A route is ACTIVE when there is an OMP session in UP state. A route is STALE when the OMP session with the peer is in GRACEFUL RESTART mode
- *Route Resolve-ability:* Valid & Reachable next-hop TLOC
- *Admin Distance:* (WAN Edge Only). Locally significant. OMP has AD of 250 on WAN Edges (Viptela) and 251 on WAN Edges (Cisco). AD is not a parameter in OMP, is not advertised, and does not influence Controller.
- Route Preference: Higher is better. Default is 0.
- *TLOC Preference:* (WAN Edge Only). TLOC routes are *not* bound to VPN-ID. Therefore, changing the TLOC preference affects WAN Edges path selection for all VPNs.
- *Origin:*
  - Connected
  - Static
  - EIGRP summary
  - eBGP
  - OSPF intra-area
  - OSPF inter-area
  - IS-IS level 1
  - EIGRP external
  - OSPF external
  - IS-IS level 2
  - iBGP
  - Unknown
- *Origin Metric:* If Origin type is same, select the route with lower origin metric
- *Tiebreaker 1 (Source Preference):* Controller only. Prefer WAN Edge sourced routes over Controller sourced
- *Tiebreaker 2 (System IP):* Select the routes that have the lowest router-id (System-IP).
- *Tiebreaker 3 (Private TLOC IP):* For routes coming from the same WAN Edge, prefer the ones with a lower private TLOC IP address.

## OMP Graceful Restart

- When SD WAN control Plane becomes unavailable, data planes continue functioning and forwarding traffic. WAN Edge and Controller cache the OMP information that they learn from peers. The cached information includes OMP, TLOC, and SERVICE routes, IPsec SA parameters, and the centralized data policies in place.

**TLOC Action** is a control-policy option that inserts an intermediate hop in an OMP route to a destination prefix. The intermediate TLOC and the ultimate TLOC must be the same color for the TLOC-action to work. The intermediate router must be enabled for service TE. There are four TLOC-action (s):

- Primary
- Backup
- ECMP
- Strict (default)

[[Cisco SDWAN]]