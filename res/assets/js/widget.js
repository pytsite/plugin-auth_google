/**
 * While writing code for this widget, refer to https://developers.google.com/identity/sign-in/web/reference
 */
$(window).on('pytsite.widget.init:plugins.auth_google._driver._SignInWidget', function (e, widget) {
    function onAuthGoogleSignIn(user) {
        var form = $('.pytsite-auth-sign-in.driver-google');
        form.find('input[id$="id-token"]').val(user.getAuthResponse().id_token);
        form.submit();
    }

    window.onGAPILoad = function () {
        gapi.load('auth2', function () {
            var auth = gapi.auth2.init({
                client_id: widget.em.data('clientId')
            });

            auth.then(function () {
                var auth = gapi.auth2.getAuthInstance();

                // First, check if the Google's user is authenticated in PytSite
                pytsite.auth.isAnonymous().done(function (isAnonymous) {
                    if (isAnonymous) {
                        // Sign out from Google and render "Sign In" button
                        auth.signOut();
                        gapi.signin2.render(widget.uid, {
                            onSuccess: onAuthGoogleSignIn
                        });
                    }
                    else {
                        console.log("Already authorized");
                    }
                });
            });


        });
    };

    pytsite.browser.addJS('https://apis.google.com/js/platform.js?onload=onGAPILoad');
});