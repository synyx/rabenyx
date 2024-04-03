#!/bin/bash

set -e

export LANG="de_DE.UTF-8"
export TZ="Europe/Berlin"

if [ "$REFERENCE_POLL_ID" == "" ]; then
  echo "No REFERENCE_POLL_ID given --- arborting"
  exit 1
fi

echo "Clones poll with id $REFERENCE_POLL_ID"
for i in 0 1 2 3 4;
do
  POLL_ID=$(./rabenyx.py --clone-poll "$REFERENCE_POLL_ID" True)
  echo "Cloned poll has id $POLL_ID"
  NEXT_WEEK=$(date -d "next-monday +$i days" "+%A, %d.%m.%Y")
  ./rabenyx.py --update-poll-title "$POLL_ID" "Anwesenheit bei synyx am $NEXT_WEEK"
  TIMESTAMP_EXPIRE_DATE=$(date -d "20:00 next-monday +$i days" +%s)
  ./rabenyx.py --clone-options "$REFERENCE_POLL_ID" "$POLL_ID"
  ./rabenyx.py --update-poll-expire "$POLL_ID" "$TIMESTAMP_EXPIRE_DATE"
  ./rabenyx.py --update-poll-access "$POLL_ID" "open"
done
