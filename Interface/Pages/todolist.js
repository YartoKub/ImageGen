// Это в первую очередь тестовый документ, так как мне нужно вспомнить как вообще работать с html и js
const object_name = "todo_list" 
const text_field_name = "todo_list_field"
const secondary_name = "data_point"
const value_field = "value_field"
const inner_list_name = "inner_list"
    async function sendData(element_that_called) {
        my_adress = 'http://127.0.0.1:2000'
        const this_id = element_that_called.id;
        const data = document.getElementById(this_id);
        var input_value = data.getElementsByClassName(value_field)[0].value
        //input_value = encodeURIComponent(input_value);
        const response = await fetch(my_adress, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: JSON.stringify({
                title: "Action",
                body: "SendDataReturnFill",
                params: encodeURIComponent(input_value)
            }) 
        });
        const result = await response.text();
        console.log(result);
        console.log(input_value);
        console.log(this_id);
    }

    function createToDoInstance() {
        body_object = document.getElementById('main_body');
        integer = GenerateNewIndex(object_name);
        my_body = `
        <form id="${object_name + integer}" onsubmit="event.preventDefault(); sendData(this);">
        <label id= "${text_field_name + integer }" for="data">Введите данные:</label>
        <input class = "${value_field}" type="text" name="data">
        <input type="submit" value="Отправить">
        <input type="button" onclick="event.preventDefault(); createDataPoint(this);" value="Отправить">
        <ul class="${inner_list_name}"> 
        </ul>
        </form>
        `;
        body_object.innerHTML = body_object.innerHTML + my_body;
        //return my_body

    }

    function createDataPoint(input_button) {
        parent_object = input_button.parentElement
        console.log(parent_object)
        inner_list = parent_object.getElementsByClassName(inner_list_name)[0]
        
        text_value = parent_object.getElementsByClassName(value_field)[0].value



        var list_point = document.createElement("li")
        var node = document.createTextNode(text_value)
        list_point.appendChild(node);

        inner_list.appendChild(list_point)
    }