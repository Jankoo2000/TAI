// #103
$(document).ready(function (){
    // add to cart
    $('.add_to_cart').on('click', function (e){
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

                }

            }
        })
    })

    $('.item_qty').each(function (){
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        $('#'+the_id).html(qty)
    })

    //decrease cart
        $('.decrease_cart').on('click', function (e){
        e.preventDefault();
        // alert('test123');
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
                    Swal.fire(response.message, '', 'error') //     return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})
                }
                else
                {
                    $('#qty-'+food_id).html(response.qty);
                }
            }
        })
    })
});