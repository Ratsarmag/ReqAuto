function updateModels() {
  var carMakeID = $("#carMake").val() || $("#editCarMake").val();
  $.ajax({
    url: "/get_models/" + carMakeID,
    success: function (data) {
      var select = $("#carModel") || $("#editCarModel");
      select.empty();
      select.append('<option value="">Выберите модель</option>');
      data.forEach(function (model) {
        select.append(
          '<option value="' + model.ID + '">' + model.carModel + "</option>"
        );
      });
    },
  });
}
