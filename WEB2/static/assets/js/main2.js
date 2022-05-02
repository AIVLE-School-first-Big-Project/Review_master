// 햄버거여닫기 
const hamburger = document.querySelector('.hamburger img');
const content = document.querySelector('.head_content');
const user = document.querySelector('.head_user');

hamburger.addEventListener("click", () => {
    console.log('clicked');
    // for (var nav in navs) {
    //     nav.classList.toggle('active');
    // }
    content.classList.toggle('active');
    user.classList.toggle('active');
})