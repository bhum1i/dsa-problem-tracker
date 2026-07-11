from pydantic import BaseModel, ConfigDict, Field
from enum import Enum


class Difficulty(str, Enum):
    easy = "Easy"
    medium = "Medium"
    hard = "Hard"

class Status(str, Enum):
    unsolved = "Unsolved"
    solved = "Solved"
    revise = "Revise"


class ProblemBase(BaseModel):
    title: str = Field(min_length=1)
    topic: str = Field(min_length=1, max_length=50)


class ProblemCreate(ProblemBase):
    difficulty: Difficulty
    status: Status
    notes: str = Field(min_length=1, max_length=300)
    leetcode_question_number: int = Field(gt=0)

class ProblemUpdate(BaseModel):
    title: str|None = Field(min_length=1, default=None)
    topic: str|None = Field(min_length=1, max_length=50, default=None)
    difficulty: Difficulty|None = Field(default=None)
    status: Status|None = Field(default=None)
    notes: str|None = Field(min_length=1, max_length=300, default=None)
    leetcode_question_number: int|None = Field(default=None, gt=0)

class ProblemResponse(ProblemCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int

class StatsResponse(BaseModel):
    total: int
    solved: int
    unsolved: int
    revise: int
    by_topic: dict[str, int]




