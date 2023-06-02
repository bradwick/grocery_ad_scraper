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
    if (button.alt === "Favorite") {
        button.querySelector("img").src = '/static/img/unpin.png'
        button.alt = `Un-Favorite`
    } else {
        button.querySelector("img").src = '/static/img/pin.png'
        button.alt = `Favorite`
    }
})

listenerOnSelector(".save", "click", e =>{
    const id = e.target.closest("button").dataset.id
    fetch("/add", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({id:id})
    })
    if (button.alt === "Save") {
        button.querySelector("img").src = '/static/img/remove.png'
        button.alt = `Un-Save`
    } else {
        button.querySelector("img").src = '/static/img/add.png'
        button.alt = `Save`
    }
})