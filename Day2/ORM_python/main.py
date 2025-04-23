"""
SQLAlchemy ORM Example Application
This module demonstrates the usage of SQLAlchemy ORM with PostgreSQL
"""

import os
import logging
from datetime import datetime
from typing import List, Optional
from dotenv import load_dotenv
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import declarative_base, relationship, Session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from faker import Faker
import typer
from rich.console import Console
from rich.table import Table
from colorama import Fore, Style
import random

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize Typer app and Rich console
app = typer.Typer()
console = Console()
fake = Faker()

# Sample department names
DEPARTMENT_NAMES = [
    "Engineering",
    "Marketing",
    "Sales",
    "Human Resources",
    "Finance",
    "Operations",
    "Research",
    "Customer Support",
    "Legal",
    "Product Management",
]

# Create SQLAlchemy base class
Base = declarative_base()


# Define models
class Department(Base):
    """Department model representing company departments"""

    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    employees = relationship("Employee", back_populates="department")

    def __repr__(self):
        return f"<Department {self.name}>"


class Employee(Base):
    """Employee model representing company employees"""

    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))
    hire_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    department = relationship("Department", back_populates="employees")

    def __repr__(self):
        return f"<Employee {self.first_name} {self.last_name}>"


# Database connection
def get_db_session() -> Session:
    """Create and return a new database session"""
    try:
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL environment variable not set")

        engine = create_engine(database_url)
        SessionLocal = sessionmaker(bind=engine)

        # Create tables if they don't exist
        Base.metadata.create_all(engine)

        return SessionLocal()
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        raise


# CLI Commands
@app.command()
def init_db():
    """Initialize the database and create tables"""
    try:
        session = get_db_session()
        Base.metadata.create_all(session.bind)
        console.print("[green]Database initialized successfully![/green]")
    except Exception as e:
        console.print(f"[red]Error initializing database: {str(e)}[/red]")
    finally:
        session.close()


@app.command()
def create_department(name: str):
    """Create a new department"""
    try:
        session = get_db_session()
        department = Department(name=name)
        session.add(department)
        session.commit()
        console.print(f"[green]Department '{name}' created successfully![/green]")
    except SQLAlchemyError as e:
        session.rollback()
        console.print(f"[red]Error creating department: {str(e)}[/red]")
    finally:
        session.close()


@app.command()
def create_employee(first_name: str, last_name: str, email: str, department_name: str):
    """Create a new employee"""
    try:
        session = get_db_session()

        # Find department
        department = session.query(Department).filter_by(name=department_name).first()
        if not department:
            console.print(f"[red]Department '{department_name}' not found![/red]")
            return

        employee = Employee(
            first_name=first_name,
            last_name=last_name,
            email=email,
            department_id=department.id,
        )
        session.add(employee)
        session.commit()
        console.print(
            f"[green]Employee {first_name} {last_name} created successfully![/green]"
        )
    except SQLAlchemyError as e:
        session.rollback()
        console.print(f"[red]Error creating employee: {str(e)}[/red]")
    finally:
        session.close()


@app.command()
def list_departments():
    """List all departments"""
    try:
        session = get_db_session()
        departments = session.query(Department).all()

        table = Table(title="Departments")
        table.add_column("ID", justify="right", style="cyan")
        table.add_column("Name", style="magenta")
        table.add_column("Employee Count", justify="right", style="green")

        for dept in departments:
            employee_count = len(dept.employees)
            table.add_row(str(dept.id), dept.name, str(employee_count))

        console.print(table)
    except SQLAlchemyError as e:
        console.print(f"[red]Error listing departments: {str(e)}[/red]")
    finally:
        session.close()


@app.command()
def list_employees(department_name: Optional[str] = None):
    """List all employees, optionally filtered by department"""
    try:
        session = get_db_session()
        query = session.query(Employee)

        if department_name:
            query = query.join(Department).filter(Department.name == department_name)

        employees = query.all()

        table = Table(title="Employees")
        table.add_column("ID", justify="right", style="cyan")
        table.add_column("Name", style="magenta")
        table.add_column("Email", style="blue")
        table.add_column("Department", style="green")

        for emp in employees:
            table.add_row(
                str(emp.id),
                f"{emp.first_name} {emp.last_name}",
                emp.email,
                emp.department.name,
            )

        console.print(table)
    except SQLAlchemyError as e:
        console.print(f"[red]Error listing employees: {str(e)}[/red]")
    finally:
        session.close()


@app.command()
def generate_sample_data(num_departments: int = 10, num_employees: int = 5000):
    """Generate sample data for departments and employees."""
    try:
        session = get_db_session()

        # Clear existing data
        session.query(Employee).delete()
        session.query(Department).delete()
        session.commit()

        # Generate departments
        departments = []
        department_names = [
            "Engineering",
            "Marketing",
            "Sales",
            "Finance",
            "Human Resources",
            "Research",
            "Development",
            "Customer Support",
            "Operations",
            "Legal",
            "Product",
            "Design",
            "Quality Assurance",
            "Business Development",
            "Administration",
        ]

        # If num_departments > len(department_names), add numbered departments
        if int(num_departments) > len(department_names):
            for i in range(len(department_names), int(num_departments)):
                department_names.append(f"Department {i+1}")

        for i in range(int(num_departments)):
            dept = Department(name=department_names[i])
            departments.append(dept)
            session.add(dept)

        session.commit()

        # Generate employees
        from faker import Faker

        fake = Faker()

        # Create employees in batches to avoid memory issues
        batch_size = 100
        for i in range(0, int(num_employees), batch_size):
            employees_batch = []
            for j in range(min(batch_size, int(num_employees) - i)):
                dept = random.choice(departments)
                first_name = fake.first_name()
                last_name = fake.last_name()
                email = f"{first_name.lower()}.{last_name.lower()}@company.com"

                emp = Employee(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    department_id=dept.id,
                )
                employees_batch.append(emp)

            session.bulk_save_objects(employees_batch)
            session.commit()

        print(
            f"Successfully generated {num_departments} departments and {num_employees} employees"
        )

    except Exception as e:
        print(f"Error generating sample data: {str(e)}")
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    app()
