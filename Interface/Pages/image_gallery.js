

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
        this.image_list.push(image_src)
        console.log(image_src)
        
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

    registerFrontImages(event) {
        var files = this.inner_file_loader.files;
        let present_pictures = this.image_list.length
        for (let i = 0; i < files.length; i++) {
            this.image_list.push(files[i])
            console.log(files[i])
        }

        for (let i = 0; i < files.length; i++) {
            let current_index = present_pictures + i
            let new_url = URL.createObjectURL(this.image_list[current_index])
            console.log("loaded new image: " + new_url)
            this.createListImage(new_url);
        }
        console.log("Я отключил очистку изображения после загрузки")
        //this.inner_file_loader.value = ""; // Эта штука опустошает значение value после загрузки, но инфа о изображении уже существует в event поэтому все ОК
    }

    async sendData2server2() {
        console.log("mom i am here");
        console.log(String(this.image_list[0]))
        /*
        //event.preventDefault();
        fetch(this.my_adress, {
            method: 'POST',
            body: JSON.stringify(this.image_list[0]) ,
            params: JSON.stringify({"doo": "doo", "fart": "fart", "pic": this.image_list[0]}) 
        }).then(response => {
            if (!response.ok) {
                throw new Error('Сетевая ошибка');
            }
            return response.json(); // или response.text(), в зависимости от того, что возвращает сервер
        })
        .then(data => {
            console.log('Успех:', data);
        })  */
        var xhr = new XMLHttpRequest();
        xhr.onload = function() {
            var reader = new FileReader();
            reader.onloadend = function() {
            console.log(reader.result);
            }
            reader.readAsDataURL(xhr.response);
        };
        xhr.open('GET', this.image_list[0]);
        xhr.responseType = 'blob';
        xhr.send();
    }

    async sendData2Server() {
        console.log("Я перехватываю sendData2Server и перенаправляю его на sendData2server2")
        this.sendData2server2()
        return "False"
        event.preventDefault();
        /*
        const formData = new FormData();
        this.image_list.forEach((image, index) => {
            formData.append(`image_${index}`, image);
        });
        console.log(formData)
        console.log("Hello, server data collected")

        fetch(this.my_adress, {
            method: 'POST',
            body: formData
        }).then(response => {
            if (!response.ok) {
                throw new Error('Сетевая ошибка');
            }
            return response.json(); // или response.text(), в зависимости от того, что возвращает сервер
        })
        .then(data => {
            console.log('Успех:', data);
        })
        .catch(error => {
            console.error('Ошибка:', error);
        });*/
        const formData = new FormData();
        formData.append("text1", "text2")
        /*
        this.image_list.forEach((image, index) => {
            formData.append(`file[${index}]`, image)
            console.log(image)
            console.log(index)
        })*/

        for (let [key, value] of formData.entries()) {
            console.log(key)
            console.log(value)
            //console.log(`Найдено изображение: ${key} - ${value.name}`);
        }
        // Я в душе не ебу почему сраный fetch не хочет отправлять ни  одного бита из ебаного formData.
        // Делал все по гайдам. По 20 разным гайдам из отовсюду.
        // но этот членожоп, ajaxHandler, какого-то хуя справляется с этим.
        
        var ajaxHandler = new XMLHttpRequest();
        
        ajaxHandler.onreadystatechange = function() {
            if(ajaxHandler.readyState == 4) { console.log(ajaxHandler.responseText); }
        };

        ajaxHandler.open("POST", "imagicunicus_yaric", false);
        ajaxHandler.send(formData);

        
        /*
        console.log(formData)
        fetch (this.my_adress, {
            method: 'POST',
            body: formData
        }).then(response => {
            if (!response.ok) { throw new Error('Ответ не ОК'); }
        })*/
        /*
        const response = await fetch(this.my_adress, {
            method: 'POST',
            //headers: { 'Content-Type': 'application/x-www-form-urlencoded', },
            body: 
                JSON.stringify({
                title: "Action",
                body: formData,
                images: true
            }) 
        }).then(response => {
            if (!response.ok) { throw new Error('Ответ не ОК'); }
        })*/
       
    }
}


function createImageGalleryInstance() {
        body_object = document.getElementById('main_body');
        integer = GenerateNewIndex(imgal_object_name);
        var my_body = document.createElement('form');
        my_body.className = imgal_object_name;
        my_body.id = imgal_object_name + integer // <div class="${}" id="${}"> </div>
        
        my_body.onsubmit = "myController.registerImage" //function() {my_body.registerImage()}

        inner_file_field = document.createElement('div'); inner_file_field.className = imgal_file_field_name
        my_body.appendChild(inner_file_field);  // Добавление внутреннего div с формой

        inner_list =  document.createElement('div'); inner_list.className = imgal_inner_list_name
        my_body.appendChild(inner_list); // Добавление спска с изображениями загруженными
        
        send_to_server_button = document.createElement('button'); send_to_server_button.innerHTML = "To server"; 
        send_to_server_button.onclick = function() {event.preventDefault();  send_to_server_button.myController.sendData2Server();};
        my_body.appendChild(send_to_server_button)
        // Тут загрузчик файлов, он коннектится к основному объекту.
        inner_file_loader = document.createElement('input'); inner_file_loader.type = 'file'; inner_file_loader.type = 'file'; inner_file_loader.multiple = "multiple";
        inner_file_loader.innerHTML = "file to upload";
        inner_file_loader.addEventListener('change', function(event) { 
            inner_file_loader.myController.registerImage(event)
            //inner_file_loader.myController.registerFrontImages(event)
        })

        my_body_controller = new imageGalleryController(my_body, inner_list, inner_file_loader);
        my_body.myController = my_body_controller;
        inner_file_loader.myController = my_body_controller;
        send_to_server_button.myController = my_body_controller;

        inner_file_field.appendChild(inner_file_loader)


        body_object.appendChild(my_body)
     }


