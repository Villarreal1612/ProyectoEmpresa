from pydantic import BaseModel
from typing import Optional

class Trabajador(BaseModel):
    nombre: str
    edad: int
    puesto: str
    salario: float
    id: Optional[str] = None  # ID autogenerado por MongoDB
