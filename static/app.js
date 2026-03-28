const chat = document.getElementById("chat")
const form = document.getElementById("form")
const input = document.getElementById("input")
const sendBtn = document.getElementById("send-btn")
const progressBar = document.getElementById("progress-bar")

let messages = []

function addMessage(role, text, isHtml = false) {
    const div = document.createElement("div")
    div.className = `message ${role}`
    const bubble = document.createElement("div")
    bubble.className = "bubble"
    if (isHtml) {
        bubble.innerHTML = text
    } else {
        bubble.textContent = text
    }
    div.appendChild(bubble)
    chat.appendChild(div)
    chat.scrollTop = chat.scrollHeight
    return bubble
}

function showProgress(active) {
    progressBar.classList.toggle("active", active)
}

form.addEventListener("submit", async (e) => {
    e.preventDefault()
    const text = input.value.trim()
    if (!text) return

    addMessage("user", text)
    messages.push({ role: "user", content: text })
    input.value = ""
    sendBtn.disabled = true
    showProgress(true)

    // Create assistant bubble for streaming
    const div = document.createElement("div")
    div.className = "message assistant"
    const bubble = document.createElement("div")
    bubble.className = "bubble"
    bubble.innerHTML = `<span class="cursor"></span>`
    div.appendChild(bubble)
    chat.appendChild(div)

    let fullText = ""

    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ messages }),
        })

        const reader = res.body.getReader()
        const decoder = new TextDecoder()

        while (true) {
            const { done, value } = await reader.read()
            if (done) break
            fullText += decoder.decode(value, { stream: true })
            bubble.innerHTML = marked.parse(fullText) + `<span class="cursor"></span>`
            chat.scrollTop = chat.scrollHeight
        }

        // Final render without cursor
        bubble.innerHTML = marked.parse(fullText)
        messages.push({ role: "assistant", content: fullText })
    } catch (err) {
        bubble.innerHTML = "Something went wrong. Please try again."
    } finally {
        showProgress(false)
        sendBtn.disabled = false
        input.focus()
    }
})
