import numpy as np

from ..utils.events import EmitterGroup


class GridCanvas:
    """Grid for canvas.

    Right now the only grid mode that is still inside one canvas with one
    camera, but future grid modes could support multiple canvases.

    Attributes
    ----------
    events : EmitterGroup
        Event emitter group
    enabled : bool
        If grid is enabled or not.
    size : 2-tuple of int
        Number of rows and columns in the grid. A value of -1 for either or
        both of will be used the row and column numbers will trigger an
        auto calculation of the necessary grid size to appropriately fill
        all the layers at the appropriate stride.
    stride : int
        Number of layers to place in each grid square before moving on to
        the next square. The default ordering is to place the most visible
        layer in the top left corner of the grid. A negative stride will
        cause the order in which the layers are placed in the grid to be
        reversed.
    """

    def __init__(self, *, size=(-1, -1), stride=1, enabled=False):

        # Events:
        self.events = EmitterGroup(
            source=self, auto_connect=True, update=None,
        )

        self._enabled = enabled
        self._stride = stride
        self._size = size

    @property
    def enabled(self):
        """bool: If grid is enabled or not."""
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        self._enabled = enabled
        self.events.update()

    @property
    def size(self):
        """2-tuple of int: Number of rows and columns in the grid."""
        return self._size

    @size.setter
    def size(self, size):
        self._size = tuple(size)
        self.events.update()

    @property
    def stride(self):
        """int: Number of layers in each grid square."""
        return self._stride

    @stride.setter
    def stride(self, stride):
        self._stride = stride
        self.events.update()

    def actual_size(self, nlayers=1):
        """Return the actual size of the grid.

        This will return the size parameter, unless one of the row
        or column numbers is -1 in which case it will compute the
        optimal size of the grid given the number of layers and
        current stride.

        If the grid is not enabled, this will return (1, 1).

        Parameters
        ----------
        nlayers : int
            Number of layers that need to be placed in the grid.

        Returns
        -------
        size : 2-tuple of int
            Number of rows and columns in the grid.
        """
        if self.enabled:
            n_row, n_column = self.size
            n_grid_squares = np.ceil(nlayers / abs(self.stride)).astype(int)

            if n_row == -1 and n_column == -1:
                n_column = np.ceil(np.sqrt(n_grid_squares)).astype(int)
                n_row = np.ceil(n_grid_squares / n_column).astype(int)
            elif n_row == -1:
                n_row = np.ceil(n_grid_squares / n_column).astype(int)
            elif n_column == -1:
                n_column = np.ceil(n_grid_squares / n_row).astype(int)

            n_row = max(1, n_row)
            n_column = max(1, n_column)

            return (n_row, n_column)
        else:
            return (1, 1)

    def position(self, index, nlayers):
        """Return the position of a given linear index in grid.

        If the grid is not enabled, this will return (0, 0).

        Parameters
        ----------
        index : int
            Position of current layer in layer list.
        nlayers : int
            Number of layers that need to be placed in the grid.

        Returns
        -------
        position : 2-tuple of int
            Row and column position of current index in the grid.
        """
        if self.enabled:
            n_row, n_column = self.actual_size(nlayers)

            # Adjust for forward or reverse ordering
            if self.stride < 0:
                adj_i = nlayers - index - 1
            else:
                adj_i = index

            adj_i = adj_i // abs(self.stride)
            adj_i = adj_i % (n_row * n_column)
            i_row = adj_i // n_column
            i_column = adj_i % n_column
            return (i_row, i_column)
        else:
            return (0, 0)
