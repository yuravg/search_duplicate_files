# for 'bash' completion file

completion_data = """# -*- shell-script -*-

#
# this file was auto-generated from sduplicate Python script
#

_sduplicate() {
    local cur=${COMP_WORDS[COMP_CWORD]}
    COMPREPLY=( $(compgen -W "--no-verbose --move --delete --no-interactive --no-warning
--write-log --path= --no-size --no-name --sum --ignore-mask --show-arguments --version" -- $cur) )
}
complete -F _sduplicate sduplicate
complete -F _sduplicate sduplicate.exe
"""

completion_fname = 'sduplicate'
