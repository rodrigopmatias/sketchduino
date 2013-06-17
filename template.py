# -*- coding: utf-8 -*-

templates = {
    'static_link': '''
\t@$(AR) rcs %(lib)s %(obj)s
\t@echo " [\033[33m\033[1mAR\033[0m] \033[37m\033[1m%(obj)s\033[0m to \033[37m\033[1m%(lib)s\033[0m"''',
    'obj_ruler': '''%(obj)s: %(source)s
\t@$(CC) $(CFLAGS) $(INCLUDE) -c %(source)s -o %(obj)s 2>1
\t@echo " [\033[33m\033[1mCC\033[0m] \033[37m\033[1m%(source)s\033[0m"''',
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
\t@echo " [\033[33m\033[1mOBJCOPY\033[0m] \033[37m\033[1mFirmware\033[0m"
\t@$(OBJCOPY) -O ihex -R .eeprom $(AOUT) $(HEX)

$(EPP): $(AOUT)
\t@echo " [\033[33m\033[1mOBJCOPY\033[0m] \033[37m\033[1mMemory of EEPROM\033[0m"
\t@$(OBJCOPY) -O ihex -j .eeprom --set-section-flags=.eeprom=alloc,load --no-change-warnings --change-section-lma .eeprom=0 $(AOUT) $(EPP)

$(AOUT): $(OBJ) $(CORE_LIB)
\t@echo " [\033[33m\033[1mLD\033[0m] \033[37m\033[1m$(AOUT)\033[0m"
\t@$(CC) $(LD_FLAGS) $(LIB) $(OBJ) $(CORE_LIB) -o $(AOUT)

$(CORE_LIB): $(CORE_OBJ)%(core_ruler)s

%(obj_rulers)s

%(core_obj_rulers)s

clean-tmp:
\t@echo " [\033[33m\033[1mRM\033[0m] Clear temporary files"
\t@rm -f tmp/*

clean-bin:
\t@echo " [\033[33m\033[1mRM\033[0m] Clear binary files"
\t@rm -f binary/*

clean:
\t@echo " [\033[33m\033[1mRM\033[0m] Clear temporary files"
\t@rm -f tmp/*
\t@echo " [\033[33m\033[1mRM\033[0m] Clear binary files"
\t@rm -f binary/*
'''
}