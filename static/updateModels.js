        function updateModels() {
            var carMakeID = $('#carMake').val();
            $.ajax({
                url: '/get_models/' + carMakeID,
                success: function(data) {
                    var select = $('#carModel');
                    select.empty();
                    select.append('<option value="">Выберите модель</option>');
                    data.forEach(function(model) {
                        select.append('<option value="' + model.ID + '">' + model.carModel + '</option>');
                    });
                }
            });
        }