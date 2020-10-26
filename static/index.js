$(document).ready(function(){
  $("#FileUpload").change(function() { this.form.submit(); });

  console.log("FileUploaded: "+fileUploaded);
  console.log(fileUploaded == true);

  if (fileUploaded == true) { $('#myModal').modal('show'); console.log("showing modal"); }

});