import  time
import  threading

import  xbmcaddon
import  xbmcgui

from    util.temperature            import Temperature
import  vera.device
from    gui.xbmc                    import *
from    gui                         import controlid

__addon__   = xbmcaddon.Addon('script.vera')
__cwd__     = __addon__.getAddonInfo('path')

class DimLightThread( threading.Thread ):

    def __init__(self, gui_):
        threading.Thread.__init__(self)
        self.gui = gui_
        self.device = gui_.device
        self.vera = gui_.parent.vera

    def run(self):
        self.runThread = True
        slider = self.gui.getControl(controlid.dimmable_light.SLIDER)
        while(self.runThread):
            newValue = slider.getPercent()
            if newValue != int( float( self.device['level'] ) ):  
                vera.device.dim(self.device, self.vera, newValue)
            time.sleep(1)

class DimmableLight( xbmcgui.WindowXMLDialog ):

    def __init__(self, *args, **kwargs):
        self.device = kwargs['device']
        self.parent = kwargs['parent']
        self.dimmerThread = DimLightThread(self)

    def onInit(self):
        self.slider().setPercent( int( float( self.device['level'] ) ) )
        self.dimmerThread.start()

    def slider(self):
        return self.getControl(controlid.dimmable_light.SLIDER)

    def onAction(self, action):
        if action in (ACTION_PREVIOUS_MENU, ACTION_ENTER):
            self.dimmerThread.runThread = False
            self.close()
        elif action == ACTION_MOVE_UP:
            self.slider().setPercent(100)
        elif action == ACTION_MOVE_DOWN:
            self.slider().setPercent(0)

