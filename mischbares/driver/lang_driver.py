import sys
import clr

from mischbares.config.main_config import config
from mischbares.logger import logger

log = logger.get_logger("lang_driver")

PYLANG_PATH = config['lang']['langDriver']['path_pylang']

sys.path.append(fr"{PYLANG_PATH}\LStepAPI\_C#_VB.net")
sys.path.append(fr"{PYLANG_PATH}\LStepAPI")


class langNet():
    def __init__(self):
        self.port = config['lang']['langDriver']['serial_port']
        self.dllpath = fr"{PYLANG_PATH}\LStepAPI\_C#_VB.net\CClassLStep64"
        self.dllconfigpath = fr"{PYLANG_PATH}\config.LSControl"
        clr.AddReference(self.dllpath)
        import CClassLStep
        self.LS = CClassLStep.LStep()
        self.connected = False
        self.connect()
        self.LS.SetVel(config['lang']['langDriver']['velocity_x'],
                       config['lang']['langDriver']['velocity_y'],
                       config['lang']['langDriver']['velocity_z'], 0)
        self.goHome()


    def connect(self):
        """Connect to the motor
        """
        res = self.LS.ConnectSimpleW(11, self.port, 115200, True)
        if res == 0:
            log.info("Motor is Connected")
        self.LS.LoadConfigW(self.dllconfigpath)
        self.connected = True


    def disconnect(self):
        """Disconnect from the motor"""
        res = self.LS.Disconnect()
        if res == 0:
            log.info("Motor is Disconnected")
        self.connected = False


    def getPos(self):
        """Get the current position of the motor

        Returns:
            list: [x,y,z] position
        """
        ans = self.LS.GetPos(0,0,0,0)
        return ans [1:-1]


    def goHome(self):
        """Move the motor to the home position
        """
        self.moveAbsFar(0,0,0)


    def moveRelFar(self,dx,dy,dz):
        """Move the motor relative to the current position

        Args:
            dx (float): distance in x direction
            dy (float): distance in y direction
            dz (float): distance in z direction
        """
        if dz > 0: #moving down -> z last
            self.moveRelXY(dx,dy)
            self.moveRelZ(dz)
        if dz <= 0: # moving up -> z first
            self.moveRelZ(dz)
            self.moveRelXY(dx,dy)


    def moveRelZ(self, dz, wait=True):
        """Move the motor relative to the current position in z direction

        Args:
            dz (float): distance in z direction
            wait (bool, optional): Wait until the motor is finished. Defaults to True.
        """
        self.LS.MoveRel(0,0,dz,0,wait)


    def moveRelXY(self, dx, dy, wait=True):
        """Move the motor relative to the current position in x and y direction

        Args:
            dx (float): distance in x direction
            dy (float): distance in y direction
            wait (bool, optional): Wait until the motor is finished. Defaults to True.
        """
        self.LS.MoveRel(dx,dy,0,0,wait)


    def moveAbsXY(self,x_pos,y_pos,wait=True):
        """Move the motor to a certain position in x and y direction

        Args:
            x_pos (float): x position
            y_pos (float): y position
            wait (bool, optional): Wait until the motor is finished. Defaults to True.

        """
        _, _, z_position = self.getPos()
        self.LS.MoveAbs(x_pos, y_pos, z_position, 0, wait)


    def moveAbsZ(self, z_pos, wait=True):
        """Move the motor to a certain position in z direction

        Args:
            z_pos (float): z position
            wait (bool, optional): Wait until the motor is finished. Defaults to True.
        """
        x_pos, y_pos, _ = self.getPos()
        self.LS.MoveAbs(x_pos, y_pos, z_pos, 0, wait)


    def moveAbsFar(self, dx, dy, dz):
        """Move the motor to a certain position

        Args:
            dx (float): x position
            dy (float): y position
            dz (float): z position
        """
        if dz > 0: #moving down -> z last
            self.moveAbsXY(dx,dy)
            self.moveAbsZ2(dz)
        if dz <= 0: # moving up -> z first
            self.moveAbsZ2(dz)
            self.moveAbsXY(dx,dy)


    def setMaxVel(self,xvel,yvel,zvel):
        """Set the maximum velocity of the motor

        Args:
            xvel (float): x velocity
            yvel (float): y velocity
            zvel (float): z velocity
        """
        self.LS.SetVel(xvel, yvel, zvel, 0)

    def moveAbsZ2(self, z_pos, wait=True):
        """Move the motor to a certain position in z direction

        Args:
            z (float): z position
            wait (bool, optional): _description_. Defaults to True.
        """
        self.moveRelZ(z_pos-self.getPos()[2],wait)


    def stopMove(self):
        """Stop the motor
        """
        self.LS.StopAxes()

