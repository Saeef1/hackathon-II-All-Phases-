from setuptools import setup, find_packages

setup(
    name="todo-backend",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn[standard]>=0.24.0",
        "sqlmodel>=0.0.16",
        "SQLAlchemy>=2.0.0",
        "passlib[bcrypt]>=1.7.4",
        "pyjwt>=2.8.0",
        "python-multipart>=0.0.6",
        "python-dotenv>=1.0.0",
        "pydantic>=2.0.0",
        "pytest>=7.0.0",
        "httpx>=0.25.0",
    ],
    author="Todo App Team",
    description="Todo backend with authentication",
    python_requires=">=3.7",
)