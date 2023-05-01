import enum


class ProductType(str, enum.Enum):
    PERISHABLE = 'PERISHABLE',
    NONPERISHABLE = 'NONPERISHABLE',


__all__ = ["ProductType"]
