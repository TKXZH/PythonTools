#!/usr/bin/env bash
mkdir /usr/java
wget --no-cookies --no-check-certificate --header "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com%2F; oraclelicense=accept-securebackup-cookie" "http://download.oracle.com/otn-pub/java/jdk/8u141-b15/336fa29ff2bb4ef291e347e091f7f4a7/jdk-8u141-linux-x64.tar.gz"
mv jdk-8u141-linux-x64.tar.gz /usr/java
tar -xzvf /usr/java/jdk-8u141-linux-x64.tar.gz /usr/java/
rm -rf /usr/java/jdk-8u141-linux-x64.tar.gz
touch /etc/profile.d/java.sh
echo -e 'JAVA_HOME=/usr/java/jdk1.8.0_141' >> /etc/profile.d/java.sh
echo -e 'PATH=$JAVA_HOME/bin:$PATH' >> /etc/profile.d/java.sh
echo -e 'CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar' >> /etc/profile.d/java.sh
echo -e 'export JAVA_HOME PATH CLASSPATH' >> /etc/profile.d/java.sh
source /etc/profile.d/java.sh
