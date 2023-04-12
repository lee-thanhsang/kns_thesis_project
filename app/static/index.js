document.addEventListener("DOMContentLoaded", () => {
    const inputField = document.querySelector("#input");
    inputField.addEventListener("keydown", async function(e) {
        if (e.code === "Enter") {
            let userMessage = inputField.value;
            inputField.value = "";

            output(userMessage);
        }
    });
});

async function output(userMessage) {
    botText = addUserEntry(userMessage);

    let formData = new FormData();
    formData.append('sentence', userMessage);

    result = await fetch('/v2/get-response-sentence', {
            method: 'POST',
            body: formData
    }).then((response) => {
        if (!response.ok) {
            throw new Error(response.error)
        }
        return response.json();
    });

    console.log(result)

    addBotEntry(botText, result['sentence']);
}

function addUserEntry(userMessage) {
    const messagesContainer = document.getElementById("messages");
    
    let userDiv = document.createElement("div");
    userDiv.id = "user";
    userDiv.className = "user response";
    userDiv.innerHTML = `${userMessage}`;
    messagesContainer.appendChild(userDiv);

    let botDiv = document.createElement("div");
    let botText = document.createElement("span");
    botDiv.id = "bot";
    botDiv.className = "bot response";
    botText.innerText = "Typing...";
    botDiv.appendChild(botText);
    messagesContainer.appendChild(botDiv);

    return botText
}

function addBotEntry(botText, botMessage) {   
    botText.innerText = `${botMessage}`;
}