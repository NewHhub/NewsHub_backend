function changePage(page, data){
    let btns_list = ['page_feeds', 'page_topics', 'page_users']
    let data_list = ['data_feeds', 'data_topics', 'data_users']
    let curent_page = document.getElementById(page)

    if (!curent_page.classList.contains("active")){
        curent_page.classList.toggle("active");
    }

    // remove active class from another btns
    for(const page_element of btns_list){
        if(page_element != page){
            document.getElementById(page_element).classList.remove("active")
        }
    }

    // hide another blocks of contant
    document.getElementById(data).style.display = 'block';
    for(const data_element of data_list){
        if(data_element != data){
            document.getElementById(data_element).style.display = 'none';
        }
    }
}

document.getElementById("search_form").addEventListener("keyup", function(event) {
    // устаревший вариант, нужно переделать в будущем
    if (event.keyCode === 13) {  // "Enter" key code
        event.preventDefault();  // prevent default "submit" behavior
        document.getElementById("search_form").submit();  // submit the form
    }
});