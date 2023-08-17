import pytest

from app.calc import Calculator
class TestCalc:
    def setup(self):
        self.calc = Calculator

    def test_multiply_success(self):
        assert self.calc.multiply(self,2, 4) == 8

    def test_division_success(self):
        assert self.calc.division(self, 8, 2) == 4

    def test_subtraction_success(self):
        assert self.calc.subtraction(self, 8, 4) == 4

    def test_adding_success(self):
        assert self.calc.adding(self, 4, 4) == 8