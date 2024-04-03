#!/bin/bash

set -e

export LANG="de_DE.UTF-8"
export TZ="Europe/Berlin"

echo "Archives polls"
for i in 0 1 2 3 4;
do
  LAST_WEEK=$(date -d "09:00 last-monday +$i days" "+%A, %d.%m.%Y")
  echo "$LAST_WEEK"
  POLL_ID=$(./rabenyx.py --get-poll-by-title "Anwesenheit bei synyx am $LAST_WEEK")
  if [ "$POLL_ID" != "" ]; then
    ./rabenyx.py --update-poll-deleted "$POLL_ID" "$(date +%s)"
  else
    echo "No Poll found to archive --- skipping"
  fi
done
