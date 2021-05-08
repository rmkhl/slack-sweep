# GNUmakefile for managing the python project

TOPDIR := $(CURDIR)
PYTHON := python3 -B
MODULE := slacksweep

.DEFAULT_GOAL := help

include mk/generic.mk

ifneq ($(wildcard mk/local.mk), )
	include mk/local.mk
endif

include mk/tools.mk

_MAKE-COMMANDS = $(sort $(patsubst %_HELP, %, $(filter %_HELP, $(.VARIABLES))))
