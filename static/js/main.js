const menuToggle = document.getElementById('menu-toggle');
const sideMenu = document.getElementById('side-menu');

menuToggle.addEventListener('click', () => {
    menuToggle.classList.toggle('active'); // ハンバーガー→バツ
    sideMenu.classList.toggle('active');   // メニュー表示
});



//------------------------------------------------------------



// 2. パスワード一致チェック機能
const pwInput = document.getElementById('password');
const pwConfirmInput = document.getElementById('password_confirm');
const msgDisplay = document.getElementById('pw_check_msg');

function checkPassword() {
    // モードがsignupの時だけチェック
    if (document.getElementById('form_mode').value === 'signup') {
        if (pwConfirmInput.value === "") {
            msgDisplay.innerText = "";
        } else if (pwInput.value === pwConfirmInput.value) {
            msgDisplay.innerText = "✓ パスワードが一致しました";
            msgDisplay.style.color = "green";
        } else {
            msgDisplay.innerText = "× パスワードが一致しません";
            msgDisplay.style.color = "red";
        }
    }
}

// 入力するたびにチェック関数を実行
pwInput.addEventListener('input', checkPassword);
pwConfirmInput.addEventListener('input', checkPassword);



//------------------------------------------------------------



// パスワードの表示非表示機能
function togglePassword(targetId) {
    const passwordInput = document.getElementById(targetId);
    // ボタンの文字も変えるために取得
    const toggleBtn = targetId === 'password'
        ? document.getElementById('toggle_password')
        : document.getElementById('toggle_password_confirm');

    if (passwordInput.type === 'password') {
        // テキスト表示に切り替え
        passwordInput.type = 'text';
        toggleBtn.innerText = '隠す';
    } else {
        // パスワード（伏せ字）に切り替え
        passwordInput.type = 'password';
        toggleBtn.innerText = '表示';
    }
}



//------------------------------------------------------------



// 入れてはいけない文字確認機能
// 要素の取得
const usernameInput = document.getElementsByName('username')[0];
const passwordInput = document.getElementById('password');
const confirmInput = document.getElementById('password_confirm');
const submitBtn = document.getElementById('submit_btn');
const errorMsg = document.getElementById('error_message');

// バリデーション関数
function validateForm() {
    const username = usernameInput.value;
    const password = passwordInput.value;
    const confirm = confirmInput.value;
    const mode = document.getElementById('form_mode').value;

    let errorMessage = "";
    let isUsernameValid = true;
    let isPasswordValid = true;
    let isConfirmValid = true;

    // 1. アカウント名のチェック (16文字以内)
    if (username.length > 16) {
        errorMessage = "※アカウント名は16文字以内で入力してください。";
        isUsernameValid = false;
    }

    // 2. パスワードのチェック (16文字以内 + 英数字のみ)
    // [a-zA-Z0-9] は英数字を意味し、^ と $ で全体を囲むことで「それ以外が含まれないか」を見ています
    const alphanumericRegex = /^[a-zA-Z0-9]*$/;
    if (password.length > 16) {
        errorMessage = "※パスワードは16文字以内で入力してください。";
        isPasswordValid = false;
    } else if (!alphanumericRegex.test(password)) {
        errorMessage = "※パスワードは英語または数字のみ使用可能です。";
        isPasswordValid = false;
    }

    // 3. アカウント作成時のみ：パスワード一致チェック
    if (mode === 'signup' && password !== confirm && confirm.length > 0) {
        errorMessage = "※パスワードが一致しません。";
        isConfirmValid = false;
    }

    // エラー表示とボタンの活性化/非活性化
    if (isUsernameValid && isPasswordValid && isConfirmValid) {
        errorMsg.innerText = "";
        submitBtn.disabled = false;
        submitBtn.style.opacity = "1";
        submitBtn.style.cursor = "pointer";
        submitBtn.style.backgroundColor = "#4a90e2";
    } else {
        errorMsg.innerText = errorMessage;
        submitBtn.disabled = true;
        submitBtn.style.opacity = "0.5";
        submitBtn.style.cursor = "not-allowed";
        submitBtn.style.backgroundColor = "#ccc"; // 無効時はグレーにする
    }
}

// すべての入力項目にイベントリスナーを設定
usernameInput.addEventListener('input', validateForm);
passwordInput.addEventListener('input', validateForm);
confirmInput.addEventListener('input', validateForm);

// 切り替えボタンを押した時も再チェック
function switchForm(mode) {
    // (以前の切り替えコードをここに...)
    const confirmGroup = document.getElementById('confirm_group');
    const tabSignin = document.getElementById('tab_signin');
    const tabSignup = document.getElementById('tab_signup');
    const modeInput = document.getElementById('form_mode');
    const submitBtn = document.getElementById('submit_btn');

    if (mode === 'signup') {
        confirmGroup.style.display = 'block';
        tabSignup.classList.add('active');
        tabSignin.classList.remove('active');
        modeInput.value = 'signup';
        submitBtn.innerText = 'アカウントを作成する';
    } else {
        confirmGroup.style.display = 'none';
        tabSignup.classList.remove('active');
        tabSignin.classList.add('active');
        modeInput.value = 'signin';
        submitBtn.innerText = 'サインイン';
    }
    // ...
    validateForm(); // 切り替え時にリセット・再チェック
}