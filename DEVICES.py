import bleak
import datetime as dt

import clr
clr.AddReference("System")

from System import Array, Byte
from bleak_winrt.windows.storage.streams import DataReader, IBuffer, UnicodeEncoding
from COMPANY import COMPANY_LOOKUP

class Device:
    """
    My own implementation of a discovered device
    """

    def __init__(self, bleak_attributes):
        self.bleak_attributes = bleak_attributes
        # raw_data: ['adv', 'count', 'index', 'scan']
        # .adv is BluetoothLEAdvertisementReceivedEventArgs objects
        # .count is built-in method of _RawAdvData object
        # .index is built-in method of _RawAdvData object
        # .scan is raw data from scan response (?)

        self.received_event_args = self.bleak_attributes.adv
        # received_event_args: ['advertisement', 'advertisement_type', 'bluetooth_address',
        #                       'bluetooth_address_type', 'is_anonymous, 'is_connectable',
        #                       'is_directed', 'is_scan_response', 'is_scannable',
        #                       'raw_signal_strength_in_d_bm', 'timestamp',
        #                       'transmit_power_level_in_d_bm']
        # For more info, go to BluetoothLEAdvertisementReceivedEventArgs docs

        self.advertisement = self.received_event_args.advertisement
        self.bluetooth_address = self.received_event_args.bluetooth_address
        self.bluetooth_address_type = self.received_event_args.bluetooth_address_type
        self.raw_signal_strength_in_d_bm = self.received_event_args.raw_signal_strength_in_d_bm
        self.transmit_power_level_in_d_bm = self.received_event_args.transmit_power_level_in_d_bm
        self.timestamp = self.received_event_args.timestamp

        
    def display(self):
        parsed_manufacturer_data = self.get_manufacturer_data()
        parsed_data = self.get_data_sections()
        parsed_mac_address = self.get_mac_address()
        display_text = "{0}: {1}\n{2}\n{3}"
        print(display_text.format(
            parsed_mac_address,
            self.raw_signal_strength_in_d_bm,
            Device._company_from_decimal_id(parsed_manufacturer_data[0]),
            parsed_data)
        )
        print("-"*20)

    def get_manufacturer_data(self):
        """
        Parameters:
        type(self) = Device: self

        Return:
        list with [0] as company_id_decimal, [1] with data
        """
        # advertisement.manufacturer_data -> IVector
        # IVector is made of BluetoothLEManufacturerData object(s)
        # Don't know why it is an IVector, as almost all of these only have 1 object
        # the 1 object being a BLEManData object
        # BluetoothLEManufacturerData.company_id = decimal ID of device company_id
        # BluetoothLEManufacturerData.data = IBuffer object
        man_data = [-1, [None]]
        for man_data_obj in self.advertisement.manufacturer_data:
            man_data[0] = man_data_obj.company_id
            data = Device._read_from_buffer(man_data_obj.data)
            # HOW TO READ DATA
            # data[0] = flag
            # data[1] = length of rest of packet
            # data[2:] = rest of packet
            man_data[1] = data
        return man_data

    def get_data_sections(self):
        """
        Parameters:
        type(self) = Device: self

        Return:
        cleaned data
        """
        # self.advertisement has attribute "data_sections", type is
        # BluetoothLEAdvertisementDataSection -> IVector

        # data (in data_section.data for data_section in data_sections) is
        # BluetoothLEAdvertisementDataSection.data -> IBuffer

        # How to read from IBuffer? go to: https://docs.microsoft.com/en-us/uwp/api/windows.storage.streams.ibuffer?view=winrt-22000

        try:
            print(self.advertisement.flags)
        except:
            pass

        data = []
        for data_section in self.advertisement.data_sections:
            data.append(Device._read_from_buffer(data_section.data))

        return data

    def get_mac_address(self):
        """
        Parameters:
        type(self) = Device: self

        Return:
        bd address formatted as MAC address
        """
        # NOTE: in to_bytes, values over \xFF are represnted as chars according to ascii values
        byte_bd_address = self.bluetooth_address.to_bytes(6, byteorder='big')
        hex_bd_address = ["{:02X}".format(num) for num in byte_bd_address]
        return ":".join(hex_bd_address)

    @staticmethod
    def _read_from_buffer(buff: IBuffer):
        """
        Parameters:
        type(buff) = IBuffer: buffer to read bytes from

        Return:
        array of bytes read from buff
        """
        # Create DataReader object which reads from IBuffer
        dataReader = DataReader.from_buffer(buff)
        storage = []
        while dataReader.unconsumed_buffer_length > 0:
            storage.append(dataReader.read_byte())
        return storage

    @staticmethod
    def _company_from_decimal_id(company_decimal_id):
        try:
            return COMPANY_LOOKUP[str(company_decimal_id)]
        except:
            return "-COMPANY NOT FOUND-"

    @staticmethod
    def _ints_to_chars(int_arr):
        try:
            return "".join([chr(i) for i in int_arr])
        except:
            return [Device._ints_to_chars(lst) for lst in int_arr]
