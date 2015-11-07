#!/bin/sh
#
# define transport in master.cf:

# flier unix  -       n       n       -       -       pipe
#  flags=FDRq user=vagrant 
#   argv=/path/to/current/dir/drop.bash 
#     flier $sender $recipient $original_recipient

MAILS=$(dirname $0)/mails
if [ ! -d $MAILS ]; then mkdir -p $MAILS ; fi
FILE=$MAILS/$(date +'%m%d%H%M%S'.$$)
cat > $FILE.eml
