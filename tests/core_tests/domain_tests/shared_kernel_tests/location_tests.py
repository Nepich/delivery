import pytest

from core.domain.shared_kernel.location import Location


class LocationShould:
    
    @pytest.mark.parametrize(
        "x,y",
        [
            (1, 1),
            (5, 10)
        ]
    )
    def be_initialized_correct(self, x: int, y: int):
        location = Location(x=x,y=y)
        assert isinstance(location, Location)
        assert location.x == x
        assert location.y == y

    @pytest.mark.parametrize(
        "x,y,error",
        [
            (1.1, 1, TypeError),
            (5, 11, ValueError),
            (-1, 7, ValueError)
        ]
    )
    def not_be_initialized(self, x: int, y: int, error: Exception):
        with pytest.raises(error):
            Location(x=x,y=y)

    @pytest.mark.parametrize(
        "x1,y1,x2,y2",
        [
            (1, 1, 1, 1),
            (5, 7, 5, 7)
        ]
    )
    def be_equal(self, x1: int, y1: int, x2: int, y2: int):
        assert Location(x=x1, y=y1) == Location(x=x2, y=y2)
        
    @pytest.mark.parametrize(
        "x1,y1,x2,y2",
        [
            (1, 1, 2, 1),
            (5, 7, 7, 5)
        ]
    )
    def not_be_equal(self, x1: int, y1: int, x2: int, y2: int):
        assert Location(x=x1, y=y1) != Location(x=x2, y=y2)
        
    def be_random(self):
        location = Location.random()
        assert isinstance(location, Location)
        assert 1 <= location.x <= 10
        assert 1 <= location.y <= 10