const imgal_object_name = "image_gallery_body" 
const imgal_file_field_name = "gallery_file_load_part"
const imgal_secondary_name = "image_gallery_block"
//const imgal_value_field = "value_field"
const imgal_inner_list_name = "gallery_list_part"

class image_list_container {

}

class imageGalleryController {
    constructor(host_element, my_image_list, inner_file_loader) {
        this.my_body = host_element;
        this.inner_list = my_image_list;
        this.inner_file_loader = inner_file_loader;
        this.my_adress = 'http://127.0.0.1:2000'; // Это адрес сервера. Пото его надо будет выкинуть в константу определяемую при запуске
        this.image_list = [];
        console.log("New image controller created");
    }

    createListImage(image_src) {
        const new_addition = document.createElement('img');
        new_addition.src = image_src;
        new_addition.className = "image_gallery_block";
        console.log("Inside createChildImage");
        this.inner_list.appendChild(new_addition)
        this.inner_file_loader.value = ""; // Эта штука опустошает значение value после загрузки, но инфа о изображении уже существует в event поэтому все ОК
    }

    registerImage(event) {
        
        const super_giga_mega_me = this;
        const file = event.target.files[0];
        if (file) {
            console.log("File i okay, the rest: ");
            console.log(file)
            console.log(this.my_body.id);
            const file_reader = new FileReader();
            // Я понятия не имею как это работает, и почему так сложно, но наверное это вызвано ассинхронностью file_reader-а
            file_reader.onload = function(e) { // Тоесть я создаю подфункцию для внутреннего объекта получающего ивент? 
                console.log(e)
                const img_src = e.target.result;
                super_giga_mega_me.createListImage(img_src);
            }
            file_reader.readAsDataURL(file);
        } 
        else { console.log("Something went wrong with a file") }
    }
}


function createImageGalleryInstance() {
        body_object = document.getElementById('main_body');
        integer = GenerateNewIndex(imgal_object_name);
        var my_body = document.createElement('form');
        my_body.className = imgal_object_name;
        my_body.id = imgal_object_name + integer // <div class="${}" id="${}"> </div>
        
        my_body.onsubmit = "myController.registerImage()" //function() {my_body.registerImage()}

        inner_file_field = document.createElement('div'); inner_file_field.className = imgal_file_field_name
        my_body.appendChild(inner_file_field);  // Добавление внутреннего div с формой

        inner_list =  document.createElement('div'); inner_list.className = imgal_inner_list_name
        my_body.appendChild(inner_list); // Добавление спска с изображениями загруженными
        
        // Тут загрузчик файлов, он коннектится к основному объекту.
        inner_file_loader = document.createElement('input'); inner_file_loader.type = 'file'; inner_file_loader.type = 'file';
        inner_file_loader.innerHTML = "file to upload";
        inner_file_loader.addEventListener('change', function(event) { 
            inner_file_loader.myController.registerImage(event)
        })

        my_body_controller = new imageGalleryController(my_body, inner_list, inner_file_loader);
        my_body.myController = my_body_controller;
        inner_file_loader.myController = my_body_controller;

        inner_file_field.appendChild(inner_file_loader)


        body_object.appendChild(my_body)
        //return my_body

    }