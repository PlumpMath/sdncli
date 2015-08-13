
def netconf_mount(name, address, port, user, password):
    data = """
    <module xmlns="urn:opendaylight:params:xml:ns:yang:controller:config">
      <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">prefix:sal-netconf-connector</type>
      <name>{name}</name>
      <address xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">{address}</address>
      <port xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">{port}</port>
      <username xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">{user}</username>
      <password xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">{password}</password>
      <tcp-only xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">false</tcp-only>
      <event-executor xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
        <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:netty">prefix:netty-event-executor</type>
        <name>global-event-executor</name>
      </event-executor>
    <binding-registry xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
      <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:md:sal:binding">prefix:binding-broker-osgi-registry</type>
      <name>binding-osgi-broker</name>
    </binding-registry>
    <dom-registry xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
      <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:md:sal:dom">prefix:dom-broker-osgi-registry</type>
      <name>dom-broker</name>
    </dom-registry>
    <client-dispatcher xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
      <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:config:netconf">prefix:netconf-client-dispatcher</type>
      <name>global-netconf-dispatcher</name>
    </client-dispatcher>
    <processing-executor xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
      <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:threadpool">prefix:threadpool</type>
      <name>global-netconf-processing-executor</name>
    </processing-executor>
    </module>
    """
    return data.format(name=name, address=address, port=port, user=user, password=password)


def netconf_mount_vdx(name, address, port, user, password):
    data = """
    <module xmlns="urn:opendaylight:params:xml:ns:yang:controller:config">
      <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">prefix:sal-netconf-connector</type>
      <name>{name}</name>
      <address xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">{address}</address>
      <port xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">{port}</port>
      <username xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">{user}</username>
      <password xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">{password}</password>
      <yang-module-capabilities xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:ietf:params:xml:ns:yang:ietf-netconf-with-defaults?revision=2011-06-01&amp;module=ietf-netconf-with-defaults</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">http://brocade.com/ns/brocade-auto-shut-edge-port?module=brocade-auto-shut-edge-port</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">http://brocade.com/ns/brocade-logical-chassis?module=brocade-logical-chassis</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">http://tail-f.com/yang/common?module=tailf-common&amp;revision=2013-11-01</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">http://www.w3.org/2001/XMLSchema?module=tailf-xsd-types&amp;revision=2009-03-17</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:ietf:params:netconf:capability:submodule:1.0?module=tailf-cli-extensions&amp;revision=2012-11-08</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:ietf:params:netconf:capability:submodule:1.0?module=tailf-meta-extensions&amp;revision=2010-08-19</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">http://tail-f.com/ns/aaa/1.1?module=tailf-aaa&amp;revision=2011-09-22</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">http://tail-f.com/ns/webui?module=tailf-webui&amp;revision=2013-03-07</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">http://tail-f.com/yang/common-monitoring?module=tailf-common-monitoring&amp;revision=2013-06-14</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">http://tail-f.com/yang/confd-monitoring?module=tailf-confd-monitoring&amp;revision=2013-06-14</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">http://tail-f.com/yang/netconf-monitoring?module=tailf-netconf-monitoring&amp;revision=2012-06-14</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-Enclosure-show?module=brocade-Enclosure-show</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-aaa?module=brocade-aaa&amp;revision=2010-10-21</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-aaa-ext?module=brocade-aaa-ext&amp;revision=2010-09-21</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-ag?module=brocade-ag</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-anycast-gateway?module=brocade-anycast-gateway&amp;revision=2014-03-27</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-arp?module=brocade-arp&amp;revision=2011-10-31</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-beacon?module=brocade-beacon&amp;revision=2011-10-31</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-bgp?module=brocade-bgp&amp;revision=2010-11-29</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-bprate-limit?module=brocade-bprate-limit&amp;revision=2011-10-31</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-bum-storm-control?module=brocade-bum-storm-control&amp;revision=2011-11-10</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-cdp?module=brocade-cdp&amp;revision=2010-08-17</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-cee-map?module=brocade-cee-map&amp;revision=2011-04-18</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-chassis?module=brocade-chassis&amp;revision=2011-04-11</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-clock?module=brocade-clock&amp;revision=2009-05-01</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-common-def?module=brocade-common-def&amp;revision=2010-02-22</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-dhcp?module=brocade-dhcp&amp;revision=2013-05-20</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-dhcpv6?module=brocade-dhcpv6&amp;revision=2014-06-11</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-distributedlog?module=brocade-distributedlog&amp;revision=2010-12-02</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-dot1x?module=brocade-dot1x&amp;revision=2011-07-13</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-eld?module=brocade-eld&amp;revision=2011-08-08</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-entity?module=brocade-entity&amp;revision=2014-05-09</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-fabric-service?module=brocade-fabric-service&amp;revision=2011-07-22</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-fc-auth?module=brocade-fc-auth&amp;revision=2010-10-21</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-fcoe?module=brocade-fcoe&amp;revision=2011-07-22</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-fcoe-ext?module=brocade-fcoe-ext&amp;revision=2011-07-15</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-firmware?module=brocade-firmware&amp;revision=2011-04-11</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-firmware-ext?module=brocade-firmware-ext&amp;revision=2011-02-25</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-ha?module=brocade-ha&amp;revision=2011-10-31</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-hardware?module=brocade-hardware&amp;revision=2012-12-20</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-http?module=brocade-http-config&amp;revision=2013-11-28</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-http-redirect?module=brocade-http-redirect&amp;revision=2013-01-14</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-icmp?module=brocade-icmp</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-igmp?module=brocade-igmp&amp;revision=2011-03-28</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-igmp-snooping?module=brocade-igmp-snooping&amp;revision=2010-06-02</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-interface?module=brocade-interface&amp;revision=2012-04-24</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-interface-ext?module=brocade-interface-ext&amp;revision=2014-04-01</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-intf-loopback?module=brocade-intf-loopback&amp;revision=2011-09-28</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-ip-access-list?module=brocade-ip-access-list&amp;revision=2011-03-01</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-ip-administration?module=brocade-ip-administration&amp;revision=2011-04-11</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-ip-config?module=brocade-ip-config&amp;revision=2011-10-31</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-ip-forward?module=brocade-ip-forward&amp;revision=2011-07-18</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-ip-policy?module=brocade-ip-policy&amp;revision=2011-03-19</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-ipv6-access-list?module=brocade-ipv6-access-list&amp;revision=2012-07-01</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-ipv6-config?module=brocade-ipv6-config&amp;revision=2013-07-26</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-ipv6-nd-ra?module=brocade-ipv6-nd-ra&amp;revision=2013-07-26</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-ipv6-rtm?module=brocade-ipv6-rtm&amp;revision=2013-10-22</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-lacp?module=brocade-lacp&amp;revision=2010-01-25</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-lag?module=brocade-lag&amp;revision=2014-04-14</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-license?module=brocade-license&amp;revision=2011-08-22</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-linecard-management?module=brocade-linecard-management&amp;revision=2011-09-06</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-lldp?module=brocade-lldp&amp;revision=2010-04-28</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-lldp-ext?module=brocade-lldp-ext&amp;revision=2014-06-01</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-mac-access-list?module=brocade-mac-access-list&amp;revision=2011-02-28</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-mac-address-table?module=brocade-mac-address-table&amp;revision=2011-02-15</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-mld-snooping?module=brocade-mld-snooping&amp;revision=2013-07-29</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-nameserver?module=brocade-nameserver&amp;revision=2012-03-07</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-netconf-ext?module=brocade-netconf-ext&amp;revision=2012-02-03</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-ntp?module=brocade-ntp&amp;revision=2009-05-01</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-ospf?module=brocade-ospf&amp;revision=2010-11-29</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-ospfv3?module=brocade-ospfv3&amp;revision=2013-08-25</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-pim?module=brocade-pim&amp;revision=2011-06-01</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-policer?module=brocade-policer&amp;revision=2011-03-04</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-port-profile?module=brocade-port-profile&amp;revision=2011-07-21</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-port-profile-ext?module=brocade-port-profile-ext&amp;revision=2000-07-15</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-qos?module=brocade-qos&amp;revision=2010-04-28</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-ras?module=brocade-ras&amp;revision=2011-04-11</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-ras-ext?module=brocade-ras-ext&amp;revision=2011-01-20</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-rbridge?module=brocade-rbridge&amp;revision=2011-06-21</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-rmon?module=brocade-rmon&amp;revision=2011-02-28</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-rtm?module=brocade-rtm&amp;revision=2011-09-28</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-sec-services?module=brocade-sec-services&amp;revision=2012-07-28</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-sflow?module=brocade-sflow&amp;revision=2009-12-10</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-snmp?module=brocade-snmp&amp;revision=2011-03-18</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-span?module=brocade-span&amp;revision=2010-04-28</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-system?module=brocade-system&amp;revision=2011-08-09</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-system-monitor?module=brocade-system-monitor&amp;revision=2011-11-16</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-system-monitor-ext?module=brocade-system-monitor-ext&amp;revision=2011-05-05</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-terminal?module=brocade-terminal&amp;revision=2011-04-18</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-threshold-monitor?module=brocade-threshold-monitor&amp;revision=2011-11-24</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-threshold-monitor-ext?module=brocade-threshold-monitor-ext&amp;revision=2011-05-05</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-trilloam?module=brocade-trilloam&amp;revision=2011-04-18</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-tunnels?module=brocade-tunnels&amp;revision=2014-03-25</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-udld?module=brocade-udld&amp;revision=2012-03-20</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-vcs?module=brocade-vcs&amp;revision=2011-05-26</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-vlan?module=brocade-vlan&amp;revision=2009-12-10</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-vrf?module=brocade-vrf&amp;revision=2012-04-28</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-vrrp?module=brocade-vrrp&amp;revision=2011-10-31</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-vrrpv3?module=brocade-vrrpv3&amp;revision=2013-10-21</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-vswitch?module=brocade-vswitch&amp;revision=2011-04-18</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-xstp?module=brocade-xstp&amp;revision=2012-09-13</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-xstp-ext?module=brocade-xstp-ext&amp;revision=2011-02-22</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:brocade-zone?module=brocade-zone&amp;revision=2010-12-01</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:brocade.com:mgmt:certutil?module=brocade-certutil&amp;revision=2011-06-13</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:ietf:params:xml:ns:yang:ietf-inet-types?module=ietf-inet-types&amp;revision=2010-09-24</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring?module=ietf-netconf-monitoring&amp;revision=2010-10-04</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:ietf:params:xml:ns:yang:ietf-netconf-notifications?module=ietf-netconf-notifications&amp;revision=2012-02-06</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:ietf:params:xml:ns:yang:ietf-yang-types?module=ietf-yang-types&amp;revision=2010-09-24</capability>
      </yang-module-capabilities>
        <tcp-only xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">false</tcp-only>
      <event-executor xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
        <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:netty">prefix:netty-event-executor</type>
        <name>global-event-executor</name>
      </event-executor>
      <binding-registry xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
        <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:md:sal:binding">prefix:binding-broker-osgi-registry</type>
        <name>binding-osgi-broker</name>
      </binding-registry>
      <dom-registry xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
        <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:md:sal:dom">prefix:dom-broker-osgi-registry</type>
        <name>dom-broker</name>
      </dom-registry>
      <client-dispatcher xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
        <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:config:netconf">prefix:netconf-client-dispatcher</type>
        <name>global-netconf-dispatcher</name>
      </client-dispatcher>
      <processing-executor xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
        <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:threadpool">prefix:threadpool</type>
        <name>global-netconf-processing-executor</name>
      </processing-executor>
      </module>
      """
    return data.format(name=name, address=address, port=port, user=user, password=password)


def netconf_mount_mlx(name, address, port, user, password):
    data = """
    <module xmlns="urn:opendaylight:params:xml:ns:yang:controller:config">
      <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">prefix:sal-netconf-connector</type>
      <name>{name}</name>
      <address xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">{address}</address>
      <port xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">{port}</port>
      <username xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">{user}</username>
      <password xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">{password}</password>
      <yang-module-capabilities xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">http://brocade.com/ns/netconf/config/netiron-config?module=netiron-config&amp;revision=0000-00-00</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">http://brocade.com/ns/netconf/config/common-defs?module=common-defs&amp;revision=0000-00-00</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">http://brocade.com/ns/netconf/config/vlan-config?module=vlan-config&amp;revision=0000-00-00</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">http://brocade.com/ns/netconf/config/interface-config?module=interface-config&amp;revision=0000-00-00</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">http://brocade.com/ns/netconf/config/mpls-config?module=mpls-config&amp;revision=0000-00-00</capability>
      <capability xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">urn:ietf:params:xml:ns:yang:ietf-yang-types?module=ietf-yang-types&amp;revision=2010-09-24</capability>
      </yang-module-capabilities>
        <tcp-only xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">false</tcp-only>
      <event-executor xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
        <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:netty">prefix:netty-event-executor</type>
        <name>global-event-executor</name>
      </event-executor>
      <binding-registry xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
        <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:md:sal:binding">prefix:binding-broker-osgi-registry</type>
        <name>binding-osgi-broker</name>
      </binding-registry>
      <dom-registry xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
        <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:md:sal:dom">prefix:dom-broker-osgi-registry</type>
        <name>dom-broker</name>
      </dom-registry>
      <client-dispatcher xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
        <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:config:netconf">prefix:netconf-client-dispatcher</type>
        <name>global-netconf-dispatcher</name>
      </client-dispatcher>
      <processing-executor xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
        <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:threadpool">prefix:threadpool</type>
        <name>global-netconf-processing-executor</name>
      </processing-executor>
      </module>
      """
    return data.format(name=name, address=address, port=port, user=user, password=password)

