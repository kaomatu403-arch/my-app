
const postForm = document.getElementById('post-form');
const submitBtn = document.getElementById('submit-btn');
const contentArea = document.getElementById('content-area');

postForm.addEventListener('submit', function () {

    // ① 送信ボタンを無効化する（連打防止）
    submitBtn.disabled = true;
    submitBtn.innerText = "送信中...";
    submitBtn.style.backgroundColor = "#ccc"; // 見た目でも無効化をわかりやすく

    // ② テキストエリアを空にする（任意ですが、送信した感覚を出すため）
    // ただし、ブラウザのリロードが走るまでの数秒間の見た目のためです。
    setTimeout(() => {
        contentArea.value = '';
    }, 10);

});