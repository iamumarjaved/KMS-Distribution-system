var count = 9;
function add(){
    for (var i = 1; i <= count; i++) {
        // count += 1;
        html = '<div class="row" id="row1'+ count +'">\
            <input type="text" name="name" id="name'+ count +'" placeholder="Name">\
        </div>'
        var form = document.getElementById('formm');
        form.innerHTML += html;
    }
}