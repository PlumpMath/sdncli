addflow = """
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<flow xmlns="urn:opendaylight:flow:inventory">
 <strict>false</strict>

    <table_id>0</table_id>
        <id>1</id>
        <cookie_mask>255</cookie_mask>
        <match>
            <in-port>2</in-port>
        </match>
        <hard-timeout>12</hard-timeout>
        <cookie>1</cookie>
        <idle-timeout>34</idle-timeout>
        <flow-name>L2-Flow</flow-name>
        <priority>2</priority>
        <installHw>true</installHw>
        <barrier>false</barrier>
    <instructions>
     <instruction>
        <order>0</order>
            <apply-actions>
                <action>
                     <order>0</order>
                     <output-action>
                         <output-node-connector>1</output-node-connector>
                     </output-action>
                </action>
            </apply-actions>
        </instruction>
    </instructions>
</flow>
"""

