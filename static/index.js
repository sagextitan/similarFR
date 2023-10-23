$(document).ready(() => {
  const video = document.getElementById("video");
  const videoContainer = document.getElementById("videoContainer");

  let imageData = null;

  /* When Click a Selfie button is clicked */
  $("#selfieCaptureBtn").click(() => {
    /*
        Welcome Section with steps instruction is taken out of view
      */
    $("section#welcome-section").addClass("display-none");
    $("section#welcome-section").removeClass("flex");

    /* Selfie Capturing section with webcam access comes into picture */
    $("section#selfie-capturing-section").addClass("flex");
    $("section#selfie-capturing-section").removeClass("display-none");

    /*
      When the selfie capturing section comes up, it needs access to the data
      sent from media source
      */
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices
        .getUserMedia({ video: true })
        .then((stream) => {
          video.srcObject = stream;
          video.play();
          videoContainer.style.display = "block";
        })
        .catch((error) => {
          console.error("Error accessing the webcam");
        });
    } else {
      console.error("getUserMedia is not supported in this browser.");
    }
  });

  /* When Find my photos button is clicked */
  $("#findMyPhotosBtn").click(() => {
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const context = canvas.getContext("2d");
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    imageData = canvas.toDataURL("image/jpeg");

    const stream = video.srcObject;
    if (stream) {
      const tracks = stream.getTracks();
      tracks.forEach((track) => {
        track.stop();
      });
      video.srcObject = null;
      $("section#selfie-capturing-section").addClass("display-none");
      $("section#selfie-capturing-section").removeClass("flex");
    }
    $.ajax({
      type: "POST",
      url: "/find_similar_images",
      data: { image_data: imageData },
      success: (data) => {
        $(".photos-grid").empty();
        if (data.similar_images.length === 0) {
          $("#no-results-found-section").removeClass("display-none");
          $("#no-results-found-section").addClass("flex");
        } else {
          $("section#results-section").removeClass("display-none");
          $("section#results-section").addClass("flex");
          data.similar_images.forEach((everyImageUrl) => {
            const imageToBeInserted = document.createElement("img");
            imageToBeInserted.src = everyImageUrl;
            imageToBeInserted.loading = "lazy";
            imageToBeInserted.alt = "User image";
            imageToBeInserted.classList.add("photo-grid-item");
            $(".photos-grid").append(imageToBeInserted);
          });
        }
      },
      error: (error) => {
        $("#error-section").removeClass("display-none");
        $("#error-section").addClass("flex");
      },
    });
  });

  /*Get your images on email button is present in 2 sections:
    1. In the section where photos of the user who submitted the selfie are displayed
    2. In the section where user who submitted the selfie is informed that currently there are no photos available
    */
  $("#proceedToFormBtnAfterResultsScreen").click(() => {
    $("#results-section").addClass("display-none");
    $("#results-section").removeClass("flex");

    $("#form-fillup-section").removeClass("display-none");
    $("#form-fillup-section").addClass("flex");
  });

  $("#proceedToFormBtnAfterNoResultsScreen").click(() => {
    $("#no-results-found-section").addClass("display-none");
    $("#no-results-found-section").removeClass("flex");

    $("#form-fillup-section").removeClass("display-none");
    $("#form-fillup-section").addClass("flex");
  });

  /* When Okay, got it button is clicked at the end when all steps
    are done like selfie capture and form fillup with submission  */
  $("#proceedToNextSelfieBtn").click(() => {
    location.reload();
  });

  /* When something is wrong text shows up then on click of it we reload */
  $("#recoverFromErrorButton").click(() => {
    $("#error-section").addClass("display-none");
    $("#error-section").removeClass("flex");
    location.reload();
  });


});
