from pydantic import BaseModel
from typing import Optional, Literal, List

class AddInput(BaseModel):
    a: int
    b: int

class AddListInput(BaseModel):
    numbers: List[int]

class SubtractInput(BaseModel):
    a: int
    b: int

class DivideInput(BaseModel):
    a: int
    b: int

class MultiplyInput(BaseModel):
    a: int
    b: int

class Output(BaseModel):
    result: int
    error: Optional[str] = None
    explaination: Optional[str] = None
    reasoning: Optional[str] = None
    type: Literal["add", "subtract", "add_list", "divide", "multiply"] = "add"