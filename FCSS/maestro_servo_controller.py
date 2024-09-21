import serial

class Controller:
    def __init__(self, ttyStr='COM3', device=0x0c):
        # Open the command port
        self.usb = serial.Serial(ttyStr)

        # Command lead-in and device number are sent for each Pololu serial command.
        self.PololuCmd = bytes([0xaa, device])
        # Track target position for each servo. The function isMoving() will
        # use the Target vs Current servo position to determine if movement is
        # occuring.  Upto 24 servos on a Maestro, (0-23). Targets start at 0.
        self.Targets = [0] * 24
        # Servo minimum and maximum targets can be restricted to protect components.
        self.Mins = [0] * 24
        self.Maxs = [0] * 24

    def close(self):
        self.usb.close()

    def sendCmd(self, cmd):
        cmdStr = self.PololuCmd + cmd
        self.usb.write(cmdStr)

    def setRange(self, chan, min, max):
        self.Mins[chan] = min
        self.Maxs[chan] = max

    def getMin(self, chan):
        return self.Mins[chan]

    def getMax(self, chan):
        return self.Maxs[chan]

    def setTarget(self, chan, target):
        # if Min is defined and Target is below, force to Min
        if self.Mins[chan] > 0 and target < self.Mins[chan]:
            target = self.Mins[chan]
        # if Max is defined and Target is above, force to Max
        if self.Maxs[chan] > 0 and target > self.Maxs[chan]:
            target = self.Maxs[chan]
        #    
        lsb = target & 0x7f #7 bits for least significant byte
        msb = (target >> 7) & 0x7f #shift 7 and take next 7 bits for msb
        cmd = bytes([0x04, chan, lsb, msb])
        self.sendCmd(cmd)
        # Record Target value
        self.Targets[chan] = target

    def setSpeed(self, chan, speed):
        lsb = speed & 0x7f #7 bits for least significant byte
        msb = (speed >> 7) & 0x7f #shift 7 and take next 7 bits for msb
        cmd = bytes([0x07, chan, lsb, msb])
        self.sendCmd(cmd)

    def setAccel(self, chan, accel):
        lsb = accel & 0x7f #7 bits for least significant byte
        msb = (accel >> 7) & 0x7f #shift 7 and take next 7 bits for msb
        cmd = bytes([0x09, chan, lsb, msb])
        self.sendCmd(cmd)

    def getPosition(self, chan):
        cmd = bytes([0x10, chan])
        self.sendCmd(cmd)
        lsb = self.usb.read()
        msb = self.usb.read()
        return (msb << 8) + lsb

    def isMoving(self, chan):
        if self.Targets[chan] > 0:
            if self.getPosition(chan) != self.Targets[chan]:
                return True
        return False

    def getMovingState(self):
        cmd = bytes([0x13])
        self.sendCmd(cmd)
        if self.usb.read() == bytes([0]):
            return False
        else:
            return True

    def runScriptSub(self, subNumber):
        cmd = bytes([0x27, subNumber])
        self.sendCmd(cmd)

    def stopScript(self):
        cmd = bytes([0x24])
        self.sendCmd(cmd)

# servo = Controller()