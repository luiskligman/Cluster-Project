# Initial Setup of Ubuntu Server on Nodes

1. Flash Ubuntu Server to a flash drive, in my instance I am using `Ubunutu 24.04.3 LTS`
2. Go through initial setup for each node, `username = luis` for each node

- Main node's hostname is `head`
- Worker node's hostname is `worker[1:4]`
- `hostname` and `servers name` are the same

3. Install `openSSH Server` during download, or don't, easy to install later
4. Finish install, follow directions, will reboot and ask you to remove `usb drive`
5. Once booted back up, `update all packages`

```bash
sudo apt upgrade
sudo apt update
```

6. Generate a `SSH key` on Macbook in root directory

```bash
cd ~
ssh-keygen -t ed25519
```

7. Make sure `openSSH Server` is running on the ubuntu server machine

```bash
sudo apt install openssh-server # if not installed
# check status
sudo systemctl status ssh
```

8. If not active, activate ssh

```bash
sudo systemctl start ssh
sudo systemctl enable ssh
```

9. Find the Optiplex `IP address`

```bash
ip a
```

10. My ip address was `10.0.1.15`, therefore, now from Macbook, do

```bash
cd ~
ssh-copy-id luis@10.0.1.15
```

10. Test the connection

```bash
ssh luis@10.0.1.15
pwd
exit
```

11. Now we need to change the ip address to a `static ip address`

```bash
cd ~
ip a
```

12. Look for something like `enp1s0`, that is what it was in this instance
13. Now edit netplan config

```bash
ls /etc/netplan  # see what files exist
sudo nano /etc/netplan/50-cloud-init.yaml  # in this case
```

14. Update the `yaml` file with this static config

```yaml
network:
  version: 2
  ethernets:
    enp1s0:
      dhcp4: no
      addresses:
        - 10.0.1.100/24
      routes:
        - to: default
          via: 10.0.1.1
      nameservers:
        addresses:
          - 8.8.8.8
          - 1.1.1.1
```

15. Apply changes by doing `control O` then `control X` to exit back to terminal
16. Apply the changes

```bash
cd ~
sudo netplan apply
```

17. Check

```bash
ip a
```

18. In my case is shows `inet 10.0.1.100/24`
19. Reconnect using new ip to check connection, this will add the new ip address to the list of hosts

```bash
cd ~
ssh luis@10.0.1.100
pwd
exit
```

20. Remove the old host name from keys

```bash
ssh-keygen -R 10.0.1.15
```

21. Check to make sure the machine maintains `static ip address` after reboot

```bash
cd ~
sudo reboot  # enter password
```

22. Either login to the machine and do once logged in

```bash
ip a
```

23. Or, ssh back in if everything worked properly and perform

```bash
ssh luis@10.0.1.100
ip a
```

24. Check that SSH will `start at boot`

```bash
sudo systemctl is-enabled ssh
```

25. Mine was disabled, so do

```bash
sudo systemctl enable ssh
sudo systemctl is-enabled ssh
# Should say 'enabled' if done correctly
```

26. Install `btop` and `neofetch` to gain more information about the system

```bash
sudo apt install neofetch
sudo apt install btop
```

27. Specs for head node: `12th Gen Intel i5-12500 (12) @ 4.600 GHz, total memory: 15681MiB`

```bash
btop
htop  # btop has cooler interface
neofetch
```

28. Setup `WoL` capability for the computer

```bash
# Find the network interface name
ip link show  # enp1s0 in this case
# Check WoL support
sudo ethtool enp1s0 | grep Wake-on
# Look for output like:
# Supports Wake-on: pumbg
# Wake-on: d

# Supports Wake-on: shows whats WoL modes the hardware supports (g = magic packet)
# Wake-on: Shows current setting (d = disabled, g = enabled)
```

29. Enable WoL

```bash
sudo ethtool -s enp1s0 wol g
```

30. Make it persistent across reboots, create a `systemd service`:

```bash
cd ~
sudo nano /etc/systemd/system/wol.service
```

31. Type this into that file

```ini
[Unit]
Description=Enable Wake-on-LAN
After=network.target

[Service]
Type=oneshot
ExecStart=/sbin/ethtool -s enp1s0 wol g

[Install]
WantedBy=multi-user.target
```

32. Enable the service

```bash
sudo systemctl enable wol.service
sudo systemctl start wol.service
```

33. Verify its enabled

```bash
sudo ethtool enp1s0 | grep Wake-on
# Should now show:  Wake-on: g
```

34. Grab the devices `Mac Address` so you can wake over the internet, on make install `wakeonlan`

```bash
ip link show enp1s0
# Look for the line with link/ether, contains mac address
```

```bash
brew install wakeonlan
```
- **Luis `Mac Address`**: 50:eb:f6:cf:ae:fc
- **Head Node `Mac Address`**: 08:92:04:eb:31:fe
- **Worker1 `Mac Address`**: 90:b1:1c:71:9a:9a
- **Worker2 `Mac Address`** : 90:b1:1c:71:95:b8
- **Worker3 `Mac Address`**: 90:b1:1c:71:a4:b9
- **Worker4 `Mac Address`**: 90:b1:1c:71:93:64

35. Adjust `Bios` settings, hold `F2` on boot, in `Power` change `Deep Sleep Control` setting to `Disabled`, go to `System Management` then to `Wake on LAN/WLAN` and select option `LAN with PXE Boot`
36. Test the `WoL` functionality

```bash
cd ~
ssh luis@10.0.1.100
sudo shutdown now
wakeonlan 08:92:04:eb:31:fe
```

37. Takes about `90 seconds to boot`, once booted, you can `ssh` into if headless, or it will load `terminal GUI` once fully booted
