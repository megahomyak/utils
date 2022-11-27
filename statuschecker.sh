#!/bin/bash

for d in $(find * -maxdepth 0 -type d)
do (
    cd $d
    unpushed="$(git log --branches --not --remotes --no-walk --decorate --oneline)"
    if [[ $? != 0 ]]; then
        echo !!! AN ERROR OCCURED WHEN TALKING TO GIT IN $d ^^^
    else
        if [[ $unpushed != "" ]]; then
            echo !!! THERE ARE UNPUSHED BRANCHES IN $d:
            echo $unpushed
        fi
        uncommitted="$(git status --porcelain)"
        if [[ $uncommitted != "" ]]; then
            echo !!! THERE IS SOME UNCOMMITTED STUFF IN $d
        fi
    fi
) done
