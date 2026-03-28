const chat = document.getElementById("chat")
const form = document.getElementById("form")
const input = document.getElementById("input")
const sendBtn = document.getElementById("send-btn")

let messages = []

function addMessage(role, text) {
    const div = document.createElement("div")
    div.className = `message ${role}`
    const bubble = document.createElement("div")
    bubble.className = "bubble"
    if (role === "assistant") {
        bubble.innerHTML = marked.parse(text)
    } else {
        bubble.textContent = text
    }
    div.appendChild(bubble)
    chat.appendChild(div)
    chat.scrollTop = chat.scrollHeight
}

function addTypingIndicator() {
    const div = document.createElement("div")
    div.className = "message assistant"
    div.id = "typing"
    div.innerHTML = `<div class="bubble typing-indicator"><span></span><span></span><span></span></div>`
    chat.appendChild(div)
    chat.scrollTop = chat.scrollHeight
}

function removeTypingIndicator() {
    const el = document.getElementById("typing")
    if (el) el.remove()
}

form.addEventListener("submit", async (e) => {
    e.preventDefault()
    const text = input.value.trim()
    if (!text) return

    addMessage("user", text)
    messages.push({ role: "user", content: text })
    input.value = ""
    sendBtn.disabled = true
    addTypingIndicator()

    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ messages }),
        })
        const data = await res.json()
        removeTypingIndicator()
        addMessage("assistant", data.response)
        messages.push({ role: "assistant", content: data.response })
    } catch (err) {
        removeTypingIndicator()
        addMessage("assistant", "Something went wrong. Please try again.")
    } finally {
        sendBtn.disabled = false
        input.focus()
    }
})
