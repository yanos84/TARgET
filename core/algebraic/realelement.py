from .intelement import Int_element

class real_Element(Int_element):
    """
    Represents a real number element in the semiring of real numbers.
    This class extends the Int_element class to handle real numbers, providing methods for setting and getting the value of the real number element, as well as overriding the addition operator to allow for addition of"
    """
    def __init__(self):
        super().__init__()