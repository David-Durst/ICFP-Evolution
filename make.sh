#!/bin/sh
rm simulator/*.cmi
rm simulator/*.cmx
rm optimizer/*.cmi
rm optimizer/*.cmx
make -C simulator -f Makefile.opt
make -C Bertl/SDL
make -C optimizer
