# 交叉编译OpenSSH服务

## Set Environment

```shell
export CROSS_COMPILE=aarch64-linux-gnu-

export ROOTFS=../install
```

## Compile zlib

```shell
AR=${CROSS_COMPILE}ar CC=${CROSS_COMPILE}gcc RANLIB=${CROSS_COMPILE}ranlib ./configure --prefix=$ROOTFS/usr
make
make install
```

## Compile OpenSSL

```shell
./Configure linux-aarch64 --prefix=$ROOTFS/usr
make
make install
```

## Compile OpenSSH


```shell
./configure --host=aarch64-linux-gnu --with-libs --with-zlib=../zlib --with-ssl-dir=../openssl-OpenSSL_1_1_1f -prefix=/usr --disable-strip
make
make INSTALL_PREFIX=$ROOTFS install

ssh-keygen -t rsa -f ssh_host_rsa_key -N ""
ssh-keygen -t dsa -f ssh_host_dsa_key -N ""
ssh-keygen -t ecdsa -f ssh_host_ecdsa_key -N ""
ssh-keygen -t dsa -f ssh_host_ed25519_key -N ""
chmod 600 ssh_host_ed25519_key

mkdir /var/empty
mkdir /var/run
```

create startup script `/etc/init.d/S50sshd`

```shell
#!/bin/sh
#
# sshd        Starts sshd.
#
 
# Make sure the ssh-keygen progam exists
[ -f /usr/bin/ssh-keygen ] || exit 0
 
# Create any missing keys
/usr/bin/ssh-keygen -A
 
umask 077
 
start() {
        echo -n "Starting sshd: "
        /usr/sbin/sshd
        touch /var/lock/sshd
        echo "OK"
}
stop() {
        echo -n "Stopping sshd: "
        killall sshd
        rm -f /var/lock/sshd
        echo "OK"
}
restart() {
        stop
        start
}
 
case "$1" in
  start)
        start
        ;;
  stop)
        stop
        ;;
  restart|reload)
        restart
        ;;
  *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
esac
 
exit $?
```