from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import String, create_engine, select, desc
from sqlalchemy.orm import DeclarativeBase, Session, mapped_column, Mapped

app = Flask(__name__)
engine = create_engine("sqlite:///db.sqlite3")

download_link = "https://github.com/EclpticRanger/Ecliptics-Competitive-Tools/releases/download/V1.2.1/ecliptics_compedative_tools-0.1.0.tar.gz"
release_link = "https://github.com/EclpticRanger/Ecliptics-Competitive-Tools/releases/tag/V1.2.1"

class Base(DeclarativeBase):
    pass
class Feedback(Base):
    __tablename__ = "feedback"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    username: Mapped[str] = mapped_column(default="Anonymous")
    text: Mapped[str] = mapped_column()

Base.metadata.create_all(engine)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/download")
def download():
    return render_template("download.html", download_link=download_link, release_link=release_link)

@app.route("/functions")
def functions():
    return render_template("functions.html")

@app.route("/class")
def classes():
    return render_template("class.html")

@app.route("/feedback", methods=['GET','POST'])
def feedback():
    with Session(engine) as session:
        if request.method == "POST":
            name = request.form['name']
            text = request.form['text']
            session.add(Feedback(username=name, text=text))
            session.commit()
            
            return redirect(url_for('feedback'))

        stmt = select(Feedback).order_by(Feedback.id.desc()).limit(10)
        recent_feedback = session.scalars(stmt).all()
                
    return render_template("feedback.html", recent_feedback=recent_feedback)

if __name__ == "__main__":
    app.run(debug=True)
