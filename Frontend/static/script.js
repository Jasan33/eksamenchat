const socket = io();
const username = document.getElementById("usernames")?.dataset.username;
localStorage.setItem("usernameplayer", username);

function SubmitMessage() {
    console.log("A message was sent")
    let message = document.getElementById("message").value;
        let user_message = username + ": " + message
        socket.emit('new_message', { user_message });
        document.getElementById("message").value = "";
}

socket.on("chat", function(data) {
    let ul = document.getElementById("chat-messages");
    let li = document.createElement("li");
    console.log(data["user_message"]);
    li.appendChild(document.createTextNode(data["user_message"]));
    ul.appendChild(li);
    ul.scrollBottom = ul.scrollHeight;SubmitSentence
});