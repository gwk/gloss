#!/usr/bin/env bash
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# git cherry shows all commits in $2 but not in $1
# commits preceded by a '-' have equivalent commits in $1 (rebased or cherry-picked)
# commits preceded by a '+' do not have detectable equivalents.

[[ "$3" == "+" ]] || [[ "$3" == "-" ]] || { echo "error: arg 3 must be + or - sign" 1>&2; exit 1; }

# this script selects either the plus or minus commits by grepping for the sign given by $3
# cut splits on space delimeter, then returns just the commit (field 2).
# this can be piped to xarg | git log -1 to view)
git cherry "$1" "$2" | grep "$3" | cut -d ' ' -f 2
