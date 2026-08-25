*This project has been created as part of the 42 curriculum by adarabi.*

# Born2beRoot

## Description

Born2beRoot is a system administration project from the 42 curriculum. The task is to build a small, hardened Linux server inside a virtual machine, applying real security practices instead of just doing a default install: disk encryption, LVM, restricted SSH access, a locked-down firewall, a strict password and sudo policy, mandatory access control, and a monitoring script that reports the machine's health.

For this submission I installed a **minimal Debian server in VirtualBox**, with no desktop environment, and completed the **mandatory part only** (no bonus).

Setup summary:

- Debian, minimal install, running in VirtualBox
- Hostname: `adarabi42`
- Encrypted LVM with a separate `/home` volume
- Regular user `adarabi`, member of the `sudo` and `user42` groups
- SSH restricted to port 4242, root login over SSH disabled
- UFW enabled, only port 4242 open
- Password aging and complexity rules enforced via `login.defs` and PAM
- `sudo` restricted with attempt limits, full input/output logging, and a locked `secure_path`
- AppArmor running at boot
- `monitoring.sh` broadcasting system stats via cron every 10 minutes

## Instructions

### What is submitted

Only two files live at the root of this repository:

- `README.md`
- `signature.txt`

The virtual disk itself is **not** part of the repo — it's excluded on purpose, per the subject's rules.

### Booting the VM

1. Open the VM in VirtualBox and start it.
2. Enter the LVM encryption passphrase when prompted — the boot pauses here until it's unlocked.
3. Debian finishes booting straight to a text login prompt (no desktop).
4. Log in with the `adarabi` user.

### Connecting over SSH

Inside the VM, `sshd` listens on port **4242** only, and I set up NAT port forwarding in VirtualBox (host 4242 → guest 4242), so from the host machine:

```
ssh adarabi@localhost -p 4242
```

Trying to connect as root should always fail, since root login is disabled:

```
ssh root@localhost -p 4242
```

### Producing the signature file

Before generating the signature, the VM must be **completely shut down** — any boot changes logs/metadata on the disk and invalidates a previously computed hash.

```
sha1sum adarabi42.vdi
```

The resulting hash (and nothing else) goes into `signature.txt`. Once that's done, the VM shouldn't be powered on again, or the signature will no longer match.

### Snapshots

No snapshot should exist right before an evaluation starts:

```
VBoxManage snapshot adarabi42 list
```

A temporary snapshot can be taken during the defense if needed, but must be deleted right after.

## Why Debian

Debian was the recommended choice for anyone new to system administration, and it's what I picked. It let me focus on the actual concepts of the project — partitioning, users, SSH, firewalling, sudo, PAM — instead of fighting with a more complex distro.

### Debian vs Rocky Linux

| | Debian | Rocky Linux |
|---|---|---|
| Governance | community-maintained | RHEL-compatible, enterprise-oriented |
| Package manager | `apt` | `dnf` |
| Default MAC module | AppArmor | SELinux |
| Default firewall tool | UFW | firewalld |
| Learning curve | gentler | steeper, closer to production RHEL systems |

### apt vs aptitude

`apt` is the standard, straightforward tool for installing/updating/removing packages on Debian (`apt update`, `apt upgrade`, `apt install`, `apt remove`). `aptitude` does the same job but adds an interactive text UI and a somewhat smarter dependency resolver — useful in edge cases, but not something I needed for a minimal server.

## Virtualization

### VirtualBox vs UTM

VirtualBox is available on Windows, Linux, and Intel Macs, and is what the project requires by default; it stores disks as `.vdi` files. UTM is the usual alternative on Apple Silicon Macs, where VirtualBox often isn't supported — it runs on QEMU and uses `.qcow2` disks instead. I used VirtualBox since it worked fine on my machine.

### My VM settings

- OS: Debian, 64-bit
- RAM: as recommended for a minimal server
- Disk: single dynamically-allocated `.vdi`
- Volume group size used for guided partitioning: **12.4 GB**
- No graphical interface installed

## No graphical environment

Since this is meant to be a server, no display server was ever installed — no X.org, no Wayland, nothing. The system boots straight into `multi-user.target`. That can be double-checked with:

```
systemctl get-default
dpkg -l | grep -Ei "xorg|gdm3|lightdm|wayland|gnome|kde|xfce"
```

## Partitioning, encryption, and LVM

During installation I chose **Guided – use entire disk and set up encrypted LVM**, with the **Separate /home partition** scheme. `/boot` stays outside the encrypted volume (the bootloader needs to read the kernel before the passphrase is even asked), while everything else sits behind the LVM-on-LUKS encrypted container.

Why encrypt: without the passphrase, nothing on the encrypted f, and does not fight another Creature twice (A-B and B-A).volume can be read, even if someone gets a hold of the raw `.vdi` file.

Why LVM: it lets `/`, `/home`, and swap live as independent logical volumes inside one volume group, instead of being locked into fixed physical partitions.

```
lsblk
sudo pvdisplay
sudo vgdisplay
sudo lvdisplay
```

## Users and groups

The regular account is `adarabi`, and it belongs to two groups:

- `sudo` — administrative rights
- `user42` — required by the subject

```
groups adarabi
getent group sudo
getent group user42
```

During a defense, evaluators may ask for a new user/group to be created on the spot, e.g.:

```
sudo adduser evaluser
sudo addgroup evalgroup
sudo adduser evaluser evalgroup
```

## Hostname

The subject requires the hostname to be `<login>42`. Mine is set to `adarabi42`:

```
hostname
cat /etc/hostname
```

## SSH

SSH is configured in `/etc/ssh/sshd_config`:

```
Port 4242
PermitRootLogin no
```

Root login is disabled deliberately — a real admin should always log in as a normal user first and escalate through `sudo` only when needed, so every privileged action is explicit and traceable.

```
sudo service ssh status
sudo ss -tlnp | grep 4242
```

## Firewall (UFW)

Only port 4242 is opened; everything else is denied by default.

```
sudo ufw status
sudo ufw allow 4242
sudo ufw enable
```

### UFW vs firewalld

UFW is a thin, easy-to-read wrapper around `iptables`, and it's the natural fit for Debian/Ubuntu. `firewalld` is the equivalent on Red Hat-family systems like Rocky, built around dynamic "zones," which is more flexible but also more to learn. Since I'm on Debian, UFW was the obvious pick.

## Password policy

### Aging — `/etc/login.defs`

```
PASS_MAX_DAYS   30
PASS_MIN_DAYS   2
PASS_WARN_AGE   7
```

A password expires after 30 days, can't be changed again within 2 days of the last change, and the user gets a heads-up 7 days before it expires.

### Complexity — PAM (`/etc/pam.d/common-password`, via `libpam-pwquality`)

```
minlen=10 ucredit=-1 dcredit=-1 lcredit=-1 maxrepeat=3 reject_username difok=7 enforce_for_root
```

- at least 10 characters
- at least one uppercase, one lowercase, one digit
- no character repeated more than 3 times in a row
- can't contain the username
- must differ from the previous password by at least 7 characters (this rule is skipped for root by the subject, but I still enforce the rest of the policy on root via `enforce_for_root`)

After wiring all of this up, every existing account's password (including root's) had to be changed so the new rules actually took effect.

## Sudo configuration

Rules live in a dedicated file, edited safely through `visudo`:

```
sudo visudo -f /etc/sudoers.d/sudo_config
```

```
Defaults passwd_tries=3
Defaults badpass_message="Wrong password, try again"
Defaults logfile="/var/log/sudo/sudo.log"
Defaults log_input, log_output
Defaults iolog_dir="/var/log/sudo"
Defaults requiretty
Defaults secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin"
```

- 3 attempts max before sudo gives up
- a custom message on a wrong password
- every sudo command (input and output) logged to `/var/log/sudo/sudo.log`
- a TTY is required to run sudo at all
- a locked-down `PATH`, so sudo can't accidentally run a malicious binary planted earlier in a user's normal `PATH`

```
sudo visudo -c
sudo tail /var/log/sudo/sudo.log
```

## AppArmor

AppArmor is Debian's default mandatory access control module — it confines what a program can touch based on path-based profiles, and it's running at startup as required.

```
sudo aa-status
```

### AppArmor vs SELinux

AppArmor (Debian's default) is path-based and generally simpler to reason about. SELinux (Rocky's default) works with security labels attached to every file and process — more powerful, but noticeably harder to configure and debug.

## Monitoring script

`monitoring.sh` runs at `/usr/local/bin/monitoring.sh` and broadcasts a status report to every open terminal with `wall`, showing:

- OS architecture and kernel version
- physical / virtual CPU count
- RAM usage and percentage
- disk usage and percentage
- current CPU load
- last reboot date/time
- whether LVM is active
- number of established TCP connections
- number of logged-in sessions
- IPv4 and MAC address
- number of commands run through sudo

Key commands used inside the script:

```
uname -a
grep "physical id" /proc/cpuinfo | wc -l
grep processor /proc/cpuinfo | wc -l
free --mega
df -m
vmstat 1 4
who -b
lsblk | grep lvm
ss -ta | grep ESTAB | wc -l
users | wc -w
ip link | grep "link/ether"
journalctl _COMM=sudo | grep COMMAND | wc -l
```

## Cron

Root's crontab triggers the script every 10 minutes:

```
sudo crontab -u root -e
*/10 * * * * /usr/local/bin/monitoring.sh
```

To pause it during a defense without touching the script itself:

```
sudo service cron stop
```

## AI usage

An AI assistant was used to:

- clarify concepts I was unsure about (LVM, PAM, sudo hardening, AppArmor vs SELinux, UFW vs firewalld)
- review my configuration notes for mistakes or missing steps
- help structure and word this README

No configuration file, script, or command in this project was generated blindly by AI — everything was applied and verified by hand on the actual VM.

## Resources

- Debian Administrator's Handbook
- Debian Wiki
- `man sshd_config`, `man sudoers`, `man pam_pwquality`, `man crontab`, `man ufw`
- VirtualBox official documentation

## Final notes

This project made it clear that setting up a server is less about "installing an OS" and more about making — and being able to explain — deliberate security decisions: what's encrypted, what's open, who can do what, and how it's all logged.
