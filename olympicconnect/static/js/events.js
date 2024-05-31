$(document).ready(function() {
    fetchEvents();
});

function fetchEvents() {
    $.ajax({
        url: '/events/api/',
        method: 'GET',
        dataType: 'json',
        success: function(data) {
            displayEvents(data);
        },
        error: function(error) {
            console.error('Error fetching events:', error);
        }
    });
}


function displayEvents(events) {
    const eventsContainer = $('#events-container');
    eventsContainer.empty(); 
    events.forEach(event => {
        const eventItem = $('<div class="event-item"></div>');

        const eventThumbnail = $('<div class="event-thumbnail"></div>');
        const img = $('<img>').attr('src', event.thumbnail);
        eventThumbnail.append(img);

        const eventInfo = $('<div class="event-info"></div>');
        const eventName = $('<h3></h3>').text(event.name);
        const eventDescription = $('<p></p>').text(event.description);
        eventInfo.append(eventName);
        eventInfo.append(eventDescription);

        const eventButton = $('<a class="btn">Réserver un billet</a>').attr('href', '/events/' + event.id);
        eventInfo.append(eventButton);
        
        eventItem.append(eventThumbnail);
        eventItem.append(eventInfo);
        

        eventsContainer.append(eventItem);
    });
}
