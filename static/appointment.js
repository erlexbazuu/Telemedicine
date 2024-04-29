$(document).ready(function() {
    // When the value of specialization field changes
    $('#id_specialization').change(function() {
        var specializationId = $(this).val();
        // Send an AJAX request to fetch doctors based on the selected specialization
        $.ajax({
            url: fetchDoctorsURL, // Using a variable for the URL
            data: {
                'specialization_id': specializationId
            },
            dataType: 'json',
            success: function(data) {
                // Update the options for the doctor field
                var options = '<option value="">Select Doctor</option>';
                for (var i = 0; i < data.length; i++) {
                    options += '<option value="' + data[i].id + '">' + data[i].name + '</option>';
                }
                $('#id_doctor').html(options);
            }
        });
    });
});
