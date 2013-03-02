"""
.. py:module:: filters
Filters Module
==============

Module for building 2D filters of various types. Can build high and low
pass, band pass/stop in both circular and linear, log transform, gamma
transform, and DC offset correction. It also includes convinence functions and
classes for building and applying a stack of filters.

"""

import numpy as np
from scipy import interpolate
from scipy import signal


def build2DLP(Window, Dim, Diameter=0, Outer=False, Cont=False):
    """
    Builds a 2D low pass filter matrix.
    
    A filter with profile defined by Window is built, with the final size being
    Dim. If the final filter is larger than the Diameter, then it will be zero 
    padded to match. The window can be constructed using either a rotational
    method, or outer product. The contour can be set to be constant in either
    the number of pixels, or percentage of the image dimensions
    
    Parameters
    ----------
    Window : string
        Name of the function to be used. See the scipy.signal documentation for
        descriptions of the available windows.
        
    Dim : tuple
        Final size of the filter in (x, y) format.
        
    Diameter : int, optional
        Size of the window in pixels. Defaults to the largets Dimesion of 
        the final filter.
        
    Outer : Bool, optional
        Selectes between using an outter product (True) or rotational 
        construction method for the 2D filter. Defaults to False, which is
        a rotational construction.
        
    Cont : Bool, optional
        Selects between making the diameter a constant number of pixels, 
        or a constant percentage of the final image size. Defaults to False
        which is a constant percentage.
            
    Returns
    -------
    Window : 2D array
        The filter is returned as a 2D array of floats.
        
    See Also
    --------
    makeLPF : builds a 2D low pass filter funciton and returns a
    :class:`GFilter` object.
        
    """
    if Diameter == 0:
        Diameter = max(Dim)
    if Outer:
        #calculate the 2D filter as an outter product of
        #two 1D filters of the correct length
        window1 = signal.get_window(Window, Diameter)
        window2 = np.outer(window1, window1)
    else:
        #calculate the 2D filter as a rotation of the 1D filter start with a
        #basis filter that is the larger dimension interpolate onto a square
        #grid of distances to every pixel.
        window1 = signal.get_window(Window, Diameter)
        lenX = (Diameter-1)/2.0
        #construct the distance vector for the 1D window
        distX = np.linspace(-lenX, lenX, Diameter)
        #build a 2D array of distances from the center pixel
        xMesh, yMesh = np.meshgrid(distX, distX)
        cutoff = np.sqrt((xMesh**2.0) + (yMesh**2.0))
        #calculate the value of the window at these distances and populate the
        #2D array with those values
        w1Interp = interpolate.interp1d(distX, window1)
        window2 = np.zeros((Diameter, Diameter))
        window2[cutoff <= lenX] = w1Interp(cutoff[cutoff <= lenX])
        #resize the array to match the data, and return it
    return resizeToMatch(window2, Dim, Cont)


def makeLPF(Window, Dim, Diameter=0, Outer=False, Cont=False):
    """
    Constructs a low pass filter object.
    
    A filter with profile defined by Window is built, with the final size being
    Dim. If the final filter is larger than the Diameter, then it will be zero 
    padded to match. The window can be constructed using either a rotational
    method, or outer product. The contour can be set to be constant in either
    the number of pixels, or percentage of the image dimensions
    
    Parameters
    ----------
    Window : string
        Name of the function to be used. See the scipy.signal documentation for
        descriptions of the available windows.
        
    Dim : tuple
        Final size of the filter in (x, y) format.
        
    Diameter : int, optional
        Size of the window in pixels. Defaults to the largets Dimesion of 
        the final filter.
        
    Outer : Bool, optional
        Selectes between using an outter product (True) or rotational 
        construction method for the 2D filter. Defaults to False, which is
        a rotational construction.
        
    Cont : Bool, optional
        Selects between making the diameter a constant number of pixels, 
        or a constant percentage of the final image size. Defaults to False
        which is a constant percentage.
            
    Returns
    -------
    Filter : :class:`GFilter`
        The returned object described by the following attributes
        
        =============== ============ ==========================================
        Attribute       Value        Description
        =============== ============ ==========================================
        Par['Type']     'Low Pass'   String defining the filter type as Low
                                     pass
        --------------- ------------ ------------------------------------------ 
        Par['Linear']   True         Type of filter
        --------------- ------------ ------------------------------------------
        Par['Dim']      Dim          Two element (x, y) tuple 
        --------------- ------------ ------------------------------------------
        Par['Diameter'] Diameter     Int for the window length
        --------------- ------------ ------------------------------------------
        Par['Outer']    Outer        Bool for the construction method
        --------------- ------------ ------------------------------------------
        Par['Contour']  Cont         Bool describing the contour type
        --------------- ------------ ------------------------------------------
        Par['Name']     Window       Filter window name
        --------------- ------------ ------------------------------------------
        Par['Shape']    Shape        optional, only found with some windows
        --------------- ------------ ------------------------------------------
        function        function     The function used to construct the filter
        =============== ============ ==========================================
        
    See Also
    --------
    build2DLP : builds a 2D low pass filter matrix.

    """
    filt = GFilter(Par={'Type': 'Low Pass',
                        'Linear': True,
                        'Dim': Dim,
                        'Diameter': Diameter,
                        'Outer': Outer,
                        'Contour': Cont})

    if isinstance(Window, str):
        filt.params['Name'] = Window
    else:
        filt.params['Name'] = Window[0]
        filt.params['Shape'] = Window[1]

    filt.function = lambda x: x*build2DLP(Window, Dim, Diameter, Outer, Cont)
    return filt


def build2DHP(Window, Dim, Diameter=0, Outer=False, Cont=False):
    """
    Constructs a 2D highpass filter.
    
    A filter with profile defined by Window is built, with the final size being
    Dim. If the final filter is larger than the Diameter, then it will be zero 
    padded to match. The window can be constructed using either a rotational
    method, or outer product. The contour can be set to be constant in either
    the number of pixels, or percentage of the image dimensions
    
    Parameters
    ----------
    Window : string
        Name of the function to be used. See the scipy.signal documentation for
        descriptions of the available windows.
        
    Dim : tuple
        Final size of the filter in (x, y) format.
        
    Diameter : int, optional
        Size of the window in pixels. Defaults to the largets Dimesion of 
        the final filter.
        
    Outer : Bool, optional
        Selectes between using an outter product (True) or rotational 
        construction method for the 2D filter. Defaults to False, which is
        a rotational construction.
        
    Cont : Bool, optional
        Selects between making the diameter a constant number of pixels, 
        or a constant percentage of the final image size. Defaults to False
        which is a constant percentage.
            
    Returns
    -------
    Window : 2D array
        The filter is returned as a 2D array of floats.
        
    See Also
    --------
    makeHPF : builds a 2D high pass filter funciton and returns a
    :class:`GFilter` object.
    
    Notes
    -----
    The high-pass filter is built by subtracting a matrix build using
    :func:`build2DLP` from a ones matrix of the same dimension.

    """
    return np.ones(Dim)-build2DLP(Window, Dim, Diameter, Outer, Cont)


def makeHPF(Window, Dim, Diameter=0, Outer=False, Cont=False):
    """
    Constructs a high pass filter object
        
    A filter with profile defined by Window is built, with the final size being
    Dim. If the final filter is larger than the Diameter, then it will be zero 
    padded to match. The window can be constructed using either a rotational
    method, or outer product. The contour can be set to be constant in either
    the number of pixels, or percentage of the image dimensions
    
    Parameters
    ----------
    Window : string
        Name of the function to be used. See the scipy.signal documentation for
        descriptions of the available windows.
        
    Dim : tuple
        Final size of the filter in (x, y) format.
        
    Diameter : int, optional
        Size of the window in pixels. Defaults to the largets Dimesion of 
        the final filter.
        
    Outer : Bool, optional
        Selectes between using an outter product (True) or rotational 
        construction method for the 2D filter. Defaults to False, which is
        a rotational construction.
        
    Cont : Bool, optional
        Selects between making the diameter a constant number of pixels, 
        or a constant percentage of the final image size. Defaults to False
        which is a constant percentage.
            
    Returns
    -------
    Filter : :class:`GFilter`
        The returned object described by the following attributes
        
        =============== ============= =========================================
        Attribute       Value         Description
        =============== ============= =========================================
        Par['Type']     'High Pass'   String defining the filter type as High
                                      pass
        --------------- ------------- ----------------------------------------- 
        Par['Linear']   True          Type of filter
        --------------- ------------- -----------------------------------------
        Par['Dim']      Dim           Two element (x, y) tuple 
        --------------- ------------- -----------------------------------------
        Par['Diameter'] Diameter      Int for the window length
        --------------- ------------- -----------------------------------------
        Par['Outer']    Outer         Bool for the construction method
        --------------- ------------- -----------------------------------------
        Par['Contour']  Cont          Bool describing the contour type
        --------------- ------------- -----------------------------------------
        Par['Name']     Window        Filter window name
        --------------- ------------- -----------------------------------------
        Par['Shape']    Shape         optional, only found with some windows
        --------------- ------------- -----------------------------------------
        function        function      The function used to construct the filter
        =============== ============= =========================================
        
    See Also
    --------
    build2DHP : builds a 2D high pass filter matrix.
    
    """
    filt = GFilter(Par={'Type': 'High Pass',
                        'Linear': True,
                        'Dim': Dim,
                        'Diameter': Diameter,
                        'Outer': Outer,
                        'Contour': Cont})

    if isinstance(Window, str):
        filt.params['Name'] = Window
    else:
        filt.params['Name'] = Window[0]
        filt.params['Shape'] = Window[1]

    filt.function = lambda x: x*build2DHP(Window, Dim, Diameter, Outer, Cont)
    return filt


def build2DBP(Window, Dim, Diameter=0, Width=3, Cont=False):
    """
    Constructs a 2D bandpass filter.
    
    A filter with profile defined by Window is built, with the final size being
    Dim. Zeros are added before and after the window to position it correctly. 
    If the final filter is larger than the Diameter, then it will be zero 
    padded to match. The window can be constructed using either a rotational
    method, or outer product. The contour can be set to be constant in either
    the number of pixels, or percentage of the image dimensions
    
    Parameters
    ----------
    Window : string
        Name of the function to be used. See the scipy.signal documentation for
        descriptions of the available windows.
        
    Dim : tuple
        Final size of the filter in (x, y) format.
        
    Diameter : int, optional
        Size of the window in pixels. Defaults to the largets Dimesion of 
        the final filter.
        
    Width : int, optional
        Sets the width of the filter in pixels. Defaults to 3 pixels
        
    Cont : Bool, optional
        Selects between making the diameter a constant number of pixels, 
        or a constant percentage of the final image size. Defaults to False
        which is a constant percentage.
            
    Returns
    -------
    Window : 2D array
        The filter is returned as a 2D array of floats.
        
    See Also
    --------
    makeBPF : builds a 2D band pass filter function and returns a
    :class:`GFilter` object.

    """
    if Diameter == 0:
        Diameter = max(Dim)
    #calculate the 2D filter as a rotation of the 1D filter start with a
    #basis filter that is the larger dimension interpolate onto a square
    #grid of distances to every pixel.
    window1 = signal.get_window(Window, Width)
    window1 = np.concatenate((np.zeros(Diameter-np.size(window1)), window1))
    lenX = (Diameter-1)/2.0
    #construct the distance vector for the 1D window
    distX = np.linspace(-lenX, lenX, Diameter)
    #build a 2D array of distances from the center pixel
    xMesh, yMesh = np.meshgrid(distX, distX)
    cutoff = np.sqrt((xMesh**2.0) + (yMesh**2.0))
    #calculate the value of the window at these distances and populate the
    #2D array with those values
    w1Interp = interpolate.interp1d(distX, window1)
    window2 = np.zeros((Diameter, Diameter))
    window2[cutoff <= lenX] = w1Interp(cutoff[cutoff <= lenX])
    #resize the array to match the data, and return it
    return resizeToMatch(window2, Dim, Cont)
    
def makeBPF(Window, Dim, Diameter=0, Width=3, Cont=False):
    """
    Constructs a band pass filter object.
    
    A filter with profile defined by Window is built, with the final size being
    Dim. Zeros are added before and after the window to position it correctly. 
    If the final filter is larger than the Diameter, then it will be zero 
    padded to match. The window can be constructed using either a rotational
    method, or outer product. The contour can be set to be constant in either
    the number of pixels, or percentage of the image dimensions
    
    Parameters
    ----------
    Window : string
        Name of the function to be used. See the scipy.signal documentation for
        descriptions of the available windows.
        
    Dim : tuple
        Final size of the filter in (x, y) format.
        
    Diameter : int, optional
        Size of the window in pixels. Defaults to the largets Dimesion of 
        the final filter.
        
    Width : int, optional
        Sets the width of the filter in pixels. Defaults to 3 pixels
        
    Cont : Bool, optional
        Selects between making the diameter a constant number of pixels, 
        or a constant percentage of the final image size. Defaults to False
        which is a constant percentage.
            
    Returns
    -------
    Filter : :class:`GFilter`
        The returned object described by the following attributes
        
        =============== ============= =========================================
        Attribute       Value         Description
        =============== ============= =========================================
        Par['Type']     'Band Pass'   String defining the filter type as Band
                                      pass
        --------------- ------------- ----------------------------------------- 
        Par['Linear']   True          Type of filter
        --------------- ------------- -----------------------------------------
        Par['Dim']      Dim           Two element (x, y) tuple 
        --------------- ------------- -----------------------------------------
        Par['Diameter'] Diameter      Int for the window length
        --------------- ------------- -----------------------------------------
        Par['Width']    Width         Int for the window width
        --------------- ------------- -----------------------------------------
        Par['Contour']  Cont          Bool describing the contour type
        --------------- ------------- -----------------------------------------
        Par['Name']     Window        Filter window name
        --------------- ------------- -----------------------------------------
        Par['Shape']    Shape         optional, only found with some windows
        --------------- ------------- -----------------------------------------
        function        function      The function used to construct the filter
        =============== ============= =========================================
        
    See Also
    --------
    build2DBP : builds a 2D band pass filter matrix.

    """
    filt = GFilter(Par={'Type': 'Band Pass',
                        'Linear': True,
                        'Dim': Dim,
                        'Diameter': Diameter,
                        'Width': Width,
                        'Contour': Cont})

    if isinstance(Window, str):
        filt.params['Name'] = Window
    else:
        filt.params['Name'] = Window[0]
        filt.params['Shape'] = Window[1]

    filt.function = lambda x: x*build2DBP(Window, Dim, Diameter, Width, Cont)
    return filt


def build2DBS(Window, Dim, Diameter=0, Width=3, Cont=False):
    """
    Constructs a 2D bandstop filter.
    
    A filter with profile defined by Window is built, with the final size being
    Dim. Zeros are added before and after the window to position it correctly. 
    If the final filter is larger than the Diameter, then it will be zero 
    padded to match. The window can be constructed using either a rotational
    method, or outer product. The contour can be set to be constant in either
    the number of pixels, or percentage of the image dimensions
    
    Parameters
    ----------
    Window : string
        Name of the function to be used. See the scipy.signal documentation for
        descriptions of the available windows.
        
    Dim : tuple
        Final size of the filter in (x, y) format.
        
    Diameter : int, optional
        Size of the window in pixels. Defaults to the largets Dimesion of 
        the final filter.
        
    Width : int, optional
        Sets the width of the filter in pixels. Defaults to 3 pixels
        
    Cont : Bool, optional
        Selects between making the diameter a constant number of pixels, 
        or a constant percentage of the final image size. Defaults to False
        which is a constant percentage.
            
    Returns
    -------
    Window : 2D array
        The filter is returned as a 2D array of floats.
        
    See Also
    --------
    makeBSF : builds a 2D band stop filter function and returns a
    :class:`GFilter` object.
    
    Notes
    -----
    The high-pass filter is built by subtracting a matrix build using
    :func:`build2DBP` from a ones matrix of the same dimension.
    
    """
    return np.ones(Dim)-build2DBP(Window, Dim, Diameter, Width, Cont)


def makeBSF(Window, Dim, Diameter=0, Width=3, Cont=False):
    """Constructs a band stop filter object
    
    A filter with profile defined by Window is built, with the final size being
    Dim. Zeros are added before and after the window to position it correctly. 
    If the final filter is larger than the Diameter, then it will be zero 
    padded to match. The window can be constructed using either a rotational
    method, or outer product. The contour can be set to be constant in either
    the number of pixels, or percentage of the image dimensions
    
    Parameters
    ----------
    Window : string
        Name of the function to be used. See the scipy.signal documentation for
        descriptions of the available windows.
        
    Dim : tuple
        Final size of the filter in (x, y) format.
        
    Diameter : int, optional
        Size of the window in pixels. Defaults to the largets Dimesion of 
        the final filter.
        
    Width : int, optional
        Sets the width of the filter in pixels. Defaults to 3 pixels
        
    Cont : Bool, optional
        Selects between making the diameter a constant number of pixels, 
        or a constant percentage of the final image size. Defaults to False
        which is a constant percentage.
            
    Returns
    -------
    Filter : :class:`GFilter`
        The returned object described by the following attributes
        
        =============== =============== =======================================
        Attribute       Value           Description
        =============== =============== =======================================
        Par['Type']     'Band Stop'     Type String for a Band Stop filter
        --------------- --------------- ---------------------------------------
        Par['Linear']   True            Type of filter
        --------------- --------------- ---------------------------------------
        Par['Dim']      Dim             Two element (x, y) tuple 
        --------------- --------------- ---------------------------------------
        Par['Diameter'] Diameter        Int for the window length
        --------------- --------------- ---------------------------------------
        Par['Width']    Width           Int for the window width
        --------------- --------------- ---------------------------------------
        Par['Contour']  Cont            Bool describing the contour type
        --------------- --------------- ---------------------------------------
        Par['Name']     Window          Filter window name
        --------------- --------------- ---------------------------------------
        Par['Shape']    Shape           Shaping value for some window types
        --------------- --------------- ---------------------------------------
        function        function        The function used to
                                        construct the filter
        =============== =============== =======================================
        
    See Also
    --------
    build2DBS : builds a 2D band stop filter matrix.
    
    """
    filt = GFilter(Par={'Type': 'Band Stop',
                        'Linear': True,
                        'Dim': Dim,
                        'Diameter': Diameter,
                        'Width': Width,
                        'Contour': Cont})

    if isinstance(Window, str):
        filt.params['Name'] = Window
    else:
        filt.params['Name'] = Window[0]
        filt.params['Shape'] = Window[1]

    filt.function = lambda x: x*build2DBS(Window, Dim, Diameter, Width, Cont)
    return filt


def build2DVBP(Window, Dim, Center, Width=3):
    """
    Constructs a 2D linear bandpass filter in the virtical direction.
    
    A filter with profile defined by Window is built, with the final size being
    Dim. Zeros are added before and after the window to position it correctly.
    The window position (Center) must be specified, as well as it's width.
    
    Parameters
    ----------
    Window : string
        Name of the function to be used. See the scipy.signal documentation for
        descriptions of the available windows.
        
    Dim : tuple
        Final size of the filter in (x, y) format.
        
    Center : int
        Column on which the filter will be centered
        
    Width : int, optional
        Sets the width of the filter in pixels. Defaults to 3 pixels

    Returns
    -------
    Window : 2D array
        The filter is returned as a 2D array of floats.
        
    See Also
    --------
    makeVBPF : builds a 2D vertical band pass filter function and returns a
    :class:`GFilter` object.

    """
    window1 = signal.get_window(Window, Width)
    post = Dim[1]+np.floor(Width/2.0)-Center
    pre = Dim[1]-post-Width
    if pre < 0:
        window1 = window1[np.abs(pre):]
        pre = 0
    windowLine = np.concatenate((np.zeros(pre), window1, np.zeros(post)))
    window2 = np.zeros(Dim)
    window2[:, ] = windowLine
    return window2


def makeVBPF(Window, Dim, Center=0, Width=3):
    """
    Constructs a vertical band pass filter object
    
    A filter with profile defined by Window is built, with the final size being
    Dim. Zeros are added before and after the window to position it correctly.
    The window position (Center) must be specified, as well as it's width.
    
    Parameters
    ----------
    Window : string
        Name of the function to be used. See the scipy.signal documentation for
        descriptions of the available windows.
        
    Dim : tuple
        Final size of the filter in (x, y) format.
        
    Center : int
        Column on which the filter will be centered
        
    Width : int, optional
        Sets the width of the filter in pixels. Defaults to 3 pixels

    Returns
    -------
    Filter : :class:`GFilter`
        The returned object described by the following attributes
        
        =============== ==================== ==================================
        Attribute       Value                Description
        =============== ==================== ==================================
        Par['Type']     'Vertical Band Pass' String defining the filter type as
                                             Vertical Band Pass
        --------------- -------------------- ----------------------------------
        Par['Linear']   True                 Type of filter
        --------------- -------------------- ----------------------------------
        Par['Dim']      Dim                  Two element (x, y) tuple 
        --------------- -------------------- ----------------------------------
        Par['Center']   Center               Int column on which the filter is 
                                             centered
        --------------- -------------------- ----------------------------------
        Par['Width']    Width                Int for the window width
        --------------- -------------------- ----------------------------------
        Par['Name']     Window               Filter window name
        --------------- -------------------- ----------------------------------
        Par['Shape']    Shape                optional, only found with some
                                             windows
        --------------- -------------------- ----------------------------------
        function        function             The function used to construct the
                                             filter
        =============== ==================== ==================================
        
    See Also
    --------
    build2DVBP : builds a 2D vertical band pass filter matrix.
    
    """
    filt = GFilter(Par={'Type': 'Vertical Band Pass',
                        'Linear': True,
                        'Dim': Dim,
                        'Center': Center,
                        'Width': Width})

    if isinstance(Window, str):
        filt.params['Name'] = Window
    else:
        filt.params['Name'] = Window[0]
        filt.params['Shape'] = Window[1]

    filt.function = lambda x: x*build2DVBP(Window, Dim, Center, Width)
    return filt


def build2DVBS(Window, Dim, Center, Width):
    """
    Constructs a 2D linear bandstop filter in the virtical direction.
    
    A filter with profile defined by Window is built, with the final size being
    Dim. Zeros are added before and after the window to position it correctly.
    The window position (Center) must be specified, as well as it's width.
    
    Parameters
    ----------
    Window : string
        Name of the function to be used. See the scipy.signal documentation for
        descriptions of the available windows.
        
    Dim : tuple
        Final size of the filter in (x, y) format.
        
    Center : int
        Column on which the filter will be centered
        
    Width : int, optional
        Sets the width of the filter in pixels. Defaults to 3 pixels

    Returns
    -------
    Window : 2D array
        The filter is returned as a 2D array of floats.
        
    See Also
    --------
    makeVBSF : builds a 2D vertical band stop filter function and returns a
    :class:`GFilter` object.
    
    Notes
    -----
    The band stop filter is built by subtracting a matrix build using
    :func:`build2DVBP` from a ones matrix of the same dimension.
    
    """
    return np.ones(Dim)-build2DVBP(Window, Dim, Center, Width)


def makeVBSF(Window, Dim, Center=0, Width=3):
    """
    Constructs a vertical band stop filter object
        
    A filter with profile defined by Window is built, with the final size being
    Dim. Zeros are added before and after the window to position it correctly.
    The window position (Center) must be specified, as well as it's width.
    
    Parameters
    ----------
    Window : string
        Name of the function to be used. See the scipy.signal documentation for
        descriptions of the available windows.
        
    Dim : tuple
        Final size of the filter in (x, y) format.
        
    Center : int
        Column on which the filter will be centered
        
    Width : int, optional
        Sets the width of the filter in pixels. Defaults to 3 pixels

    Returns
    -------
    Filter : :class:`GFilter`
        The returned object described by the following attributes
        
        =============== ==================== ==================================
        Attribute       Value                Description
        =============== ==================== ==================================
        Par['Type']     'Vertical Band Stop' String defining the filter type as
                                             Vertical Band stop
        --------------- -------------------- ----------------------------------
        Par['Linear']   True                 Type of filter
        --------------- -------------------- ----------------------------------
        Par['Dim']      Dim                  Two element (x, y) tuple 
        --------------- -------------------- ----------------------------------
        Par['Center']   Center               Int column on which the filter is 
                                             centered
        --------------- -------------------- ----------------------------------
        Par['Width']    Width                Int for the window width
        --------------- -------------------- ----------------------------------
        Par['Name']     Window               Filter window name
        --------------- -------------------- ----------------------------------
        Par['Shape']    Shape                optional, only found with some
                                             windows
        --------------- -------------------- ----------------------------------
        function        function             The function used to construct the
                                             filter
        =============== ==================== ==================================
        
    See Also
    --------
    build2DVBS : builds a 2D vertical band stop filter matrix.
   
    """
    filt = GFilter(Par={'Type': 'Vertical Band Stop',
                        'Linear': True,
                        'Dim': Dim,
                        'Center': Center,
                        'Width': Width})

    if isinstance(Window, str):
        filt.params['Name'] = Window
    else:
        filt.params['Name'] = Window[0]
        filt.params['Shape'] = Window[1]

    filt.function = lambda x: x*build2DVBS(Window, Dim, Center, Width)
    return filt


def build2DHBP(Window, Dim, Center, Width):
    """
    Constructs a 2D linear bandpass filter in the horizontal direction.
        
    A filter with profile defined by Window is built, with the final size being
    Dim. Zeros are added before and after the window to position it correctly.
    The window position (Center) must be specified, as well as it's width.
    
    Parameters
    ----------
    Window : string
        Name of the function to be used. See the scipy.signal documentation for
        descriptions of the available windows.
        
    Dim : tuple
        Final size of the filter in (x, y) format.
        
    Center : int
        Column on which the filter will be centered
        
    Width : int, optional
        Sets the width of the filter in pixels. Defaults to 3 pixels

    Returns
    -------
    Window : 2D array
        The filter is returned as a 2D array of floats.
        
    See Also
    --------
    makeHBPF : builds a 2D horizontal band pass filter function and returns a
    :class:`GFilter` object.

    """
    return build2DVBP(Window, Dim[::-1], Center, Width).T


def makeHBPF(Window, Dim, Center=0, Width=3):
    """
    Constructs a Horizontal band pass filter object
        
    A filter with profile defined by Window is built, with the final size being
    Dim. Zeros are added before and after the window to position it correctly.
    The window position (Center) must be specified, as well as it's width.
    
    Parameters
    ----------
    Window : string
        Name of the function to be used. See the scipy.signal documentation for
        descriptions of the available windows.
        
    Dim : tuple
        Final size of the filter in (x, y) format.
        
    Center : int
        Column on which the filter will be centered
        
    Width : int, optional
        Sets the width of the filter in pixels. Defaults to 3 pixels

    Returns
    -------
    Filter : :class:`GFilter`
        The returned object described by the following attributes
        
        =============== ====================== ================================
        Attribute       Value                   Description
        =============== ====================== ================================
        Par['Type']     'Horizontal Band Pass' String defining the filter type 
                                               as Horizontal Band pass
        --------------- ---------------------- --------------------------------
        Par['Linear']   True                   Type of filter
        --------------- ---------------------- --------------------------------
        Par['Dim']      Dim                    Two element (x, y) tuple 
        --------------- ---------------------- --------------------------------
        Par['Center']   Center                 Int column on which the filter
                                               is centered
        --------------- ---------------------- --------------------------------
        Par['Width']    Width                  Int for the window width
        --------------- ---------------------- --------------------------------
        Par['Name']     Window                 Filter window name
        --------------- ---------------------- --------------------------------
        Par['Shape']    Shape                  optional, only found with some
                                               windows
        --------------- ---------------------- --------------------------------
        function        function               The function used to construct
                                               the filter
        =============== ====================== ================================
        
    See Also
    --------
    build2DHBP : builds a 2D Horizontal band pass filter matrix.
    
    """
    filt = GFilter(Par={'Type': 'Horizontal Band Pass',
                        'Linear': True,
                        'Dim': Dim,
                        'Center': Center,
                        'Width': Width})

    if isinstance(Window, str):
        filt.params['Name'] = Window
    else:
        filt.params['Name'] = Window[0]
        filt.params['Shape'] = Window[1]

    filt.function = lambda x: x*build2DHBP(Window, Dim, Center, Width)
    return filt


def build2DHBS(Window, Dim, Center, Width):
    """
    Constructs a 2D linear bandstop filter in the horizontal direction.
    
    A filter with profile defined by Window is built, with the final size being
    Dim. Zeros are added before and after the window to position it correctly.
    The window position (Center) must be specified, as well as it's width.
    
    Parameters
    ----------
    Window : string
        Name of the function to be used. See the scipy.signal documentation for
        descriptions of the available windows.
        
    Dim : tuple
        Final size of the filter in (x, y) format.
        
    Center : int
        Column on which the filter will be centered
        
    Width : int, optional
        Sets the width of the filter in pixels. Defaults to 3 pixels

    Returns
    -------
    Window : 2D array
        The filter is returned as a 2D array of floats.
        
    See Also
    --------
    makeVBSF : builds a 2D vertical band stop filter function and returns a
    :class:`GFilter` object.
    
    Notes
    -----
    The band stop filter is built by subtracting a matrix build using
    :func:`build2DHBP` from a ones matrix of the same dimension.
    
    """
    return np.ones(Dim)-build2DHBP(Window, Dim, Center, Width)


def makeHBSF(Window, Dim, Center=0, Width=3):
    """
    Constructs a Horizontal band stop filter object
            
    A filter with profile defined by Window is built, with the final size being
    Dim. Zeros are added before and after the window to position it correctly.
    The window position (Center) must be specified, as well as it's width.
    
    Parameters
    ----------
    Window : string
        Name of the function to be used. See the scipy.signal documentation for
        descriptions of the available windows.
        
    Dim : tuple
        Final size of the filter in (x, y) format.
        
    Center : int
        Column on which the filter will be centered
        
    Width : int, optional
        Sets the width of the filter in pixels. Defaults to 3 pixels

    Returns
    -------
    Filter : :class:`GFilter`
        The returned object described by the following attributes
        
        =============== ====================== ================================
        Attribute       Value                   Description
        =============== ====================== ================================
        Par['Type']     'Horizontal Band Stop' String defining the filter type 
                                               as Horizontal Band Stop
        --------------- ---------------------- --------------------------------
        Par['Linear']   True                   Type of filter
        --------------- ---------------------- --------------------------------
        Par['Dim']      Dim                    Two element (x, y) tuple 
        --------------- ---------------------- --------------------------------
        Par['Center']   Center                 Int column on which the filter
                                               is centered
        --------------- ---------------------- --------------------------------
        Par['Width']    Width                  Int for the window width
        --------------- ---------------------- --------------------------------
        Par['Name']     Window                 Filter window name
        --------------- ---------------------- --------------------------------
        Par['Shape']    Shape                  optional, only found with some
                                               windows
        --------------- ---------------------- --------------------------------
        function        function               The function used to construct
                                               the filter
        =============== ====================== ================================
        
    See Also
    --------
    build2DHBS : builds a 2D Horizontal band stop filter matrix.
    
    """
    filt = GFilter(Par={'Type': 'Horizontal Band Stop',
                        'Linear': True,
                        'Dim': Dim,
                        'Center': Center,
                        'Width': Width})

    if isinstance(Window, str):
        filt.params['Name'] = Window
    else:
        filt.params['Name'] = Window[0]
        filt.params['Shape'] = Window[1]

    filt.function = lambda x: x*build2DHBS(Window, Dim, Center, Width)
    return filt


def buildNF(Window, Dim, Center, Width=3):
    """
    Constructs a notch centered at some point (Center) with a given Width

    A filter with profile defined by Window is built, with the final size being
    Dim. Zeros are added before and after the window to position it correctly.
    The window position (Center) must be specified, as well as it's width.
    
    Parameters
    ----------
    Window : string
        Name of the function to be used. See the scipy.signal documentation for
        descriptions of the available windows.
        
    Dim : tuple
        Final size of the filter in (x, y) format.
        
    Center : int
        Point on which the filter will be centered
        
    Width : int, optional
        Sets the width of the filter in pixels. Defaults to 3 pixels

    Returns
    -------
    Window : 2D array
        The filter is returned as a 2D array of floats.
        
    See Also
    --------
    makeNF : builds a 2D vertical band stop filter function and returns a
    :class:`GFilter` object.
    
    Notes
    -----
    The notch filter is built using :func:`build2DLP` to construct a low pass
    filter of size Window, then padding with zeros to position the notch as
    desired.
    
    """
    base = build2DLP(Window, (Width, Width), Width, Outer=False, Cont=True)
    return np.ones(Dim)-resizeToMatch(base, Dim, True, Center)


def makeNF(Window, Dim, Center=0, Width=3):
    """
    Constructs a notch filter object

    A filter with profile defined by Window is built, with the final size being
    Dim. Zeros are added before and after the window to position it correctly.
    The window position (Center) must be specified, as well as it's width.
    
    Parameters
    ----------
    Window : string
        Name of the function to be used. See the scipy.signal documentation for
        descriptions of the available windows.
        
    Dim : tuple
        Final size of the filter in (x, y) format.
        
    Center : int
        Column on which the filter will be centered
        
    Width : int, optional
        Sets the width of the filter in pixels. Defaults to 3 pixels

    Returns
    -------
    Filter : :class:`GFilter`
        The returned object described by the following attributes
        
        =============== ====================== ================================
        Attribute       Value                   Description
        =============== ====================== ================================
        Par['Type']     'Notch'                String defining the filter type 
                                               as Notch
        --------------- ---------------------- --------------------------------
        Par['Linear']   True                   Type of filter
        --------------- ---------------------- --------------------------------
        Par['Dim']      Dim                    Two element (x, y) tuple 
        --------------- ---------------------- --------------------------------
        Par['Center']   Center                 Int column on which the filter
                                               is centered
        --------------- ---------------------- --------------------------------
        Par['Width']    Width                  Int for the window width
        --------------- ---------------------- --------------------------------
        Par['Name']     Window                 Filter window name
        --------------- ---------------------- --------------------------------
        Par['Shape']    Shape                  optional, only found with some
                                               windows
        --------------- ---------------------- --------------------------------
        function        function               The function used to construct
                                               the filter
        =============== ====================== ================================
        
    See Also
    --------
    build2NF : builds a 2D Notch filter matrix.
    
    """
    filt = GFilter(Par={'Type': 'Notch',
                        'Linear': True,
                        'Dim': Dim,
                        'Center': Center,
                        'Width': Width})

    if isinstance(Window, str):
        filt.params['Name'] = Window
    else:
        filt.params['Name'] = Window[0]
        filt.params['Shape'] = Window[1]

    filt.function = lambda x: x*buildNF(Window, Dim, Center, Width)
    return filt


def resizeToMatch(Window, Size, Cont=False, Center=None):
    """
    Resizes the 2D filter w to have the same dimensions as size. The constant
    contour is selected as being constant in the pixels (cr=True) or constant
    in the percentage of the final dimension (cr=false). Returns the resized
    filter.

    Parameters
    ----------
    Window : 2D array
        The array that will be resized
        
    Size : tuple
        Final size of the filter in (x, y) format.
        
    Cont : Bool, optional
        Selects between making the diameter a constant number of pixels, 
        or a constant percentage of the final image size. Defaults to False
        which is a constant percentage.
        
    Center : int, optional
        Sets the center point of the filter window in the resized matrix. Can
        be disabled by passing None (the default) so that the window is
        centered in the final array.

    Returns
    -------
    Window: 2D array
        The resized filter array.
        
    """
    if Cont:
        #Down sample the filter to have the correct ratio, if the contour is
        #constant in number of pixels
        Window = signal.resample(Window, num=(int(np.shape(Window)[0] *
                                          float(Size[0])/Size[1])), axis=0)

    dZero = Size[0]-np.shape(Window)[0]
    dOne = Size[1]-np.shape(Window)[1]

    #pad or section the array to match the image size
    #do for the first axis
    if dZero > 0:
        #if the filter is too small, pad with zeros and rotate it to the center
        Window = np.concatenate((Window,
                                 np.zeros([dZero,np.shape(Window)[1]])),
                                axis=0)
        if Center is not None:
            Window = np.roll(Window, Center[0], 0)
        else:
            Window = np.roll(Window, int(np.floor(dZero/2.0)), 0)
    elif dZero < 0:
        #if the fitler is too big, take the center section
        Window = Window[-int(np.ceil(dZero/2.0)):int(np.floor(dZero/2.0)), :]

    #do for the second axis
    if dOne > 0:
        #if the filter is too small, pad with zeros and rotate it to the center
        Window = np.concatenate((Window, np.zeros([np.shape(Window)[0],
                                                   dOne])), axis=1)
        if Center is not None:
            Window = np.roll(Window, Center[1], 1)
        else:
            Window = np.roll(Window, int(np.floor(dOne/2.0)), 1)
    elif dOne < 0:
        #if the fitler is too big, take the center section
        Window = Window[:, -int(np.ceil(dOne/2.0)):int(np.floor(dOne/2.0))]
    return Window


def computeDCOffset(Kspace, Size=5):
    """
    Computes the average value of the data in the four corners.
    
    Parameters
    ----------
    Size : int, optional
        The number of pixels averaged over in order to calculate the DC offset
        of the data. Defaults to 5 pixels in each corner
    
    Returns
    -------
    Kspace : 2D array
        The frequency domain data, with the DC offset subtracted from it.
    """
    corner1 = np.mean(Kspace[:Size, :Size])
    corner2 = np.mean(Kspace[:-Size, :Size])
    corner3 = np.mean(Kspace[:-Size, :-Size])
    corner4 = np.mean(Kspace[:Size, :-Size])
    return Kspace-((corner1+corner2+corner3+corner4)/4)


def makeDCO(Size=10):
    """
    Creates a DC Offset correction filter object
    
    Parameters
    ----------
    Size : int, optional
        The number of pixels averaged over in order to calculate the DC offset
        of the data. Defaults to 10 pixels in each corner

    Returns
    -------
    Filter : :class:`GFilter`
        The returned object described by the following attributes
        
        =============== ====================== ================================
        Attribute       Value                   Description
        =============== ====================== ================================
        Par['Name']     'DC Offset'            Name of the filter type
        --------------- ---------------------- --------------------------------       
        Par['Type']     'DC Offset'            String defining the filter type 
                                               as a DC offset correction
        --------------- ---------------------- --------------------------------
        Par['Linear']   False                  Type of filter
        --------------- ---------------------- --------------------------------
        Par['Size']     Size                   Number of pixels to average over
        --------------- ---------------------- --------------------------------
        function        function               The offset correction function
        =============== ====================== ================================
        
    See Also
    --------
    computeDCOffset : Compute and apply a DC offset correction on an image.
    
    """
    filt = GFilter(Par={'Name': 'DC Offset',
                        'Type': 'DC Offset',
                        'Linear': False,
                        'Size': Size})

    filt.function = lambda x: computeDCOffset(x, Size)
    return filt


def mask(Image, Threshold=0.1):
    """
    Builds a binary mask for the supplied image.
    
    Parameters
    ----------
    Image : 2D array
        The image that a mask is to be generated for.
    
    Threshold : float
        The cut-off value for including a pixel in the masked image.
        
    Returns
    -------
    imageMask : 2D array
        A 2D binary array with ones in pixels above the Threshold and zeros
        elsewhere.
        
    """
    imageMask = np.copy(Image)
    imageMask[np.abs(imageMask)<Threshold] = 0
    imageMask[np.abs(imageMask)>0] = 1
    imageMask = np.abs(imageMask)
    return imageMask


def makeLogTransform():
    """
    Constructs a log transform filter object defined by log10(1+i(x, y))
    
    Parameters
    ----------
 
    Returns
    -------
    Filter : :class:`GFilter`
        The returned object described by the following attributes
        
        =============== ====================== ================================
        Attribute       Value                   Description
        =============== ====================== ================================
        Par['Type']     'LogTransform'         String defining the filter type 
                                               as a log transform
        --------------- ---------------------- --------------------------------
        Par['Linear']   False                  Type of filter
        --------------- ---------------------- --------------------------------
        function        function               The gamma function
        =============== ====================== ================================
        
    See Also
    --------
    makeGammaTransform : Gamma intensity transform filter object.
    
    """
    filt = GFilter(Par={'Type': 'Log Transform',
                        'Linear': False})

    filt.function = lambda x: np.log10(1.0+x)
    return filt


def makeGammaTransform(Gamma=1):
    """
    Constructs a gamma transform filter object defined by i(x, y)**(Gamma)
    
    Parameters
    ----------
    Gamma : Float, optional
        The power that the image intensity should be raised to. It will default
        to one if not otherwise supplied.        

    Returns
    -------
    Filter : :class:`GFilter`
        The returned object described by the following attributes
        
        =============== ====================== ================================
        Attribute       Value                   Description
        =============== ====================== ================================
        Par['Type']     'Gamma Transform'      String defining the filter type 
                                               as a gamma transform
        --------------- ---------------------- --------------------------------
        Par['Linear']   False                  Type of filter
        --------------- ---------------------- --------------------------------
        Par['Gamma']    Gamma                  Value of exponential
        --------------- ---------------------- --------------------------------
        function        function               The gamma function
        =============== ====================== ================================
        
    See Also
    --------
    makeLogTransform : Log intensity transform filter object.
    
    """
    filt = GFilter(Par={'Type': 'Gamma Transform',
                        'Linear': False,
                        'Gamma': Gamma})

    filt.function = lambda x: x**Gamma
    return filt


class GFilter(object):
    """
    Object to hold an arbitrary filter
    
    Parameters
    ----------
    Par : Dictionary
        Hold the description of the filter
    
    """
    def __init__(self, Par={}):
        self.function = lambda x: x
        self.params = Par


def applyStack(Data, Stack):
    """
    Returns image filtered by the stack of :class:`GFilter` objects
    
    Filter objects in the `Stack` will be sequentially applied to the image 
    supplied as `Data`. The filter is applied by calling filt.function
    on the data. Filters can be linear or non-linear, and the stack order is
    preserved.
    
    Parameters
    ----------
    Data : 2D array floats
        The image to be filtered as a numpy array.
        
    Stack : 1D array :class:`GFilter`\s
        containing the filter objects to be applied.
        
    See Also
    --------
    :class:`GFilter` : the filter object used
    
    """
    filtered = np.copy(Data)
    for filt in Stack:
        filtered = filt.function(filtered)
    return filtered
