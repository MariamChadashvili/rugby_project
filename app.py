from flask import Flask, redirect, url_for, render_template, request, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key = "my_secret_key"


@app.route("/")
def home():
    return render_template('home.html', name='home')


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form.get("name")
        email = request.form.get("email")
        mobile_number = request.form.get("mobile_number")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmPassword")

        if password != confirm_password:
            flash("Passwords do not match", "danger")
            return redirect(url_for("register"))

        try:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash("Email already registered", "danger")
                return redirect(url_for("register"))

            cursor.execute("INSERT INTO users (full_name, email, mobile_number, password) VALUES (?, ?, ?, ?)",
                           (full_name, email, mobile_number, password))
            conn.commit()
            flash("Registration successful", "success")
            return redirect(url_for("login"))

        except sqlite3.Error as e:
            flash(f"Error: {e}", "danger")

        finally:
            if conn:
                conn.close()
    return render_template("register.html", name='register')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
            user = cursor.fetchone()

            if user:
                session["user_id"] = user[0]
                # session["full_name"] = user[1]
                flash("Login successful", "success")
                return redirect(url_for("teams"))
            else:
                flash("Invalid email or password", "danger")
                return redirect(url_for("login"))

        except sqlite3.Error as e:
            flash(f"Error: {e}", "danger")

        finally:
            if conn:
                conn.close()
    return render_template("login.html", name="login")


@app.route('/logout')
def logout():
    session.pop('user_id')
    # session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


@app.route("/teams", methods=["GET", "POST"])
def teams():
    if "user_id" not in session:
        flash("You need to login first", "danger")
        return redirect(url_for("login"))

    if request.method == "POST":
        return redirect(url_for("create_team"))

    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT t.id, t.name, t.player_num, t.address, t.rank, COUNT(tm.player_id) AS player_count FROM teams t LEFT JOIN team_members tm ON t.id = tm.team_id GROUP BY t.id")
        teams_data = cursor.fetchall()

        teams = []
        for team in teams_data:
            team_dict = {
                'id': team[0],
                'name': team[1],
                'player_num': team[2],
                'address': team[3],
                'rank': team[4],
                'player_count': team[5]
            }
            teams.append(team_dict)

    except sqlite3.Error as e:
        flash(f"Error: {e}", "danger")
        teams = []

    finally:
        if conn:
            conn.close()

    return render_template("teams.html", teams=teams)

@app.route("/create_team", methods=["POST"])
def create_team():
    if "user_id" not in session:
        flash("You need to login first", "danger")
        return redirect(url_for("login"))

    team_name = request.form["team_name"]
    player_num = request.form["player_num"]
    address = request.form["address"]
    rank = request.form["rank"]
    creator_id = session["user_id"]

    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("INSERT INTO teams (name, player_num, address, rank, creator_id) VALUES (?, ?, ?, ?, ?)",
                       (team_name, player_num, address, rank, creator_id))
        conn.commit()
        flash("Team created successfully", "success")

    except sqlite3.Error as e:
        flash(f"Error: {e}", "danger")
        conn.rollback()

    finally:
        if conn:
            conn.close()

    return redirect(url_for("teams"))

@app.route("/join_team/<int:team_id>", methods=["POST"])
def join_team(team_id):
    if "user_id" not in session:
        flash("You need to login first", "danger")
        return redirect(url_for("login"))

    user_id = session["user_id"]

    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM team_members WHERE player_id = ? AND team_id = ?", (user_id, team_id))
        existing_membership = cursor.fetchone()

        if existing_membership:
            flash("You are already a member of this team", "warning")
        else:
            cursor.execute("INSERT INTO team_members (player_id, team_id) VALUES (?, ?)", (user_id, team_id))
            conn.commit()
            flash("You have successfully joined the team", "success")
            return redirect(url_for("team_detail", team_id=team_id))

    except sqlite3.Error as e:
        flash(f"Error: {e}", "danger")
        conn.rollback()

    finally:
        if conn:
            conn.close()

    return redirect(url_for("teams"))


@app.route("/team/<int:team_id>")
def team_detail(team_id):
    if "user_id" not in session:
        flash("You need to login first", "danger")
        return redirect(url_for("login"))

    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT t.id, t.name, t.player_num, t.address, t.rank, t.creator_id, COUNT(tm.player_id) AS player_count FROM teams t LEFT JOIN team_members tm ON t.id = tm.team_id WHERE t.id = ? GROUP BY t.id", (team_id,))
        team_data = cursor.fetchone()

        if team_data:
            team = {
                'id': team_data[0],
                'name': team_data[1],
                'player_num': team_data[2],
                'address': team_data[3],
                'rank': team_data[4],
                'creator_id': team_data[5],
                'player_count': team_data[6]
            }

            cursor.execute(
                "SELECT u.full_name, u.mobile_number FROM users u JOIN team_members tm ON u.id = tm.player_id WHERE tm.team_id = ?",
                (team_id,))
            team_members = cursor.fetchall()

            return render_template("team_detail.html", team=team, team_members=team_members)
        else:
            flash("Team not found", "danger")
            return redirect(url_for("teams"))

    except sqlite3.Error as e:
        flash(f"Error: {e}", "danger")

    finally:
        if conn:
            conn.close()

    return redirect(url_for("teams"))


@app.route("/exit_team/<int:team_id>", methods=["POST"])
def exit_team(team_id):
    if "user_id" not in session:
        flash("You need to login first", "danger")
        return redirect(url_for("login"))

    user_id = session["user_id"]

    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("DELETE FROM team_members WHERE player_id = ? AND team_id = ?", (user_id, team_id))
        conn.commit()
        flash("You have successfully exited the team", "success")

    except sqlite3.Error as e:
        flash(f"Error: {e}", "danger")
        conn.rollback()

    finally:
        if conn:
            conn.close()

    return redirect(url_for("teams"))


@app.route("/update_team/<int:team_id>", methods=["GET", "POST"])
def update_team(team_id):
    if "user_id" not in session:
        flash("You need to login first", "danger")
        return redirect(url_for("login"))

    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT name, player_num, address, rank FROM teams WHERE id = ? AND creator_id = ?", (team_id, session["user_id"]))
        team_data = cursor.fetchone()

        if team_data:
            team = {
                'id': team_id,
                'name': team_data[0],
                'player_num': team_data[1],
                'address': team_data[2],
                'rank': team_data[3]
            }

            if request.method == "POST":
                team_name = request.form["team_name"]
                player_num = request.form["player_num"]
                address = request.form["address"]
                rank = request.form["rank"]

                cursor.execute("UPDATE teams SET name = ?, player_num = ?, address = ?, rank = ? WHERE id = ? AND creator_id = ?", (team_name, player_num, address, rank, team_id, session["user_id"]))
                conn.commit()
                flash("Team updated successfully", "success")
                return redirect(url_for("team_detail", team_id=team_id))

            return render_template("update_team.html", team=team)

        else:
            flash("You are not authorized to update this team", "danger")
            return redirect(url_for("teams"))

    except sqlite3.Error as e:
        flash(f"Error: {e}", "danger")
        conn.rollback()

    finally:
        if conn:
            conn.close()

    return render_template("update_team.html")

@app.route("/delete_team/<int:team_id>", methods=["POST"])
def delete_team(team_id):
    if "user_id" not in session:
        flash("You need to login first", "danger")
        return redirect(url_for("login"))

    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT creator_id FROM teams WHERE id = ?", (team_id,))
        creator_id = cursor.fetchone()[0]

        if creator_id == session["user_id"]:
            cursor.execute("DELETE FROM teams WHERE id = ?", (team_id,))
            cursor.execute("DELETE FROM team_members WHERE team_id = ?", (team_id,))
            conn.commit()
            flash("Team deleted successfully", "success")
        else:
            flash("You are not authorized to delete this team", "danger")

    except sqlite3.Error as e:
        flash(f"Error: {e}", "danger")
        conn.rollback()

    finally:
        if conn:
            conn.close()

    return redirect(url_for("teams"))

if __name__ == '__main__':
    app.run(debug=True)
