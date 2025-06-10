from pydantic import BaseModel
from typing import List 


class RecipeOutput(BaseModel):
    title: str
    ingredients: List[str]
    instructions: List[str]

