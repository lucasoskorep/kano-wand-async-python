import asyncio
import numpy as np

from .constants import *
from bleak import BleakClient


class Wand(object):
    """
    A wand class to interact with the Kano wand
    """

    def __init__(self, device_addr, name, bot_loop, debug=True):
        """
        Create a new wand

        Arguments:
            device {bluepy.ScanEntry} -- Device information

        Keyword Arguments:
            debug {bool} -- Print debug messages (default: {False})
        """
        self.debug = debug
        self._dev = BleakClient(device_addr)
        self.name = name
        self.bot_loop = bot_loop

        if debug:
            print("Wand: {}\n\rWand Mac: {}".format(self.name, self._dev.address))

        # Notification stuff
        self.connected = False
        self._position_callbacks = {}
        self._position_subscribed = False
        self._button_callbacks = {}
        self._button_subscribed = False
        self._temperature_callbacks = {}
        self._temperature_subscribed = False
        self._battery_callbacks = {}
        self._battery_subscribed = False
        self._notification_thread = None
        self._position_notification_handle = 41
        self._button_notification_handle = 33
        self._temp_notification_handle = 56
        self._battery_notification_handle = 23

    async def connect(self):
        if self.debug:
            print("Connecting to {}...".format(self.name))

        connected = await self._dev.connect()
        if not connected:
            raise Exception("ERROR NOT CONNECTED TO THE DEVICE")

        self.connected = True
        await self.post_connect()

        if self.debug:
            print("Connected to {}".format(self.name))

    async def post_connect(self):
        """
        Do anything necessary after connecting
        """
        pass

    async def disconnect(self):

        await self._dev.disconnect()
        self.connected = False
        await self.post_disconnect()

        if self.debug:
            print("Disconnected from {}".format(self.name))

    async def post_disconnect(self):
        """
        Do anything necessary after disconnecting
        """
        pass

    async def get_organization(self):
        """
        Get organization of device
        Returns {str} -- Organization name
        """
        result = await self._dev.read_gatt_char(INFO.ORGANIZATION_CHAR.value)
        return result.decode("utf-8")

    async def get_software_version(self):
        """
        Get software version
        Returns {str} -- Version number
        """
        result = await self._dev.read_gatt_char(INFO.SOFTWARE_CHAR.value)
        return result.decode("utf-8")

    async def get_hardware_version(self):

        """
        Get hardware version
        Returns {str} -- Hardware version
        """
        result = await self._dev.read_gatt_char(INFO.HARDWARE_CHAR.value)
        return result.decode("utf-8")

    async def get_battery(self):
        """
        Get battery level (currently only returns 0)
        Returns {str} -- Battery level
        """
        result = await self._dev.read_gatt_char(IO.BATTERY_CHAR.value)
        print(f"battery is {result}")
        print(f"battery is {result.decode('utf-8')}")
        return result.decode("utf-8")

    async def get_button(self):
        """
        Get current button status
        Returns {bool} -- Button pressed status
        """
        data = await self._dev.read_gatt_char(IO.USER_BUTTON_CHAR.value)
        return data[0] == 1

    async def get_temperature(self):
        """
        Get temperature

        Returns {str} -- Battery level
        """
        # with self._lock:
        # if not hasattr(self, "_temperature_handle"):
        #     handle = self._sensor_service.getCharacteristics(SENSOR.TEMP_CHAR.value)[0]
        #     self._temperature_handle = handle.getHandle()
        result = await self._dev.read_gatt_char(SENSOR.TEMP_CHAR.value)
        print(f"temp is {result}")
        return result

    async def keep_alive(self):
        """
        Keep the wand's connection active

        Returns {bytes} -- Status
        """
        if self.debug:
            print("Keeping wand alive.")
        return await self._dev.write_gatt_char(IO.KEEP_ALIVE_CHAR.value, bytearray([1]), response=True)

    async def vibrate(self, pattern=PATTERN.REGULAR):
        """
        Vibrate wand with pattern

        Keyword Arguments:
            pattern {kano_wand.PATTERN} -- Vibration pattern (default: {PATTERN.REGULAR})

        Returns {bytes} -- Status
        """
        if isinstance(pattern, PATTERN):
            message = [pattern.value]
        else:
            message = [pattern]
        if self.debug:
            print("Setting Vibration to {}".format(message))
        return await self._dev.write_gatt_char(IO.VIBRATOR_CHAR.value, bytearray(message), response=True)

    async def set_led(self, color="0x2185d0", on=True):
        """
        Set the LED's color

        Keyword Arguments:
            color {str} -- Color hex code (default: {"0x2185d0"})
            on {bool} -- Whether light is on or off (default: {True})

        Returns {bytes} -- Status
        """
        message = []
        if on:
            message.append(1)
        else:
            message.append(0)

        color = int(color.replace("#", ""), 16)
        r = (color >> 16) & 255
        g = (color >> 8) & 255
        b = color & 255
        rgb = (((r & 248) << 8) + ((g & 252) << 3) + ((b & 248) >> 3))
        message.append(rgb >> 8)
        message.append(rgb & 0xff)

        if self.debug:
            print("Setting LED to {}".format(message))
            return await self._dev.write_gatt_char(IO.LED_CHAR.value, bytearray(message), response=True)

    async def subscribe_position(self):
        """
        Subscribe to position notifications and start thread if necessary
        """
        if self.debug:
            print("Subscribing to position notification")
        self._position_subscribed = True
        await self._dev.start_notify(SENSOR.QUATERNIONS_CHAR.value, self.handle_notification)

    async def unsubscribe_position(self, continue_notifications=False):
        """
        Unsubscribe to position notifications

        Keyword Arguments:
            continue_notifications {bool} -- Keep notification thread running (default: {False})
        """
        if self.debug:
            print("Unsubscribing from position notification")

        self._position_subscribed = continue_notifications
        await self._dev.stop_notify(SENSOR.QUATERNIONS_CHAR.value)

    async def subscribe_button(self):
        """
        Subscribe to button notifications and start thread if necessary
        """
        if self.debug:
            print("Subscribing to button notification")

        self._button_subscribed = True
        await self._dev.start_notify(IO.USER_BUTTON_CHAR.value, self.handle_notification)

    async def unsubscribe_button(self, continue_notifications=False):
        """
        Unsubscribe to button notifications

        Keyword Arguments:
            continue_notifications {bool} -- Keep notification thread running (default: {False})
        """
        if self.debug:
            print("Unsubscribing from button notification")
        self._button_subscribed = continue_notifications
        await self._dev.stop_notify(IO.USER_BUTTON_CHAR.value)

    async def subscribe_temperature(self):
        """
        Subscribe to temperature notifications and start thread if necessary
        """
        if self.debug:
            print("Subscribing to temperature notification")

        self._temperature_subscribed = True
        await self._dev.start_notify(SENSOR.TEMP_CHAR.value, self.handle_notification)

    async def unsubscribe_temperature(self, continue_notifications=False):
        """
        Unsubscribe to temperature notifications

        Keyword Arguments:
            continue_notifications {bool} -- Keep notification thread running (default: {False})
        """
        if self.debug:
            print("Unsubscribing from temperature notification")

        self._temperature_subscribed = continue_notifications
        await self._dev.stop_notify(SENSOR.TEMP_CHAR.value)

    #
    #
    async def subscribe_battery(self):
        """
        Subscribe to battery notifications and start thread if necessary
        """
        if self.debug:
            print("Subscribing to battery notification")

        self._battery_subscribed = True
        await self._dev.start_notify(IO.BATTERY_CHAR.value, self.handle_notification)

    async def unsubscribe_battery(self, continue_notifications=False):
        """
        Unsubscribe to battery notifications

        Keyword Arguments:
            continue_notifications {bool} -- Keep notification thread running (default: {False})
        """
        if self.debug:
            print("Unsubscribing from battery notification")

        self._battery_subscribed = continue_notifications
        await self._dev.stop_notify(IO.BATTERY_CHAR.value)

    async def _on_position(self, data):
        """
        Private function for position notification

        Arguments:
            data {bytes} -- Data from device
        """
        # I got part of this from Kano's node module and modified it
        y = np.int16(np.uint16(int.from_bytes(data[0:2], byteorder='little')))
        x = -1 * np.int16(np.uint16(int.from_bytes(data[2:4], byteorder='little')))
        w = -1 * np.int16(np.uint16(int.from_bytes(data[4:6], byteorder='little')))
        z = np.int16(np.uint16(int.from_bytes(data[6:8], byteorder='little')))

        if self.debug:
            pitch = "Pitch: {}".format(z).ljust(16)
            roll = "Roll: {}".format(w).ljust(16)
            # print("{}{}(x, y): ({}, {})".format(pitch, roll, x, y))

        await self.on_position(x, y, z, w)
        for callback in self._position_callbacks.values():
            await callback(x, y, z, w)

    async def on_position(self, x, y, pitch, roll):
        """
        Function called on position notification

        Arguments:
            x {int} -- X position of wand (Between -1000 and 1000)
            y {int} -- Y position of wand (Between -1000 and 1000)
            pitch {int} -- Pitch of wand (Between -1000 and 1000)
            roll {int} -- Roll of wand (Between -1000 and 1000)
        """
        pass

    async def reset_position(self):
        """
        Reset the quaternains of the wand
        """
        if self.debug:
            print("resetting the quarternion position")
        return await self._dev.write_gatt_char(SENSOR.QUATERNIONS_RESET_CHAR.value, bytearray([1]), response=True)

    async def _on_button(self, data):
        """
        Private function for button notification

        Arguments:
            data {bytes} -- Data from device
        """
        val = data[0] == 1

        if self.debug:
            print("Button: {}".format(val))

        await self.on_button(val)
        for callback in self._button_callbacks.values():
            await callback(val)

    async def on_button(self, value):
        """
        Function called on button notification

        Arguments:
            pressed {bool} -- If button is pressed
        """
        pass

    async def _on_temperature(self, data):
        """
        Private function for temperature notification

        Arguments:
            data {bytes} -- Data from device
        """
        val = np.int16(np.uint16(int.from_bytes(data[0:2], byteorder='little')))

        if self.debug:
            print("Temperature: {}".format(val))

        await self.on_temperature(val)
        for callback in self._temperature_callbacks.values():
            await callback(val)

    async def on_temperature(self, value):
        """
        Function called on temperature notification

        Arguments:
            value {int} -- Temperature of the wand
        """
        pass

    async def _on_battery(self, data):
        """
        Private function for battery notification

        Arguments:
            data {bytes} -- Data from device
        """
        val = data[0]

        if self.debug:
            print("Battery: {}".format(val))
        print("subscribing to the")

        await self.on_battery(val)
        for callback in self._battery_callbacks.values():
            await callback(val)

    async def on_battery(self, value):
        """
        Function called on battery notification

        Arguments:
            value {int} -- Battery level of the wand
        """
        pass

    def handle_notification(self, sender, data):
        """
        Handle notifications subscribed to

        Arguments:
            cHandle {int} -- Handle of notification
            data {bytes} -- Data from device
        """
        future = None
        if sender == SENSOR.QUATERNIONS_CHAR.value:
            future = asyncio.run_coroutine_threadsafe(self._on_position(data), self.bot_loop)
        elif sender == IO.USER_BUTTON_CHAR.value:
            future = asyncio.run_coroutine_threadsafe(self._on_button(data), self.bot_loop)
        elif sender == SENSOR.TEMP_CHAR.value:
            future = asyncio.run_coroutine_threadsafe(self._on_temperature(data), self.bot_loop)
        elif sender == IO.BATTERY_CHAR.value:
            future = asyncio.run_coroutine_threadsafe(self._on_battery(data), self.bot_loop)
        if future != None:
            future.result()
