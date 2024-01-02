#/bin/bash
 
interval=$2
dev=$1
 
rx_vport_rdma_unicast_packets1=$(ethtool -S $dev | grep rx_vport_rdma_unicast_packets|awk '{print $NF}')
rx_vport_rdma_unicast_bytes1=$(ethtool -S $dev | grep rx_vport_rdma_unicast_bytes|awk '{print $NF}')
tx_vport_rdma_unicast_packets1=$(ethtool -S $dev | grep tx_vport_rdma_unicast_packets|awk '{print $NF}')
tx_vport_rdma_unicast_bytes1=$(ethtool -S $dev | grep tx_vport_rdma_unicast_bytes|awk '{print $NF}')
time1=$(date +%s)
 
while true
do
    sleep $interval
    rx_vport_rdma_unicast_packets2=$(ethtool -S $dev | grep rx_vport_rdma_unicast_packets|awk '{print $NF}')
    rx_vport_rdma_unicast_bytes2=$(ethtool -S $dev | grep rx_vport_rdma_unicast_bytes|awk '{print $NF}')
    tx_vport_rdma_unicast_packets2=$(ethtool -S $dev | grep tx_vport_rdma_unicast_packets|awk '{print $NF}')
    tx_vport_rdma_unicast_bytes2=$(ethtool -S $dev | grep tx_vport_rdma_unicast_bytes|awk '{print $NF}')
    time2=$(date +%s)
    rx_packet_speed=$((($rx_vport_rdma_unicast_packets2 - $rx_vport_rdma_unicast_packets1) / ($time2 - $time1)))
    rx_byte_speed=$((($rx_vport_rdma_unicast_bytes2 - $rx_vport_rdma_unicast_bytes1) / ($time2 - $time1)))
    tx_packet_speed=$((($tx_vport_rdma_unicast_packets2 - $tx_vport_rdma_unicast_packets1) / ($time2 - $time1)))
    tx_byte_speed=$((($tx_vport_rdma_unicast_bytes2 - $tx_vport_rdma_unicast_bytes1) / ($time2 - $time1)))
 
    echo "RX packet rate: $rx_packet_speed"
    echo "RX byte   rate: $rx_byte_speed"
    echo "TX packet rate: $tx_packet_speed"
    echo "TX byte   rate: $tx_byte_speed"
    echo
 
    rx_vport_rdma_unicast_packets1=$rx_vport_rdma_unicast_packets2
    rx_vport_rdma_unicast_bytes1=$rx_vport_rdma_unicast_bytes2
    tx_vport_rdma_unicast_packets1=$tx_vport_rdma_unicast_packets2
    tx_vport_rdma_unicast_bytes1=$tx_vport_rdma_unicast_bytes2
    time1=$time2
done
