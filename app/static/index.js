document.addEventListener("DOMContentLoaded", () => {
    const inputField = document.querySelector("#input");
    inputField.addEventListener("keydown", async function(e) {
        if (e.code === "Enter") {
            let input = inputField.value;
            inputField.value = "";

            output(input);
        }
    });
});

async function output(input) {
    let formData = new FormData();
    formData.append('sentence', input);

    result = await fetch('http://127.0.0.1:5000/v2/get-responce-sentence', {
            method: 'POST',
            body: formData,
    }).then((response) => {
        if (!response.ok) {
            throw new Error(response.error)
        }
        return response.json();
    });

    addChatEntry(input, result['sentence']);
}

function addChatEntry(input, product) {
    const messagesContainer = document.getElementById("messages");
    
    let userDiv = document.createElement("div");
    userDiv.id = "user";
    userDiv.className = "user response";
    userDiv.innerHTML = `${input}`;
    messagesContainer.appendChild(userDiv);
   
    let botDiv = document.createElement("div");
    let botText = document.createElement("span");
    botDiv.id = "bot";
    botDiv.className = "bot response";
    botText.innerText = "Typing...";
    botDiv.appendChild(botText);
    messagesContainer.appendChild(botDiv);
   
    setTimeout(() => {
      botText.innerText = `${product}`;
    }, 2000);
}