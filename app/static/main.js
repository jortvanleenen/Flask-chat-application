// Initialise frameworks from script tags within base.html
const socket = io();
const DateTime = luxon.DateTime;

let currentUser;

// Adds WTForms CSRF-token to all future AJAX-requests
const csrf_token = $('meta[name=csrf-token]').attr('content');

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        }
    }
});

/**
 * Retrieves all messages of a certain chat and performs DOM-modifications to display the chat.
 *
 * @param chatId the chat to have displayed
 */
function openChat(chatId) {
    getMessages(chatId, openChatSuccess);
}

/**
 * Updates a chat by adding a message to it and then updating its representation within the DOM.
 */
function updateChat() {
    sendMessage(updateChatSuccess);
}

/**
 * The function that is called upon a successful, completed POST-request from openChat().
 *
 * @param response the response of the POST-request
 */
function openChatSuccess(response) {
    if (response['status'] === 'success') {
        currentUser = response['current_user'];
        displayMessages(response, false)
        $('#formChatId').val(response['chat_id']);
        $('#messageForm').removeClass("hidden-element");
        $('#messagesAlert').addClass("hidden-element")
        socket.emit("join_chat", {chat_id: response['chat_id']})
    } else {
        alert("Error, could not retrieve messages. Please try again.");
    }
}

/**
 * The function that is called upon a successful, completed POST-request from updateChat().
 *
 * @param response the response of the POST-request
 */
function updateChatSuccess(response) {
    if (response['status'] === 'success') {
        $('#formContent').val('');
        socket.emit('send_message', response);
    } else {
        alert("Error, could not send message. Please try again.");
    }
}

/**
 * Requests all messages of a chat with 'chatId' as chat_id. Executes success() on callback.
 *
 * @param chatId the chat_id of the chat which messages should be retrieved
 * @param success the function that should be called on a successful callback
 */
function getMessages(chatId, success) {
    $.post("/open-chat", {
        chat_id: chatId
    }).done(function (response) {
        success(response);
    }).fail(function () {
        alert('A fatal AJAX error occurred. Please try again later.');
    });
}

/**
 * Adds a message to a certain chat based on the attributes contained within the submitted form.
 *
 * @param success the function that should be called on a successful callback
 */
function sendMessage(success) {
    $.post("/send-message", {
        chat_id: $('#formChatId').val(),
        csrf_token: $('#formCsrfToken').val(),
        content: $('#formContent').val(),
        send: $('#formSend').val()
    }).done(function (response) {
        success(response);
    }).fail(function () {
        alert('A fatal AJAX error occurred. Please try again later.');
    });
}

/**
 * Displays all message in the response of a POST-request of a certain chat indicated by the chatId parameter.
 *
 * @param response the response of the POST-request
 * @param update True when the current chatScreenContent just needs to get updated, instead of completely reloaded
 */
function displayMessages(response, update) {
    const chatScreenContent = $('#chatScreenContent');

    if (!update) {
        // Keeps important hidden template elements, while clearing previously displayed chat messages
        chatScreenContent.children(":visible").remove();
    }

    // Creates a new message element based on the hidden template elements within the DOM
    for (let i = 0; i < response['messages'].length; i++) {
        let message;
        if (response['messages'][i][0] === currentUser) {
            message = $('#messageRight').clone();
        } else {
            message = $('#messageLeft').clone();
        }

        // Make use of the Luxon framework for easy DateTime parsing and formatting (from UTC to locale)
        const correctedTimestamp = response['messages'][i][1].replace(/ /g, "T");
        // noinspection JSUnresolvedVariable
        const localTimestamp = DateTime.fromISO(correctedTimestamp, {zone: "UTC"}).toLocal()
            .toLocaleString(DateTime.DATETIME_SHORT_WITH_SECONDS);

        // [0]: sender, [1]: sent_timestamp, [2]: content
        message.find("#messageUsername").text(response['messages'][i][0]).attr("id", 'u' + i);
        message.find("#messageTimestamp").append(localTimestamp).attr("id", 't' + i);
        message.find("#messageContent").text(response['messages'][i][2]).attr("id", 'c' + i);
        // Ensure all ID's stay unique for future use
        message.attr("id")
        // d-flex does not work with the display: none property, so has to be added afterwards
        message.addClass("d-flex").removeClass("hidden-element")
        message.appendTo('#chatScreenContent')
        // For user's convenience display most recent messages by scrolling to bottom of chatContent
        chatScreenContent.scrollTop(chatScreenContent[0].scrollHeight);

    }
}

socket.on("new_message", (json) => {
    displayMessages(json, true)
});
