from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from models import ResponseSignal
import re
import os


class DataController(BaseController):

    def __init__(self):
        super().__init__()
        self.size_scale =  1048576

    def validate_file(self, file:UploadFile):

        
        if file.content_type not in self.app_setting.ALLOWED_FILE_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        
        if file.size >  self.app_setting.MAX_FILE_SIZE_MB * self.size_scale: # from MB To Binary
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value
        
        return True, ResponseSignal.FILE_VALIDATED_SUCCCESS.value
    

    
    def generate_unique_filepath(self,project_id:int,orig_filname:str):

        project_Path = ProjectController().get_project_dir(project_id)

        random_key = self.generate_random_string()

        clean_file_name = self.get_clean_file_name(orig_filname)

        new_file_path = os.path.join(project_Path,
                                     random_key + "_" + clean_file_name
                                     )
        
        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path = os.path.join(
                project_Path,
                random_key + "_" + clean_file_name
                )

        return new_file_path, random_key + "_" + clean_file_name



    def get_clean_file_name(self, orig_file_name: str):

        # replace spaces with underscore
        cleaned_file_name = orig_file_name.strip().replace(" ", "_")

        # remove any special characters except underscore and dot
        cleaned_file_name = re.sub(r'[^\w.]', '', cleaned_file_name)

        return cleaned_file_name
