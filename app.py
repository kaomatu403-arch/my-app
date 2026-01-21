from flask import Flask, render_template, request, session, redirect, url_for, flash  # request を追加
from supabase import create_client, Client # 新しく追加
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# --- Supabase接続設定 ---
SUPABASE_URL = "https://wmcptefbfggervdkmlwl.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndtY3B0ZWZiZmdnZXJ2ZGttbHdsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njg3MTYyNDAsImV4cCI6MjA4NDI5MjI0MH0.6NZG1THnqv3N3qub-1Eac2X8Rz_auyR0He8AVgEMXk4"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/show_signin')
def show_signin():
    # templatesフォルダの中にある sign_in.html を表示する
    return render_template('sign_in.html')

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/auth', methods=['POST'])
def auth():
    # 1. フォームから送られてきたデータをキャッチする
    mode = request.form.get('mode')          # 'signin' か 'signup' か
    username = request.form.get('username')  # アカウント名
    password = request.form.get('password')  # パスワード
    
    # 2. 動作確認のために、まずはターミナル（黒い画面）に表示してみる
    print(f"モード: {mode}")
    print(f"ユーザー名: {username}")
    print(f"パスワード: {password}")

    # 3. 判定ロジックの「土台」を作る
    if mode == 'signup':

        existing_user = supabase.table("User_Information").select("*").eq("username", username).execute()
        
        if len(existing_user.data) > 0:
            # flashでメッセージを登録し、サインイン画面に戻す
            flash("そのユーザーネームは既に使われています。", "error")
            return redirect(url_for('show_signin'))

        # 生のパスワードをハッシュ化する
        hashed_password = generate_password_hash(password)

        data = {
            "username": username,
            "password": hashed_password  # ←暗号化された文字列
        }
        # usersテーブルにデータを保存してね、という命令
        response = supabase.table("User_Information").insert(data).execute()

        return redirect(url_for('index'))
    
    else:
        # --- サインイン処理 ---
        # 1. 指定されたユーザー名のデータをSupabaseから探す
        response = supabase.table("User_Information").select("*").eq("username", username).execute()
        
        # 2. ユーザーが見つかったか確認
        user_data = response.data # 見つかったデータがリストで入る
        
        if len(user_data) > 0:
            # ユーザーが存在した場合、パスワードを照合
            stored_password = user_data[0]['password'] # DB内のハッシュ化されたパスワード
            
            if check_password_hash(stored_password, password):
                # セッション（ブラウザのメモ帳）にユーザー名を保存
                session['user_name'] = username
                # ログイン後はトップページ（index.html）へ飛ばす
                return redirect(url_for('index'))
            else:
                return "エラー：パスワードが違います。"
        else:
            return "エラー：ユーザー名が見つかりません。"

@app.route('/logout')
def logout():
    # セッションからユーザー情報を消去
    session.pop('user_name', None)
    # ログアウトしたらトップページへ戻る
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)