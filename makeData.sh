#!/bin/sh
DIRECTORY=$(pwd)
DATABASE_FILE="db.sqlite3"
DATA_FOLDER_NAME="data"
if ! command -v sha1sum &> /dev/null; then
    DATA_FILE_NAME=`shasum "$DIRECTORY/$DATABASE_FILE" | awk '{ print $1 }'`
else
    DATA_FILE_NAME=`sha1sum "$DIRECTORY/$DATABASE_FILE" | awk '{ print $1 }'`
fi
NEW_DATA_FILE_NAME="$DIRECTORY/$DATA_FOLDER_NAME/$DATA_FILE_NAME.json"

if test -f "$DATABASE_FILE"; then
    echo "=== $DATABASE_FILE exists."
else
    echo "=== db.sqlite3 does not exist. Invalid directory."
    exit 1
fi

if [ ! -d "./$DATA_FOLDER_NAME" ]; then
    mkdir $DATA_FOLDER_NAME && echo "=== Making directory 'data' under $DIRECTORY"
else 
    echo "=== Directory 'data' exists."
fi

echo "$NEW_DATA_FILE_NAME"

exit 0

