function listenerOnSelector (selector, eventType, myFunction) {
    document.querySelectorAll(selector).forEach((item) => {
        item.addEventListener(eventType, (event) => myFunction(event))
    })
}

listenerOnSelector(".hide", "click", e =>{
    const id = e.target.closest("button").dataset.id
    fetch("/hide", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({id:id})
    })
    document.getElementById(`${id}`).classList.add("hidden")
})

listenerOnSelector(".pin", "click", e =>{
    const button = e.target.closest("button")
    const id = button.dataset.id
    fetch("/favorite", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({id:id})
    })
    const img = button.querySelector("img")
    if (img.alt === "Favorite") {
        img.src = '/static/img/unpin.png'
        img.alt = `Un-Favorite`
    } else {
        img.src = '/static/img/pin.png'
        img.alt = `Favorite`
    }
})

listenerOnSelector(".save", "click", e =>{
    const id = e.target.closest("button").dataset.id
    fetch("/add", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({id:id})
    })
    const img = button.querySelector("img")
    if (img.alt === "Save") {
        img.src = '/static/img/remove.png'
        img.alt = `Un-Save`
    } else {
        img.src = '/static/img/add.png'
        img.alt = `Save`
    }
})