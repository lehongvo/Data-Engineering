"""
FastAPI server for the Employee Management System
"""

from fastapi import FastAPI, HTTPException, Query, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from main import Department, Employee, get_db_session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Employee Management API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models for request/response
class DepartmentBase(BaseModel):
    name: str


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentResponse(DepartmentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    employee_count: int

    class Config:
        from_attributes = True


class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    department_id: int


class EmployeeCreate(EmployeeBase):
    pass


class DepartmentInfo(BaseModel):
    id: int
    name: str


class EmployeeResponse(EmployeeBase):
    id: int
    department: DepartmentInfo
    hire_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SampleDataRequest(BaseModel):
    num_departments: int = 5
    num_employees: int = 20


class DepartmentStats(BaseModel):
    name: str
    employee_count: int


class StatsResponse(BaseModel):
    total_departments: int
    total_employees: int
    departments: List[DepartmentStats]


# Dependency
def get_db():
    db = get_db_session()
    try:
        yield db
    finally:
        db.close()


# Department endpoints
@app.get("/api/departments", response_model=List[DepartmentResponse])
async def list_departments(db: Session = Depends(get_db)):
    departments = db.query(Department).all()
    return [
        DepartmentResponse(
            id=dept.id,
            name=dept.name,
            created_at=dept.created_at,
            updated_at=dept.updated_at,
            employee_count=len(dept.employees),
        )
        for dept in departments
    ]


@app.get("/api/departments/{dept_id}", response_model=DepartmentResponse)
async def get_department(dept_id: int, db: Session = Depends(get_db)):
    dept = db.query(Department).filter(Department.id == dept_id).first()
    if not dept:
        raise HTTPException(
            status_code=404, detail=f"Department with ID {dept_id} not found"
        )
    return DepartmentResponse(
        id=dept.id,
        name=dept.name,
        created_at=dept.created_at,
        updated_at=dept.updated_at,
        employee_count=len(dept.employees),
    )


@app.post("/api/departments", response_model=DepartmentResponse)
async def create_department(dept: DepartmentCreate, db: Session = Depends(get_db)):
    try:
        new_dept = Department(name=dept.name)
        db.add(new_dept)
        db.commit()
        db.refresh(new_dept)
        return DepartmentResponse(
            id=new_dept.id,
            name=new_dept.name,
            created_at=new_dept.created_at,
            updated_at=new_dept.updated_at,
            employee_count=0,
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/api/departments/{dept_id}", response_model=DepartmentResponse)
async def update_department(
    dept_id: int, dept: DepartmentCreate, db: Session = Depends(get_db)
):
    db_dept = db.query(Department).filter(Department.id == dept_id).first()
    if not db_dept:
        raise HTTPException(
            status_code=404, detail=f"Department with ID {dept_id} not found"
        )

    try:
        db_dept.name = dept.name
        db.commit()
        db.refresh(db_dept)
        return DepartmentResponse(
            id=db_dept.id,
            name=db_dept.name,
            created_at=db_dept.created_at,
            updated_at=db_dept.updated_at,
            employee_count=len(db_dept.employees),
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/api/departments/{dept_id}")
async def delete_department(dept_id: int, db: Session = Depends(get_db)):
    dept = db.query(Department).filter(Department.id == dept_id).first()
    if not dept:
        raise HTTPException(
            status_code=404, detail=f"Department with ID {dept_id} not found"
        )

    try:
        db.delete(dept)
        db.commit()
        return {"message": f"Department {dept_id} deleted successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# Employee endpoints
@app.get("/api/employees", response_model=List[EmployeeResponse])
async def list_employees(
    department: Optional[str] = Query(None, description="Filter by department name"),
    db: Session = Depends(get_db),
):
    query = db.query(Employee)
    if department:
        query = query.join(Department).filter(Department.name == department)

    employees = query.all()
    return [
        EmployeeResponse(
            id=emp.id,
            first_name=emp.first_name,
            last_name=emp.last_name,
            email=emp.email,
            department_id=emp.department_id,
            department=DepartmentInfo(id=emp.department.id, name=emp.department.name),
            hire_date=emp.hire_date,
            created_at=emp.created_at,
            updated_at=emp.updated_at,
        )
        for emp in employees
    ]


@app.get("/api/employees/{emp_id}", response_model=EmployeeResponse)
async def get_employee(emp_id: int, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if not emp:
        raise HTTPException(
            status_code=404, detail=f"Employee with ID {emp_id} not found"
        )
    return EmployeeResponse(
        id=emp.id,
        first_name=emp.first_name,
        last_name=emp.last_name,
        email=emp.email,
        department_id=emp.department_id,
        department=DepartmentInfo(id=emp.department.id, name=emp.department.name),
        hire_date=emp.hire_date,
        created_at=emp.created_at,
        updated_at=emp.updated_at,
    )


@app.post("/api/employees", response_model=EmployeeResponse)
async def create_employee(emp: EmployeeCreate, db: Session = Depends(get_db)):
    # Check if department exists
    dept = db.query(Department).filter(Department.id == emp.department_id).first()
    if not dept:
        raise HTTPException(
            status_code=404, detail=f"Department with ID {emp.department_id} not found"
        )

    try:
        new_emp = Employee(
            first_name=emp.first_name,
            last_name=emp.last_name,
            email=emp.email,
            department_id=emp.department_id,
        )
        db.add(new_emp)
        db.commit()
        db.refresh(new_emp)
        return EmployeeResponse(
            id=new_emp.id,
            first_name=new_emp.first_name,
            last_name=new_emp.last_name,
            email=new_emp.email,
            department_id=new_emp.department_id,
            department=DepartmentInfo(id=dept.id, name=dept.name),
            hire_date=new_emp.hire_date,
            created_at=new_emp.created_at,
            updated_at=new_emp.updated_at,
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/api/employees/{emp_id}", response_model=EmployeeResponse)
async def update_employee(
    emp_id: int, emp: EmployeeCreate, db: Session = Depends(get_db)
):
    # Check if employee exists
    db_emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if not db_emp:
        raise HTTPException(
            status_code=404, detail=f"Employee with ID {emp_id} not found"
        )

    # Check if department exists
    dept = db.query(Department).filter(Department.id == emp.department_id).first()
    if not dept:
        raise HTTPException(
            status_code=404, detail=f"Department with ID {emp.department_id} not found"
        )

    try:
        db_emp.first_name = emp.first_name
        db_emp.last_name = emp.last_name
        db_emp.email = emp.email
        db_emp.department_id = emp.department_id

        db.commit()
        db.refresh(db_emp)
        return EmployeeResponse(
            id=db_emp.id,
            first_name=db_emp.first_name,
            last_name=db_emp.last_name,
            email=db_emp.email,
            department_id=db_emp.department_id,
            department=DepartmentInfo(id=dept.id, name=dept.name),
            hire_date=db_emp.hire_date,
            created_at=db_emp.created_at,
            updated_at=db_emp.updated_at,
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/api/employees/{emp_id}")
async def delete_employee(emp_id: int, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if not emp:
        raise HTTPException(
            status_code=404, detail=f"Employee with ID {emp_id} not found"
        )

    try:
        db.delete(emp)
        db.commit()
        return {"message": f"Employee {emp_id} deleted successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# Other endpoints
@app.post("/api/generate-sample-data")
async def generate_sample_data(
    request: SampleDataRequest, db: Session = Depends(get_db)
):
    from main import generate_sample_data

    try:
        generate_sample_data(request.num_departments, request.num_employees)
        return {"message": "Sample data generated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats", response_model=StatsResponse)
async def get_stats(db: Session = Depends(get_db)):
    departments = db.query(Department).all()
    total_employees = db.query(Employee).count()

    dept_stats = [
        DepartmentStats(name=dept.name, employee_count=len(dept.employees))
        for dept in departments
    ]

    return StatsResponse(
        total_departments=len(departments),
        total_employees=total_employees,
        departments=dept_stats,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
