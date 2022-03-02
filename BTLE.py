import bleak
import asyncio
import inspect

from DEVICES import Device



async def get_devices():
    # Create scanner
    scanner = bleak.BleakScanner()

    # Scan for 5 seconds
    # This fills the scanner._discovered_devices attribute
    await scanner.start()
    await asyncio.sleep(5)
    await scanner.stop()

    devices = []
    
    # Create Device objects from scanner._discovered_devices
    # Note: scanner._discovered_devices = Dict[int, _RawAdvData] : (bt_address, raw_data)
    for bt_addr in scanner._discovered_devices:
        devices.append(Device(scanner._discovered_devices[bt_addr]))
            
    for device in devices:
        if Device._company_from_decimal_id(device.get_manufacturer_data()[0]) == "Microsoft":
            device.display()

    print("----------------------------------")




async def main():
    await get_devices()

loop = asyncio.get_event_loop()

while True:
    loop.run_until_complete(main())
