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

document.getElementById('input-file').addEventListener('change', function() {
    var filename = document.getElementById('filepath');
    if (this.files[0] == undefined) {
        console.log('no');
        filename.innerText = '선택된 파일 없음';
        return;
    }
    filename.innerText = this.files[0].name;
});