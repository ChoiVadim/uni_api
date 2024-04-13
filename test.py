from main import app, db
from sqlalchemy import text


with app.app_context():
    with db.engine.connect() as conn:
        result = conn.execution_options(stream_results=True).execute(text("SELECT * FROM course"))
        for row in result:
            print(row)
