
$(document).ready(function(){
    $(".select2_el").select2({
    });
});

$(document).ready(function () {
    //Toggle fullscreen
    $(".chat-bot-icon").click(function (e) {
        $(this).children('img').toggleClass('hide');
        $(this).children('svg').toggleClass('animate');
        $('.chat-screen').toggleClass('show-chat');
    });
    $('.chat-mail button').click(function () {
        $('.chat-mail').addClass('hide');
        $('.chat-body').removeClass('hide');
        $('.chat-input').removeClass('hide');
        $('.chat-header-option').removeClass('hide');
    });
    $('.end-chat').click(function () {
        $('.chat-body').addClass('hide');
        $('.chat-input').addClass('hide');
        $('.chat-session-end').removeClass('hide');
        $('.chat-header-option').addClass('hide');
    });
});

$(document).ready(function () {
    const inputField = document.querySelector("#input-message");
    inputField.addEventListener("keydown", async function(e) {
        if (e.code === "Enter") {
            let userMessage = inputField.value;
            inputField.value = "";
    
            output(userMessage);
        }
    });

    const buttonSendMessage = document.querySelector("#button-send");
    buttonSendMessage.addEventListener("click", async function(e) {
            let userMessage = inputField.value;
            if(userMessage != ""){
                inputField.value = "";
        
                output(userMessage);
            }
    });

    async function output(userMessage) {
        botDiv = addUserEntry(userMessage);
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
    
        addBotEntry(botDiv, result['sentence']);
    };
    
    function addUserEntry(userMessage) {
        const messagesContainer = document.getElementById("chat-body");
        
        let userDiv = document.createElement("div");
        userDiv.id = "user";
        userDiv.className = "chat-bubble me";
        userDiv.innerHTML = `${userMessage}`;
        messagesContainer.appendChild(userDiv);
    
        let botDiv = document.createElement("div");
        botDiv.id = "bot";
        botDiv.className = "chat-bubble you";
        botDiv.innerHTML = "<svg xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' style='margin: auto;display: block;shape-rendering: auto;width: 43px;height: 20px;' viewBox='0 0 100 100' preserveAspectRatio='xMidYMid'><circle cx='0' cy='44.1678' r='15' fill='#ffffff'><animate attributeName='cy' calcMode='spline' keySplines='0 0.5 0.5 1;0.5 0 1 0.5;0.5 0.5 0.5 0.5' repeatCount='indefinite' values='57.5;42.5;57.5;57.5' keyTimes='0;0.3;0.6;1' dur='1s' begin='-0.6s'></animate></circle> <circle cx='45' cy='43.0965' r='15' fill='#ffffff'><animate attributeName='cy' calcMode='spline' keySplines='0 0.5 0.5 1;0.5 0 1 0.5;0.5 0.5 0.5 0.5' repeatCount='indefinite' values='57.5;42.5;57.5;57.5' keyTimes='0;0.3;0.6;1' dur='1s' begin='-0.39999999999999997s'></animate></circle> <circle cx='90' cy='52.0442' r='15' fill='#ffffff'><animate attributeName='cy' calcMode='spline' keySplines='0 0.5 0.5 1;0.5 0 1 0.5;0.5 0.5 0.5 0.5' repeatCount='indefinite' values='57.5;42.5;57.5;57.5' keyTimes='0;0.3;0.6;1' dur='1s' begin='-0.19999999999999998s'></animate></circle></svg>"
        messagesContainer.appendChild(botDiv);
    
        return botDiv
    };
    
    function addBotEntry(botText, botMessage) {   
        botText.innerText = `${botMessage}`;
    };
});
