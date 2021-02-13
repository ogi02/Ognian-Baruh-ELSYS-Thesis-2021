UNAME_S := $(shell uname -s)

ifeq ($(UNAME_S),Linux)
	UNAME_M := $(shell uname -m)
	ifneq ($(filter arm%,$(UNAME_M)))
		OS := Raspbian
	endif
else
	OS := Other
endif