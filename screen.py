class Screen:

    def start_screen( display, version ):
        display_name = "Pool " + version

        # clear screen
        display.fill(1)
        display.fill(0)

        display.text(display_name, 0, 0, 1)
        display.text('Hello :)', 0, 20, 1)
        display.text('Start...', 0, 40, 1)

        display.show()

    def clear_screen( display, version ):
        display_name = "Pool " + version

        # clear screen
        display.fill(1)
        display.fill(0)

        display.text(display_name, 0, 0, 1)

        display.show()

    def print_screen( display, pool_temp, ext_temp, relay_status, datetime ):
        display.text('Po:{}C'.format(pool_temp), 0, 10, 1)      #Pool
        display.text('Ex:{}C'.format(ext_temp), 0, 20, 1)       #Exterior
        display.text('Pu:{}'.format(relay_status), 0, 30, 1)    #Pump
        display.text('DT:{}'.format(datetime), 0, 40, 1)        #DateTiem
        display.show()
