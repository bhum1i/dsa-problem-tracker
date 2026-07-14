from fastapi import FastAPI
app = FastAPI()

from schemas import ProblemCreate, ProblemResponse, ProblemUpdate, StatsResponse
from typing import Annotated
from fastapi import Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session
import models
from database import Base, engine, get_db
from fastapi.templating import Jinja2Templates

Base.metadata.create_all(bind=engine)

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException
from fastapi import Request



@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/problems"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )

@app.exception_handler(HTTPException)
def general_HTTP_exception_handler(request: Request, exception: HTTPException):
    message = (exception.detail if exception.detail else "an error occurred, try later")
    if request.url.path.startswith("/problems"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )
@app.get("/problems/stats", response_model=StatsResponse)  
def problem_stats(db:Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Problem))
    problems = result.scalars().all()
    total = len(problems)
    solved = len([problem for problem in problems if problem.status=="Solved"])
    unsolved = len([problem for problem in problems if problem.status=="Unsolved"]) 
    revise = len([problem for problem in problems if problem.status=="Revise"])
    by_topic = {}
    for problem in problems:
        if problem.topic not in by_topic:
            by_topic[problem.topic] = 1
        else:
            by_topic[problem.topic] += 1
    
    return StatsResponse(
        total=total,
        solved=solved,
        unsolved=unsolved,
        revise=revise,
        by_topic=by_topic
    )

@app.get("/problems", response_model=list[ProblemResponse])
def get_problems(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Problem))
    problems = result.scalars().all()
    return problems

@app.get("/problems/{id}", response_model=ProblemResponse)
def get_problem(id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Problem).where(models.Problem.id==id))
    problem = result.scalars().first()
    if problem:
        return problem
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="problem not found")

@app.get("/problems/topic/{topic}", response_model=list[ProblemResponse])
def get_topic_problem(topic: str, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Problem).where(models.Problem.topic==topic))
    problems = result.scalars().all()
    return problems

@app.get("/problems/difficulty/{difficulty}", response_model=list[ProblemResponse])
def get_difficulty_problem(difficulty: str, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Problem).where(models.Problem.difficulty==difficulty))
    problems = result.scalars().all()
    return problems

@app.get("/problems/status/{status}", response_model=list[ProblemResponse])
def get_status_problem(status: str, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Problem).where(models.Problem.status==status))
    problems = result.scalars().all()
    return problems

@app.post("/problems", response_model=ProblemResponse, status_code=status.HTTP_201_CREATED)
def post_problem(problem: ProblemCreate, db: Annotated[Session, Depends(get_db)]):
    new_problem = models.Problem(
        title = problem.title,
        topic = problem.topic,
        difficulty = problem.difficulty,
        status = problem.status,
        notes = problem.notes,
        leetcode_question_number = problem.leetcode_question_number
    )
    db.add(new_problem)
    db.commit()
    db.refresh(new_problem)
    return new_problem



@app.patch("/problems/{id}", response_model=ProblemResponse)
def update_problem(id: int, post_data: ProblemUpdate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Problem).where(models.Problem.id==id))
    problem = result.scalars().first()
    if not problem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="problem not found")

    update_data = post_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(problem, field, value)

    db.commit()
    db.refresh(problem)
    return problem

@app.delete("/problems/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_problem(id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Problem).where(models.Problem.id==id))
    problem = result.scalars().first()
    if not problem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="problem not found")
    db.delete(problem)
    db.commit()


    
    
    
