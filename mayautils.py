import logging
import os

import maya.cmds as cmds

import pymel.core as pmc
from pymel.core.system import Path

log = logging.getLogger(__name__)

class SceneFile(object):
    """Class used to to represent a DCC software scene file

    The class will be a convenient object that we can use to manipulate our
    scene files. Examples features include the ability to predefine our naming
    conventions and automatically increment our versions.

    Attributes:
        dir (Path, optional): Directory to the scene file. Defaults to ''.
        descriptor (str, optional): Short descriptor of the scene file.
            Defaults to "main".
        version (int, optional): Version number. Defaults to 1.
        ext (str, optional): Extension. Defaults to "ma"
    """

    def __init__(self, dir='', descriptor='main', version=1, ext='ma'):
        pathString = cmds.file(query=True, sceneName=True)
        fileName = os.path.basename(pathString)
        self._dir = os.path.dirname(pathString)
        self.descriptor = os.path.splitext(fileName)[0].split('_')[0]
        self.version = int(os.path.splitext(pathString)[0].split('_')[-1])
        self.ext = os.path.splitext(pathString)[1].split('.')[1]

    @property
    def dir(self):
        return self._dir

    @dir.setter
    def dir(self, val):
        self._dir = Path(val)

    def basename(self):
        """Return a scene file name.
        e.g. ship_001.ma, car_011.hip
        Returns:
            str: The name of the scene file.
        """

        name_pattern = "{descriptor}_{version:03d}.{ext}"
        name = name_pattern.format(descriptor=self.descriptor,
                                   version=self.version,
                                   ext=self.ext)
        return name

    def path(self):
        """The function returns a path to scene file.
        This includes the drive letter, any directory path and the file name.
        Returns:
            Path: The path to the scene file.
        """
        return Path(self.dir) / self.basename()

    def save(self):
        """Saves the scene file.
        Returns:
            Path: The path to the scene file if successful, None, otherwise.
        """
        try:
            pmc.system.saveAs(self.path())
        except RuntimeError:
            log.warning("Missing Directories... Creating Directories.")
            Path(self.dir).makedirs_p()
            pmc.system.saveAs(self.path())

    def increment_and_save(self):
        """Increments the version and saves the scene file.
        If existing versions of a file already exist, it should increment
        from the largest number available in the folder.

        Returns:
            Path: The path to the scene file if successful, None, otherwise.
        """
        self.version += 1
        pmc.system.saveAs(self.path())