const menuToggle = document.getElementById('menu-toggle');
const sideMenu = document.getElementById('side-menu');

menuToggle.addEventListener('click', () => {
    menuToggle.classList.toggle('active'); // ハンバーガー→バツ
    sideMenu.classList.toggle('active');   // メニュー表示
});