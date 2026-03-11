from fastapi import APIRouter,Depends,UploadFile,status
from fastapi.responses import JSONResponse
import os 
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController
from models import ResponseSignal
import aiofiles
import logging

logger = logging.getLogger('uvicorn.error')

data_router  = APIRouter(
    prefix="/api/v1/data",
   tags=["api_v1","data"],
   )


@data_router.post("/upload/{project_id}")
async def upload_data(project_id:str, file:UploadFile, app_setting:Settings = Depends(get_settings)):
    
    data_controller = DataController()
    #1. validate file type and size
    is_valid, response_signal = data_controller.validate_file(file=file)

    if not is_valid:
         return JSONResponse(
              status_code=status.HTTP_400_BAD_REQUEST,
              content={
                    "signal":response_signal
              }
         )
    #2. get unique filepath
    file_path, file_id = data_controller.generate_unique_filepath(
        orig_filname=file.filename,
        project_id=project_id
    )

    #3. write chunck in the file path
    try:
        async with aiofiles.open(file_path,"wb") as f:
            while chunk := await file.read(app_setting.CHUNK_FILE_SIZE):
                await f.write(chunk)

    except Exception as e:
            
            logger.error(f"Error while uploading file: {e}")

            return JSONResponse(
              status_code=status.HTTP_400_BAD_REQUEST,
              content={
                    "signal":ResponseSignal.FILE_UPLOAD_FAIL.value
              }
         )
        
    return JSONResponse(
              content={
                    "signal":ResponseSignal.FILE_UPLOAD_SUCCESS.value,
                    "file_id":file_id
              }
         )

