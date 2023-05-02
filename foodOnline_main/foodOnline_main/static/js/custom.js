// #103
$(document).ready(function (){
    // add to cart
    $('.add_to_cart').on('click', function (e)
    {
        e.preventDefault();
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        $.ajax({
            type : 'GET',
            url : url,
            success : function (response){
                console.log(response)
                if(response.status == 'login_required')
                {
                    Swal.fire(response.message) //     return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})
                }
                if(response.status == 'Failed') {
                    Swal.fire(response.message) //     return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})
                }
                else
                {
                    $('#qty-'+food_id).html(response.qty);
                    applyCartAmounts(response.cart_amount['total_price'])
                }

            }
        })
    })

    $('.item_qty').each(function ()
    {
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        $('#'+the_id).html(qty)
    })

    //decrease cart
    $('.decrease_cart').on('click', function (e)
    {
        e.preventDefault();
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        cart_id = $(this).attr('id');

        $.ajax({
            type : 'GET',
            url : url,
            success : function (response){
                console.log(response)
                if(response.status == 'login_required')
                {
                    Swal.fire(response.message) //     return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})
                }
                if(response.status == 'Failed') {
                    Swal.fire(response.message, '', 'error') //     return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})
                }
                else
                {
                    $('#qty-'+food_id).html(response.qty);
                    removeCartItem(response.qty, cart_id);


                    applyCartAmounts(response.cart_amount['total_price'])
                    // JsonResponse({'status': 'Sucess', 'message': 'Increased the cart quantity',
                    //                      'cart_counter': get_cart_counter(request), 'qty': checkCart.quantity,
                    //                      'cart_amount': get_cart_amounts(request)})

                    // from context processor def get_cart_amounts(request) return dict(total_price=total_price)

                }
            }
        })
    })

    function removeCartItem(cartItemQty, cart_id)
    {
            if(cartItemQty <= 0)
            {
                document.getElementById("cart-item-"+cart_id).remove()
            }
    }


    function applyCartAmounts(total)
    {
        //<b><span id="total">{{ total_price }}</span></b> {# context processor var form dictionary #}
        $('#total').html(total) // podmienienie wartosci obiektu o id total na total , tylko wizualnie tak zeby nie odswiezac strony

        // $ is a shortcut for the jQuery library,
        // and ('#total') selects the HTML element with the ID of "total".
        // .html() is a jQuery method that sets or retrieves the HTML content of the selected element.
        // total is a JavaScript variable that contains a value to be displayed in the "total" element.
        // The html() method is called on the selected element, and the total variable is passed as an argument. This sets the HTML content of the "total" element to the value of total.

    }
});