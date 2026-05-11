from flask import Flask, request, redirect, url_for, render_template_string
import sqlite3
from datetime import datetime, timezone, timedelta

app = Flask(__name__)

DB_NAME = "absensi.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kehadiran (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            nim TEXT NOT NULL,
            jam_kehadiran TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def ambil_data_kehadiran():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nama, nim, jam_kehadiran
        FROM kehadiran
        ORDER BY id DESC
    """)

    data = cursor.fetchall()
    conn.close()
    return data


@app.route("/")
def index():
    data_kehadiran = ambil_data_kehadiran()

    html = """
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <title>Sistem Kehadiran</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f6f8;
                margin: 0;
                padding: 30px;
            }

            .container {
                max-width: 900px;
                margin: auto;
                background: white;
                padding: 25px;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            }

            h1 {
                text-align: center;
                color: #222;
            }

            form {
                display: flex;
                gap: 10px;
                margin-bottom: 25px;
            }

            input {
                flex: 1;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 6px;
            }

            button {
                padding: 10px 18px;
                border: none;
                background: #2563eb;
                color: white;
                border-radius: 6px;
                cursor: pointer;
            }

            button:hover {
                background: #1d4ed8;
            }

            table {
                width: 100%;
                border-collapse: collapse;
            }

            th, td {
                border: 1px solid #ddd;
                padding: 10px;
                text-align: left;
            }

            th {
                background: #2563eb;
                color: white;
            }

            tr:nth-child(even) {
                background: #f9fafb;
            }

            .hapus {
                background: #dc2626;
                color: white;
                padding: 6px 10px;
                border-radius: 5px;
                text-decoration: none;
            }

            .hapus:hover {
                background: #991b1b;
            }

            .kosong {
                text-align: center;
                color: #777;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Sistem Pencatatan Kehadiran</h1>

            <form action="/tambah" method="POST">
                <input type="text" name="nama" placeholder="Masukkan Nama" required>
                <input type="text" name="nim" placeholder="Masukkan NIM" required>
                <button type="submit">Catat Hadir</button>
            </form>

            <table>
                <thead>
                    <tr>
                        <th>No</th>
                        <th>Nama</th>
                        <th>NIM</th>
                        <th>Jam Kehadiran</th>
                        <th>Aksi</th>
                    </tr>
                </thead>

                <tbody>
                    {% if data_kehadiran %}
                        {% for item in data_kehadiran %}
                        <tr>
                            <td>{{ loop.index }}</td>
                            <td>{{ item[1] }}</td>
                            <td>{{ item[2] }}</td>
                            <td>{{ item[3] }}</td>
                            <td>
                                <a class="hapus" href="/hapus/{{ item[0] }}" onclick="return confirm('Yakin hapus data ini?')">
                                    Hapus
                                </a>
                            </td>
                        </tr>
                        {% endfor %}
                    {% else %}
                        <tr>
                            <td colspan="5" class="kosong">Belum ada data kehadiran.</td>
                        </tr>
                    {% endif %}
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """

    return render_template_string(html, data_kehadiran=data_kehadiran)


@app.route("/tambah", methods=["POST"])
def tambah():
    nama = request.form.get("nama")
    nim = request.form.get("nim")

    if not nama or not nim:
        return redirect(url_for("index"))

    wib = timezone(timedelta(hours=7))
    jam_kehadiran = datetime.now(wib).strftime("%d-%m-%Y %H:%M:%S WIB")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO kehadiran (nama, nim, jam_kehadiran)
        VALUES (?, ?, ?)
    """, (nama, nim, jam_kehadiran))

    conn.commit()
    conn.close()

    return redirect(url_for("index"))


@app.route("/hapus/<int:id>")
def hapus(id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM kehadiran WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect(url_for("index"))


init_db()


if __name__ == "__main__":
    app.run(debug=True)