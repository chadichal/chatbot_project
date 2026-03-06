
function addMessage(text, sender){
    let chat = document.getElementById("chatbox")
    let msg = document.createElement("div")
    msg.className = sender
    msg.innerText = text
    chat.appendChild(msg)
    chat.scrollTop = chat.scrollHeight
}

async function sendMessage(){
    let input = document.getElementById("userInput")
    let message = input.value
    if(!message) return

    addMessage("You: " + message, "user")
    input.value = ""

    let res = await fetch("/chat",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({message:message})
    })

    let data = await res.json()

    addMessage("Bot: " + data.reply,"bot")

    speak(data.reply)
}

async function addQA(){

    let q = document.getElementById("newQ").value
    let a = document.getElementById("newA").value

    let res = await fetch("/add_qa",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({question:q, answer:a})
    })

    let data = await res.json()
    alert(data.msg)
}

function startVoice(){

    const recognition = new webkitSpeechRecognition()
    recognition.lang = "en-US"

    recognition.onresult = function(event){
        let text = event.results[0][0].transcript
        document.getElementById("userInput").value = text
        sendMessage()
    }

    recognition.start()
}

function speak(text){
    let speech = new SpeechSynthesisUtterance(text)
    speech.lang = "en-US"
    speechSynthesis.speak(speech)
}
