from pydantic import Field
import pydantic


class BaseBody(pydantic.BaseModel):
    hash: str = Field(..., example='14fb5d016557165019abaac200785048',
                      description="valor md5 hexdigest de string resultante")
