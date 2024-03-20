$(document).ready(function() {
    $('#currency, #sale, #purchase').on('input', function() {
        this.value = this.value.replace(/[^0-9.,%+-]/g, '');
    });
    $('#airline').on('blur', function() {
        // Shift focus to the 'supplier_id' field and open the dropdown
        $('#supplier_id').select2('open');
    });
    $('#supplier_id').on('select2:select', function (e) {
        $('#customer_id').select2('open');
    });
    
    $('#currency, #sale, #purchase').keydown(function(e){
        if(e.which == 13){  // Enter key pressed
            e.preventDefault();  // Prevent form submission
            var input = $(this).val();
            var sum = eval(input);
            $(this).val(sum);
        }
    });

        $('#pnr').keypress(function(e) {
            if (e.which == 13) {  // Detect the Enter key
                e.preventDefault();
                var pnr = $(this).val();
                $.ajax({
                    url: '/get_ticket/',
                    data: {
                        'pnr': pnr
                    },
                    dataType: 'json',
                    success: function(data) {
                        if (data.travel_date) {
                            console.log(data.travel_date)
                            var travel_date = new Date(data.travel_date);
                            var formatted_date = travel_date.toISOString().split('T')[0];
                            $('#travel_date').val(formatted_date);
                        }
                        $('#ticket_type').val(data.ticket_type);
                        $('#sector').val(data.sector);
                        $('#passenger').val(data.passenger);
                        $('#airline').val(data.airline);
                        $('#supplier_id').val(data.supplier).trigger('change');
                        $('#customer_id').val(data.customer).trigger('change');
                        $('#sale').val(data.sale);
                        $('#purchase').val(data.purchase);
                    }
                });
            }
        });
        $('#ticket-form').on('submit', function(e){
            // theme
            $(this).prop("disabled", true);
            var form = $(this);
            e.preventDefault();
            $.ajax({
                type: "POST",
                url: '/tickets/create/',
                data: form.serialize(),
                success: function(data) {
                    if (data.status == 200){
                        $("#info-message").html(data.message).show().delay(5000).fadeOut('slow');;
                        window.location.href = '/tickets/';   
                    }
                    $("#info-message").html(data.message);
                    $('#ticket-form')[0].reset();
                    $('#supplier_id').val(null).trigger('change');
                    $('#customer_id').val(null).trigger('change');
    
                },
                error: function(e) {
                    $("#info-message").html('Error: ' + e.status + ' ' + e.responseText).show().delay(5000).fadeOut('slow');;
                },
                complete: function () {
                    $("#ticket-submit").prop("disabled", false);
                }
            });
    
        });
    
        $('#ticket-del, #cus-sup-del, #ledger-del, #visa-del').click(function(e) {
            e.preventDefault();
            let result = confirm('Are you sure you want to delete this?');
            if (result) {
                let ticketId = $(this).data('tid');
                let modelName = $(this).data('model');
                $.ajax({
                    url: '/delete/' + modelName + '/' + ticketId + '/delete/', 
                    type: 'POST',
                    data: {
                        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                    },
                    success: function(data) {
                        if(data.status == 'success')
                        {
                            $("#info-message").html(data.message).show().delay(5000).fadeOut('slow');
                        }
                        location.reload(false);
                    },
                    error: function(e) {
                    $("#info-message").html('Error: ' + e.status + ' ' + e.responseText).show().delay(5000).fadeOut('slow');;
                    }
                });
            }
        });
        

        $("#close-alert").click(function(){
            $(this).closest('.info-alert').hide();
        });
   
        
        $('#visa_type').change(function() {
            var visaType = $(this).val();
            var durationMapping = {
                '36': '36 Hours',
                '96': '96 Hours',
                '1m': '1 Month',
                '2m': '2 Months',
                '3m': '3 Months'
            };
            if (visaType === 'UV') {
                durations = ['1m', '3m'];
            } else {
                durations = ['36', '96', '1m', '2m'];
            }
    
            var durationSelect = $('#duration');
            durationSelect.empty();
    
            $.each(durations, function(index, value) {
                durationSelect.append($('<option></option>').attr('value', value).text(durationMapping[value]));
            });
        });
});
