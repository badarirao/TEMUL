
import periodictable as pt

'''
Element and radius calibration
'''


def get_and_return_element(element_symbol):
    '''
    From the elemental symbol, e.g., 'H' for Hydrogen, returns Hydrogen as
    a periodictable.core.Element object for further use.

    Parameters
    ----------

    element_symbol : string, default None
        Symbol of an element from the periodic table of elements

    Returns
    -------
    A periodictable.core.Element object

    Examples
    --------
    >>> from temul.element_tools import get_and_return_element
    >>> Moly = get_and_return_element(element_symbol='Mo')
    >>> print(Moly.covalent_radius)
    >>> print(Moly.symbol)
    >>> print(Moly.number)

    '''

    for pt_element in pt.elements:
        if pt_element.symbol == element_symbol:
            chosen_element = pt_element

    return(chosen_element)


def atomic_radii_in_pixels(sampling, element_symbol):
    '''
    Get the atomic radius of an element in pixels, scaled by an image sampling

    Parameters
    ----------
    sampling : float, default None
        sampling of an image in units of nm/pix
    element_symbol : string, default None
        Symbol of an element from the periodic table of elements

    Returns
    -------
    Half the colavent radius of the input element in pixels

    Examples
    --------

    >>> import atomap.api as am
    >>> from temul.element_tools import atomic_radii_in_pixels
    >>> image = am.dummy_data.get_simple_cubic_signal()
    >>> # pretend it is a 5x5 nm image
    >>> image_sampling = 5/len(image.data) # units nm/pix
    >>> radius_pix_Mo = atomic_radii_in_pixels(image_sampling, 'Mo')
    >>> radius_pix_S = atomic_radii_in_pixels(image_sampling, 'S')

    '''

    element = get_and_return_element(element_symbol=element_symbol)

    # mult by 0.5 to get correct distance (google image of covalent radius)
    # divided by 10 to get nm
    radius_nm = (element.covalent_radius*0.5)/10

    radius_pix = radius_nm/sampling

    return(radius_pix)


'''
Assigning Elements and Z height

split_symbol must be a list
splitting an element
'''


def split_and_sort_element(element, split_symbol=['_', '.']):
    '''
    Extracts info from input atomic column element configuration
    Split an element and its count, then sort the element for
    use with other functions.

    Parameters
    ----------

    element : string, default None
        element species and count must be separated by the
        first string in the split_symbol list.
        separate elements must be separated by the second
        string in the split_symbol list.
    split_symbol : list of strings, default ['_', '.']
        The symbols used to split the element into its name
        and count.
        The first string '_' is used to split the name and count
        of the element.
        The second string is used to split different elements in
        an atomic column configuration.

    Returns
    -------
    list with element_split, element_name, element_count, and
    element_atomic_number

    Examples
    --------
    >>> from temul.element_tools import split_and_sort_element
    >>> single_element = split_and_sort_element(element='S_1')
    >>> complex_element = split_and_sort_element(element='O_6.Mo_3.Ti_5')

    '''
    splitting_info = []

    if '.' in element:
        # if len(split_symbol) > 1:

        if split_symbol[1] == '.':

            stacking_element = element.split(split_symbol[1])
            for i in range(0, len(stacking_element)):
                element_split = stacking_element[i].split(split_symbol[0])
                element_name = element_split[0]
                element_count = int(element_split[1])
                element_atomic_number = pt.elements.symbol(
                    element_name).number
                splitting_info.append(
                    [element_split, element_name, element_count,
                     element_atomic_number])
        else:
            raise ValueError(
                "To split a stacked element use: split_symbol=['_', '.']")

    # elif len(split_symbol) == 1:
    elif '.' not in element:
        element_split = element.split(split_symbol[0])
        element_name = element_split[0]
        element_count = int(element_split[1])
        element_atomic_number = pt.elements.symbol(element_name).number
        splitting_info.append(
            [element_split, element_name, element_count,
             element_atomic_number])

    else:
        raise ValueError(
            "You must include a split_symbol. Use '_' to separate element "
            "and count. Use '.' to separate elements in the same xy position")

    return(splitting_info)