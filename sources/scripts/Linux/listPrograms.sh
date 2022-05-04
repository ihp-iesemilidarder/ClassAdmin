#!/bin/bash
programs=`ls /usr/share/applications/*.desktop`
listPrograms=(${programs// /})
echo ${listPrograms[1]}
