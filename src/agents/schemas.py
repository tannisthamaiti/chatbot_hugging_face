from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel




##########################################
# API schemas
##########################################


class ChatAgentResponse(BaseModel):
    generated_text: str
    
