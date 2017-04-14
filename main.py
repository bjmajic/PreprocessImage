import numpy as np


def _whctrs(anchor):
    """
    Return width, height, x center, and y center for an anchor (window).
    """

    w = anchor[2] - anchor[0] + 1
    h = anchor[3] - anchor[1] + 1
    x_ctr = anchor[0] + 0.5 * (w - 1)
    y_ctr = anchor[1] + 0.5 * (h - 1)
    return w, h, x_ctr, y_ctr


def _ratio_enum(anchor, ratios):
    """
    Enumerate a set of anchors for each aspect ratio wrt an anchor.
    """

    w, h, x_ctr, y_ctr = _whctrs(anchor)
    size = w * h
    size_ratios = size / ratios
    ws = np.round(np.sqrt(size_ratios))
    hs = np.round(ws * ratios)
    anchors = _mkanchors(ws, hs, x_ctr, y_ctr)
    return anchors


def _mkanchors(ws, hs, x_ctr, y_ctr):
    """
    Given a vector of widths (ws) and heights (hs) around a center
    (x_ctr, y_ctr), output a set of anchors (windows).
    """

    ws = ws[:, np.newaxis]
    hs = hs[:, np.newaxis]
    anchors = np.hstack((x_ctr - 0.5 * (ws - 1),
                         y_ctr - 0.5 * (hs - 1),
                         x_ctr + 0.5 * (ws - 1),
                         y_ctr + 0.5 * (hs - 1)))
    return anchors

if __name__ == '__main__':
    base_anchor = np.array([0, 0, 15, 15])
    # ratios = np.array([0.5, 1.0, 2.0])
    ratios_ = [0.5, 1, 2]
    ratio_anchors = _ratio_enum(base_anchor, ratios_)
    shift_x = np.arange(0, 3) * 5
    shift_y = np.arange(0, 2) * 5
    shift_x, shift_y = np.meshgrid(shift_x, shift_y)
    shifts = np.vstack((shift_x.ravel(), shift_y.ravel(),
                        shift_x.ravel(), shift_y.ravel())).transpose()
    print shifts.shape
    K = shifts.shape[0]
    print shifts
    print K
    shiftT = shifts.reshape((1, K, 4))
    print shiftT.shape
    shiftT = shifts.reshape((1, K, 4)).transpose((1, 0, 2))
    print shiftT.shape
    print type(shiftT)
    
    anchors = np.array([
        [-1.,  -2.,  3.,   4.],
        [-5.,  -6.,  7.,  8.],
        # [-359., -183.,  376.,  200.],
        # [-55.,  -55.,   72.,   72.],
        # [-119., -119.,  136.,  136.],
        # [-247., -247.,  264.,  264.],
        # [-35.,  -79.,   52.,   96.],
        # [-79., -167.,   96.,  184.],
        # [-167., -343.,  184.,  360.]
    ])
    print "anchors.shape = ", anchors.shape
    Tt = anchors.reshape((1, 2, 4))
    print "Tt.shape = ", Tt.shape
    addarray = anchors.reshape((1, 2, 4)) + shifts.reshape((1, K, 4)).transpose((1, 0, 2))
    print addarray