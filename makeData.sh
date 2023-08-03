#!/bin/sh

DIRECTORY=$(pwd)
DATABASE_FILE="db.sqlite3"
DATA_FOLDER_NAME="data"
DATA_FILE_NAME=`shasum "$DIRECTORY/$DATABASE_FILE" | awk '{ print $1 }'`
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

python3 manage.py dumpdata --indent 2 collect > $NEW_DATA_FILE_NAME 2> /dev/null

if [ $? == 0 ]; then
    echo "=== Successfully converted database file at:\n$NEW_DATA_FILE_NAME."
else
    echo "*** Errors occurred. Ensure you are in the correct Python3 environment."
    exit 1
fi

exit 0

