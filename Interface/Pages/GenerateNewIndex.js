function GenerateNewIndex(ID_Name) { 
    // Эта функция создает новый ID для добавления нового уникального объекта на страницу. 
    // Таким образом объекты одного типа будут иметь idшники вроде: my_form1, my_form2, my_form3
    // Не самая эффективная реализация, можно использовать массив какой-нибудь со ссылками на подмассивы, или словари, хз есть ли они в JS
    // и так сойдет
    let index = 0; // Начальный индекс
    while (true) {
        const currentID = ID_Name + index;
        if (document.getElementById(currentID)) {
            index++;
        } else {
            return index;
        }
    }
}

function MakeACheck(insert_name) {
    console.log(GenerateNewIndex(insert_name));
}
    