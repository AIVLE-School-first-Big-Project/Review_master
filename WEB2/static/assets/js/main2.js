// 햄버거여닫기 
const hamburger = document.querySelector('.hamburger img');
const head_content = document.querySelector('head_content ul');
hamburger.addEventListener("click", () => {
    console.log('clicked');
    hamburger.classList.toggle('active');
    head_content.classList.toggle('active');
})