from fastapi import APIRouter, HTTPException
from backend.database import trabajadores_collection
from backend.models import Trabajador
from bson import ObjectId
import pandas as pd
import io
from fastapi.responses import StreamingResponse

router = APIRouter()

@router.post("/trabajadores/")
async def agregar_trabajador(trabajador: Trabajador):
    nuevo_trabajador = await trabajadores_collection.insert_one(trabajador.dict())
    return {"id": str(nuevo_trabajador.inserted_id)}

@router.get("/trabajadores/")
async def listar_trabajadores():
    trabajadores = await trabajadores_collection.find().to_list(None)
    for trabajador in trabajadores:
        trabajador["_id"] = str(trabajador["_id"])
    return trabajadores

@router.put("/trabajadores/{trabajador_id}")
async def actualizar_trabajador(trabajador_id: str, trabajador: Trabajador):
    resultado = await trabajadores_collection.update_one(
        {"_id": ObjectId(trabajador_id)},
        {"$set": trabajador.dict(exclude_unset=True)}
    )
    if resultado.modified_count == 0:
        raise HTTPException(status_code=404, detail="Trabajador no encontrado")
    return {"mensaje": "Trabajador actualizado correctamente"}

@router.delete("/trabajadores/{trabajador_id}")
async def eliminar_trabajador(trabajador_id: str):
    resultado = await trabajadores_collection.delete_one({"_id": ObjectId(trabajador_id)})
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Trabajador no encontrado")
    return {"mensaje": "Trabajador eliminado correctamente"}

@router.get("/trabajadores/exportar/")
async def exportar_excel():
    trabajadores = await trabajadores_collection.find().to_list(None)
    df = pd.DataFrame(trabajadores)
    if "_id" in df:
        df.drop(columns=["_id"], inplace=True)
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Trabajadores")
    
    output.seek(0)
    return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                             headers={"Content-Disposition": "attachment; filename=trabajadores.xlsx"})
