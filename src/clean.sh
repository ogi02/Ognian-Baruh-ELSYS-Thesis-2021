#!/bin/bash
if [[ $OSTYPE == "linux-gnueabihf" ]]
then
      	rm -r env
else
        pipenv --rm
fi
