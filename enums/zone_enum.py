import enum


class ZoneEnum(str, enum.Enum):
    ZONA_CENTRO = 'ZONA CENTRO',
    ZONA_ESTE = 'ZONA ESTE',
    ZONA_OESTE = 'ZONA OESTE',
    ZONA_NORTE = 'ZONA NORTE',
    ZONA_SUR = 'ZONA SUR ',


__all__ = ['ZoneEnum']
