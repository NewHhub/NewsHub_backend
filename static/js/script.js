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

// не отправляем форму при нажатии на enter
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.post_create');
    const inputs = form.querySelectorAll('input, select');
  
    inputs.forEach(function(input) {
      input.addEventListener('keypress', function(event) {
        if (event.keyCode === 13) {
          event.preventDefault();
        }
      });
    });
  });



const chipsContainer = document.querySelector('.chips-container');
const selectedChips = document.querySelector('.selected-chips');
const newChipInput = document.querySelector('.new-chip-input');


// Remove chips from selectedChips on click
selectedChips.addEventListener('click', (event) => {
  const option = event.target.closest('option');
  if (option) {
    const chip = chipsContainer.querySelector(`.chip:not(.selected)[data-value="${option.value}"]`);
    if (chip) {
      chip.classList.remove('selected');
    }
    selectedChips.removeChild(option);
  }
});

// Add new chip to chipsContainer and selectedChips on input enter
newChipInput.addEventListener('keydown', (event) => {
  if (event.key === 'Enter' && newChipInput.value) {
    const chip = document.createElement('div');
    chip.classList.add('chip');
    chip.dataset.value = newChipInput.value.replace(/\s/g, '_'); // заменяем пробелы на _
    chip.textContent = newChipInput.value.replace(/\s/g, '_'); // заменяем пробелы на _
    chip.addEventListener('click', () => {
      chip.remove();
      const option = selectedChips.querySelector(`option[value="${chip.dataset.value}"]`);
      if (option) {
        option.remove();
      }
    });
    chipsContainer.insertBefore(chip, newChipInput);
    
    const option = document.createElement('option');
    option.value = newChipInput.value.replace(/\s/g, '_'); // заменяем пробелы на _
    option.selected = true;
    selectedChips.appendChild(option);
    
    newChipInput.value = '';
  }
});

// загружаем первый элемент в див с превьюшкой 
const fileInput = document.querySelector('input[type="file"]#poster')
const previewImage = document.querySelector('#preview')
const reset_preview_btn = document.querySelector('#reset_preview')
const choose_file_button = document.querySelector('#choose_file_button')

fileInput.addEventListener('change', function() {
  const file = fileInput.files[0];
  const reader = new FileReader();

  reader.addEventListener('load', function() {
    previewImage.src = reader.result;
    previewImage.style.marginBottom = '16px' // делаем отступ от фото к форме выбора фото
    reset_preview_btn.style.display = 'flex'
    choose_file_button.style.display = 'none' // убираем кнопку загрузки фото
  });

  if (file) {
    reader.readAsDataURL(file);
  }
});

// при нажатии на кнопку убираем фото
function reset_preview(){
    fileInput.value = []
    reset_preview_btn.style.display = 'none'
    previewImage.src = ''
    previewImage.style.marginBottom = '0'
    choose_file_button.style.display = 'inline-block'
}

// делаем увеличени текстарии
var textarea = document.querySelector('#textComment');

textarea.addEventListener('input', function(){
    setTimeout(function(){
        textarea.style.cssText = 'height:auto;';
        textarea.style.cssText = 'height:' + textarea.scrollHeight + 'px';
      },0);
});

function reply(tread_id, parent_id, username){
  document.getElementById('textComment').value = '@' + username + ', '
  document.getElementById('parent').value = parent_id
  document.getElementById('tread').value = tread_id

  // размер шапки + 32px отступа от контрола 
  let yOffset = 88
  let element = document.getElementById('reply')
  let y = element.getBoundingClientRect().top + window.pageYOffset - yOffset

  window.scrollTo({top: y, behavior: 'smooth'})
}

function go_to_comment(){
  let yOffset = 88
  let element = document.getElementById('reply')
  let y = element.getBoundingClientRect().top + window.pageYOffset - yOffset

  window.scrollTo({top: y, behavior: 'smooth'})
}