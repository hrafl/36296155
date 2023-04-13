import json
from src.services import data_importing_service
from src.services.log_service import convert_exception_to_dict

def main():
    try:
        data_importing_service.execute()
    except Exception as e:
        with open("erro.json", 'w') as arquivo:
            exception_dict = convert_exception_to_dict(e)
            json.dump(exception_dict, arquivo)

main()