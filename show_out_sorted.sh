#!/bin/bash -ex
cat out | sort -k1,1 | less -S
