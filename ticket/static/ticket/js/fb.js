$(document).ready(function () {
  window.fbAsyncInit = function () {
    FB.init({
      appId: "404167532322217",
      xfbml: true,
      version: "v19.0",
    });
    FB.AppEvents.logPageView();
  };

  var id = "facebook-jssdk";
  if ($("#" + id).length) {
    return;
  }
  var js = document.createElement("script");
  js.id = id;
  js.src = "https://connect.facebook.net/en_US/sdk.js";
  $("script")[0].parentNode.insertBefore(js, $("script")[0]);
});
