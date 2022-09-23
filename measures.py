from machine import Pin
import onewire, ds18x20
import utime as time

class Measures:
    def init(pin_measures):
        ow = onewire.OneWire(Pin(pin_measures, Pin.IN, Pin.PULL_UP))
        ds = ds18x20.DS18X20(ow)

        return ds

    def get_data(ds):
        try:
            roms = ds.scan()
            ds.convert_temp()
            time.sleep_ms(750)

            pool = 'NaN'
            ext = 'NaN'
            count = 0
            for rom in roms:
                if count == 0:
                    pool = ds.read_temp(rom)
                else:
                    ext = ds.read_temp(rom)

                count = count + 1

            return (pool, ext)
        except:
            return False

