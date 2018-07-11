"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template, redirect

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""
    github = request.args.get('github')
    first, last, github = hackbright.get_student_by_github(github)
    rows = hackbright.get_grades_by_github(github)

    return render_template('student_info.html',
                           first=first, last=last, github=github, rows=rows)


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/student-add")
def get_new_student_form():
    """Show form for searching for a student."""

    return render_template("student_add.html")


@app.route("/student-add", methods=['POST'])
def student_add():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    github = request.form.get("github")

    hackbright.make_new_student(first_name, last_name, github)

    return render_template('student_info.html',
                           first=first_name, last=last_name, github=github)


@app.route("/project-add")
def get_new_project_form():
    """Show form for searching for a student."""

    return render_template("project_add.html")


@app.route("/project-add", methods=['POST'])
def project_add():
    title = request.form.get("title")
    description = request.form.get("description")
    max_grade = request.form.get("max_grade")

    hackbright.add_project(title, description, max_grade)
    project = (title, description, max_grade)

    return render_template('project_info.html',
                           project=project)


@app.route("/project")
def get_project():
    title = request.args.get("title")
    project = hackbright.get_project_by_title(title)
    project_grades = hackbright.get_grades_by_title(title)
    return render_template("project_info.html", project=project,
                           project_grades=project_grades)


@app.route("/assign-grade")
def get_grade_form():
    students = hackbright.get_all_students()
    projects = hackbright.get_all_projects()
    return render_template("assign_grade.html",
                           students=students, projects=projects)


@app.route("/assign-grade", methods=['POST'])
def assign_grade():
    github = request.form.get("github")
    project_title = request.form.get("title")
    grade = request.form.get("grade")

    if not (hackbright.get_grade_by_github_title(github, project_title)):
        hackbright.assign_grade(github, project_title, grade)
        return redirect('/')
    else:
        hackbright.update_grade(github, project_title, grade)
        return redirect('/')


@app.route("/")
def get_homepage():
    students = hackbright.get_all_students()
    projects = hackbright.get_all_projects()
    return render_template("homepage.html",
                           students=students, projects=projects)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
