from app import app
import os

if __name__ == "__main__":
    app.run(os.environ.get("HOST"), os.environ.get("PORT"), debug=True)
