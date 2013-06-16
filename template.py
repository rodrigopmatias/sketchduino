# -*- coding: utf-8 -*-

templates = {
    'static_link': '''
\t$(AR) rcs %(lib)s %(obj)s''',
    'obj_ruler': '''%(obj)s: %(source)s
\t@$(CC) $(CFLAGS) $(INCLUDE) -c %(source)s -o %(obj)s
\t@echo "Compile \033[36m\033[4m%(source)s\033[0m to \033[36m\033[4m%(obj)s\033[0m"''',
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

# Defines of Arduino
ARDUINO_HOME=%(sdk_home)s
ARDUINO_CORE=$(ARDUINO_HOME)/hardware/arduino/cores
ARDUINO_VARIANT=$(ARDUINO_HOME)/hardware/arduino/variants/standard

# Define toolchain
CC=%(cc)s
LD=%(ld)s
AR=%(ar)s
OBJCOPY=%(objcopy)s
LIB=
INCLUDE=-I$(ARDUINO_CORE)/arduino -I$(ARDUINO_VARIANT) -I$(ARDUINO_CORE)

#Define of MCU
MCU=%(mcu)s
CLOCK=%(clock_hz)sL
ARDUINO=101

# Define compiler flags
CFLAGS=-Os -Os -Wall -fno-exceptions -ffunction-sections -fdata-sections -mmcu=$(MCU) \\
          -DF_CPU=$(CLOCK) -MMD -DARDUINO=$(ARDUINO) \\
          -fpermissive -lm -Wl,-u,vfprintf -lprintf_flt
CCFLAGS=$(CFLAGS)

# Define compiler rulers
OBJ=%(obj_dep)s
CORE_OBJ=%(core_obj_dep)s
AOUT=binary/%(project_name)s-%(mcu)s.elf
HEX=binary/%(project_name)s-%(mcu)s.hex
EPP=binary/%(project_name)s-%(mcu)s.epp
CORE_LIB=binary/core.a
LD_FLAGS=-Os -Wl,--gc-sections -mmcu=atmega8 -lm

all: $(HEX) $(EPP)

$(HEX): $(EPP)
\t@echo Generate HEX
\t$(OBJCOPY) -O ihex -R .eeprom $(AOUT) $(HEX)

$(EPP): $(AOUT)
\t$(OBJCOPY) -O ihex -j .eeprom --set-section-flags=.eeprom=alloc,load --no-change-warnings --change-section-lma .eeprom=0 $(AOUT) $(EPP)

$(AOUT): $(OBJ) $(CORE_LIB)
\t$(CC) $(LD_FLAGS) $(LIB) $(OBJ) $(CORE_LIB) -o $(AOUT)

$(CORE_LIB): $(CORE_OBJ)%(core_ruler)s

%(obj_rulers)s

%(core_obj_rulers)s

clean:
\trm -f tmp/*
\trm -f binary/*
'''
}