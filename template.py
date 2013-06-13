# -*- coding: utf-8 -*-

templates = {
    'obj_ruler': '''tmp/%(obj)s: src/%(source)s
\t$(CC) $(CFLAGS) -c src/%(source)s -o tmp/%(obj)s''',
    'main.cc': '''/**
 * Generated with sketch %(version)s
 **/
 #include <Arduino.h>

/**
 * Setup of the firmware
 **/
 void setup() {
 }

/**
 * Schedule events for firmware program
 **/
 void loop() {
    delay(250);
 }''',
    'Makefile': '''##########################################
# Makefile generated with sketch %(version)s
##########################################

# Define toolchain
CC=%(cc)s
LD=%(ld)s
AR=%(ar)s
OBJCOPY=%(objcopy)s
LIB=
INCLUDE=

#Define of MCU
MCU=%(mcu)s
CLOCK=%(clock_hz)sL

# Define compiler flags
CFLAGS=
CCFLAGS=$(CFLAGS)

# Define compiler rulers
OBJ=%(obj_dep)s
AOUT=%(project_name)s-%(mcu)s.aout
HEX=%(project_name)s-%(mcu)s.hex

ALL=$(HEX)

HEX: $(AOUT)
\techo Generate HEX

$(AOUT): $(OBJ)
\t$(CC) $(CFLAGS) $(LIB) $(OBJ) -o $(AOUT)

%(obj_rulers)s

clean:
\trm $(OBJ)
\trm $(AOUT)
\trm $(HEX)
'''
}