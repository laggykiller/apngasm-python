#!/bin/sh

if [[ -z $APNGASM_COMPILE_TARGET ]]; then
    arch=$(uname --machine)
    if [[ $arch == x86_64* ]]; then
        APNGASM_COMPILE_TARGET=x64
    elif [[ $arch == i*86 ]]; then
        APNGASM_COMPILE_TARGET=x86
    elif [[ $arch == aarch64 ]]; then
        APNGASM_COMPILE_TARGET=arm64
    elif [[ $arch == '' ]]; then
        APNGASM_COMPILE_TARGET=x64
    else
        APNGASM_COMPILE_TARGET=$arch
    fi
fi

export APNGASM_COMPILE_TARGET=$APNGASM_COMPILE_TARGET

printf '%s' $APNGASM_COMPILE_TARGET