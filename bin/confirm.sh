read -n 1 -p "$@? press 'y' to confirm: "
echo
[[ "$REPLY" == "y" ]]
