let bg = document.querySelector('.bg');
let img = document.querySelector('.img');
let upload = document.querySelector('#file-input');
upload.addEventListener('change', e => {
    img.classList.remove('hide');
    bg.classList.add('hide');
});



document.getElementById('url').onchange = function() {
    var val = document.getElementById('url').value;
    document.getElementById('selected-image').src = val;
	let bg = document.querySelector('.bg');
	let img = document.querySelector('.img');
    img.classList.remove('hide');
    bg.classList.add('hide');
}

