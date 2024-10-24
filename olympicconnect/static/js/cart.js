$(document).ready(function() {

    document.addEventListener("DOMContentLoaded", function() {
        const modal = document.getElementById("paymentModal");
        const btn = document.getElementById("checkout-btn");
        const span = document.getElementsByClassName("close")[0];
        const form = document.getElementById("payment-form");
    
        btn.onclick = function() {
            modal.style.display = "block";
        }
    
        span.onclick = function() {
            modal.style.display = "none";
        }
    
        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        }
    
        form.onsubmit = function(event) {
            event.preventDefault();
            alert("Paiement validé!");
            window.location.href = "/tickets/ticketlist/";
        }
    });

    
    $('.add-to-cart').click(function() {
        const eventId = $(this).data('event-id');
        const price = $(this).data('price');
        const offerName = $(this).data('offer-name');
        const csrfElement  = document.querySelector('[name=csrfmiddlewaretoken]').value;

        if (!csrfElement) {
            // Si le CSRF token n'est pas trouvé, cela signifie que l'utilisateur n'est pas connecté.
            alert('Veuillez vous connecter pour ajouter des articles au panier.');
            window.location.href = '/accounts/login/';
            return;
        }
    
        const csrftoken = csrfElement.value;
    
        $.ajax({
            url: `/cart/add/${eventId}/`,
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: {
                price: price,
                offer_name: offerName
            },
            dataType: 'json',
            success: function(response) {
                if (response.success) {
                    alert('Article ajouté au panier.');
                    $('#cart-total').text(response.cart_total);
                } else if (response.error === 'not_authenticated') {
                    window.location.href = '/accounts/login/';
                } else {
                    alert('Erreur lors de l\'ajout de l\'article au panier.');
                }
            },
            error: function() {
                alert('Erreur lors de l\'ajout de l\'article au panier.');
            }
        });
    });

    $('.remove-from-cart').click(function() {
        const itemId = $(this).data('item-id');
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        $.ajax({
            url: `/cart/remove/${itemId}/`,
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            dataType: 'json',
            success: function(response) {
                if (response.success) {
                    $('#cart-total').text(response.cart_total);
                    $(`button[data-item-id="${itemId}"]`).closest('li').remove();
                } else {
                    alert('Erreur lors du retrait de l\'article du panier.');
                }
            },
            error: function() {
                alert('Erreur lors du retrait de l\'article du panier.');
            }
        });
    });
});
