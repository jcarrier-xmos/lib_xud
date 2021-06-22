# Copyright 2016-2021 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.
from usb_packet import CreateSofToken
from usb_session import UsbSession
from usb_transaction import UsbTransaction
from usb_signalling import UsbDeviceAttach

import pytest
from conftest import PARAMS, test_RunUsbSession


@pytest.fixture
def test_session(ep, address, bus_speed):

    ep = 1
    address = 1
    start_length = 10
    end_length = 12
    pktLength = 10
    frameNumber = 52  # Note, for frame number 52 we expect A5 34 40 on the bus

    session = UsbSession(
        bus_speed=bus_speed,
        run_enumeration=False,
        device_address=address,
        initial_delay=19000,
    )

    session.add_event(UsbDeviceAttach())

    session.add_event(CreateSofToken(frameNumber, interEventDelay=100))

    session.add_event(
        UsbTransaction(
            session,
            deviceAddress=address,
            endpointNumber=ep,
            endpointType="BULK",
            direction="OUT",
            dataLength=pktLength,
            interEventDelay=0,
        )
    )

    frameNumber = frameNumber + 1
    pktLength = pktLength + 1

    session.add_event(CreateSofToken(frameNumber))
    session.add_event(
        UsbTransaction(
            session,
            deviceAddress=address,
            endpointNumber=ep,
            endpointType="BULK",
            direction="OUT",
            dataLength=pktLength,
            interEventDelay=0,
        )
    )

    return session
