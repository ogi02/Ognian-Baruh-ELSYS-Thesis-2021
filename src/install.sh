#!/bin/bash
if [[ $OSTYPE == "linux-gnueabihf" ]]
then
	python3 -m pip install --upgrade pip
	python3 -m pip install virtualenv
	python3 -m virtualenv env
	source "./env/bin/activate"
	env/bin/pip install -r requirements.txt
	env/bin/pip install https://github.com/bitsy-ai/tensorflow-arm-bin/releases/download/v2.4.0-rc2/tensorflow-2.4.0rc2-cp37-none-linux_armv7l.whl
else
	python3 -m pip install --upgrade pip
	python3 -m pip install pipenv
	pipenv install -r pc.txt
fi
