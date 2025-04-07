
#!/bin/bash
set -e

APP=SecureComm
VERSION=1.0.0
ARCH=amd64

mkdir -p $APP-$VERSION/DEBIAN
mkdir -p $APP-$VERSION/usr/local/bin

cp dist/SecureComm $APP-$VERSION/usr/local/bin/

cat <<EOF > $APP-$VERSION/DEBIAN/control
Package: $APP
Version: $VERSION
Section: base
Priority: optional
Architecture: $ARCH
Depends: python3
Maintainer: ParaCryptid
Description: Offline secure communications system
EOF

dpkg-deb --build $APP-$VERSION
