#!/bin/sh
############# Defining && Checking ###############
PATH=${ROOT_DIR}
MAIN_EVENT="ttct"
if [ -z "$PATH" ]
then
    echo "\$PATH is empty , initializing env .."
    if [ -f ../.env ]; then
        CURRENT=$(/bin/pwd)
        PARENT="$(/bin/dirname "${CURRENT}")"
        PROFILE="${PARENT}/.env"
        # shellcheck disable=SC1090
        . "${PROFILE}"
    fi
    sleep 1
fi
CURRENT=$(/bin/pwd)
PROFILE="$(/bin/dirname "${CURRENT}")/.env"
# shellcheck disable=SC1090
. "${PROFILE}"
echo $PROFILE
# Init logging
LOG_PATH="${LOG_PATH_TTC}ttct"$(/bin/date +"%Y%m%d".log)
# shellcheck disable=SC1073
if [ ! -f "${LOG_PATH}" ]; then
    echo "$LOG_PATH does not exist. Creating $LOG_PATH .."
    /bin/touch "${LOG_PATH}"
fi
### Test log path
if [ -w "${LOG_PATH}" ]; then
   echo "Write permission is granted on $LOG_PATH"
else
   echo "Write permission is NOT granted on $LOG_PATH"
   exit 1
fi
############ Run script ############
# shellcheck disable=SC2164
cd "${PATH}"
# shellcheck disable=SC1090
. "${VIRTUAL_ENV}"
## Cat
flask import cat "${MAIN_EVENT}"  >> "${LOG_PATH}" &
flask import term-relate "${MAIN_EVENT}" "${SCRAP_LIMIT}" "${SCRAP_RANGE_BY_DAY}" 0  >> "${LOG_PATH}" &
## Tag
flask import tag "${MAIN_EVENT}" "${SCRAP_LIMIT}" "${SCRAP_RANGE_BY_DAY}" 0 >> "${LOG_PATH}" &
flask import tag-relate "${MAIN_EVENT}" "${SCRAP_LIMIT}" "${SCRAP_RANGE_BY_DAY}" 0 >> "${LOG_PATH}" &
## Topic
flask import topic "${MAIN_EVENT}" >> "${LOG_PATH}" &
flask import topic-relate "${MAIN_EVENT}" "${SCRAP_LIMIT}" "${SCRAP_RANGE_BY_DAY}" 0 >> "${LOG_PATH}" &
## Thread
flask import thread "${MAIN_EVENT}" >> "${LOG_PATH}" &
flask import thread-relate "${MAIN_EVENT}" "${SCRAP_LIMIT}" "${SCRAP_RANGE_BY_DAY}" 0 >> "${LOG_PATH}" &
## Resource
flask import resources "${MAIN_EVENT}" "${SCRAP_LIMIT}" "${SCRAP_RANGE_BY_DAY}" 0 >> "${LOG_PATH}" &
flask import resource-relate "${MAIN_EVENT}" "${SCRAP_LIMIT}" "${SCRAP_RANGE_BY_DAY}" 0 >> "${LOG_PATH}" &
## Author
flask import author "${MAIN_EVENT}" "${SCRAP_LIMIT}" "${SCRAP_RANGE_BY_DAY}" 0 >> "${LOG_PATH}" &
flask import author-relate "${MAIN_EVENT}" "${SCRAP_LIMIT}" "${SCRAP_RANGE_BY_DAY}" 0 >> "${LOG_PATH}" &
## Object
flask import object "${MAIN_EVENT}" "${SCRAP_LIMIT}" "${SCRAP_RANGE_BY_DAY}" 0 >> "${LOG_PATH}" &
flask import object-relate "${MAIN_EVENT}" "${SCRAP_LIMIT}" "${SCRAP_RANGE_BY_DAY}" 0 >> "${LOG_PATH}" &
## Done task
deactivate
echo "Completed task TTCT"
