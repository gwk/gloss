#!/usr/bin/sh

set -ex

chflags nohidden ~/Library # Make user Library visible.
sudo chflags nohidden /Volumes

# Desktop services. Do not write .DS_Store files to network or USB volumes.
defaults write com.apple.desktopservices DSDontWriteNetworkStores -bool true
defaults write com.apple.desktopservices DSDontWriteUSBStores -bool true

# Dock.
defaults write com.apple.dock autohide -bool true
#defaults write com.apple.Dock autohide-delay -float 0
defaults write com.apple.dock autohide-time-modifier -float 0.4
defaults write com.apple.dock expose-animation-duration -float 0.1 # Mission Control animation speed.
defaults write com.apple.dock expose-group-by-app -bool true
defaults write com.apple.dock show-recents -bool false
defaults write com.apple.Dock showhidden -bool true # Hidden apps rendered as translucent in dock.
defaults write com.apple.dock showLaunchpadGestureEnabled -int 0
killall Dock

#Finder.
#defaults write com.apple.finder _FXShowPosixPathInTitle -bool true
defaults write com.apple.finder FXEnableExtensionChangeWarning -bool false
defaults write com.apple.finder FXPreferredViewStyle Clmv # Column view.
#defaults write com.apple.Finder AppleShowAllFiles -bool true
defaults write com.apple.finder QLEnableTextSelection -bool true # Allow text selection in quicklook.
defaults write com.apple.finder ShowExternalHardDrivesOnDesktop -bool true
#defaults write com.apple.finder DisableAllAnimations -bool true
defaults write com.apple.finder FXDefaultSearchScope -string "SCcf"
defaults write com.apple.finder _FXSortFoldersFirst -bool true

defaults write com.apple.finder FXInfoPanesExpanded -dict \
	General -bool true \
	OpenWith -bool true \
	Privileges -bool true

killall Finder

# Prevent pasting of full names along with copied email addresses.
defaults write com.apple.mail AddressesIncludeNameOnPasteboard -bool false

defaults write com.apple.screencapture location ~/Pictures/screenshots

defaults write com.apple.Safari IncludeDevelopMenu -bool true
defaults write com.apple.Safari WebKitDeveloperExtrasEnabledPreferenceKey -bool true

defaults write com.apple.SoftwareUpdate ScheduleFrequency -int 1 # Check for updates daily.

defaults write com.apple.TextEdit RichText -int 0
defaults write com.apple.TextEdit PlainTextEncoding -int 4
defaults write com.apple.TextEdit PlainTextEncodingForWrite -int 4

#sudo defaults write com.apple.universalaccess closeViewScrollWheelToggle -bool true
#sudo defaults write com.apple.universalaccess closeViewScrollWheelModifiersInt -int 1835008

defaults write NSGlobalDomain AppleShowAllExtensions -bool true
defaults write NSGlobalDomain NSAutomaticCapitalizationEnabled -bool true
defaults write NSGlobalDomain NSAutomaticDashSubstitutionEnabled -bool false
defaults write NSGlobalDomain NSAutomaticPeriodSubstitutionEnabled -bool true
defaults write NSGlobalDomain NSAutomaticQuoteSubstitutionEnabled -bool false
defaults write NSGlobalDomain NSDisableAutomaticTermination -bool true
defaults write NSGlobalDomain NSDocumentSaveNewDocumentsToCloud -bool false
defaults write NSGlobalDomain NSNavPanelExpandedStateForSaveMode -bool true
defaults write NSGlobalDomain NSNavPanelExpandedStateForSaveMode2 -bool true
#defaults write NSGlobalDomain NSTextShowsControlCharacters -bool true
defaults write NSGlobalDomain PMPrintingExpandedStateForPrint -bool true
defaults write NSGlobalDomain PMPrintingExpandedStateForPrint2 -bool true
defaults write NSGlobalDomain WebKitDeveloperExtras -bool true


defaults write com.apple.TimeMachine DoNotOfferNewDisksForBackup -bool true

defaults write com.apple.messageshelper.MessageController SOInputLineSettings -dict-add automaticEmojiSubstitutionEnablediMessage -bool false
defaults write com.apple.messageshelper.MessageController SOInputLineSettings -dict-add automaticQuoteSubstitutionEnabled -bool false


#defaults write com.apple.BluetoothAudioAgent "Apple Bitpool Min (editable)" -int 40 # Increase bluetooth sound quality.
#defaults write NSGlobalDomain AppleKeyboardUIMode -int 3 # Enable full keyboard control.
#defaults write NSGlobalDomain ApplePressAndHoldEnabled -bool false # Enable repeat instead of press-and-hold for letter keys.
#defaults write NSGlobalDomain KeyRepeat -int 0 # Fast keyboard repeat.