"""QtRender widget.
"""


from qtpy.QtWidgets import QVBoxLayout, QWidget

from ....layers.image import Image
from ....layers.image.experimental.octree_image import OctreeImage
from .qt_image_info import QtImageInfo
from .qt_mini_map import MiniMap
from .qt_octree_info import QtOctreeInfo
from .qt_test_image import QtTestImage


class QtRender(QWidget):
    """Dockable widget for render controls.

    Parameters
    ----------
    viewer : Viewer
        The napari viewer.
    layer : Optional[Layer]
        Show controls for this layer. If no layer show minimal controls.
    """

    def __init__(self, viewer, layer=None):
        """Create our windgets.
        """
        super().__init__()
        self.viewer = viewer
        self.layer = layer

        layout = QVBoxLayout()

        # Basic info for any image layer.
        if isinstance(layer, Image):
            layout.addWidget(QtImageInfo(layer))

        # Octree specific controls and minimap.
        if isinstance(layer, OctreeImage):
            layout.addWidget(QtOctreeInfo(layer))

            self.mini_map = MiniMap(viewer, layer)
            layout.addWidget(self.mini_map)
            self.viewer.camera.events.center.connect(self._on_camera_move)

        # Controls to create a new test image.
        layout.addStretch(1)
        layout.addWidget(QtTestImage(viewer))
        self.setLayout(layout)

    def _on_camera_move(self, event=None):
        """Called when the camera was moved."""
        self.mini_map.update()
