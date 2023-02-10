from serial import Serial, SerialException, SerialTimeoutException
import time

class SerialCommunication:

    def __init__(self, port, baudrate, timeout=1, debug=True):
        self._serial_object = None
        self._connected = False
        self._reading = False
        self._port = port
        self._baudrate = baudrate
        self._timeout = timeout
        self._debug = debug

    def __del__(self):

        self.disconnect()

    def connect(self):
        """
        Open serial connection.
        """

        self._connected = False
        try:
            self._serial_object = Serial(
                self._port, self._baudrate, timeout=self._timeout
            )

            self._connected = True
            if self._debug:
                print("INFO: Connected Successfully to port: {}".format(self._port))
            
        except (SerialException, SerialTimeoutException) as err:
            print(f"Error connecting to serial port {err}")

        return self._connected

    def disconnect(self):
        """
        Close serial connection.
        """

        if self._connected and self._serial_object:
            try:
                self._serial_object.close()
            except (SerialException, SerialTimeoutException) as err:
                print(f"Error disconnecting from serial port {err}")
        self._connected = False

        return self._connected

    def send(self, data):
        """
        Send data to serial connection.
        """

        self._serial_object.write(data)

    def flush(self):
        """
        Flush input buffer
        """

        self._serial_object.reset_input_buffer()
    
    def read(self, size=1):
        """
        Read bytes(size) from serial connection.
        """

        return self._serial_object.read(size)

    def readline(self):
        """
        Read line from serial connection.
        """

        return self._serial_object.readline()
    
    def readlines(self):
        """
        Read a list of recived lines from serial connection.
        """
        
        # return [line.decode() for line in self._serial_object.readlines()]
        return self._serial_object.readlines()

    @property
    def is_available(self):
        """
        Check if any messages remaining in the input buffer
        """

        return self._serial_object.in_waiting


# lora = SerialCommunication("/dev/ttyUSB0", 9600, timeout=1)
# lora.connect()
# lora.send(b"AT+DEVINFO=?\r\n")
# time.sleep(0.1)
# print("coming data: ",  lora.is_available)
# data = lora.readlines()
# print(data)
