from utils import check_service_status, getNodeStats, getSyncRemote, getSyncLocal, get_available_space, post_to_vstats
from config import NODE_ARRAY
from time import sleep
import os
import socket
from logging_util import setup_logging  # Correct import assumed

# Setup log
log = setup_logging()
hostname = socket.gethostname()
count = 0

while True:
    count += 1  # Increment count
    log.info('Command Center Loop - Start')
    
    load = os.getloadavg()  # Returns a tuple

    for node in NODE_ARRAY:
        enabled, active = check_service_status(node.get('service_name'))
        space = get_available_space(node.get('harmony_folder'))

        if not enabled or not active:
            if not enabled:
                log.error(f"{node['service_name']} Service not enabled")
            if not active:
                log.error(f"{node['service_name']} Service not active")
            post_to_vstats({
                "unique_name": node.get('unique_name'),
                "hostname": hostname,
                "shard": node.get('shard'),
                "service_name": node.get('service_name'),
                "service_enabled": enabled,
                "service_status": active,
                "load": load,
                "space": space,
                "count": count
            })
        else:
            node_stats = getNodeStats(node)
            if node_stats and 'consensus' in node_stats:
                log.info("Found node_stats and consensus.")
                try:                    
                    post_to_vstats({
                        "unique_name": node.get('unique_name'),
                        "hostname": hostname,
                        "shard": node.get('shard'),
                        "service_name": node.get('service_name'),
                        "service_enabled": enabled,
                        "service_status": active,
                        "load": load,
                        "space": space,
                        "signing_mode": node_stats["consensus"]["mode"],
                        "block_remote": getSyncRemote(node, f'https://api.s{node_stats["shard-id"]}.t.hmny.io'),
                        "block_local": getSyncLocal(node, node_stats['shard-id']),
                        "blskey": node_stats.get('blskey'),
                        "peerid": node_stats.get('peerid'),
                        "count": count
                    })
                except Exception as e:
                    log.error(f'Problem getting sync data: {e}')
            else:
                log.info(f"node_stats or consensus not found.")
                post_to_vstats({
                    "unique_name": node.get('unique_name'),
                    "hostname": hostname,
                    "shard": node.get('shard'),
                    "service_name": node.get('service_name'),
                    "service_enabled": enabled,
                    "service_status": active,
                    "load": load,
                    "space": space,
                    "count": count
                })

    log.info('Command Center Loop - End')
    sleep(60*30)  # Adjust the sleep time as needed
