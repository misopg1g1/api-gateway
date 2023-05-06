import enum


class IdentificationTypeEnum(str, enum.Enum):
    PASAPORTE = 'PASAPORTE',
    NIT = 'NIT',
    DNI = 'DNI',
    RUT = 'RUT',
    CEDULA_DE_EXTRANJERIA = 'CEDULA DE EXTRANJERIA',


__all__ = ["IdentificationTypeEnum"]
