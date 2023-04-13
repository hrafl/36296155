from datetime import datetime

def convert_exception_to_dict(e: Exception) -> dict:
    exception_dict = {
        "type": type(e).__name__,
        "args": e.args,
        "message": str(e)
    }
    
    return exception_dict