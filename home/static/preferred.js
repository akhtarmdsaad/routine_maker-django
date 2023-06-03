
const addBtn = document.querySelector("#add");
const routineContainer = document.querySelector(".routine");
const title = document.querySelector("select#title1")
let rowNumber = 2;

addBtn.addEventListener("click", () => {
  const newRow = document.createElement("div");
  newRow.classList.add("row");
  newRow.innerHTML = `
    <div class="cell">
        <select name="title"  class="form-control" id="title${rowNumber}">
            ${title.innerHTML}
        </select>
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

