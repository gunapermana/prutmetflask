from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import auth

app = Flask(__name__)

# Inisialisasi Firebase Admin SDK
cred = firebase_admin.credentials.Certificate("serviceAccount.json")
firebase_admin.initialize_app(cred)

app.debug = True


@app.route('/login', methods=['POST'])
def login():
    try:
        # Periksa tipe konten permintaan
        if request.headers['Content-Type'] != 'application/json':
            return jsonify({'error': 'Tipe konten tidak didukung'}), 415

        # Ambil email dan password dari body permintaan
        email = request.json.get('email')
        password = request.json.get('password')

        # Verifikasi email dan password
        if not email or not password:
            return jsonify({'error': 'Email dan password harus diisi'}), 400

        # Authentikasi pengguna dengan email dan password menggunakan Firebase Authentication
        user = auth.get_user_by_email(email)

        # Buat token akses menggunakan Firebase Authentication
        custom_token = auth.create_custom_token(user.uid)

        # Dapatkan UID pengguna
        uid = user.uid

        # Berikan respons dengan token akses dan UID
        return jsonify({'token': custom_token.decode(), 'uid': uid}), 200

    except auth.AuthError as e:
        return jsonify({'error': str(e)}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run()
