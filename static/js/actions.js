function listenerOnSelector (selector, eventType, myFunction) {
    document.querySelectorAll(selector).forEach((item) => {
        item.addEventListener(eventType, (event) => myFunction(event))
    })
}

listenerOnSelector(".hide", "click", e =>{
    const id = e.target.closest("button").dataset.id
    fetch("/hide", {
        method: "POST",
        body: JSON.stringify({id:id})
    })
    e.target.closest(".deal-row").classList.add("hidden")
})

listenerOnSelector(".pin", "click", e =>{
    const button = e.target.closest("button")
    const id = button.dataset.id
    fetch("/favorite", {
        method: "POST",
        body: JSON.stringify({id:id})
    })
    if (button.alt === "Un-Favorite")
        button.querySelector("img").src = '/static/img/unpin.png'
    else
        button.querySelector("img").src = '/static/img/pin.png'
})

listenerOnSelector(".save", "click", e =>{
    const id = e.target.closest("button").dataset.id
    fetch("/add", {
        method: "POST",
        body: JSON.stringify({id:id})
    })
    if (button.alt === "Un-Save")
        button.querySelector("img").src = '/static/img/remove.png'
    else
        button.querySelector("img").src = '/static/img/add.png'
})