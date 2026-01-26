const menuToggle = document.getElementById('menu-toggle');
const sideMenu = document.getElementById('side-menu');

menuToggle.addEventListener('click', () => {
    menuToggle.classList.toggle('active'); // ハンバーガー→バツ
    sideMenu.classList.toggle('active');   // メニュー表示
});




const threadInput = document.getElementById('thread-title');
const threadBtn = document.getElementById('thread-submit-btn');
const threadError = document.getElementById('thread-error-msg');


threadInput.addEventListener('input', () => {
    const val = threadInput.value;
    const trimmedVal = val.trim();
    let errorText = "";

    // 1. 空白チェック
    if (trimmedVal.length === 0) {
        errorText = "タイトルを入力してください。";
    }
    // 2. 文字数チェック（50文字以下）
    else if (val.length > 50) {
        errorText = `タイトルは50文字以内で入力してください (${val.length}/50)`;
    }
    // 3. 文字数チェック（10文字以上）
    else if (val.length < 10) {
        errorText = `タイトルは10文字以上で入力してください (${val.length}/10)`;
    }
    // 3. 改行チェック（コピペ対策）
    else if (/\r|\n/.test(val)) {
        errorText = "タイトルに改行を含めることはできません。";
    }

    // 画面への反映
    if (errorText) {
        threadError.textContent = errorText;
        threadError.style.display = "block";
        threadBtn.disabled = true;
    } else {
        threadError.style.display = "none";
        threadBtn.disabled = false;
    }
});

// 初期状態のチェック
threadInput.dispatchEvent(new Event('input'));
