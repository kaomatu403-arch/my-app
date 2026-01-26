const menuToggle = document.getElementById('menu-toggle');
const sideMenu = document.getElementById('side-menu');

menuToggle.addEventListener('click', () => {
    menuToggle.classList.toggle('active'); // ハンバーガー→バツ
    sideMenu.classList.toggle('active');   // メニュー表示
});




const textarea = document.getElementById('content-area');
const submitBtn_thread = document.getElementById('submit-btn');
const errorMsg_thread = document.getElementById('error-message');

textarea.addEventListener('input', () => {
    const content = textarea.value;
    const charCount = content.length;
    const lineCount = content.split(/\r\n|\r|\n/).length;

    // 前後の空白を除去したテキスト（空欄チェック用）
    const trimmedContent = content.trim();

    let errorText = "";

    // 条件判定（優先順位が高いものからチェック）
    if (trimmedContent.length === 0) {
        // 何も入力されていない、またはスペースのみの場合
        errorText = "メッセージを入力してください。";
    } else if (charCount > 2000) {
        // 文字数オーバー
        errorText = `文字数オーバーです (${charCount}/2000文字)`;
    } else if (lineCount > 60) {
        // 行数オーバー
        errorText = `行数オーバーです (${lineCount}/60行)`;
    }

    // 表示とボタン制御の切り替え
    if (errorText) {
        errorMsg_thread.textContent = errorText;
        errorMsg_thread.style.display = "block";
        submitBtn_thread.disabled = true;
    } else {
        errorMsg_thread.style.display = "none";
        submitBtn_thread.disabled = false;
    }
});

// ページ読み込み時にも一度実行して、初期状態（空欄）でボタンを無効化しておく
textarea.dispatchEvent(new Event('input'));