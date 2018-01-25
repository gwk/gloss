set -ex

sudo cp noatime.plist /Library/LaunchDaemons/noatime.plist
sudo launchctl load /Library/LaunchDaemons/noatime.plist
mount | grep noatime
