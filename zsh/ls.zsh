# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# ls coloring, unified across macOS (BSD ls) and Linux (GNU ls).
#
# The two implementations read different, incompatible variables:
# * BSD ls (macOS) reads LSCOLORS: 11 (foreground, background) letter-pairs in a fixed category order.
# * GNU ls (Linux) reads LS_COLORS: `keyword=SGR` entries, colon-separated.
# We define the palette once, then derive both variables from it, so both platforms share one source of truth.
# Both variables are exported unconditionally; each platform's ls ignores the one it does not understand.
#
# Enabling color is separate from the palette: BSD ls needs CLICOLOR=1 (set in rc.zsh);
# GNU ls needs `--color=auto`. These variables only define the colors used once color is enabled.
#
# The palette is written in the same color letters as the TXT_* variables in env.zsh, rather than either the
# BSD ls letters or the ANSI SGR numbers. Only plain (non-bold) colors are supported; x is the terminal default.
#   K black   R red   G green   Y yellow   B blue   M magenta   C cyan   W white   x default
# Each category is a (foreground, background) pair. The values below reproduce the BSD ls defaults.

() {
  emulate -L zsh

  local dir=Bx     # Directory: blue.
  local sym=Mx     # Symlink: magenta.
  local sock=Gx    # Socket: green.
  local pipe=Yx    # Pipe/FIFO: yellow.
  local exec=Rx    # Executable: red.
  local block=BC   # Block special: blue on cyan.
  local char=BY    # Character special: blue on yellow.
  local suid=KR    # Setuid: black on red.
  local sgid=KC    # Setgid: black on cyan.
  local sticky=KG  # Other-writable dir with sticky bit: black on green.
  local owr=KY     # Other-writable dir without sticky bit: black on yellow.

  # Our color letters map onto the ANSI color indices 0-7. BSD ls encodes the same indices as letters a-h;
  # GNU ls encodes them as SGR codes (foreground 3N, background 4N).
  local -A ansi=( K 0 R 1 G 2 Y 3 B 4 M 5 C 6 W 7 )
  local bsd_letters=abcdefgh

  # LSCOLORS: translate each pair to BSD letters and concatenate, in category order.
  local -a order=( $dir $sym $sock $pipe $exec $block $char $suid $sgid $sticky $owr )
  local pair fc bc bsd=""
  for pair in $order; do
    fc=${pair[1]}; bc=${pair[2]}
    if [[ $fc == x ]]; then bsd+=x; else bsd+=${bsd_letters[${ansi[$fc]}+1]}; fi
    if [[ $bc == x ]]; then bsd+=x; else bsd+=${bsd_letters[${ansi[$bc]}+1]}; fi
  done
  export LSCOLORS=$bsd

  # LS_COLORS: GNU keyword -> category pair, each translated to an SGR value.
  # `st` (sticky, not other-writable) has no distinct BSD category; approximate with sticky.
  local -A gnu_from=(
    di $dir    ln $sym    so $sock   pi $pipe   ex $exec
    bd $block  cd $char   su $suid   sg $sgid   tw $sticky  ow $owr  st $sticky
  )
  local -a entries=(rs=0)
  local key sgr
  for key pair in ${(kv)gnu_from}; do
    fc=${pair[1]}; bc=${pair[2]}; sgr=""
    [[ $fc != x ]] && sgr="3${ansi[$fc]}"
    if [[ $bc != x ]]; then
      [[ -n $sgr ]] && sgr+=";"
      sgr+="4${ansi[$bc]}"
    fi
    [[ -n $sgr ]] || sgr=0
    entries+="$key=$sgr"
  done
  export LS_COLORS="${(j.:.)entries}"
}
