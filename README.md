# Node Stats

# vStats Alerts
This is an automated script that will periodically ( every 30 mins ) send your node data to vStats for dashboard + alerts.

Dashboard:
- Shows your node stats on a single page.
- Unique page can be found by running /nodestats in vStatsBot

Alerts:
- Blockchain Sync - Compares local vs remote height
```
🔻Shard2-Hel --- Shard 0 Behind🔻
Remote: 22716160
Local: 22711441
Difference: -4719
```
- Space Left - Alerts you when space is lower than 25GB
```
🔻Shard2-fsn --- Space Low 20GB Left🔻
```
- Double Signing Check - Alerts you if a bls key is found on one or more signing servers
```
🚨Double Signing🚨
Identical Keys exist on multiple signing Shard 3 servers: 
shard3-fsn
shard3-hel
Matched Keys:
0701becb090da6d7a74175f645c3827756433278064b89a3299fceaf95c5faa2faeab642bd5c46e30128f1240742ce8f
Date & Time: 2022-02-07 13:03:34
```
- If your node has gone into 'Syncing' mode due to a harmony error, it will alert you.
```
🚨!!! shard3-fsn = Syncing !!!🚨
Please check node.
```
- <b>Daily Node Summary Updates</b>
```
🔶Shard3 Fsn🔶
Mode: Normal
Space: 846G
Shard 0: Synced
Shard 3: Synced
Load: 2.63
Updated: 28 mins ago 
```


### 1) Download the script
We suggest storing it in your home folder.

```
cd ~/
git clone https://github.com/DavidWhicker/harmony_node_stats.git
cd harmony_node_stats
```
To update use `git pull`

### 2) Get a token
Send the command `/token` to the @vStatsBot on telegram to get your token.

Copy the token, as message on telegram will auto delete after 60 seconds.

### 3) Setup 
Install required packages if missing:

<!-- `sudo apt update && sudo apt upgrade -y` -->
```
sudo apt install python3-pip
pip3 install -r requirements.txt
```
Rename .env.example to .env and edit the following variables:
```
cp .env.example .env
nano .env
```
```
#Add your token from vstats. Run /token on vStatsBot
VSTATS_TOKEN="" 

# Validator Address
VALIDATOR_ADDRESS=""

# Alert when blskey match is found on 1 or more servers | Default: false  
DOUBLE_SIGN_CHECK_ENABLED=true|false 

# Alert when local vs remote gap is larger than 100 | Default: false  
SYNC_CHECK_ENABLED=true|false 

# Alert when space is less than 25GB | Default: false  
SPACE_CHECK_ENABLED=true|false

# Add path containing .hmy. Run pwd in .hmy location to get full path e.g /home/serviceharmony/harmony 
HARMONY_FOLDER=""
```
### 4) Test Script 
Test the .env variables and script is working as expected. 

Run the below from the script directory:

```
python3 main.py
```

Alerts on screen AND vStatsBot should appear. Once successful, please cancel the script ( CTRL + C ) and move onto the next step.

### 5) Setup Service
Now setup script to run as a service in the background. 

Run the following with root privileges. If you do not have access with root then you may setup a tmux session ( see: Alternative Setup - Tmux ).

Please note: add correct info for < USER > & < PATH TO SCRIPT >

```
cat<<-EOF > /etc/systemd/system/harmony_node_stats.service
[Unit]
Description=harmony_node_stats daemon
After=network-online.target

[Service]
Type=simple
Restart=always
RestartSec=1
User=<USER>
WorkingDirectory=<PATH TO SCRIPT>
ExecStart=python3 main.py
SyslogIdentifier=harmony_node_stats
StartLimitInterval=0
LimitNOFILE=65536
LimitNPROC=65536

[Install]
WantedBy=multi-user.target
EOF
```
Followed by:

```
sudo systemctl daemon-reload
sudo chmod 755 /etc/systemd/system/harmony_node_stats.service
sudo systemctl enable harmony_node_stats.service
sudo service harmony_node_stats start
sudo service harmony_node_stats status
```

### 5b) Alternative Setup - Tmux

`tmux new-session -s harmony_node_stats`

`cd ~/harmony_node_stats/`

`python3 main.py`


### Logs
Check logs to make sure the script is running as expected. 

### Misc
Start Service
```
sudo service harmony_node_stats start
```

Stop Service
```
sudo service harmony_node_stats stop
```

Status Check
```
sudo service harmony_node_stats status
```
