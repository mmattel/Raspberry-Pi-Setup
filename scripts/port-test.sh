#! /bin/bash

# on the command line, check the error code of the last command with echo $?

# check if there are arguments
if [ $# -eq 0 ]; then
  cat << USAGE >&2
Usage:

    $(basename "$0") port [loops]

    port       The port that is being tested
    loops      Optional, number of check loops
               Each number doubles the waiting time in seconds
               Defaults to 5 (=62s), max to 10 (=18.5min)

    Return status is set and can be queried by the caller
    0 ... success
    1 ... port inaccessible
    2 ... parameter missing
    3 ... parameter is not a positive integer number or too high

USAGE
  exit 2
fi

# check if port pattern is a number
if echo "$1" | grep -vqE '^[0-9]+$'; then
    echo "Port is not a valid number"
    exit 3
fi

# check if port in in range
if (( $1 > 65536 )); then
    echo "Port is not in range of 0...65535"
    exit 3
fi

# check if loop is present
if [ $# -eq 2 ]; then
  # check if loop pattern is a number
  if echo "$2" | grep -vqE '^[0-9]+$'; then
      echo "Loops is not a valid number"
      exit 3
  fi
  # check if loop is greater then 10
  if (( $2 > 11 )); then
      echo "Loops is greater than 10"
      exit 3
  fi
fi

# check if the port is available
for EXPONENTIAL_BACKOFF in $(eval echo {1..${2:-5}}); do
    nc -w 1 -z $(hostname) $1
    STATUS=$?
    [ $STATUS -eq 0 ] && break;
    DELAY=$((2**$EXPONENTIAL_BACKOFF))
    SUM=$((SUM + DELAY))
    echo "Port $1 not yet available, sleeping for $DELAY seconds"
    sleep $DELAY
done

if [ -z $STATUS ]; then
    echo "Port $1 was not reachable after $SUM seconds"
fi

exit $STATUS

