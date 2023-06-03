// form_container = document.querySelector('.fixed form .container')
// form = document.querySelector('.fixed form')
// add_button = document.querySelector('#add')
// submit_button = document.querySelector('#submit')
// var no=1

// add_button.onclick = (e)=>{
    // if(e.target==add_button){
		// e.preventDefault()
        // console.log(e)
        // no+=1
        
        // var new_cell = document.createElement("div");
        // new_cell.className = "cell";
        // new_cell.innerHTML = '<label for="title">Title</label>\n<input type="text" name="title" id="title">\n&nbsp;&nbsp;&nbsp;\n<label for="start">Start</label>\n<input type="time" name="start" id="start' + no + '">\n\n<label for="end">End</label>\n<input type="time" name="end" id="end' + no + '">';

        // form_container.appendChild(new_cell);
        
        
    // }
// }
const addBtn = document.querySelector("#add");
const routineContainer = document.querySelector(".routine");
let rowNumber = 2;

addBtn.addEventListener("click", () => {
  const newRow = document.createElement("div");
  newRow.classList.add("row");
  newRow.innerHTML = `
    <div class="cell">
      <input type="text" name="title" id="title${rowNumber}">
    </div>
    <div class="cell">
      <input type="time" name="start" id="start${rowNumber}">
    </div>
    <div class="cell">
      <input type="time" name="end" id="end${rowNumber}">
    </div>
  `;
  
  //creating buttons
  const newButton = document.createElement("button");
  newButton.classList.add("btn");
  newButton.classList.add("btn-outline-primary");
  newButton.innerHTML = '<i class="fas fa-trash\"></i>';
  newButton.addEventListener("click",(e)=>{
    e.preventDefault();
    routineContainer.removeChild(newRow);
  })

  //creating cell
  const cell = document.createElement("div")
  cell.classList.add("cell")

  //appending elements
  cell.appendChild(newButton);
  newRow.appendChild(cell);
  routineContainer.appendChild(newRow);
  rowNumber++;
});

