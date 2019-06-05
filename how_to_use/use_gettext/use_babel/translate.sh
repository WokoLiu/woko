#!/bin/bash

if [ $1 == "init" ]
then
    if [ -z "$2" ]; then echo "Language must be specified" && exit; fi
    pybabel extract -F babel.cfg -o messages.pot .
    pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .
    pybabel init -i messages.pot -d translations -l $2
elif [ $1 == "update" ]
then
    pybabel extract -F babel.cfg -o messages.pot .
    pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .
    pybabel update -i messages.pot -d translations
elif [ $1 == "build" ]
then
    pybabel compile -d translations
else
    echo "unknown command: \""$1"\""
fi
