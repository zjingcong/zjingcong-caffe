#!/bin/bash

EXPECTED_ARGS=2
E_BADARGS=65

NAME=${1%.*}
FRAMES=$2
TMPDIR=$3

if [ $# -lt $EXPECTED_ARGS ]
then
  echo "Usage: `basename $0` video frames/sec [size=256]"
  exit $E_BADARGS
fi

mkdir -m 775 $3
BNAME=`basename $NAME`
mkdir -m 755 $3/$BNAME
ffmpeg -i $1 -r $FRAMES $3/$BNAME/$BNAME.%4d.jpg > /dev/null 2>&1
