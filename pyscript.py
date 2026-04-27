script.jimport json
from datetime import datetime

addBox = document.querySelector(".add-box")
popupBox = document.querySelector(".popup-box")
popupTitle = popupBox.querySelector("header p")
closeIcon = popupBox.querySelector("header i")
titleTag = popupBox.querySelector("input")
descTag = popupBox.querySelector("textarea")
addBtn = popupBox.querySelector("button")
months = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]
notes = json.loads(localStorage.getItem("notes") or "[]")
isUpdate = False
updateId = None

def showNotes():
    if not notes:
        return
    for li in document.querySelectorAll(".note"):
        li.remove()
    for id, note in enumerate(notes):
        filterDesc = note["description"].replace("\n", "<br/>")
        liTag = f"""<li class="note">
                        <div class="details">
                            <p>{note["title"]}</p>
                            <span>{filterDesc}</span>
                        </div>
                        <div class="bottom-content">
                            <span>{note["date"]}</span>
                            <div class="settings">
                                <i onclick="showMenu(this)" class="uil uil-ellipsis-h"></i>
                                <ul class="menu">
                                    <li onclick="updateNote({id}, '{note["title"]}', '{filterDesc}')"><i class="uil uil-pen"></i>Edit</li>
                                    <li onclick="deleteNote({id})"><i class="uil uil-trash"></i>Delete</li>
                                </ul>
                            </div>
                        </div>
                    </li>"""
        addBox.insertAdjacentHTML("afterend", liTag)

def showMenu(elem):
    elem.parentElement.classList.add("show")
    def click_handler(e):
        if e.target.tagName != "I" or e.target != elem:
            elem.parentElement.classList.remove("show")
    document.addEventListener("click", click_handler)

def deleteNote(noteId):
    confirmDel = confirm("Are you sure you want to delete this note?")
    if not confirmDel:
        return
    notes.pop(noteId)
    localStorage.setItem("notes", json.dumps(notes))
    showNotes()

def updateNote(noteId, title, filterDesc):
    description = filterDesc.replace("<br/>", "\r\n")
    global updateId, isUpdate
    updateId = noteId
    isUpdate = True
    addBox.click()
    titleTag.value = title
    descTag.value = description
    popupTitle.innerText = "Update a Note"
    addBtn.innerText = "Update Note"

def addBtn_click_handler(e):
    e.preventDefault()
    title = titleTag.value.strip()
    description = descTag.value.strip()
    if title or description:
        currentDate = datetime.now()
        month = months[currentDate.month - 1]
        day = currentDate.day
        year = currentDate.year
        noteInfo = {"title": title, "description": description, "date": f"{month} {day}, {year}"}
        if not isUpdate:
            notes.append(noteInfo)
        else:
            isUpdate = False
            notes[updateId] = noteInfo
        localStorage.setItem("notes", json.dumps(notes))
        showNotes()
        closeIcon.click()

addBox.addEventListener("click", lambda: (
    popupTitle.innerText = "Add a new Note",
    addBtn.innerText = "Add Note",
    popupBox.classList.add("show"),
    document.querySelector("body").style.overflow = "hidden",
    titleTag.focus() if window.innerWidth > 660 else None
))

closeIcon.addEventListener("click", lambda: (
    isUpdate = False,
    titleTag.value = descTag.value = "",
    popupBox.classList.remove("show"),
    document.querySelector("body").style.overflow = "auto"
))

addBtn.addEventListener("click", addBtn_click_handler)

showNotes()



