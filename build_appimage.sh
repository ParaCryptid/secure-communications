
#!/bin/bash
set -e

APP=SecureComm
APPDIR=AppDir
VERSION=1.0.0

mkdir -p $APPDIR/usr/bin
mkdir -p $APPDIR/usr/share/applications
mkdir -p $APPDIR/usr/share/icons/hicolor/256x256/apps

cp dist/SecureComm $APPDIR/usr/bin/
echo -e "[Desktop Entry]\nName=$APP\nExec=SecureComm\nIcon=SecureComm\nType=Application\nCategories=Utility;" > $APPDIR/usr/share/applications/$APP.desktop

cp resources/icon.png $APPDIR/usr/share/icons/hicolor/256x256/apps/SecureComm.png
chmod +x $APPDIR/usr/bin/SecureComm

wget -O appimagetool https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool
./appimagetool $APPDIR
