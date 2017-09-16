
#!/usr/bin/python
"""This module defines constants that facilitate the generation of the
control byte for the MCP3424 chip. 

The config byte is (data sheet section 5.2)
    s cc m rr gg
    | |  | |  gain:  00 => 1, 01 => 2, 10 => 4, 11 => 8  
    | |  | |--range: 00 => 12, 01 => 14, 10 => 16, 11 => 18 bit  
    | |  |----mode: 0 => single shot, 1 => continuous
    | |-------channel: 00 => 0, 01 => 1, 10 => 2, 11 => 3  
    |---------init: in single shot mode, 1 initiates a new conversion.

CONSTANTS

    START =       0b10000000 
    STATUS =      0b10000000
    CHAN0 =       0b00000000
    CHAN1 =       0b00100000
    CHAN2 =       0b01000000
    CHAN3 =       0b01100000
    SINGLE_SHOT = 0b00000000
    CONTINUOUS =  0b00010000
    R12BIT =      0b00000000
    R14BIT =      0b00000100
    R16BIT =      0b00001000
    R18BIT =      0b00001100
    GAIN1 =       0b00000000
    GAIN2 =       0b00000001
    GAIN4 =       0b00000010
    GAIN8 =       0b00000011

Combine these with | to generate the configuration byte e.g. a
configuration byte of

mcp3424.START|mcp3424.CHAN0|mcp3424.CONTINUOUS|mcp3424.R12BIT|mcp3424.GAIN1

sets things up for channel 0, continuous mode, 12-bit, unity gain.

"""
START =     0b10000000 
STATUS =      0b10000000
CHAN0 =       0b00000000
CHAN1 =       0b00100000
CHAN2 =       0b01000000
CHAN3 =       0b01100000
SINGLE_SHOT = 0b00000000
CONTINUOUS =  0b00010000
R12BIT =      0b00000000
R14BIT =      0b00000100
R16BIT =      0b00001000
R18BIT =      0b00001100
GAIN1 =       0b00000000
GAIN2 =       0b00000001
GAIN4 =       0b00000010
GAIN8 =       0b00000011

