from flask import Flask, render_template, request, session, redirect, url_for, flash  # request を追加
from supabase import create_client, Client # 新しく追加
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid
import os  # 追加
from dotenv import load_dotenv  # 追加

# .envファイルを読み込む
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY") # これを追記

# コードに直接書くのではなく、環境変数から取得する
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/signin_or_up')
def show_signin():
    # templatesフォルダの中にある sign_in.html を表示する
    return render_template('sign_in.html')

@app.route("/")
def index():
    # Supabaseからスレッド一覧を取得
    response = supabase.table("threads").select("*").order("created_at", desc=True).execute()

    print("取得したデータ:", response.data)
    
    # HTMLを表示。threadsという変数名でリストを渡す
    return render_template('index.html', threads=response.data)

@app.route('/thread/<thread_id>')
def show_thread(thread_id):

    # スレッド取得
    thread_res = supabase.table("threads").select("*").eq("id", thread_id).single().execute()
    
    # メッセージ取得
    posts_res = supabase.table("posts").select("*").eq("thread_id", thread_id).execute()
    
    return render_template('thread.html', thread=thread_res.data, posts=posts_res.data)

@app.route('/auth', methods=['POST'])
def auth():
    # 1. フォームから送られてきたデータをキャッチする
    mode = request.form.get('mode')          # 'signin' か 'signup' か
    username = request.form.get('username').strip() # アカウント名
    password = request.form.get('password')  # パスワード

    # バリデーション処理
    if not username:
        # 1. 空白（またはスペースのみ）の確認
        print("エラー：ユーザーネームの入力が空です。")

    elif not password:
        print("エラー：パスワードの入力が空です。")

    elif len(username) > 16:
        # 2. 文字数の確認（16文字を超えているか）
        print("エラー：16文字以内で入力してください。")

    elif len(username) > 16:
        # 2. 文字数の確認（16文字を超えているか）
        print("エラー：16文字以内で入力してください。")

    else:
    
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
    session.clear() 

    # 2. 「どこから来たか」のURLを取得する
    # 直前のURLがない（ブックマーク等から直接来た）場合は index へ戻す
    next_url = request.referrer or url_for('index')

    # 3. 直前のページに戻る
    return redirect(next_url)

@app.route("/add_thread")
def add_thread():
    return render_template('add_thread.html')

@app.route('/create_thread', methods=['POST'])
def create_thread():

    title = request.form.get('title', '').strip()

    # 1. 未入力チェック
    if not title:
        return "タイトルが必要です", 400

    # 2. 文字数チェック（50文字以内）
    if len(title) > 50:
        return "タイトルは50文字以内で入力してください", 400

    # 3. 改行チェック（Pythonの文字列内に改行が含まれていないか）
    if "\n" in title or "\r" in title:
        return "タイトルに改行を含めることはできません", 400

    user_name = session.get('user_name')

    if not user_name:
        # 2. まだ名前がない場合、セッションに一度だけIDを保存する
        # すでにセッションにIDがあればそれを使い、なければ新しく作る
        if 'temp_id' not in session:
            session['temp_id'] = str(uuid.uuid4())[:8] # 8文字のランダム文字
        
        # 3. 表示用の名前を組み立てる
        user_name = f"名無しさん (ID:{session['temp_id']})"

    # Supabaseにデータを挿入。作成した行のデータを返すように指定する
    response = supabase.table("threads").insert({
        "title": title,
        "created_by": user_name
    }).execute()

    print(title)
    print(user_name)

    # 今作ったスレッドの情報を取得（リストの最初に入っています）
    new_thread = response.data[0]
    new_id = new_thread['id']

    # indexではなく、作成したスレッドの「詳細ページ」へリダイレクト！
    return redirect(url_for('show_thread', thread_id=new_id))

@app.route('/thread/<thread_id>/post', methods=['POST'])
def post_message(thread_id):

    content = request.form.get('content', '').strip()
    
    # 1. 空白チェック
    if not content:
        return "内容は必須です", 400
    
    # 2. 文字数チェック
    if len(content) > 1000:
        return "文字数が制限を超えています", 400
        
    # 3. 行数チェック
    lines = content.splitlines() # 改行で分割
    if len(lines) > 60:
        return "行数が制限を超えています", 400

    user_name = session.get('user_name')

    if not user_name:
        # 2. まだ名前がない場合、セッションに一度だけIDを保存する
        # すでにセッションにIDがあればそれを使い、なければ新しく作る
        if 'temp_id' not in session:
            session['temp_id'] = str(uuid.uuid4())[:8] # 8文字のランダム文字
        
        # 3. 表示用の名前を組み立てる
        user_name = f"名無しさん (ID:{session['temp_id']})"

    # postsテーブルにメッセージを挿入
    supabase.table("posts").insert({
        "thread_id": thread_id,
        "content": content,
        "username": user_name
    }).execute()

    # 投稿が終わったら、今見ていたスレッドのページを再表示
    return redirect(url_for('show_thread', thread_id=thread_id) + '#latest')

@app.template_filter('datetimeformat')
def datetimeformat(value):
    if not value:
        return ""
    # Supabaseの時刻文字列（ISO形式）を読み込む
    # T や Z が含まれる形式に対応
    try:
        dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
        # 好きな形式に変換（例: 2026/01/26 10:15）
        return dt.strftime('%Y/%m/%d %H:%M')
    except ValueError:
        return value # 変換できない場合はそのまま返す

if __name__ == "__main__":
    app.run(debug=True)