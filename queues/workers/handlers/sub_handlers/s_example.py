from pydantic import BaseModel


class ExampleData(BaseModel):
    userId: int
    id: int
    title: str
    body: str
