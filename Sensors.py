import uadi2c
import mcp3424

addr1 = 0x68

adr01 = uadi2c.uadi2c(addr1, debug=False)
config01 =  mcp3424.START | mcp3424.CHAN0 | mcp3424.CONTINUOUS | mcp3424.R12BIT | mcp3424.GAIN1
config02 =  mcp3424.START | mcp3424.CHAN1 | mcp3424.CONTINUOUS | mcp3424.R12BIT | mcp3424.GAIN1
config03 =  mcp3424.START | mcp3424.CHAN2 | mcp3424.CONTINUOUS | mcp3424.R12BIT | mcp3424.GAIN1
config04 =  mcp3424.START | mcp3424.CHAN3 | mcp3424.CONTINUOUS | mcp3424.R12BIT | mcp3424.GAIN1

def read(adr, config):
    s2 = 128
    try:
        while (s2 & mcp3424.STATUS): # bit 7 of s2 is 1 until conversion complete.
            reading = adr.readList(config, 4) # role of config unclear!
            (hi,lo,s1,s2) = reading
            d = (hi << 8) | lo 
        # hi byte is sign extended so 16-bit 2's complement works for all
        # resolutions
        if (d & 0x8000):
            d = -(0x10000 -d)
    # N. B. This depends on the resolution!
        v = d*2.6/2048 # we only get 11 bit, unity gain, LSB = 5/2**11 volts
    except:
        return 0
    return round(v, 2)

def readSensors():
    return [read(adr01, config01), read(adr01, config02), read(adr01, config03), read(adr01, config04)]
