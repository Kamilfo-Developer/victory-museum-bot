from bot.configs.config import MONGO_DB_URI_FOR_CLIENT, MONGO_DB_NAME, MONGO_DB_PHOTO_COLLECTION_NAME
from bot.utils.utils import check_photo_type
import pymongo


class ExhibitPhoto:
    ALLOWED_TYPES_FOR_VALUES = [str, dict, list]
    
    def __init__(self, id: str | int):
        
        try:
            self.__id = int(id)
        except ValueError:
            raise ValueError("id parameter should be an integer or a convertable to integer string")
        
        data = ExhibitPhoto.__get_photo_data(id)

        if not data:
            ExhibitPhoto.__add_photo_data(id=id)
            
            data = {}
        
        self.__name = data.get("name")
        self.__description = data.get("description")
        self.__file_name = data.get("file_name")
        self.__telegram_file_id = data.get("telegram_file_id")
    
#region properties_decorators    
    @property
    def id(self):
        return self.__id        
        
    @id.setter
    def id(self, value):
        raise AttributeError("id property is not supposed to be changed")
    
    @id.deleter
    def id(self):
        raise AttributeError("id property is not supposed to be deleted")
    
    
    
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value):
        check_photo_type(value, ExhibitPhoto.ALLOWED_TYPES_FOR_VALUES)
        
        ExhibitPhoto.__update_photo_data(self.__id, {"name": value})
        self.__name = value

    @name.deleter
    def name(self):
        ExhibitPhoto.__update_photo_data(self.__id, {"name": None})
        self.__name = None    


    
    @property
    def description(self):
        return self.__description
    
    @description.setter
    def description(self, value):
        check_photo_type(value, ExhibitPhoto.ALLOWED_TYPES_FOR_VALUES)
        
        ExhibitPhoto.__update_photo_data(self.__id, {"description": value})
        self.__description = value
       
    @description.deleter
    def description(self):
        ExhibitPhoto.__update_photo_data(self.__id, {"description": None})
        self.__description = None            
     
        
        
    @property
    def file_name(self):
        return self.__file_name
    
    @file_name.setter
    def file_name(self, value):
        check_photo_type(value, ExhibitPhoto.ALLOWED_TYPES_FOR_VALUES)
        ExhibitPhoto.__update_photo_data(self.__id, {"file_name": value})
        self.__file_name = value
        
    @file_name.deleter
    def file_name(self):
        ExhibitPhoto.__update_photo_data(self.__id, {"file_name": None})
        self.__file_name = None
        
        
        
    @property
    def telegram_file_id(self):
        return self.__telegram_file_id
       
    @telegram_file_id.setter
    def telegram_file_id(self, value):
        ExhibitPhoto.__update_photo_data(self.__id, {"telegram_file_id": value})
        self.__telegram_file_id = value
       
    @telegram_file_id.deleter
    def telegram_file_id(self):
        ExhibitPhoto.__update_photo_data(self.__id, {"telegram_file_id": None})
        self.__telegram_file_id = None
#endregion
        
    def __get_photo_data(id: str) -> dict:
        """Returnes a dictionary with photo data

        Returns:
            dict: a dictionary with photo data
        """
        
        client = pymongo.MongoClient(MONGO_DB_URI_FOR_CLIENT)
        
        db = client[MONGO_DB_NAME]
        
        collection = db[MONGO_DB_PHOTO_COLLECTION_NAME]
        
        data = collection.find_one({"_id": id})
        
        return data
    
    
    
    def __add_photo_data(id: int, data: dict = {}) -> None:
        
        client = pymongo.MongoClient(MONGO_DB_URI_FOR_CLIENT)
        
        db = client[MONGO_DB_NAME]
        
        collection = db[MONGO_DB_PHOTO_COLLECTION_NAME]
        
        current_data = collection.find_one({"_id": id})
        
        if current_data:
            raise ValueError("Photo data with this id already exists")
            
        data["_id"] = id
        
        collection.insert_one(data)
                    
        
        
            
    def __update_photo_data(id: int, data: dict) -> None:
        """Changes the description and name of the photo in Mongo Database

        Args:
            id (int): id of data
            data (dict): new data, represented as a dictionary
        """
        
        client = pymongo.MongoClient(MONGO_DB_URI_FOR_CLIENT)
        
        db = client[MONGO_DB_NAME]
        
        collection = db[MONGO_DB_PHOTO_COLLECTION_NAME]
        
        current_data = collection.find_one({"_id": id})

        if not current_data:
            raise ValueError("No photo data with this id exists")
        
        collection.update_one({"_id": id}, {
            "$set": data
        })
        